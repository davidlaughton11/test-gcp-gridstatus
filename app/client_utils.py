import os
import pandas as pd
from io import BytesIO
from google.cloud import storage
from gridstatusio import GridStatusClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

GRIDSTATUS_API_KEY = os.getenv("GRIDSTATUS_API_KEY")

def fetch_pjm_data(start, end, query_limit=100):
    """Fetch PJM day-ahead LMP data for selected nodes."""
    client = GridStatusClient(api_key=GRIDSTATUS_API_KEY)

    data = client.get_dataset(
        dataset="pjm_lmp_day_ahead_hourly",
        start=start,
        end=end,
        filter_column="location",
        filter_operator="in",
        filter_value=[
            "DOMINION HUB", "WESTERN HUB", "EASTERN HUB",
            "02HAMILT138 KV  LD1", "02HAMLTN138 KV  TR1",
            "02HAMLTN138 KV  TR2", "02HAMLTN138 KV  TR3",
            "02HAMLTN138 KV  TR4", "02HUMMEL36 KV   LDFDR",
            "02INCA  138 KV  TR71", "02IRON  138 KV  TR71",
            "02IRON  138 KV  TR72", "02JMP   138 KV  TR1",
            "02JMP2  138 KV  TR10", "02JMP2  138 KV  TR11",
            "02JOHNCT138 KV  LDJC", "02JOHNCT138 KV  LDJC2",
            "02JOHNCT138 KV  TR1", "02JP    138 KV  TR1",
            "02JP    138 KV  TR2", "02JP    138 KV  TR3",
            "02KYHS  138 KV  TR1", "02KYHS  138 KV  TR2",
        ],
        timezone="market",
        limit=query_limit,
    )

    return data


def upload_to_gcs(df, bucket_name, dest_blob):
    """Upload a DataFrame to GCS as a Parquet file (in-memory)."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-sa-key.json"
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(dest_blob)

    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    blob.upload_from_file(buffer, content_type="application/octet-stream")
    print(f"Uploaded DataFrame to gs://{bucket_name}/{dest_blob}")
