# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer
from zetta._utils.connections import check_api_status

from zetta.job import worker_get_job, worker_run_job, process_zetta_job_config, init_zetta_job_config

job_cli = typer.Typer(
    name="job", help="Build your models in Zetta Workspace.", no_args_is_help=True
)


@job_cli.command(name="list", help="List all build jobs that are currently running.")
@synchronizer.create_blocking
async def list(json: bool = False):
    pass


@job_cli.command(name="get", help="get a job status.")
@synchronizer.create_blocking
async def get(jobid, json: bool = False):
    job = worker_get_job(jobid, json_output=json)
    if job is not None:
        print(job)
    else:
        print(f"Job {jobid} not found.")
    pass


@job_cli.command(name="update", help="update a job.")
@synchronizer.create_blocking
async def update(json: bool = False):
    pass


@job_cli.command(name="cancel", help="cancel a running job for current user.")
@synchronizer.create_blocking
async def cancel(json: bool = False):
    pass


@job_cli.command(name="status", help="check the status of Zetta ai-network API.")
@synchronizer.create_blocking
async def status(env: str = typer.Option("testnet", help="Environment to use: 'testnet' or 'mainnet'")):
    result = check_api_status(env)
    print(result['status'])
    return result


@job_cli.command(
    name="init", help="Initialize a new fine-tune job at designated location."
)
@synchronizer.create_blocking
async def init(
    project_name: str, framework: str = "llama-factory", location: str = "."
):
    """
    Initialize a new fine-tune project with name `project_name`. A config template will be downloaded at designated file location.
    `project_name` is the default name of the fine-tune model.
    """
    if framework == "llama-factory":
        config_path = init_zetta_job_config(project_name, location)
        print(f"Created config file at {config_path}. Fill in and get started!")
    else:
        print(f"Framework {framework} is not supported.")
    pass


@job_cli.command(
    name="run", help="Create a new fine-tune job with given configuration."
)
@synchronizer.create_blocking
async def run(config: str, gpu: str = None, multi_gpu: bool = False):
    """
    Submit a new fine-tune job with given config file and optional hardware requirements.
    `config` can be a local file path or a URL to a public GitHub repository with `config.yaml` file in the root.
    Return a job id.
    """
    lf_config = process_zetta_job_config(config)
    try:
        resp = worker_run_job(lf_config)
        print(f"Job submitted: {resp}")
        return resp
    except Exception as e:
        print(f"Failed to submit job: {e}")
        return None


@job_cli.command(name="logs", help="Show the logs of a job with given job id.")
@synchronizer.create_blocking
async def logs(job_id: str):
    pass
