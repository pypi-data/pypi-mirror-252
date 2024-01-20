import numpy as np
import pytest

from guided_molecule_gen.testutils.check_client import TRITON_SERVER_LIVE, BioNemoTritonClient


@pytest.mark.skipif(not TRITON_SERVER_LIVE, reason="No triton server connection")
def test_encode(client):
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',  # This does not come back identical in round trip
    ]

    response = client.encode(smis)
    # TODO - check if we should squeeze this
    assert response.shape == (1, len(smis), client.num_latent_dimensions)
    assert not np.any(np.isnan(response))
    assert not np.all(response == 0)


@pytest.mark.skipif(not TRITON_SERVER_LIVE, reason="No triton server connection")
def test_decode(client):
    num_samples = 10
    features = np.random.rand(1, num_samples, client.num_latent_dimensions).astype(np.float32)
    smis = client.decode(features)
    assert len(smis) == num_samples
    for sample in smis:
        assert isinstance(sample, str)


@pytest.mark.skipif(not TRITON_SERVER_LIVE, reason="No triton server connection")
def test_decode_bad_input(client):
    bad_features = np.random.rand(1, 1, client.num_latent_dimensions + 10).astype(np.float32)
    with pytest.raises(ValueError):
        client.decode(bad_features)


@pytest.mark.skipif(not TRITON_SERVER_LIVE, reason="No triton server connection")
def test_round_trip_identical(client):
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
    ]

    encoding = client.encode(smis)
    decoding = client.decode(encoding)
    assert smis == decoding


@pytest.mark.skipif(not TRITON_SERVER_LIVE, reason="No triton server connection")
def test_round_trip_perturbation_not_identical(client):
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
    ]

    encoding = client.encode(smis)
    encoding += np.random.rand(*encoding.shape)
    decoding = client.decode(encoding)
    assert smis != decoding


@pytest.mark.skipif(TRITON_SERVER_LIVE, reason="Triton server is live")
def test_graceful_failure_if_not_installed():
    with pytest.raises(RuntimeError):
        BioNemoTritonClient()
