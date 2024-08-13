"""
This script generates a Slurm script for MLPerf inference benchmarking for bert-99.
"""

import argparse
from util import from_yaml_csv_config

parser = argparse.ArgumentParser(prog="submit_bert-99", description="Generates a Slurm script for MLPerf inference benchmarking for bert-99.")

parser.add_argument('-y', '--yaml_path', help='Path to config.yaml', default="config.yaml")
parser.add_argument('-c', '--csv_path', help="Path to run_config.csv", default="run_config.csv")

args = parser.parse_args()

def submit_bert99(yaml_path: str, csv_path: str) -> None:
    script_objects = from_yaml_csv_config(yaml_path, csv_path)

    for run_id, (script_writer, script_submitter) in script_objects.items():
        logger = script_submitter.logger
        logger.info(f"Run {run_id}:")
        logger.info(f"Benchmark: {script_writer.BENCHMARK}")
        logger.info(f"Model: {script_writer.MODEL}")
        logger.info(f"Backend: {script_writer.BACKEND}")
        logger.info(f"Architecture: {script_writer.ARCH}")

        script_submitter.write()
        script_submitter.submit()
        logger.info(f"Run {run_id} submitted successfully.\n")

if __name__ == "__main__":
    submit_bert99(args.yaml_path, args.csv_path)

# # Read the YAML file
# try:
#     with open("config.yaml", 'r') as file:
#         general_params = yaml.safe_load(file) # Returns None, if file is empty
# except OSError as e:
#     raise e

# # Parse the CSV
# run_config_df = pd.read_csv("run_config.csv")

# for _, run in run_config_df.iterrows():
#     # Get model args
#     run_id = run["RUN_ID"]
#     benchmark = run["BENCHMARK"]
#     model = run["MODEL"]
#     backend = run["BACKEND"]
#     arch = run["ARCH"]

#     num_runs = general_params["num_runs"]

#     # Set the script path
#     PWD = os.environ.get('PWD')
#     script_path = os.path.join(os.path.join(PWD, 'scripts'), f'{run_id}_{benchmark}_{model}_{datetime.now().strftime("%Y%m%d")}.submit')

#     # Declare the writer
#     script_writer = MLPerfScriptWriter(run_id, benchmark, model, backend, arch, **general_params["model"][model])

#     # Configure the logger
#     logger = script_writer.config_logger()

#     # Log batch variables
#     logger.info("Batch variables:")
#     for arg, val in general_params["arch"][arch].items():
#         logger.info(f"{arg}: {val}")

#     # Declare the submitter with writer
#     job_submitter = MLPerfJobSubmitter(script_writer, script_path, **general_params["arch"][arch], num_runs=num_runs)

#     job_submitter.write()
#     job_submitter.submit()

#     # Log successful submission
#     logger.info("Batch script submitted successfully.\n")