from unittest import mock

import cma
import numpy as np
import pytest

from guided_molecule_gen.optimizer import MoleculeGenerationOptimizer


class FakeClient:
    """Decode keeps history, so each decode() call iterates the strings called.

    For the first iteration, the "smiles" output is [["1", "2", "3"...]["4", "5", "6"]]
    For the second, it's [["2", "3", "4"...],["5", "6", "7"]].

    See the associated checking function
    """

    def __init__(self, num_latent_dims: int):
        self.count = 0
        self._num_latent_dims = num_latent_dims

    def encode(self, smis):  # noqa static
        return np.random.rand(1, len(smis), self._num_latent_dims)

    def decode(self, latents):
        res = [str(i + self.count) for i in range(latents.shape[1])]
        self.count += 1
        return res

    def num_latent_dims(self):
        return self._num_latent_dims


def fake_oracle(smis, **_):
    return np.arange(len(smis))


def check_generated_contents(generated_smis, num_iterations, num_molecules, popsize):
    """Asserts proper contents of generated smiles, based on the fake client decoder"""
    assert len(generated_smis) == num_molecules
    for i, mol in enumerate(generated_smis):
        assert len(mol) == popsize, f"{i=}"
        for j, smi in enumerate(mol):
            # minus num_iterations since it should start from 0
            expected_val = str((num_iterations - 1) + i * popsize + j)
            assert smi == expected_val, f"{i=}, {j=}"


@pytest.mark.parametrize("num_latent_dims,pop_size", ((512, 10), (100, 8)))
def test_basic_step(num_latent_dims, pop_size):
    num_smis = 5

    client = FakeClient(num_latent_dims)
    client.encode_resp = np.random.rand(num_smis, num_latent_dims)
    client.decode_resp = [""] * pop_size * num_smis

    mock_rv = np.ones((pop_size, num_latent_dims), dtype=np.float32)
    with mock.patch.object(cma.CMAEvolutionStrategy, 'ask', return_value=mock_rv) as mock_ask, mock.patch.object(
        cma.CMAEvolutionStrategy, 'tell'
    ) as mock_tell:
        optimizer = MoleculeGenerationOptimizer(client, fake_oracle, [""] * num_smis, popsize=pop_size)
        optimizer.step()
        mock_ask.assert_called()
        mock_tell.assert_called()
        optimizer.step()
        mock_ask.assert_called()
        mock_tell.assert_called()
    check_generated_contents(optimizer.generated_smis, 2, num_smis, pop_size)


@pytest.mark.parametrize("num_latent_dims,pop_size", ((512, 10), (100, 8)))
def test_optimize(num_latent_dims, pop_size):
    num_smis = 5
    num_steps = 5

    client = FakeClient(num_latent_dims)
    client.encode_resp = np.random.rand(num_smis, num_latent_dims)
    client.decode_resp = [""] * pop_size * num_smis

    mock_rv = np.ones((pop_size, num_latent_dims), dtype=np.float32)
    with mock.patch.object(cma.CMAEvolutionStrategy, 'ask', return_value=mock_rv), mock.patch.object(
        cma.CMAEvolutionStrategy, 'tell'
    ):
        optimizer = MoleculeGenerationOptimizer(client, fake_oracle, [""] * num_smis, popsize=pop_size)
        optimizer.optimize(num_steps)
    check_generated_contents(optimizer.generated_smis, num_steps, num_smis, pop_size)

    # Now reset and optimize again. Note the changed number of smiles
    num_smis = 3
    # Should not expect a continuation of values from the first run.
    client.count = 0
    optimizer.reset([""] * num_smis)
    with mock.patch.object(cma.CMAEvolutionStrategy, 'ask', return_value=mock_rv), mock.patch.object(
        cma.CMAEvolutionStrategy, 'tell'
    ):
        optimizer.optimize(num_steps)
    check_generated_contents(optimizer.generated_smis, num_steps, num_smis, pop_size)
