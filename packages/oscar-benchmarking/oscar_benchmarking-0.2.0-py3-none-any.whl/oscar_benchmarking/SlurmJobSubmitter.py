import subprocess
from abc import ABC, abstractmethod
from oscar_benchmarking.SlurmScriptWriter import SlurmScriptWriter

class SlurmJobSubmitter(ABC):
    """
    This class is an abstract base class for submitting jobs to the Slurm scheduler. 
    Example use cases: MLPerf jobs, generic gpu jobs, generic cpu jobs, array jobs, etc.

    NOTE: This class only submits jobs from ONE script. If you need to write another script, declare another submitter object.
    """
    def __init__(self,
                    script_writer: SlurmScriptWriter,
                    script_path: str, 
                    nodes: int, 
                    gres: str, 
                    ntasks_per_node: int, 
                    memory: str, 
                    time: str, 
                    partition: str, 
                    error_file_name: str,
                    output_file_name: str) -> None:
        """
        Initialize variables necessary to write a SBATCH header.

        Args:
            script_writer (SlurmScriptWriter): The script writer to use.
            script_path (str): File path to write to.
            nodes (int): The number of nodes to use.
            gres (str): Generic resources required for the job.
            ntasks_per_node (int): Number of tasks to run per node.
            memory (str): Amount of memory required.
            time (str): Maximum time the job can run.
            partition (str): The partition to submit the job to.
            error_file_name (str): Name of the file to which standard error will be written.
            output_file_name (str): Name of the file to which standard output will be written.
        """
        self.script_writer = script_writer
        self.script_path = script_path
        self.nodes = nodes
        self.gres = gres
        self.ntasks_per_node = ntasks_per_node
        self.memory = memory
        self.time = time
        self.partition = partition
        self.error_file_name = error_file_name
        self.output_file_name = output_file_name
    
    @abstractmethod
    def write(self) -> None:
        """
        Writes the given SBATCH header and script body to a file.
        """
        pass

    @abstractmethod
    def submit(self) -> None:
        """
        Submits the script to Slurm.
        """
        pass

class MLPerfJobSubmitter(SlurmJobSubmitter):
    """
    This class submits MLPerf jobs to the Slurm scheduler.

    NOTE: This class only submits jobs from ONE script. If you need to write another script, declare another submitter object.
    """
    def __init__(self,
                    script_writer: SlurmScriptWriter,
                    script_path: str, 
                    nodes: int, 
                    gres: str, 
                    ntasks_per_node: int, 
                    memory: str, 
                    time: str, 
                    partition: str, 
                    error_file_name: str = "%j.err",
                    output_file_name: str = "%j.out", 
                    account: str = None,
                    num_runs: int = 1) -> None:
        """
        Initialize variables necessary to write a SBATCH header for a MLPerf script.

        Raises ValueError, if num_runs is less than 1.

        Args:
            script_writer (SlurmScriptWriter): The script writer to use.
            script_path (str): File path to write to.
            nodes (int): The number of nodes to use.
            gres (str): Generic resources required for the job.
            ntasks_per_node (int): Number of tasks to run per node.
            memory (str): Amount of memory required.
            time (str): Maximum time the job can run.
            partition (str): The partition to submit the job to.
            error_file_name (str, optional): Name of the file to which standard error will be written. Defaults to "%j.err".
            output_file_name (str, optional): Name of the file to which standard output will be written. Defaults to "%j.out".
            account (str, optional): Account to be charged for the job. Defaults to None.
            num_runs (int, optional): Number of times to run the MLPerf script. Defaults to 1.
        """
        # Initialize the super class variables
        super().__init__(script_writer, script_path, nodes, gres, ntasks_per_node, memory, time, partition, error_file_name, output_file_name)
        
        # Initialize the subclass variables
        self.account = account

        # Check the number of runs
        if num_runs < 1:
            raise ValueError("Number of runs must be at least 1.")
        self.num_runs = num_runs

        # Configure logger
        self.logger = self.script_writer.config_logger()

        self.params = [
            nodes,
            partition,
            gres,
            account,
            ntasks_per_node,
            memory,
            time,
            error_file_name,
            output_file_name
        ]

        self.gpu_lines = [
            f'#SBATCH --nodes={nodes}\n',
            f'#SBATCH -p {partition}\n',
            f'#SBATCH --gres={gres}\n',
            f'#SBATCH --account={account}\n',
            f'#SBATCH --ntasks-per-node={ntasks_per_node}\n',
            f'#SBATCH --mem={memory}\n',
            f'#SBATCH -t {time}\n',
            f'#SBATCH -e {error_file_name}\n',
            f'#SBATCH -o {output_file_name}\n',
        ]
    
    def write(self) -> None:
        """
        Writes to a batch script to file, given a file path and script content.

        Raises OSError, if opening the file fails.
        """
        sbatch_header = ['#!/bin/bash\n', '\n',]

        # If the parameter is valid, then append the respective line to the sbatch header
        for param, line in zip(self.params, self.gpu_lines):
            if param:
                sbatch_header.append(line)
        
        # If array job, add the array job line.
        if self.num_runs > 1:
            sbatch_header.append(f"#SBATCH --array 1-{self.num_runs}")

        # Generate the script body using the script writer
        script_body = self.script_writer.generate_script_body()

        # Write the batch script to file
        try:
            with open(self.script_path, 'w') as f:
                f.writelines(
                    sbatch_header 
                    + ['\n'] 
                    + script_body)
        except OSError as e:
            raise e
    
    def submit(self) -> None:
        """
        Submits the SBATCH script file to gpu node(s).
        """
        # print("Submitted job 123456.")
        try:
            sbatch_result = subprocess.run(["sbatch", self.script_path], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            raise e
        print(sbatch_result.stdout)
