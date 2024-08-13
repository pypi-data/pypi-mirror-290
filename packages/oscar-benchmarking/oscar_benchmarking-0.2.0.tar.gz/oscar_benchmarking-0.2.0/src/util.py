"""
This module contains utility functions for writing Python scripts for submitting MLPerf jobs to Slurm using the oscar_benchmarking package.
"""

from datetime import datetime
import os
from typing import Dict, Tuple

import pandas as pd
import yaml
from oscar_benchmarking.SlurmJobSubmitter import SlurmJobSubmitter, MLPerfJobSubmitter
from oscar_benchmarking.SlurmScriptWriter import SlurmScriptWriter, MLPerfScriptWriter

def from_yaml_csv_config(yaml_path: str, csv_path: str) -> Dict[int, Tuple[SlurmScriptWriter, SlurmJobSubmitter]]:
    """
    From given YAML and CSV configuration files, return a dictionary of run IDs and their corresponding SlurmScriptWriter and SlurmJobSubmitter.

    Args:
        yaml_path (str): Path to the YAML file.
        csv_path (str): Path to the CSV file.
    
    Returns:
    A dictionary of run IDs and their corresponding SlurmScriptWriter and SlurmJobSubmitter.
    """
    # Read the YAML file
    try:
        with open(yaml_path, 'r') as file:
            general_params = yaml.safe_load(file) # Returns None, if file is empty
    except OSError as e:
        raise e
    
    # Parse the CSV
    run_config_df = pd.read_csv(csv_path)

    script_objects = {}

    # Loop through each run configuration in the CSV
    for _, run in run_config_df.iterrows():
        # Get model args
        run_id = run["RUN_ID"]
        benchmark = run["BENCHMARK"]
        model = run["MODEL"]
        backend = run["BACKEND"]
        arch = run["ARCH"]

        num_runs = general_params["num_runs"]

        # Set the script path
        pwd = os.environ.get('PWD')
        script_path = os.path.join(os.path.join(pwd, 'scripts'), f'{run_id}_{benchmark}_{model}_{datetime.now().strftime("%Y%m%d-%H:%M:%S")}.submit')

        # Declare the writer
        script_writer = MLPerfScriptWriter(run_id, benchmark, model, backend, arch, **general_params["model"][model])

        # Declare the submitter with writer
        job_submitter = MLPerfJobSubmitter(script_writer, script_path, **general_params["arch"][arch], num_runs=num_runs)

        # Get logger 
        logger = job_submitter.logger

        # Log batch variables
        logger.info("Batch variables:")
        for arg, val in general_params["arch"][arch].items():
            logger.info(f"{arg}: {val}")
        logger.info("\n")

        script_objects[run_id] = (script_writer, job_submitter)

    return script_objects
    
def from_yaml_config(yaml_path: str, run_id: int, benchmark: str, model: str, backend: str, arch: str) -> Tuple[SlurmScriptWriter, SlurmJobSubmitter]:
    """
    From given YAML configuration file, return a SlurmScriptWriter and SlurmJobSubmitter for the given run.

    Args:
        yaml_path (str): Path to the YAML file.
        run_id (int): Unique ID of this benchmark run
        benchmark (str): Type of benchmark
        model (str): Name of model
        backend (str): Backend of the model
        arch (str): GPU architecture

    Returns:
    The SlurmScriptWriter and SlurmJobSubmitter for the given run.
    """
    # Read the YAML file
    try:
        with open(yaml_path, 'r') as file:
            general_params = yaml.safe_load(file) # Returns None, if file is empty
    except OSError as e:
        raise e

    # Get model args
    num_runs = general_params["num_runs"]

    # Set the script path
    pwd = os.environ.get('PWD')
    script_path = os.path.join(os.path.join(pwd, 'scripts'), f'{run_id}_{benchmark}_{model}_{datetime.now().strftime("%Y%m%d-%H:%M:%S")}.submit')

    # Declare the writer
    script_writer = MLPerfScriptWriter(run_id, benchmark, model, backend, arch, **general_params["model"][model])

    # Declare the submitter with writer
    job_submitter = MLPerfJobSubmitter(script_writer, script_path, **general_params["arch"][arch], num_runs=num_runs)

    # Get logger 
    logger = job_submitter.logger

    # Log batch variables
    logger.info("Batch variables:")
    for arg, val in general_params["arch"][arch].items():
        logger.info(f"{arg}: {val}")
    logger.info("\n")

    return script_writer, job_submitter
