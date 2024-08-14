import pandas as pd
from .observer import Observer


class DataFrameHandler(Observer):

    def __init__(self):
        super().__init__()
        self.df = None

    def update(self, dataframe):
        self.df = dataframe

    def filter_rows(self, include=None, exclude=None):

        query = []

        def build_condition(column, condition, is_exclude=False):
            operator, value = condition
            if operator in ("==", "!=", "<", ">", "<=", ">="):
                if is_exclude:
                    return f"({column} {invert_operator(operator)} {repr(value)})"
                else:
                    return f"({column} {operator} {repr(value)})"
            elif operator == "in":
                if is_exclude:
                    return f"(~{column}.isin({value}))"
                else:
                    return f"({column}.isin({value}))"
            elif operator == "contains":
                if is_exclude:
                    return f"(~{column}.str.contains({repr(value)}))"
                else:
                    return f"({column}.str.contains({repr(value)}))"
            else:
                raise ValueError(f"Unsupported operator: {operator}")

        def invert_operator(operator):
            return {"==": "!=", "!=": "==", "<": ">=", ">": "<=", "<=": ">", ">=": "<"}[
                operator
            ]

        if include:
            query += [
                (
                    build_condition(col, val)
                    if isinstance(val, tuple)
                    else build_condition(col, ("==", val))
                )
                for col, val in include.items()
            ]

        if exclude:
            query += [
                (
                    build_condition(col, val, is_exclude=True)
                    if isinstance(val, tuple)
                    else build_condition(col, ("!=", val))
                )
                for col, val in exclude.items()
            ]
        query = " & ".join(query)
        return self.df.query(query)

    def group_and_aggregate(self, group_by, **aggregations):
        """그룹화 및 집계"""
        return self.df.groupby(group_by).agg(aggregations)

    def fill_missing(self, strategy="mean", columns=None):
        """결측값 채우기"""
        if columns is None:
            columns = self.df.select_dtypes(include="number").columns
        else:
            columns = self.df[columns].select_dtypes(include="number").columns

        if strategy == "mean":
            self.df[columns] = self.df[columns].fillna(self.df[columns].mean())
        elif strategy == "median":
            self.df[columns] = self.df[columns].fillna(self.df[columns].median())
        elif strategy == "mode":
            self.df[columns] = self.df[columns].fillna(self.df[columns].mode().iloc[0])
        elif strategy == "ffill":
            self.df[columns] = self.df[columns].fillna(method="ffill")
        elif strategy == "bfill":
            self.df[columns] = self.df[columns].fillna(method="bfill")

        return self.df

    def normalize(self, columns=None):
        """정규화"""
        if columns is None:
            columns = self.df.select_dtypes(include="number").columns
        else:
            columns = self.df[columns].select_dtypes(include="number").columns

        self.df[columns] = (self.df[columns] - self.df[columns].mean()) / self.df[
            columns
        ].std()

        return self.df
