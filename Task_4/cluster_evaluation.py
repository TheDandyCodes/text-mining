import bcubed
from sklearn.metrics import adjusted_rand_score


def bcubed_evaluation(ldict: dict, cdict: dict):
    """Evaluate clustering using BCubed metrics.

    Parameters
    ----------
    cdict : dict
        Predicted cluster labels.
    ldict : dict
        Ground truth labels.

    Returns
    -------
    tuple
        BCubed precision, recall, and F-score.
    """
    precision = bcubed.precision(cdict, ldict)
    recall = bcubed.recall(cdict, ldict)
    fscore = bcubed.fscore(precision, recall)

    return precision, recall, fscore


def ari_evaluation(ldict: dict, cdict: dict):
    """Evaluate clustering using Adjusted Rand Index (ARI).

    Parameters
    ----------
    ldict : dict
        Ground truth labels.
    cdict : dict
        Predicted cluster labels.

    Returns
    -------
    float
        ARI score.
    """
    return adjusted_rand_score(ldict, cdict)
