import argparse
import pandas as pd
from app.client_utils import fetch_pjm_data, upload_to_gcs


def main():
    parser = argparse.ArgumentParser(description="Fetch PJM LMP data and optionally upload to GCS.")
    parser.add_argument("--start", default="2025-10-10", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default="2025-10-28", help="End date (YYYY-MM-DD)")
    parser.add_argument("--output", default="results.parquet", help="Local output Parquet file name")
    parser.add_argument("--upload", action="store_true", help="Upload to GCS if provided")
    parser.add_argument("--bucket", default="my-data-bucket-davidl", help="GCS bucket name")
    parser.add_argument("--dest", default="results/pjm_LMP_data.parquet", help="Destination path in GCS")

    args = parser.parse_args()

    # Fetch data
    df = fetch_pjm_data(args.start, args.end)
    df.to_parquet(args.output, index=False)
    print(f"Data saved locally to {args.output}")

    # Optional upload
    if args.upload:
        upload_to_gcs(df, args.bucket, args.dest)
    else:
        print("Skipping GCS upload (use --upload to enable)")


if __name__ == "__main__":
    main()
