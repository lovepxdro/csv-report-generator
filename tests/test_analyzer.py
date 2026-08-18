import pandas as pd

from src.analyzer import DatasetAnalyzer


def test_detects_numeric_columns():
    df = pd.DataFrame(
        {
            "produto": ["A", "B"],
            "quantidade": [10, 20],
            "valor": [100.0, 200.0],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.numeric_columns == ["quantidade", "valor"]


def test_detects_categorical_columns():
    df = pd.DataFrame(
        {
            "produto": ["A", "B"],
            "regiao": ["Recife", "Olinda"],
            "valor": [100, 200],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.categorical_columns == ["produto", "regiao"]


def test_detects_datetime_columns():
    df = pd.DataFrame(
        {
            "data": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03",
            ],
            "valor": [100, 200, 300],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.datetime_columns == ["data"]
    assert "data" not in analysis.categorical_columns


def test_counts_null_values():
    df = pd.DataFrame(
        {
            "produto": ["A", None, "C"],
            "valor": [100, 200, None],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.null_values["produto"] == 1
    assert analysis.null_values["valor"] == 1

    
def test_generates_numeric_statistics():
    df = pd.DataFrame(
        {
            "valor": [100, 200, 300],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    stats = analysis.numeric_stats["valor"]

    assert stats["mean"] == 200
    assert stats["min"] == 100
    assert stats["max"] == 300
    assert stats["sum"] == 600


def test_counts_unique_categorical_values():
    df = pd.DataFrame(
        {
            "regiao": [
                "Recife",
                "Recife",
                "Olinda",
            ]
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.unique_values["regiao"] == 2


def test_generates_date_range():
    df = pd.DataFrame(
        {
            "data": [
                "2026-01-01",
                "2026-01-05",
                "2026-01-03",
            ]
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert str(
        analysis.date_ranges["data"]["min"].date()
    ) == "2026-01-01"

    assert str(
        analysis.date_ranges["data"]["max"].date()
    ) == "2026-01-05"
    
def test_detects_mixed_profile():
    df = pd.DataFrame(
        {
            "data": ["2026-01-01", "2026-01-02"],
            "categoria": ["A", "B"],
            "valor": [100, 200],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.profile_type == "mixed"


def test_detects_numeric_profile():
    df = pd.DataFrame(
        {
            "feature_a": [1, 2, 3],
            "feature_b": [4, 5, 6],
            "feature_c": [7, 8, 9],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.profile_type == "numeric"


def test_selects_primary_metric():
    df = pd.DataFrame(
        {
            "quantidade": [1, 2, 3],
            "valor": [100, 200, 300],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.primary_metric == "valor"


def test_returns_none_when_primary_metric_is_unknown():
    df = pd.DataFrame(
        {
            "CRIM": [1, 2, 3],
            "ZN": [4, 5, 6],
            "RM": [7, 8, 9],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.primary_metric is None


def test_calculates_standard_deviation():
    df = pd.DataFrame(
        {
            "valor": [10, 20, 30],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert round(
        analysis.numeric_stats["valor"]["std"],
        2,
    ) == 10.00


def test_finds_strongest_correlations():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": [2, 4, 6, 8],
            "c": [8, 2, 7, 1],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    strongest = analysis.top_correlations[0]

    assert strongest["column_a"] == "a"
    assert strongest["column_b"] == "b"
    assert strongest["correlation"] == 1.0
    
def test_calculates_coefficient_of_variation():
    df = pd.DataFrame(
        {
            "valor": [10.5, 20.2, 30.8, 40.1],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    stats = analysis.numeric_stats["valor"]

    expected = stats["std"] / stats["mean"]

    assert stats["cv"] is not None

    assert round(
        stats["cv"],
        4,
    ) == round(
        expected,
        4,
    )
    
def test_detects_binary_numeric_column():
    df = pd.DataFrame(
        {
            "flag": [0, 1, 0, 1],
            "valor": [10.5, 20.5, 30.5, 40.5],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.numeric_types["flag"] == "binary"


def test_does_not_calculate_cv_for_binary_column():
    df = pd.DataFrame(
        {
            "flag": [0, 1, 0, 1],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert (
        analysis.numeric_stats["flag"]["cv"]
        is None
    )


def test_detects_continuous_numeric_column():
    df = pd.DataFrame(
        {
            "valor": [
                1.2,
                2.4,
                3.7,
                4.9,
            ]
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert (
        analysis.numeric_types["valor"]
        == "continuous"
    )
    

def test_detects_categorical_profile():
    df = pd.DataFrame(
        {
            "departamento": ["TI", "RH", "TI"],
            "status": ["Ativo", "Ativo", "Inativo"],
            "regiao": ["Recife", "Olinda", "Recife"],
        }
    )

    analysis = DatasetAnalyzer(df).analyze()

    assert analysis.profile_type == "categorical"
