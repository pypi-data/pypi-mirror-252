import datetime
import json
import pathlib

import pytest

import mantik.compute_backend.config as config
import mantik_compute_backend.unicore._properties as _properties

FILE_DIR = pathlib.Path(__file__).parent


@pytest.fixture(scope="function")
def example_config() -> config.core.Config:
    return config.core.Config(
        unicore_api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            ),
            variables={"SRUN_CPUS_PER_TASK": 100},
        ),
        resources=config.resources.Resources(queue="batch"),
        exclude=["*.py", "*.sif"],
    )


@pytest.fixture()
def example_job_property_response() -> dict:
    with open(
        FILE_DIR
        / "../../../resources/unicore-responses/job-property-response.json",
    ) as f:
        return json.load(f)


@pytest.fixture()
def example_job_properties():
    return _properties.Properties(
        status=_properties.Status.SUCCESSFUL,
        logs=[],
        owner="owner",
        site_name="siteName",
        consumed_time=_properties.ConsumedTime(
            total=datetime.timedelta(seconds=1),
            queued=datetime.timedelta(seconds=2),
            stage_in=datetime.timedelta(seconds=3),
            pre_command=datetime.timedelta(seconds=4),
            main=datetime.timedelta(seconds=5),
            post_command=datetime.timedelta(seconds=6),
            stage_out=datetime.timedelta(seconds=7),
        ),
        current_time=datetime.datetime(
            2000, 1, 1, tzinfo=_properties.TZ_OFFSET
        ),
        submission_time=datetime.datetime(
            2000, 1, 1, tzinfo=_properties.TZ_OFFSET
        ),
        termination_time=datetime.datetime(
            2000, 1, 2, tzinfo=_properties.TZ_OFFSET
        ),
        status_message="statusMessage",
        tags=["tag"],
        resource_status="resourceStatus",
        name="name",
        exit_code="0",
        queue="queue",
        submission_preferences={"any": "preferences"},
        resource_status_message="resourceStatusMessage",
        acl=["acl"],
        batch_system_id="batchSystemID",
    )


@pytest.fixture()
def example_config_for_python() -> config.core.Config:
    return config.core.Config(
        unicore_api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Python(
                path=pathlib.Path("/venv"),
            ),
            pre_run_command_on_compute_node="precommand compute node",
            post_run_command_on_compute_node="postcommand compute node",
        ),
        resources=config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )
