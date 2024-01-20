# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
"""Classes for running inference on small molecule representations."""
import base64
import io
from typing import Any, Callable, Dict, List, Protocol

import numpy as np

from guided_molecule_gen.bionemo_model_metadata import bionemo_model_info

BIONEMO_SERVER_SUPPORTED = False
try:
    from bionemo.api import BionemoClient

    BIONEMO_SERVER_SUPPORTED = True
except ImportError:
    BionemoClient = None

TRITON_SERVER_SUPPORTED = False
try:
    import tritonclient.http as httpclient
    from tritonclient.utils import np_to_triton_dtype

    TRITON_SERVER_SUPPORTED = True
except ImportError:
    np_to_triton_dtype = None
    httpclient = None


class InferenceClientBase(Protocol):
    """Abstract class representing the required method signatures for inference.

    The functionality required is to be able to encode smiles strings into latent space,
    and decode latent space into a smiles string.

    Implementers could be (for example) a triton client wrapper, or a wrapper around the Bionemo service.
    """

    def encode(self, smis: List[str]) -> np.ndarray:
        """Encode some number of smiles strings into latent space.

        Parameters
        ----------
        smis : List[str]
            Smiles strings

        Returns
        -------
        np.ndarray
            (1 x len(smis) x num_latent_dimensions) embeddings
        """
        pass

    def decode(self, latent_features: np.ndarray) -> List[str]:
        """Decode latent space features into generated smiles.

        Parameters
        ----------
        latent_features : np.ndarray
            (1 x num_molecules x num_latent_dimensions) embeddings

        Returns
        -------
        List[str]
            Generated smiles strings
        """
        pass

    def num_latent_dims(self) -> int:
        """Return the dimensionality of latent space"""
        pass


class BioNemoTritonClient:
    """Triton client wrapper for simple encoding and decoding operations."""

    def __init__(
        self,
        url: str = "localhost:8000",
        encoder_model: str = "embeddings",
        decoder_model: str = "decoder",
        latent_space_dimensions: int = 512,
        timeout_seconds: int = 300,
    ):
        """

        Parameters
        ----------
        url : str
            Address of the running Triton Server, containing the port-specifying suffix
        encoder_model : str
            Endpoint of the encoding model
        decoder_model : str
            Endpoint of the decoding model
        latent_space_dimensions : int
            Number of dimensions in the latent space model
        timeout_seconds : int
            Runtime and connection timeout.
        """

        if not TRITON_SERVER_SUPPORTED:
            raise RuntimeError("Attempted to build Triton client, but triton is not installed")
        self._client = httpclient.InferenceServerClient(
            url, connection_timeout=timeout_seconds, network_timeout=timeout_seconds
        )
        self._encoder_model: str = encoder_model
        self._decoder_model: str = decoder_model
        self._num_latent_dimensions: int = latent_space_dimensions
        self._timeout: int = timeout_seconds
        self._format_input: np.ndarray = np.array([["npz"]]).astype(bytes)

    @property
    def num_latent_dimensions(self):
        """Returns the latent space dimensionality"""
        return self._num_latent_dimensions

    def ping_connection(self) -> bool:
        """Returns True if server is live. Propagates any exceptions."""
        return self._client.is_server_live()

    def encode(self, smis: List[str]) -> np.ndarray:
        """Encode some number of smiles strings into latent space.

        Parameters
        ----------
        smis : List[str]
            Smiles strings

        Returns
        -------
        np.ndarray
            (1 x len(smis) x num_latent_dimensions) embeddings
        """
        smis_input = np.array([smis]).astype(bytes)

        inputs = [
            httpclient.InferInput("strings", list(smis_input.shape), np_to_triton_dtype(smis_input.dtype)),
            httpclient.InferInput(
                "format", list(self._format_input.shape), np_to_triton_dtype(self._format_input.dtype)
            ),
        ]

        inputs[0].set_data_from_numpy(smis_input)
        inputs[1].set_data_from_numpy(self._format_input)

        outputs = [
            httpclient.InferRequestedOutput("data"),
        ]
        # Client call timeout is in microseconds
        response = self._client.infer(
            self._encoder_model, inputs, request_id=str(1), outputs=outputs, timeout=self._timeout * 10**6
        )

        embeddings = response.as_numpy("data")
        embeddings = base64.b64decode(embeddings[0][0])

        embeddings = io.BytesIO(embeddings)
        return np.load(embeddings)['embeddings']

    def decode(self, latent_features: np.ndarray) -> List[str]:
        """Decode latent space features into generated smiles.

        Parameters
        ----------
        latent_features : np.ndarray
            (1 x num_molecules x num_latent_dimensions) embeddings

        Returns
        -------
        List[str]
            Generated smiles strings
        """
        dims = list(latent_features.shape)
        if not len(dims) == 3 or not dims[-1] == self.num_latent_dimensions:
            raise ValueError(f"Input dimensions need to be (1, x, {self.num_latent_dimensions}), got  {dims}")

        # To line up with the server API, we doubly pack the features.
        # First, we save the array in NPZ format as bytes.
        # We then wrap that into a 1x1 "2D" numpy array. The server will index the array, then deserialize the indexed
        # bytes object.
        with io.BytesIO() as buffer:
            np.savez(buffer, embeddings=latent_features)
            condensed_features = buffer.getvalue()
        enc_embeddings = np.array([[condensed_features]], dtype=object)
        is_staged = np.array([[False]]).astype(bool)
        inputs = [
            httpclient.InferInput("embedding", enc_embeddings.shape, np_to_triton_dtype(enc_embeddings.dtype)),
            httpclient.InferInput(
                "format", list(self._format_input.shape), np_to_triton_dtype(self._format_input.dtype)
            ),
            httpclient.InferInput("is_staged", is_staged.shape, np_to_triton_dtype(is_staged.dtype)),
        ]
        inputs[0].set_data_from_numpy(enc_embeddings)
        inputs[1].set_data_from_numpy(self._format_input)
        inputs[2].set_data_from_numpy(is_staged)

        outputs = [
            httpclient.InferRequestedOutput("smis"),
        ]
        # Client call timeout is in microseconds
        response = self._client.infer(
            self._decoder_model, inputs, request_id=str(1), outputs=outputs, timeout=self._timeout * 10**6
        )

        generated_smis = response.as_numpy('smis')
        return [elem.decode() for elem in generated_smis[0]]

    def num_latent_dims(self) -> int:
        return self._num_latent_dimensions


class BioNemoServiceClient(InferenceClientBase):
    def __init__(self, bionemo_client: BionemoClient, model_name: str = 'molmim'):
        if not BIONEMO_SERVER_SUPPORTED:
            raise RuntimeError("Attempted to build bionemo client, but bionemo is not installed")
        self._client: BionemoClient = bionemo_client

        try:
            model_config: Dict[str, Any] = bionemo_model_info[model_name]
        except KeyError:
            raise ValueError(f"Unsupported model {model_name}. Supported models are {bionemo_model_info.keys()}.")

        self.num_latent_dimensions: int = bionemo_model_info[model_name]['num_latent_dimensions']
        self._embedding_endpoint: Callable = self._extract_endpoint(model_config, 'encode_endpoint_name')
        self._decoding_endpoint: Callable = self._extract_endpoint(model_config, 'decode_endpoint_name')

    def _extract_endpoint(self, model_config: Dict[str, Any], endpoint_query: str) -> Callable:
        endpoint_name: str = model_config[endpoint_query]
        try:
            return getattr(self._client, endpoint_name)
        except AttributeError:
            raise RuntimeError(f"The bionemo client API does not have the {endpoint_name} endpoint")

    def encode(self, smis: List[str]) -> np.ndarray:
        """Encode some number of smiles strings into latent space.

        Parameters
        ----------
        smis : List[str]
            Smiles strings

        Returns
        -------
        np.ndarray
            (1 x len(smis) x num_latent_dimensions) embeddings
        """

        return np.expand_dims(np.vstack(self._embedding_endpoint(smis)), 0)

    def decode(self, latent_features: np.ndarray) -> List[str]:
        """Decode latent space features into generated smiles.

        Parameters
        ----------
        latent_features : np.ndarray
            (1 x num_molecules x num_latent_dimensions) embeddings

        Returns
        -------
        List[str]
            Generated smiles strings
        """
        dims = list(latent_features.shape)
        if len(dims) == 2:
            latent_features = np.expand_dims(latent_features, 0)
            dims = list(latent_features.shape)
        if not len(dims) == 3 or not dims[-1] == self.num_latent_dims():
            raise ValueError(f"Input dimensions need to be (1, x, {self.num_latent_dimensions}), got  {dims}")

        return self._decoding_endpoint(np.split(latent_features.squeeze(), latent_features.shape[1], 0))

    def num_latent_dims(self) -> int:
        """Return the dimensionality of latent space"""
        return self.num_latent_dimensions
