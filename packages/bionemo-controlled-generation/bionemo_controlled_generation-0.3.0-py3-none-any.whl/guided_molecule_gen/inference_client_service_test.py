import numpy as np
import pytest

from guided_molecule_gen.inference_client import BioNemoServiceClient
from guided_molecule_gen.testutils.check_client import BIONEMO_SERVER_LIVE, bionemo_env_credentials


@pytest.fixture
def bionemo_base_client():
    from bionemo.api import BionemoClient

    host, key = bionemo_env_credentials()
    return BionemoClient(api_key=key, api_host=host)


@pytest.mark.parametrize('model_name', ('molmim', 'moflow'))
@pytest.mark.skipif(not BIONEMO_SERVER_LIVE, reason="No BioNemo server connection")
def test_encode(bionemo_base_client, model_name):
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',  # This does not come back identical in round trip
    ]
    bionemo_client = BioNemoServiceClient(bionemo_base_client, model_name=model_name)
    response = bionemo_client.encode(smis)
    # TODO - check if we should squeeze this
    assert response.squeeze().shape == (len(smis), bionemo_client.num_latent_dimensions)
    assert not np.any(np.isnan(response))
    assert not np.all(response == 0)


@pytest.mark.parametrize('model_name', ('molmim', 'moflow'))
@pytest.mark.skipif(not BIONEMO_SERVER_LIVE, reason="No BioNemo server connection")
def test_decode(bionemo_base_client, model_name):
    num_samples = 10
    bionemo_client = BioNemoServiceClient(bionemo_base_client, model_name=model_name)
    features = np.random.rand(1, num_samples, bionemo_client.num_latent_dimensions).astype(np.float32)
    smis = bionemo_client.decode(features)
    assert len(smis) == num_samples
    for sample in smis:
        assert isinstance(sample, str)


@pytest.mark.parametrize('model_name', ('molmim', 'moflow'))
@pytest.mark.skipif(not BIONEMO_SERVER_LIVE, reason="No BioNemo server connection")
def test_decode_bad_input(bionemo_base_client, model_name):
    bionemo_client = BioNemoServiceClient(bionemo_base_client, model_name=model_name)
    bad_features = np.random.rand(1, 1, bionemo_client.num_latent_dimensions + 10).astype(np.float32)
    with pytest.raises(ValueError):
        bionemo_client.decode(bad_features)


@pytest.mark.skipif(not BIONEMO_SERVER_LIVE, reason="No BioNemo server connection")
def test_bad_model_entry(bionemo_base_client):
    with pytest.raises(ValueError):
        BioNemoServiceClient(bionemo_base_client, model_name='notamodel')


@pytest.mark.skipif(not BIONEMO_SERVER_LIVE, reason="No BioNemo server connection")
def test_no_api_endpoint():
    class MockAPI:
        pass

    base_client = MockAPI()
    with pytest.raises(RuntimeError):
        BioNemoServiceClient(base_client)  # noqa intentional type mismatch


@pytest.mark.parametrize('model_name', ('molmim', 'moflow'))
@pytest.mark.skipif(not BIONEMO_SERVER_LIVE, reason="No BioNemo server connection")
def test_round_trip_identical(bionemo_base_client, model_name):
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
    ]
    bionemo_client = BioNemoServiceClient(bionemo_base_client, model_name=model_name)

    encoding = bionemo_client.encode(smis)
    decoding = bionemo_client.decode(encoding)
    assert smis == decoding


@pytest.mark.parametrize('model_name', ('molmim', 'moflow'))
@pytest.mark.skipif(not BIONEMO_SERVER_LIVE, reason="No BioNemo server connection")
def test_round_trip_perturbation_not_identical(bionemo_base_client, model_name):
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
    ]
    bionemo_client = BioNemoServiceClient(bionemo_base_client, model_name=model_name)

    encoding = bionemo_client.encode(smis)
    encoding += np.random.rand(*encoding.shape)
    decoding = bionemo_client.decode(encoding)
    assert smis != decoding


@pytest.mark.skipif(BIONEMO_SERVER_LIVE, reason="BioNemo server is live")
def test_graceful_failure_if_not_installed():
    with pytest.raises(RuntimeError):
        BioNemoServiceClient(None)  # noqa type mismatch
