from typing import List
from uuid import NAMESPACE_DNS, uuid5

from pandas import DataFrame, Series
from typeguard import typechecked

from tommytomato_utils.hashing_client.constants import HASHING_FIELD_SEPARATOR
from tommytomato_utils.hashing_client.exceptions import \
    DuplicateHashValuesError  # New custom exception
from tommytomato_utils.hashing_client.exceptions import MissingHashColumnsError


class HashingClient:
    """
    Client to generate a hash based on either a list of string values or specific columns of a
    DataFrame.
    """

    @typechecked
    @staticmethod
    def get_hash_uuid_from_string(string_value: str) -> str:
        string_value = str(string_value)
        output_hash = str(uuid5(NAMESPACE_DNS, string_value))
        return output_hash

    @typechecked
    @staticmethod
    def add_dataframe_column_hash_given_column_names(
        dataframe: DataFrame,
        hash_column_names: List[str],
        column_name: str,
        allow_duplicates: bool = True,
    ) -> DataFrame:
        try:
            concatenated_columns = Series(
                map(
                    HASHING_FIELD_SEPARATOR.join,
                    dataframe[hash_column_names].astype(str).values.tolist(),
                ),
                index=dataframe.index,
            )
        except KeyError:
            raise MissingHashColumnsError(dataframe, hash_column_names)

        if not allow_duplicates:
            duplicate_values = concatenated_columns[concatenated_columns.duplicated()]
            if not duplicate_values.empty:
                raise DuplicateHashValuesError(duplicate_values)

        dataframe[column_name] = concatenated_columns.apply(
            HashingClient.get_hash_uuid_from_string
        )
        return dataframe
