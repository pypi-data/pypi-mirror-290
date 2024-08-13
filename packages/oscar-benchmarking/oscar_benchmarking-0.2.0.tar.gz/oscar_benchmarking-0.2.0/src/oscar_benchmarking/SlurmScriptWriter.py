import os
import logging
from typing import List
import re
import pandas as pd
import subprocess
from io import StringIO
from abc import ABC, abstractmethod
import yaml

class SlurmScriptWriter(ABC):
    """
    This abstract base class is a template for script-writing classes that writes the body of Slurm scripts.
    """

    @abstractmethod
    def generate_script_body(self) -> List[str]:
        """
        Generates the body of the script. Returns a List of lines as strings.
        """
        pass

class MLPerfScriptWriter(SlurmScriptWriter):
    """
    Writes the script body for MLPerf scripts.
    """

    def __init__(self, 
                 run_id: int, 
                 benchmark: str, 
                 model: str, 
                 backend: str, 
                 arch: str,
                 container_image: str, 
                 data_path: str,
                 **model_config) -> None:
        """
        Initialize relevants variables for writing an MLPerf script.

        Args:
            run_id (int): Unique ID of this benchmark run
            benchmark (str): Type of benchmark
            model (str): Name of model (e.g. resnet50, bert99, etc.)
            backend (str): Backend of the model (e.g. tf, torch)
            arch (str): GPU architecture (e.g. gh200, h100, etc.)
            container_image (str): Path to pre-configured Apptainer image
            data_path (str): Path to dataset
            model_config (dict): Configuration for the model. Keys are model args, values are their values. Model args may be different for different models.
        """
        # Get relevant environment variables
        self.PWD = os.environ.get('PWD')
        self.USER = os.environ.get('USER')

        self.RUN_ID = run_id

        # Validate + assign model parameters
        if not benchmark:
            raise ValueError("Invalid input for `benchmark`. Cannot be an empty string.")
        self.BENCHMARK = benchmark

        if not model:
            raise ValueError("Invalid input for `model`. Cannot be an empty string.")
        self.MODEL = model

        if not backend:
            raise ValueError("Invalid input for `backend`. Cannot be an empty string.")
        self.BACKEND = backend

        if not arch:
            raise ValueError("Invalid input for `arch`. Cannot be an empty string.")
        self.ARCH = arch

        # Initialize the directory for output files + directories
        self.RESULTS_DIR = os.path.join(self.PWD, "results")
        self.SLURM_OUTPUT_DIR = os.path.join(self.PWD, "slurm_out")
        self.SLURM_ERROR_DIR = os.path.join(self.PWD, "slurm_err")
        self.LOG_DIR = os.path.join(self.PWD, "submit_log")
        self.SCRIPT_DIR = os.path.join(self.PWD, "scripts")
        self.OUTFILE = os.path.join(self.PWD, "test_results/default-reference-gpu-tf-v2.15.0-default_config/resnet50/offline/performance/run_1/mlperf_log_detail.txt")
        
        # Validate + assign path inputs
        if not os.path.exists(container_image):
            raise ValueError(f"A valid container image must be specified. Given: {container_image}")
        self.CONTAINER_IMAGE = container_image

        if not os.path.exists(data_path) and self.MODEL == "resnet50":
            raise ValueError(f"A valid path to dataset must be specified. Given: {data_path}")
        self.DATA_PATH = data_path

        # Initialize other relevant paths
        self.SCRAPE_METRICS_PATH = os.path.join(self.PWD, "scrape_metrics.py")
        self.YAML_PATH = os.path.join(self.PWD, "config.yaml")

        # Read the YAML file
        try:
            with open(self.YAML_PATH, 'r') as file:
                yaml_params = yaml.safe_load(file) # Returns None, if file is empty
        except OSError as e:
            raise e
        
        # If the model config doesn't exist, use the yaml params
        if not model_config:
            model_config = yaml_params["model"][model]
        
        # Initialize MLPerf-Inference model-specific variables
        try:
            self.HW_NAME            = model_config["hw_name"]
            self.IMPLEMENTATION     = model_config["implementation"]
            self.DEVICE             = model_config["device"]
            self.SCENARIO           = model_config["scenario"]
            self.ADR_COMPILER_TAGS  = model_config["adr.compiler.tags"]
            self.TARGET_QPS         = model_config["target_qps"]
            self.CATEGORY           = model_config["category"]
            self.DIVISION           = model_config["division"]
        except KeyError as e:
            raise e

    def make_dirs(self) -> None:
        """
        This function creates the relevant directories for the script.
        """
        os.makedirs(self.RESULTS_DIR, exist_ok=True) # emulates 'mkdir -p' Linux command
        os.makedirs(self.SLURM_OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.SLURM_ERROR_DIR, exist_ok=True)
        os.makedirs(self.SCRIPT_DIR, exist_ok=True)
    
    def config_logger(self) -> logging.Logger:
        """
        This function configures the logger and creates its log file.

        Returns:
        The Logger object.
        """
        os.makedirs(self.LOG_DIR, exist_ok=True)
        LOG_PATH = os.path.join(self.LOG_DIR, "submit_benchmarks_log.txt")
        logging.basicConfig(filename=LOG_PATH,
                            level=logging.INFO,
                            format="%(asctime)s - %(levelname)s: %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
        logger = logging.getLogger(__name__)
        return logger            
    
    def generate_script_body(self) -> List[str]:
        """
        This function will create the body of the sbatch file.

        Raises LookupError, if the CM commands for the model are not found.
		"""
        # CM commands to run in apptainer
        CM_COMMANDS = {
            "resnet50":
                f'cm run script "get validation dataset imagenet _2012 _full" --input={self.DATA_PATH}\n',
            "bert-99":
                f'cm run script "get generic-sys-util _wget" --env.CM_SUDO=""\n',
        }
        try:
            get_dataset = CM_COMMANDS[self.MODEL]
        except KeyError:
            raise LookupError(f"CM commands for this MODEL ({self.MODEL}) not found!")
        
        # Make directories
        self.make_dirs()
        
        return [
            # 'echo "Hello World"\n',
            # Move Slurm output files into directories
            f"mv *.out {self.SLURM_OUTPUT_DIR}\n",
            f"mv *.err {self.SLURM_ERROR_DIR}\n",
            'unset LD_LIBRARY_PATH\n',
            f'export APPTAINER_BINDPATH="/oscar/home/{self.USER}, /oscar/scratch/{self.USER}, /oscar/data"\n',
            'export APPTAINER_CACHEDIR=/tmp\n',
            '\n',
            'echo $SLURM_JOBID\n',
            '\n',
            f"srun apptainer exec --nv {self.CONTAINER_IMAGE} sh << 'EOF'\n" ,
            'export CM_REPOS=/tmp/CM\n',
            'cp -r /CM /tmp/.\n',
            '\n',
            get_dataset,
            f'cmr "run mlperf inference generate-run-cmds _submission" --quiet --submitter="MLCommons" --hw_name={self.HW_NAME} --model={self.MODEL} --implementation={self.IMPLEMENTATION} --backend={self.BACKEND} --device={self.DEVICE} --scenario={self.SCENARIO} --adr.compiler.tags={self.ADR_COMPILER_TAGS} --target_qps={self.TARGET_QPS} --category={self.CATEGORY} --division={self.DIVISION} --results_dir={self.RESULTS_DIR}\n',
            'EOF\n',
            '\n',
        ] # + self.scrape_metrics()
    
    def scrape_metrics(self) -> List[str]:
        """
        This function creates the command to run the scrape_metrics script.

        Raises ValueError if scrape_metrics path is not provided.
        Raise FileNotFoundError if the script does not exist.

        Returns:
        The command to run the scrape_metrics script.
        """
        if not self.SCRAPE_METRICS_PATH:
            raise ValueError("No scrape_metrics path provided!")
        if not os.path.exists(self.SCRAPE_METRICS_PATH):
            raise FileNotFoundError(f"{self.SCRAPE_METRICS_PATH} does not exist!")
        
        return [
            # Save results to sqlite3 database
            f'python {self.SCRAPE_METRICS_PATH} {self.OUTFILE} --runid={self.RUN_ID} --benchmark={self.BENCHMARK} --model={self.MODEL} --backend={self.BACKEND} --arch={self.ARCH}\n'
        ]
        
    def slurm_input(self) -> List[int]:
        """
        Read input from slurm commands like sfeature and
        get the actual list of gpus to submit to.

        Returns:
        The list of GPU IDs.
        """
        # Create text file of the sfeature output
        try:
            result = subprocess.run(args=["sinfo", "-o", r"%N %P %c %m %f %G"], 
                                    shell=False, 
                                    capture_output=True, 
                                    text=True, 
                                    check=True) # check=True throws subprocess.CalledProcessError, if exits with code > 0
        except subprocess.CalledProcessError as e:
            print(e)

        # Read the output from sinfo into a pandas DataFrame
        df = pd.read_table(StringIO(result.stdout), delimiter=' ')

        # Extract the gpus
        gpus_df = df.loc[df["PARTITION"] == "gpu"]
        gpus_df.reset_index(drop=True, inplace=True)

        # Get the nodelist column
        nodelists = gpus_df["NODELIST"]
        node_list = []

        # Get a list of all the nodes
        pattern = re.compile(r'\[([^\[\]]+)\]') # Regex for strings enclosed in square brackets
        for nodelist in nodelists:
            stripped_node = nodelist.strip("gpu")
            match = pattern.search(stripped_node)
            if match:
                enclosed_string = match.group(1)
                items = enclosed_string.split(',')

                for item in items:
                    if '-' in item:
                        start, end = map(int, item.split('-'))
                        node_list.extend(range(start, end + 1))
                    else:
                        node_list.append(int(item))
            else:
                node_list.append(int(stripped_node))
        
        return node_list
