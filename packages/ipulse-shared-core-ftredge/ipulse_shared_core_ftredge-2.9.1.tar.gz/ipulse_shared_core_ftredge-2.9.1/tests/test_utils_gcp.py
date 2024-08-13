# pylint: disable=missing-module-docstring
# pylint: disable=import-error
# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long
# pylint: disable=missing-function-docstring

import os
import json
from unittest.mock import MagicMock, patch
import pytest
from ipulse_shared_core_ftredge.utils_cloud_gcp import write_json_to_gcs


# Mocking Google Cloud Storage components for testing using pytest-mock

@pytest.fixture
def mock_blob(mocker):
    mock_blob_class = mocker.patch('google.cloud.storage.Blob', autospec=True)
    mock_blob = mock_blob_class.return_value
    mock_blob.exists.return_value = False
    return mock_blob


@pytest.fixture
def mock_bucket(mocker, mock_blob):
    mock_bucket_class = mocker.patch('google.cloud.storage.Bucket', autospec=True)
    mock_bucket = mock_bucket_class.return_value
    mock_bucket.list_blobs.return_value = []
    mock_bucket.blob.return_value = mock_blob # this avoids creating a new blob for each test, which will confuse the test results
    return mock_bucket
 
@pytest.fixture
def mock_storage_client(mocker, mock_bucket):
    mock_client_class = mocker.patch('google.cloud.storage.Client', autospec=True)
    mock_client = mock_client_class.return_value
    mock_client.bucket.return_value = mock_bucket
    return mock_client



# --- Test Cases ---

def test_successful_gcs_upload(mock_storage_client):
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name, test_file_name)

    assert result['gcs_path'] == f"gs://{test_bucket_name}/{test_file_name}"
    assert result['local_path'] is None
    assert result['gcs_file_already_exists'] is False
    assert result['gcs_file_overwritten'] is False
    assert result['gcs_file_saved_with_increment'] is False


def test_invalid_data_type(mock_storage_client):
    with pytest.raises(ValueError) as exc_info:
        write_json_to_gcs(mock_storage_client, 12345, "test_bucket", "test_file.json")
    assert str(exc_info.value) == "Unsupported data type. Data must be a list, dict, or str."


def test_overwrite_if_exists(mock_storage_client, mock_blob):
    mock_blob.exists.return_value = True  # Simulate existing file
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name, test_file_name, overwrite_if_exists=True)

    assert result['gcs_file_overwritten'] is True


def test_overwrite_with_substring(mock_storage_client, mock_bucket):
    mock_bucket.list_blobs.return_value = [MagicMock(name='test_prefix_file1.json'), MagicMock(name='test_prefix_file2.json')]  
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"
    test_prefix = 'test_prefix'

    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name, 
                            test_file_name, overwrite_if_exists=True, 
                            file_exists_if_starts_with_prefix=test_prefix)
    assert result['gcs_file_overwritten'] is True
    assert result['gcs_file_exists_checked_on_name'] == test_prefix


def test_increment_if_exists(mock_storage_client, mock_blob):
    mock_blob.exists.side_effect = [True, True, False]  # Simulate existing files 
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"
    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name, test_file_name, increment_if_exists=True)
    assert result['gcs_path'] == f"gs://{test_bucket_name}/test_file_v2.json"
    assert result['gcs_file_saved_with_increment'] is True


def test_overwrite_and_increment_raise_value_error(mock_storage_client):
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"
    with pytest.raises(ValueError) as exc_info:
        write_json_to_gcs(mock_storage_client, test_data, test_bucket_name, 
                        test_file_name, overwrite_if_exists=True,
                        increment_if_exists=True)
    assert str(exc_info.value) == "Both 'overwrite_if_exists' and 'increment_if_exists' cannot be True simultaneously."


@patch('os.path.exists', return_value=False)  # Assume local file exists for simplicity
@patch('builtins.open', new_callable=MagicMock)
def test_local_save_after_gcs_failure(mock_open, mock_exists, mock_storage_client, mock_blob):
    mock_blob.upload_from_string.side_effect = Exception("GCS Upload Failed")
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    # Expecting an exception because GCS upload fails
    with pytest.raises(Exception) as exc_info:
        result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name, test_file_name, save_locally=True)

    assert "GCS Upload Failed" in str(exc_info.value)
    mock_open.assert_called_once_with(os.path.join("/tmp", test_file_name), 'w', encoding='utf-8')


@patch('builtins.open', new_callable=MagicMock)
def test_local_save_with_custom_path(mock_open, mock_storage_client):
    local_path = "/my/custom/path"
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name,
                                test_file_name, local_path=local_path)

    assert result['local_path'] == os.path.join(local_path, test_file_name)
    mock_open.assert_called_once()

@patch('os.path.exists', side_effect=[True, True, False])
@patch('builtins.open', new_callable=MagicMock)
def test_local_save_with_increment(mock_open, mock_exists, mock_storage_client, mock_blob):
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name,
                                test_file_name, save_locally=True, increment_if_exists=True)

    assert f"/tmp/test_file_v1.json" == result['local_path']
    mock_open.assert_called_once()


@patch('builtins.open', new_callable=MagicMock)
def test_local_save_overwrite(mock_open, mock_storage_client):
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    # Execute function
    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name,
                               test_file_name, save_locally=True, overwrite_if_exists=True)

    # Check results
    assert result['local_path'] == os.path.join("/tmp", test_file_name)
    mock_open.assert_called_once_with(os.path.join("/tmp", test_file_name), 'w', encoding='utf-8')
    file_handle = mock_open()


@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=MagicMock)
def test_local_save_skip(mock_open, mock_exists, mock_storage_client):
    test_data = {"key": "value"}
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    result = write_json_to_gcs(mock_storage_client, test_data, test_bucket_name,
                            test_file_name, save_locally=True, overwrite_if_exists=False)

    assert result['local_path'] == os.path.join("/tmp", test_file_name)
    mock_open.assert_not_called()


def test_string_data_handling(mock_storage_client, mock_blob):
    test_string_data = "This is a test string."
    test_bucket_name = "test_bucket"
    test_file_name = "test_file.json"

    result = write_json_to_gcs(mock_storage_client, test_string_data, test_bucket_name, test_file_name)

    assert result['gcs_path'] == f"gs://{test_bucket_name}/{test_file_name}" 