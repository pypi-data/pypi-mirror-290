"""
TEST:
- Successfully makes directories
- Successfully configures logger
- Generates the correct script body given the correct parameters
- TODO: Test scrape_metrics.py
- TODO: Test `slurm_input()`
"""

import pytest
from oscar_benchmarking.SlurmScriptWriter import MLPerfScriptWriter
import os

@pytest.fixture
def pwd():
    """
    Fixture for getting the current working directory.
    """
    return os.environ.get("PWD")

@pytest.fixture
def resnet_script_writer(pwd):
    """
    Fixture for creating an instance of MLPerfScriptWriter.
    """
    return MLPerfScriptWriter(
        run_id=1,
        benchmark="MLPerf-Inference",
        model="resnet50",
        backend="tf",
        arch="arm64-gracehopper",
        container_image="oscar/data/shared/eval_gracehopper/container_images/MLPerf/arm64/mlperf-resnet-50-tf-arm64",
        data_path="/oscar/data/ccvinter/mstu/gracehopper_eval/data/imagenet/ILSVRC2012/val",
        destination=pwd
    )

@pytest.fixture
def bert_script_writer(pwd):
    """
    Fixture for creating an instance of MLPerfScriptWriter.
    """
    return MLPerfScriptWriter(
        run_id=1,
        benchmark="MLPerf-Inference",
        model="bert-99",
        backend="pytorch",
        arch="arm64-gracehopper",
        container_image="oscar/data/shared/eval_gracehopper/container_images/MLPerf/arm64/mlperf-resnet-50-tf-arm64",
        data_path=None,
        destination=pwd
    )

def test_make_dirs(resnet_script_writer):
    """
    Test that `make_dirs()` creates the correct directories.
    """
    resnet_script_writer.make_dirs()
    assert(os.path.isdir(resnet_script_writer.RESULTS_DIR))
    assert(os.path.isdir(resnet_script_writer.SLURM_OUTPUT_DIR))
    assert(os.path.isdir(resnet_script_writer.SLURM_ERROR_DIR))
    assert(os.path.isdir(resnet_script_writer.LOG_DIR))
    assert(os.path.isdir(resnet_script_writer.SCRIPT_DIR))

def test_config_logger(resnet_script_writer):
    """
    Test that `config_logger()` configures the logger correctly.
    """
    logger = resnet_script_writer.config_logger()
    assert(logger)

def test_generate_script_body(resnet_script_writer):
    """
    Test that `generate_script_body()` generates the correct script body.
    """
    target = [
        'unset LD_LIBRARY_PATH\n',
        f'export APPTAINER_BINDPATH="/oscar/home/{resnet_script_writer.USER}, /oscar/scratch/{resnet_script_writer.USER}, /oscar/data"\n',
        'export APPTAINER_CACHEDIR=/tmp\n',
        '\n',
        'echo $SLURM_JOBID\n',
        '\n',
        f"srun apptainer exec --nv {resnet_script_writer.CONTAINER_IMAGE} sh << 'EOF'\n" ,
        'export CM_REPOS=/tmp/CM\n',
        'cp -r /CM /tmp/.\n',
        '\n',
        f'cm run script "get validation dataset imagenet _2012 _full" --input={resnet_script_writer.DATA_PATH}\n',
        f'cmr "run mlperf inference generate-run-cmds _submission" --quiet --submitter="MLCommons" --hw_name={resnet_script_writer.HW_NAME} --model={resnet_script_writer.MODEL} --implementation={resnet_script_writer.IMPLEMENTATION} --backend={resnet_script_writer.BACKEND} --device={resnet_script_writer.DEVICE} --scenario={resnet_script_writer.SCENARIO} --adr.compiler.tags={resnet_script_writer.ADR_COMPILER_TAGS} --target_qps={resnet_script_writer.TARGET_QPS} --category={resnet_script_writer.CATEGORY} --division={resnet_script_writer.DIVISION} --results_dir={resnet_script_writer.RESULTS_DIR}\n',
        'EOF\n',
        '\n',
        f"mv *.out {resnet_script_writer.SLURM_OUTPUT_DIR}\n",
        f"mv *.err {resnet_script_writer.SLURM_ERROR_DIR}\n",
        ]
    script_body = resnet_script_writer.generate_script_body()
    assert(target == script_body)

def test_cm_commands(bert_script_writer):
    """
    Test that CM commands are generated correctly.
    """
    target = f'cm run script "get generic-sys-util _wget" --env.CM_SUDO=""\n'
    script_body = bert_script_writer.generate_script_body()
    assert(target in script_body)