from unittest import mock

import numpy as np
import pytest

import guided_molecule_gen.oracles
from guided_molecule_gen.oracles import (
    gsk3b,
    jnk3,
    molmim_qed_with_similarity,
    penalized_logp,
    qed,
    synthetic_accessibility,
    tanimoto_similarity,
)

# Don't rely on the oracle module variable to know if we want to skip a test, it may not be initialized.
TDC_SUPPORTED = False
try:
    import tdc

    TDC_SUPPORTED = True
except ImportError:
    pass


def test_qed():
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',
        'xxxx',  # one invalid smiles
    ]

    want = [0.74746149, 0.5501218, 0.62165856, 0.0]
    got = qed(smis)
    np.testing.assert_allclose(got, want)


def test_similarity():
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',  # This is the identical one
        'Cc1cccc(N(C)C(=O)Oc2ccc3ccccc3c2)c1',  # This is highly similar, changed one atom typein the same column
        'xxxx',  # one invalid smiles
    ]

    want = [0.106667, 0.176471, 1.0, 0.714286, 0.0]
    reference = 'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1'

    got = tanimoto_similarity(smis, reference)
    np.testing.assert_allclose(got, want, rtol=10**-5)  # Calculation is a bit noisy


def test_similarity_bad_reference():
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',
        'xxxx',  # one invalid smiles
    ]
    reference = 'xxxxx'
    with pytest.raises(ValueError):
        tanimoto_similarity(smis, reference)


def test_molmim_qed_similarity():
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',
        'xxxx',  # one invalid smiles
    ]
    reference = 'CC(=O)Oc1ccccc1C(=O)O'  # Element 2, similarity score is 1
    want = [1.24034883, 1.61124644, 1.13190821, 0.0]
    got = molmim_qed_with_similarity(smis, reference)
    np.testing.assert_allclose(got, want)


def test_molmim_qed_similarity_bad_reference():
    smis = [
        'COc1cc2c(cc1OC)C(=O)C(CC1CCN(Cc3ccccc3)CC1)C2',
        'CC(=O)Oc1ccccc1C(=O)O',
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',
        'xxxx',  # one invalid smiles
    ]
    reference = 'xxxxx'
    with pytest.raises(ValueError):
        molmim_qed_with_similarity(smis, reference)


@pytest.mark.parametrize(
    "method,default_value", ((jnk3, 0.0), (gsk3b, 0.0), (synthetic_accessibility, 100.0), (penalized_logp, -100.0))
)
@pytest.mark.skipif(not TDC_SUPPORTED, reason="Py TDC not installed")
def test_tdc_oracles_execute(method, default_value):
    smis = [
        'Cc1cccc(N(C)C(=S)Oc2ccc3ccccc3c2)c1',
        'xxxx',
    ]

    num_smis = len(smis)
    results = method(smis)
    assert len(results) == num_smis
    assert results[0] != default_value
    assert results[1] == default_value


def test_no_tdc_support():
    # This is a dumb test, as we're just catching an importerror that's already thrown, but one can see the codepath
    # is exercised in the coverage report.
    smis = ["cccccc"]
    with mock.patch.dict('sys.modules', {'tdc': None}):
        # Set TDC support to false to execute code path
        guided_molecule_gen.oracles.TDC_SUPPORTED = False
        # your tests with foo.bar
        with pytest.raises(ImportError):
            jnk3(smis)


@pytest.mark.skipif(not TDC_SUPPORTED, reason="Py TDC not installed")
def test_tdc_bad_np_version():
    smis = ["cccccc"]
    with mock.patch('numpy.version') as mock_numpy_version:
        mock_numpy_version.full_version = "1.24.1"
        with pytest.raises(RuntimeError):
            jnk3(smis)
