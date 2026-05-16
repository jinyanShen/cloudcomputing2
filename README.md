# cloudcomputing2
This project analyzes a cloud service log dataset using two different distributed computing frameworks: **MapReduce (via mrjob)** and **Ray**.
## Requirements
Ensure you have Python 3.x installed along with the following libraries:

pip install mrjob ray requests

## Project Structure

mr_request_count.py : MapReduce job for Output 1 (Request count by service).

mr_error_count.py : MapReduce job for Output 2 (Server error count).

mr_slow_endpoints.py : MapReduce job for Output 3 (Top 10 slow endpoints).

run_all_with_timing.py : Master script to run all MR jobs locally (-r inline), record execution time, and save logs.

ray_degradation.py : Ray task to calculate service degradation based on slow requests, errors, and timeouts. Downloads data directly from Alibaba Cloud OSS.

mr_outputs/ : Directory containing all MapReduce output files and the runtime_log.txt.

ray_output.txt : The output file of the Ray job.

## How to Run the Code

1. Run MapReduce Tasks

We have provided an automated script to run all three MapReduce tasks sequentially.
Please ensure the dataset file Comp3041J MiniProject 2 Dataset.csv is placed in the same directory as the scripts.
Execute the following command in your terminal:
bash

python run_all_with_timing.py

Output: The results will be saved in the mr_outputs/ folder, including a runtime_log.txt detailing system environment and execution time.

2. Run the Ray Task

The Ray script downloads the dataset directly from our cloud storage (OSS). No local dataset file is required to run this script.
Execute the following command:
bash
python ray_degradation.py

Output: The script will print the results to the console and save them locally as ray_output.txt.

## Cloud Storage Strategy

For this project, the large dataset was uploaded to Alibaba Cloud OSS (Object Storage Service). The Ray script utilizes requests to fetch data chunks dynamically via a public URL, simulating a real-world cloud data processing pipeline without relying on local machine storage limitations.