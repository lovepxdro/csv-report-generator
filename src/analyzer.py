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

    numeric_stats: dict[str, dict[str, float | None]]
    numeric_types: dict[str, str]

    unique_values: dict[str, int]
    date_ranges: dict[str, dict[str, pd.Timestamp]]

    primary_metric: str | None
    profile_type: str

    top_correlations: list[dict[str, float | str]]


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

    def _detect_numeric_types(
        self,
        numeric_columns: list[str],
    ) -> dict[str, str]:
        numeric_types = {}

        for column in numeric_columns:
            series = self.df[column].dropna()

            if series.empty:
                numeric_types[column] = "unknown"
                continue

            unique_values = series.nunique()

            if unique_values <= 2:
                numeric_types[column] = "binary"

            elif pd.api.types.is_integer_dtype(series):
                if unique_values <= 20:
                    numeric_types[column] = "discrete"
                else:
                    numeric_types[column] = "continuous"

            else:
                numeric_types[column] = "continuous"

        return numeric_types

    def _build_numeric_stats(
        self,
        numeric_columns: list[str],
        numeric_types: dict[str, str],
    ) -> dict[str, dict[str, float | None]]:
        stats = {}

        for column in numeric_columns:
            series = self.df[column].dropna()

            if series.empty:
                continue

            mean = float(series.mean())
            std = float(series.std())

            column_type = numeric_types[column]

            cv = None

            if (
                column_type == "continuous"
                and mean != 0
                and abs(mean) > 1e-9
            ):
                cv = abs(std / mean)

            stats[column] = {
                "mean": mean,
                "min": float(series.min()),
                "max": float(series.max()),
                "sum": float(series.sum()),
                "std": std,
                "cv": cv,
            }

        return stats

    def _build_unique_values(
        self,
        categorical_columns: list[str],
    ) -> dict[str, int]:
        return {
            column: int(
                self.df[column].nunique(dropna=True)
            )
            for column in categorical_columns
        }

    def _build_date_ranges(
        self,
        datetime_columns: list[str],
    ) -> dict[str, dict[str, pd.Timestamp]]:
        ranges = {}

        for column in datetime_columns:
            series = self.df[column].dropna()

            if series.empty:
                continue

            ranges[column] = {
                "min": series.min(),
                "max": series.max(),
            }

        return ranges

    def _select_primary_metric(
        self,
        numeric_columns: list[str],
    ) -> str | None:
        if not numeric_columns:
            return None

        high_priority = [
            "valor",
            "receita",
            "revenue",
            "faturamento",
            "amount",
            "sales",
            "vendas",
            "preco",
            "price",
            "total",
        ]

        medium_priority = [
            "quantidade",
            "quantity",
            "volume",
            "count",
        ]

        low_priority = [
            "id",
            "codigo",
            "code",
            "idade",
            "age",
            "latitude",
            "longitude",
            "ano",
            "year",
        ]

        def score(column: str) -> int:
            normalized = (
                column.lower()
                .strip()
                .replace("_", " ")
            )

            for keyword in high_priority:
                if keyword in normalized:
                    return 100

            for keyword in medium_priority:
                if keyword in normalized:
                    return 50

            for keyword in low_priority:
                if keyword == normalized:
                    return -100

            return 10

        scored = [
            (column, score(column))
            for column in numeric_columns
        ]

        best_column, best_score = max(
            scored,
            key=lambda item: item[1],
        )

        if best_score < 50:
            return None

        return best_column

    def _detect_profile(
        self,
        numeric_columns: list[str],
        categorical_columns: list[str],
        datetime_columns: list[str],
    ) -> str:
        total_columns = len(self.df.columns)

        if total_columns == 0:
            return "unknown"

        numeric_ratio = len(numeric_columns) / total_columns
        categorical_ratio = (
            len(categorical_columns) / total_columns
        )
        datetime_ratio = (
            len(datetime_columns) / total_columns
        )

        if numeric_ratio >= 0.8:
            return "numeric"

        if categorical_ratio >= 0.8:
            return "categorical"

        if (
            datetime_columns
            and numeric_columns
            and not categorical_columns
        ):
            return "temporal"

        if (
            datetime_columns
            and datetime_ratio >= 0.5
        ):
            return "temporal"

        return "mixed"

    def _build_top_correlations(
        self,
        numeric_columns: list[str],
        limit: int = 10,
    ) -> list[dict[str, float | str]]:
        if len(numeric_columns) < 2:
            return []

        correlation_matrix = (
            self.df[numeric_columns].corr()
        )

        correlations = []

        for index, column_a in enumerate(
            numeric_columns
        ):
            for column_b in numeric_columns[
                index + 1:
            ]:
                value = correlation_matrix.loc[
                    column_a,
                    column_b,
                ]

                if pd.isna(value):
                    continue

                correlations.append(
                    {
                        "column_a": column_a,
                        "column_b": column_b,
                        "correlation": float(value),
                    }
                )

        correlations.sort(
            key=lambda item: abs(
                item["correlation"]
            ),
            reverse=True,
        )

        return correlations[:limit]

    def analyze(self) -> DatasetAnalysis:
        datetime_columns = (
            self._detect_datetime_columns()
        )

        numeric_columns = list(
            self.df.select_dtypes(
                include="number"
            ).columns
        )

        categorical_columns = [
            column
            for column in self.df.columns
            if column not in numeric_columns
            and column not in datetime_columns
        ]

        numeric_types = (
            self._detect_numeric_types(
                numeric_columns
            )
        )

        numeric_stats = (
            self._build_numeric_stats(
                numeric_columns,
                numeric_types,
            )
        )

        return DatasetAnalysis(
            rows=len(self.df),
            columns=len(self.df.columns),

            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            datetime_columns=datetime_columns,

            null_values=(
                self.df.isnull()
                .sum()
                .to_dict()
            ),

            numeric_stats=numeric_stats,
            numeric_types=numeric_types,

            unique_values=(
                self._build_unique_values(
                    categorical_columns
                )
            ),

            date_ranges=(
                self._build_date_ranges(
                    datetime_columns
                )
            ),

            primary_metric=(
                self._select_primary_metric(
                    numeric_columns
                )
            ),

            profile_type=(
                self._detect_profile(
                    numeric_columns,
                    categorical_columns,
                    datetime_columns,
                )
            ),

            top_correlations=(
                self._build_top_correlations(
                    numeric_columns
                )
            ),
        )

    def get_dataframe(self) -> pd.DataFrame:
        return self.df.copy()
