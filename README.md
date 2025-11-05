PJM lmp data pipline from the grid status API, run through docker

Explainer on main code:
1. it fetches day ahead LMPs from gridstatus for PJM hubs
2. saves the data as a parquet file
3. uploads it to google cloud storage (GCS)
4. can download the parquet file from GCS as well

Testing:
built a pytest dependancy to check the read_from_gcs function locally

Learned:
containerization (with docker and control paths), api integration, cloud storage and GCS set up, CLI tooling, testings with pytest
