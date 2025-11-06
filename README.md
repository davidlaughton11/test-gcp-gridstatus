PJM lmp data pipline from the grid status API, able to be run through dockerfile CLI

Explainer on main app code:
Ability, through argparse to
1. pull data from the gridstatus API for 20 PJM hubs
2. upload the data to GCS bucket as a parquet file
3. read files from GCS given a bucket and file name

Testing:
built a pytest dependancy to check the read_from_gcs function locally without making any real GCS calls.

Learned through back and forth iteration:
containerization (with docker and control paths), api calls, cloud storage and GCS set up, CLI tooling, and testings with pytest

## Folder Structure
```text
.
├── src/
│   └── app/
│       ├── main.py             ← CLI entrypoint (argparse)
│       └── client_utils.py     ← fetch, upload, read from GCS
│
├── data_local/                 ← output Parquet files
│
├── tests/                      ← local pytests (not in Docker)
│
├── pyproject.toml              ← Poetry dependencies (pandas, gridstatusio, etc.)
├── .env                        ← GRIDSTATUS_API_KEY
├── gcp-sa-key.json             ← GCP service account key
├── Dockerfile                  ← builds production image
└── README.md
