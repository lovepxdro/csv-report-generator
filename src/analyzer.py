from dataclasses import dataclass

import pandas as pd


@dataclass
class DatasetAnalysis:
    rows: int
    columns: int
    numeric_columns: list[str]
    categorical_columns: list[str]
    datetime_columns: list[str]
    null_values: dict[str, int]


class DatasetAnalyzer:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def _detect_datetime_columns(self) -> list[str]:
        datetime_columns = []

        for column in self.df.columns:
            series = self.df[column]

            if pd.api.types.is_datetime64_any_dtype(series):
                datetime_columns.append(column)
                continue

            if not pd.api.types.is_string_dtype(series):
                continue

            converted = pd.to_datetime(
                series,
                errors="coerce",
                format="mixed",
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.8:
                self.df[column] = converted
                datetime_columns.append(column)

        return datetime_columns

    def analyze(self) -> DatasetAnalysis:
        datetime_columns = self._detect_datetime_columns()

        numeric_columns = list(self.df.select_dtypes(include="number").columns)

        categorical_columns = [
            column
            for column in self.df.columns
            if column not in numeric_columns and column not in datetime_columns
        ]

        return DatasetAnalysis(
            rows=len(self.df),
            columns=len(self.df.columns),
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            datetime_columns=datetime_columns,
            null_values=self.df.isnull().sum().to_dict(),
        )
