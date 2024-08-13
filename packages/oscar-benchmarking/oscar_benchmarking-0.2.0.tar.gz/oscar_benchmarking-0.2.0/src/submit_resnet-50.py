"""
This script creates a batch script that submits jobs to Slurm to run the MLPerf inference benchmarks.
"""

import argparse
from util import from_yaml_csv_config

parser = argparse.ArgumentParser(prog="submit_resnet-99", description="Generates a Slurm script for MLPerf inference benchmarking for resnet-50.")

parser.add_argument('-y', '--yaml_path', help='Path to config.yaml', default="config.yaml")
parser.add_argument('-c', '--csv_path', help="Path to run_config.csv", default="run_config.csv")

args = parser.parse_args()

def submit_resnet50(yaml_path: str, csv_path: str) -> None:
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
    submit_resnet50(args.yaml_path, args.csv_path)

# # Read the YAML file
# try:
#     with open("config.yaml", 'r') as file:
#         general_params = yaml.safe_load(file) # Returns None, if file is empty
# except OSError as e:
#     raise e

# # Parse the CSV
# run_config_df = pd.read_csv("run_config.csv")

# # Get the working directory + user from ENV
# PWD = os.environ.get('PWD')
# USER = os.environ.get('USER')

# # Loop through each run configuration in the CSV
# for _, run in run_config_df.iterrows():
#     # Parameters for the current run
#     RUN_ID = run["RUN_ID"]
#     BENCHMARK = run["BENCHMARK"]
#     MODEL = run["MODEL"]
#     BACKEND = run["BACKEND"]
#     ARCH = run["ARCH"]

#     # Get model args
#     NUM_RUNS =          general_params["num_runs"]
#     DATA_PATH =         general_params["model"][MODEL]["data_path"]
#     CONTAINER_IMAGE =   general_params["model"][MODEL]["container_image"]

#     # Define the output script path
#     BATCH_PATH = os.path.join(os.path.join(PWD, "scripts"), f'{RUN_ID}_{BENCHMARK}_{MODEL}_{datetime.now().strftime("%Y%m%d")}.submit')

#     slurm_script_writer = MLPerfScriptWriter(RUN_ID, BENCHMARK, MODEL, BACKEND, ARCH, container_image=CONTAINER_IMAGE, data_path=DATA_PATH, destination=PWD)

#     # Batch Variables
#     NODES =             general_params["arch"][ARCH]["nodes"]
#     PARTITION =         general_params["arch"][ARCH]["partition"]
#     GRES =              general_params["arch"][ARCH]["gres"]
#     ACCOUNT =           general_params["arch"][ARCH]["account"]
#     NTASKS_PER_NODE =   general_params["arch"][ARCH]["ntasks_per_node"]
#     MEMORY =            general_params["arch"][ARCH]["memory"]
#     TIME =              general_params["arch"][ARCH]["time"]
#     ERROR_FILE_NAME =   general_params["arch"][ARCH]["error_file_name"]
#     OUTPUT_FILE_NAME =  general_params["arch"][ARCH]["output_file_name"]

#     # Configure the logger
#     logger = slurm_script_writer.config_logger()

#     # Log important info
#     logger.info("Command-line arguments:")
#     for arg, val in general_params["arch"][ARCH].items():
#         logger.info(f"{arg}: {val}")

#     slurm_job_submitter = MLPerfJobSubmitter(slurm_script_writer,
#                                         script_path=BATCH_PATH,
#                                         nodes=NODES, 
#                                         gres=GRES, 
#                                         ntasks_per_node=NTASKS_PER_NODE, 
#                                         memory=MEMORY, 
#                                         time=TIME, 
#                                         partition=PARTITION, 
#                                         error_file_name=ERROR_FILE_NAME, 
#                                         output_file_name=OUTPUT_FILE_NAME, 
#                                         account=ACCOUNT,
#                                         num_runs=NUM_RUNS)
    
#     slurm_job_submitter.write()
#     slurm_job_submitter.submit()

#     # Log successful submission
#     logger.info("Batch script submitted successfully.\n")