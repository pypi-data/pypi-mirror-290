from unittest import TestCase

from pandas import DataFrame
from pandas.testing import assert_frame_equal
from typeguard import TypeCheckError

from tommytomato_utils.hashing_client.exceptions import (
    DuplicateHashValuesError, MissingHashColumnsError
)
from tommytomato_utils.hashing_client.hashing_client import HashingClient


class TestHashGenerator(TestCase):

    def test_hashing_string(self):
        input_string = 'hello'
        expected_output = '9342d47a-1bab-5709-9869-c840b2eac501'
        output = HashingClient.get_hash_uuid_from_string(input_string)
        self.assertEqual(output, expected_output)

    def test_dataframe_hash_with_just_columns_needed(self):
        df = DataFrame({
            'col1': ['value1', 'value2'],
            'col2': ['value3', 'value4'],
        })
        hash_columns = ['col1', 'col2']

        expected_output = df.copy()
        expected_output['box_id'] = [
            '1f3ac418-9828-51c9-9404-f88123f7fa65', 'f9171cd3-e34d-50c2-993d-803a16ace55f'
        ]

        output = HashingClient.add_dataframe_column_hash_given_column_names(
            df, hash_columns, 'box_id'
        )
        assert_frame_equal(output, expected_output)

    def test_dataframe_hash_with_additional_column(self):
        """Same as previous test, but adding a new column that has no impact on output."""
        df = DataFrame(
            {
                'col1': ['value1', 'value2'],
                'col2': ['value3', 'value4'],
                'col3': ['value5', 'value6'],
            }
        )
        hash_columns = ['col1', 'col2']

        expected_output = df.copy()
        expected_output['box_id'] = [
            '1f3ac418-9828-51c9-9404-f88123f7fa65', 'f9171cd3-e34d-50c2-993d-803a16ace55f'
        ]

        output = HashingClient.add_dataframe_column_hash_given_column_names(
            df, hash_columns, 'box_id'
        )
        assert_frame_equal(output, expected_output)

    def test_missing_columns_error(self):
        df = DataFrame({
            'col1': ['value1', 'value2'],
        })
        hash_columns = ['col1', 'col2']  # Col 2 not in dataframe!

        with self.assertRaises(MissingHashColumnsError):
            HashingClient.add_dataframe_column_hash_given_column_names(df, hash_columns, 'box_id')

    def test_wrong_input_type(self):
        df = None
        with self.assertRaises(TypeCheckError):
            HashingClient.add_dataframe_column_hash_given_column_names(df, ['col1'], 'box_id')

    def test_no_duplicates_allowed_raises_error(self):
        df = DataFrame({
            'col1': ['value1', 'value1'],
            'col2': ['value3', 'value3'],
        })
        hash_columns = ['col1', 'col2']

        with self.assertRaises(DuplicateHashValuesError):
            HashingClient.add_dataframe_column_hash_given_column_names(
                df, hash_columns, 'box_id', allow_duplicates=False
            )

    def test_no_duplicates_allowed_passes(self):
        df = DataFrame({
            'col1': ['value1', 'value2'],
            'col2': ['value3', 'value4'],
        })
        hash_columns = ['col1', 'col2']

        expected_output = df.copy()
        expected_output['box_id'] = [
            '1f3ac418-9828-51c9-9404-f88123f7fa65', 'f9171cd3-e34d-50c2-993d-803a16ace55f'
        ]

        output = HashingClient.add_dataframe_column_hash_given_column_names(
            df, hash_columns, 'box_id', allow_duplicates=False
        )
        assert_frame_equal(output, expected_output)
