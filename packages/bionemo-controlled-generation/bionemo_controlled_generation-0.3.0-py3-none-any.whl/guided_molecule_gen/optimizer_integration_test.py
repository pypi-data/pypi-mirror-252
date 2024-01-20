import numpy as np
import pytest

from guided_molecule_gen.optimizer import MoleculeGenerationOptimizer
from guided_molecule_gen.oracles import molmim_qed_with_similarity, qed, tanimoto_similarity
from guided_molecule_gen.testutils.check_client import TRITON_SERVER_LIVE


def scoring_function(smis, **kwargs):
    reference: str = kwargs['reference']
    scores = molmim_qed_with_similarity(smis, reference)
    return -1 * scores


@pytest.mark.long
@pytest.mark.skipif(not TRITON_SERVER_LIVE, reason="No triton server connection")
def test_optimize(client, optimizer_args):
    num_steps = 20
    pop_size = 20
    num_molecules = 5
    similarity_threshold = 0.3  # Target is 0.4, add some buffer for noise and low iterations

    # Taken from MolMIM QED testset
    smis = [
        "CC(=O)NCCNC(=O)c1cnn(-c2ccc(C)c(Cl)c2)c1C1CC1",
        "C[C@@H](C(=O)C1=c2ccccc2=[NH+]C1)[NH+]1CCC[C@@H]1[C@@H]1CC=CS1",
        "CCN(C[C@@H]1CCOC1)C(=O)c1ccnc(Cl)c1",
        "Cc1ccccc1C[S@](=O)CCCc1ccccc1",
        "CSCC(=O)NNC(=O)c1c(O)cc(Cl)cc1Cl",
    ]
    oracle = scoring_function
    original_qeds = qed(smis)
    optimizer = MoleculeGenerationOptimizer(client, oracle, smis, popsize=pop_size, optimizer_args=optimizer_args)
    optimizer.optimize(num_steps)

    # Score all the molecules
    similarities = np.zeros((num_molecules, pop_size))
    qeds = np.zeros_like(similarities)

    for molecule_num in range(num_molecules):
        reference_smi = smis[molecule_num]

        smi_selection = optimizer.generated_smis[molecule_num]

        similarities[molecule_num, :] = tanimoto_similarity(smi_selection, reference_smi)
        qeds[molecule_num, :] = qed(smi_selection)

    # Use median because there are 0 values from invalid smiles dragging down the mean.
    assert np.median(qeds) > np.median(original_qeds)
    assert np.median(similarities) > similarity_threshold
