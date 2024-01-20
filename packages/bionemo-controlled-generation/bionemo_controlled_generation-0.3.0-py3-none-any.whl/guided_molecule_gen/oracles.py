# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
"""Collection of oracles, for users and for testing. Note that user can always bring in their own scoring functions."""


from typing import Any, Callable, List, Optional

import numpy as np
from rdkit import Chem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem.Descriptors import MolLogP as rdkit_logp
from rdkit.Chem.QED import qed as rdkit_qed
from rdkit.DataStructs import TanimotoSimilarity

# Global instances of TDC oracles that require either model downloads or local files. Will
# be instantiated at first usage to avoid repeated loads.
JNK: Optional[Any] = None
GSK3B: Optional[Any] = None

TDC_SUPPORTED = False


def _check_tdc_compatibility():
    global TDC_SUPPORTED
    if TDC_SUPPORTED:
        return
    try:
        from tdc import Oracle
    except ImportError:
        print("Unable to import PyTDC. For full installation, run pip install guided_molecule_gen[extra_oracles]")
        raise
    if np.version.full_version != "1.22.4":
        raise RuntimeError(
            f"For TDC oracles, numpy version 1.22.4 is required. Your version: {np.version.full_version}"
        )
    TDC_SUPPORTED = True
    global JNK, GSK3B
    JNK = Oracle("jnk3")
    GSK3B = Oracle("gsk3b")


def _iterate_and_score_smiles(
    smis: List[str], scorer: Callable[[Chem.Mol], float], default_val: float = 0.0
) -> np.ndarray:
    """Iterates over a list of smiles, loading into RDKit and scoring based on the callback.

    If RDKit parsing fails, assigns the default value.


    Returns an array of length smis
    """
    results: np.ndarray = np.zeros((len(smis),)) + default_val
    for i, smi in enumerate(smis):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        results[i] = scorer(mol)
    return results


def qed(smis: List[str]) -> np.ndarray:
    """Compute QED score for a list of molecules.

    Returns zeros for smiles that RDKit cannot parse.

    Parameters
    ----------
    smis : List[str]

    Returns
    -------
    np.ndarray
        QED scores for each smiles string.
    """
    return _iterate_and_score_smiles(smis, rdkit_qed, default_val=0.0)


def logp(smis: List[str]):
    """Compute logP for a list of molecules.

    Returns zeros for smiles that RDKit cannot parse.

    Parameters
    ----------
    smis : List[str]

    Returns
    -------
    np.ndarray
        logP values for each smiles string.
    """
    return _iterate_and_score_smiles(smis, rdkit_logp, default_val=0.0)


def penalized_logp(smis: List[str]) -> np.ndarray:
    from tdc.chem_utils.oracle.oracle import penalized_logp as tdc_penalized_logp

    results: np.ndarray = np.zeros((len(smis),))
    for i, smi in enumerate(smis):
        try:
            results[i] = tdc_penalized_logp(smi)
        except ZeroDivisionError:
            results[i] = -100

    return results


def jnk3(smis: List[str]) -> np.ndarray:
    _check_tdc_compatibility()

    results: np.ndarray = np.zeros((len(smis),))
    for i, smi in enumerate(smis):
        results[i] = JNK(smi)

    return results


def gsk3b(smis: List[str]) -> np.ndarray:
    _check_tdc_compatibility()

    results: np.ndarray = np.zeros((len(smis),))
    for i, smi in enumerate(smis):
        results[i] = GSK3B(smi)

    return results


def synthetic_accessibility(smis: List[str]) -> np.ndarray:
    _check_tdc_compatibility()
    from tdc.chem_utils.oracle.oracle import SA as tdc_SA  # noqa not a constant

    results: np.ndarray = np.zeros((len(smis),))
    for i, smi in enumerate(smis):
        try:
            results[i] = tdc_SA(smi)
        except ZeroDivisionError:
            results[i] = 100
    return results


def tanimoto_similarity(smis: List[str], reference: str):
    fingerprint_radius_param = 2
    fingerprint_nbits = 2048

    reference_mol = Chem.MolFromSmiles(reference)
    if reference_mol is None:
        raise ValueError(f"Invalid reference smiles {reference}")
    reference_fingerprint = GetMorganFingerprintAsBitVect(
        reference_mol, radius=fingerprint_radius_param, nBits=fingerprint_nbits
    )

    results: np.ndarray = np.zeros((len(smis),))
    for i, smi in enumerate(smis):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue

        fingerprint = GetMorganFingerprintAsBitVect(mol, radius=fingerprint_radius_param, nBits=fingerprint_nbits)
        results[i] = TanimotoSimilarity(fingerprint, reference_fingerprint)
    return results


def molmim_qed_with_similarity(smis: List[str], reference: str):
    """Computes a score based on QED and Tanimoto similarity, based on the MolMIM paper.

    Returns zeros for smiles that RDKit cannot parse, raises ValueError if the reference is not parsable.

    Reference publication - https://arxiv.org/pdf/2208.09016.pdf, Appendix 3.1

    """
    qed_scaling_factor: float = 0.9
    similarity_scaling_factor: float = 0.4

    fingerprint_radius_param = 2
    fingerprint_nbits = 2048

    reference_mol = Chem.MolFromSmiles(reference)
    if reference_mol is None:
        raise ValueError(f"Invalid reference smiles {reference}")
    reference_fingerprint = GetMorganFingerprintAsBitVect(
        reference_mol, radius=fingerprint_radius_param, nBits=fingerprint_nbits
    )

    results: np.ndarray = np.zeros((len(smis),))
    for i, smi in enumerate(smis):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue

        rdkit_qed_score: float = rdkit_qed(mol)
        fingerprint = GetMorganFingerprintAsBitVect(mol, radius=fingerprint_radius_param, nBits=fingerprint_nbits)
        rdkit_similarity_score: float = TanimotoSimilarity(fingerprint, reference_fingerprint)

        results[i] = np.clip(rdkit_qed_score / qed_scaling_factor, 0, 1) + np.clip(
            rdkit_similarity_score / similarity_scaling_factor, 0, 1
        )
    return results
