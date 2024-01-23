import numpy as np
import pandas as pd
import pytest
from sklearn import datasets
import multivariateach as mt

def test_manova_skulls():
    """
    This test recreates that in the SAS documentation which
    describes the math for MANOVA:

    https://documentation.sas.com/doc/en/statcdc/14.2/statug/statug_introreg_sect038.htm

    """

    X, Y, L, M = skulls()
    results = mt.run_manova(X, Y, L, M)

    expected_wilks_lambda = 0.60143661
    expected_pillais_trace = 0.44702843
    expected_hotelling_lawley_trace = 0.58210348
    expected_roys_largest_root = 0.35530890

    # Assert that the result meets your expectations
    assert results.wilks_lambda.statistic == pytest.approx(expected_wilks_lambda, rel=1e-6)
    assert results.pillais_trace.statistic == pytest.approx(expected_pillais_trace, rel=1e-6)
    assert results.hotelling_lawley_trace.statistic == pytest.approx(expected_hotelling_lawley_trace, rel=1e-6)
    assert results.roys_largest_root.statistic == pytest.approx(expected_roys_largest_root, rel=1e-6)

def test_manova_iris():
    """
    This is the well-known iris data set.

    To re-create these results in SAS, first save the data from
    Python with the following:

    ----8<----8<----8<----
from sklearn import datasets

iris = datasets.load_iris()
data = iris.data
target = iris.target
target_names = iris.target_names

# Convert numerical target values to their corresponding string labels
species = [target_names[i] for i in target]

# Combine data and species into a single list of tuples
combined_data = list(zip(data, species))

# Print the combined data in a SAS-compatible format
for row in combined_data:
    print("{:.1f} {:.1f} {:.1f} {:.1f} {}".format(row[0][0], row[0][1], row[0][2], row[0][3], row[1]))
    ---->8---->8---->8----

    Then, paste the output from that into the appropriate place in
    the following SAS program:

data iris;
    input Sepal_Length Sepal_Width Petal_Length Petal_Width Species $;
    datalines;
5.1 3.5 1.4 0.2 Setosa
4.9 3.0 1.4 0.2 Setosa
4.7 3.2 1.3 0.2 Setosa
...
7.4 2.8 6.1 1.9 Virginica
7.9 3.8 6.4 2.0 Virginica
6.4 2.8 5.6 2.2 Virginica
;
run;

proc glm data=iris;
    class Species;
    model Sepal_Length Sepal_Width Petal_Length Petal_Width = Species / nouni;
    manova h=Species;
run;
quit;

    """

    X, Y, L, M = iris()
    results = mt.run_manova(X, Y, L, M)

    expected_wilks_lambda = 0.023438630650877965
    expected_pillais_trace = 1.191898825041458
    expected_hotelling_lawley_trace = 32.4773202409019
    expected_roys_largest_root = 32.19192919827884

    # Assert that the result meets your expectations
    assert results.wilks_lambda.statistic == pytest.approx(expected_wilks_lambda, rel=1e-6)
    assert results.pillais_trace.statistic == pytest.approx(expected_pillais_trace, rel=1e-6)
    assert results.hotelling_lawley_trace.statistic == pytest.approx(expected_hotelling_lawley_trace, rel=1e-6)
    assert results.roys_largest_root.statistic == pytest.approx(expected_roys_largest_root, rel=1e-6)

def test_box_m_iris():
    """
    We check Box's M test with the Iris data.
    """

    X, Y, _, _ = iris()
    results = mt.perform_box_m_test(X, Y)

    expected_statistic = 146.6632492125118
    expected_chi2 = 140.94304992349774
    expected_df = 20
    expected_p_value = 0

    assert results.statistic == pytest.approx(expected_statistic, rel = 1e-6)
    assert results.chi2      == pytest.approx(expected_chi2, rel = 1e-6)
    assert results.df        == pytest.approx(expected_df, rel = 1e-6)
    assert results.p_value   == pytest.approx(expected_p_value, rel = 1e-6)

def test_mauchly_iris():
    """
    Mauchly's test for sphericity, again with the Iris data.
    """
    X, Y, _, _ = iris()
    results = mt.mauchly(X, Y)

    expected_statistic = 0.5581441308964978
    expected_chi2 = 84.97617263316313
    expected_df = 5
    expected_p_value = 0

    assert results.statistic == pytest.approx(expected_statistic, rel = 1e-6)
    assert results.chi2      == pytest.approx(expected_chi2, rel = 1e-6)
    assert results.df        == pytest.approx(expected_df, rel = 1e-6)
    assert results.p_value   == pytest.approx(expected_p_value, rel = 1e-6)

def test_greenhouse_geisser_iris():

    X, Y, _, _ = iris()
    levels = np.array(np.arange(Y.shape[1])) + 1
    degree = Y.shape[1] - 1
    M = mt.create_orthopolynomial_contrasts(levels, degree)

    epsilon = mt.greenhouse_geisser_correction(X, Y, M)

    expected_epsilon = 360.62415882399614

    assert epsilon == pytest.approx(epsilon, rel = 1e-6)

# Data loaders

def skulls():

    data = pd.DataFrame([
        ['Minas Graes, Brazil',  2.068, 2.070, 1.580],
        ['Minas Graes, Brazil',  2.068, 2.074, 1.602],
        ['Minas Graes, Brazil',  2.090, 2.090, 1.613],
        ['Minas Graes, Brazil',  2.097, 2.093, 1.613],
        ['Minas Graes, Brazil',  2.117, 2.125, 1.663],
        ['Minas Graes, Brazil',  2.140, 2.146, 1.681],
        ['Matto Grosso, Brazil', 2.045, 2.054, 1.580],
        ['Matto Grosso, Brazil', 2.076, 2.088, 1.602],
        ['Matto Grosso, Brazil', 2.090, 2.093, 1.643],
        ['Matto Grosso, Brazil', 2.111, 2.114, 1.643],
        ['Santa Cruz, Bolivia',  2.093, 2.098, 1.653],
        ['Santa Cruz, Bolivia',  2.100, 2.106, 1.623],
        ['Santa Cruz, Bolivia',  2.104, 2.101, 1.653],
    ])
    data.columns = ['Loc', 'Basal', 'Occ', 'Max']

    X = mt.create_design_matrix(data, 'Loc')
    Y = mt.create_response_matrix(data, ['Basal', 'Occ', 'Max'])
    L = mt.create_type_iii_hypothesis_contrast(X)
    M = np.eye(Y.shape[1])

    return X, Y, L, M

def iris():
    iris = datasets.load_iris()

    data = pd.DataFrame(np.hstack([iris.target.reshape(-1, 1), iris.data]))
    data.columns = ['group', 'x1', 'x2', 'x3', 'x4']

    X = mt.create_design_matrix(data, 'group')
    Y = mt.create_response_matrix(data, ['x1', 'x2', 'x3', 'x4'])

    L = mt.create_type_iii_hypothesis_contrast(X)
    M = np.eye(Y.shape[1])

    return X, Y, L, M
