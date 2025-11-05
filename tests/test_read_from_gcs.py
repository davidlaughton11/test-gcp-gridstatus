# tests/test_read_from_gcs.py

# goal - to prove that read_from_gcs() returns the exact same DataFrame that was uploaded to GCS — without ever touching real GCS
import pytest
import pandas as pd
from io import BytesIO
from unittest.mock import MagicMock, patch

# import the function to test
from app.client_utils import read_from_gcs

# returns real local file path
@pytest.fixture
def real_parquet_path():
    return "data_local/pjm_LMP_data.parquet"

# returns bytes of real parquet file
@pytest.fixture
def real_parquet_bytes(real_parquet_path):
    with open(real_parquet_path, "rb") as f:
        return f.read()

# returns the actual DataFrame from the local file
@pytest.fixture
def expected_df(real_parquet_path):
    return pd.read_parquet(real_parquet_path)


def test_read_from_gcs_returns_exact_local_dataframe(real_parquet_bytes, expected_df):
    mock_blob = MagicMock()
    mock_blob.download_to_file = lambda buf: buf.write(real_parquet_bytes)

    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    mock_client = MagicMock()
    mock_client.bucket.return_value = mock_bucket

    with patch("app.client_utils.storage.Client", return_value=mock_client):
        with patch.dict("os.environ", {"GOOGLE_APPLICATION_CREDENTIALS": "gcp-sa-key.json"}):
            df = read_from_gcs(
                bucket_name="my-data-bucket-davidl",
                source_blob="results/pjm_LMP_data.parquet"
            )

    pd.testing.assert_frame_equal(
        df.reset_index(drop=True),
        expected_df.reset_index(drop=True),
        check_dtype=True,
        check_like=True
    )