# coding: utf-8

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification


def make_uplift_problem(
        n_samples_per_group: int = 1000,
        n_features: int = 10,
        n_informative: int = 5,
        n_uplift_mix_informative: int = 5,
        n_redundant: int = 0,
        n_repeated: int = 0,
        flip_y: float = 0.,
        pos_weight: float = 0.5,
        delta_uplift_increase: float = 0.1,
        random_seed: int = None,
):
    """
    Generate a synthetic dataset for classification uplift problem with binary treatment.

    Parameters
    ----------
    n_samples_per_group : int, optional (default=1000)
        The number of samples per group.
    n_features : int, optional (default=10)
        The total number of features.
    n_informative : int, optional (default=5)
        The number of informative features.
    n_uplift_mix_informative : int, optional (default=5)
        The number of mix features.
    n_redundant : int, optional (default=0)
        The number of redundant features.
    n_repeated : int, optional (default=0)
        The number of duplicated features, drawn randomly from the informative
        and the redundant features.
    flip_y : float, optional (default=0.)
        The fraction of samples whose class is assigned randomly.
    pos_weight : float, optional (default=0.5)
        The proportions of samples assigned to positive class.
    delta_uplift_increase : float, optional (default=0.1)
        Positive treatment effect.
    random_seed : int, optional (default=None)
        Random seed.
    Returns
    -------
    output : DataFrame
        Data frame with the treatment, label, features, and effect.
    features : list of strings
        Feature names in output.
    References
    ----------
    [1] I. Guyon, "Design of experiments for the NIPS 2003 variable selection benchmark", 2003.
    """
    if random_seed is not None:
        np.random.seed(seed=random_seed)
    # dataset dataframe
    output = pd.DataFrame()
    n_samples = n_samples_per_group * 2
    # generate treatments
    treatments = [0] * n_samples_per_group + [1] * n_samples_per_group
    treatments = np.random.permutation(treatments)
    output["treatment"] = treatments
    X1, Y1 = make_classification(n_samples=n_samples, n_features=n_features, n_informative=n_informative,
                                 n_redundant=n_redundant, n_repeated=n_repeated, n_clusters_per_class=1,
                                 weights=[1 - pos_weight, pos_weight], flip_y=flip_y)
    features = []
    x_informative_name = []
    for i in range(n_informative):
        x_name_i = "x" + str(len(features) + 1) + "_informative"
        features.append(x_name_i)
        x_informative_name.append(x_name_i)
        output[x_name_i] = X1[:, i]
    for i in range(n_redundant):
        x_name_i = "x" + str(len(features) + 1) + "_redundant"
        features.append(x_name_i)
        output[x_name_i] = X1[:, n_informative + i]
    for i in range(n_repeated):
        x_name_i = "x" + str(len(features) + 1) + "_repeated"
        features.append(x_name_i)
        output[x_name_i] = X1[:, n_informative + n_redundant + i]
    for i in range(n_features - n_informative - n_redundant - n_repeated):
        x_name_i = "x" + str(len(features) + 1) + "_irrelevant"
        features.append(x_name_i)
        output[x_name_i] = np.random.normal(0, 1, n_samples)
    # default treatment effects
    Y = Y1.copy()
    # generate positive uplift signal
    treatment_index = output.index[output["treatment"] == 1].tolist()
    x_uplift_increase_name = []
    adjust_class_proportion = delta_uplift_increase / (1 - pos_weight)
    X_increase, Y_increase = make_classification(n_samples=n_samples, n_features=n_informative,
                                                 n_informative=n_informative, n_redundant=0,
                                                 n_clusters_per_class=1,
                                                 weights=[1 - adjust_class_proportion, adjust_class_proportion])
    for i in range(n_informative):  # informative x
        x_name_i = "x" + str(len(features) + 1) + "_uplift_increase"
        features.append(x_name_i)
        x_uplift_increase_name.append(x_name_i)
        output[x_name_i] = X_increase[:, i]
    Y[treatment_index] = Y[treatment_index] + Y_increase[treatment_index]
    if n_uplift_mix_informative > 0:  # mix informative x
        for i in range(n_uplift_mix_informative):
            x_name_i = "x" + str(len(features) + 1) + "_uplift_increase_mix"
            features.append(x_name_i)
            output[x_name_i] = (np.random.uniform(-1, 1) * output[np.random.choice(x_informative_name)]
                                + np.random.uniform(-1, 1) * output[np.random.choice(x_uplift_increase_name)])

    Y = np.clip(Y, 0, 1)
    output['label'] = Y
    output["effect"] = Y - Y1
    return output, features
