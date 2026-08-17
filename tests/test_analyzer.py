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
