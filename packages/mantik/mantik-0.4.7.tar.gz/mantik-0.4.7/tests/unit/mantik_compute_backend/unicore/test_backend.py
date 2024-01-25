import functools
import json
import pathlib

import mlflow.projects as projects
import pytest
import pyunicore.client
from mlflow.projects import _project_spec

import mantik.compute_backend.config.core as core
import mantik.compute_backend.config.exceptions as exceptions
import mantik.compute_backend.credentials as _credentials
import mantik.testing as testing
import mantik.utils as mantik_utils
import mantik_compute_backend.unicore._client as _client
import mantik_compute_backend.unicore.backend as backend
import mantik_compute_backend.utils as utils

FILE_PATH = pathlib.Path(__file__).parent

ALL_ENV_VARS = [
    _credentials.UNICORE_USERNAME_ENV_VAR,
    _credentials.UNICORE_PASSWORD_ENV_VAR,
    core._PROJECT_ENV_VAR,
]


class FakeProject:
    pass


class TestUnicoreBackend:
    def test_run(
        self, monkeypatch, example_project_path, tmp_path, env_vars_set, caplog
    ):
        monkeypatch.setattr(
            pyunicore.client,
            "Transport",
            testing.pyunicore.FakeTransport,
        )
        fake_client_with_successful_login = functools.partial(
            testing.pyunicore.FakeClient,
            login_successful=True,
        )
        monkeypatch.setattr(
            pyunicore.client,
            "Client",
            fake_client_with_successful_login,
        )
        backend_config_path = (
            example_project_path / "compute-backend-config.json"
        )
        with open(backend_config_path) as infile:
            backend_config = json.load(infile)
        # Following env vars are set by MLflow before running a project.
        backend_config[
            projects.PROJECT_STORAGE_DIR
        ] = example_project_path.as_posix()

        # Point MLFLOW_TRACKING_URI to a temporary directory
        tracking_uri = tmp_path / "mlruns"

        run_name = "my incredible run"

        with env_vars_set(
            {
                # Following env vars must be set for the config.
                **{key: "test-val" for key in ALL_ENV_VARS},
                mantik_utils.mlflow.TRACKING_URI_ENV_VAR: tracking_uri.as_uri(),
                utils.mlflow.RUN_NAME_ENV_VAR: run_name,
            }
        ):
            submitted_run = backend.UnicoreBackend().run(
                project_uri=example_project_path.as_posix(),
                entry_point="main",
                params={"print": "test"},
                version=None,
                backend_config=backend_config,
                tracking_uri=None,
                experiment_id=None,
            )

            assert submitted_run._job._job.started
            assert "with name my incredible run" in caplog.text


def test_submit_job_in_staging_in_and_upload_input_files(
    example_project_path, example_project, example_config
):
    client = testing.pyunicore.FakeClient()
    entry_point = example_project.get_entry_point("main")
    parameters = {"print": "test"}
    apptainer_image = example_project_path / "mantik-test.sif"
    client = _client.Client(client)
    backend._submit_job_in_staging_in_and_upload_input_files(
        client=client,
        entry_point=entry_point,
        parameters=parameters,
        storage_dir="",
        input_files=[apptainer_image],
        config=example_config,
        run_id="example_run_id",
    )


def test_create_job_description_apptainer(
    example_project_path, example_project, example_config
):
    entry_point = example_project.get_entry_point("main")
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"
    expected = {
        "Executable": (
            "srun apptainer run mantik-test.sif python main.py whatever"
        ),
        "Arguments": [],
        "Project": "test-project",
        "Resources": {"Queue": "batch"},
        "RunUserPrecommandOnLoginNode": True,
        "RunUserPostcommandOnLoginNode": True,
        "Stderr": "mantik.log",
        "Stdout": "mantik.log",
    }
    result = backend.create_job_description(
        entry_point=entry_point,
        parameters=parameters,
        storage_dir=storage_dir,
        config=example_config,
    )

    # Environment contains additional MLFLOW env vars,
    # which depend on the execution environment
    expected_environment = {"SRUN_CPUS_PER_TASK": 100}
    actual_environment = result.pop("Environment")
    assert all(
        actual_environment[key] == value
        for key, value in expected_environment.items()
    )

    assert result == expected


def test_create_job_description_apptainer_entry_point_multi_line(
    example_project_path, example_project, example_config
):
    entry_point = example_project.get_entry_point("multi-line")
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"
    expected = {
        "Executable": (
            "srun apptainer run mantik-test.sif python main.py whatever  "
            "--o option1  --i option2"
        ),
        "Arguments": [],
        "Project": "test-project",
        "Resources": {"Queue": "batch"},
        "RunUserPrecommandOnLoginNode": True,
        "RunUserPostcommandOnLoginNode": True,
        "Stderr": "mantik.log",
        "Stdout": "mantik.log",
    }
    result = backend.create_job_description(
        entry_point=entry_point,
        parameters=parameters,
        storage_dir=storage_dir,
        config=example_config,
    )

    # Environment contains additional MLFLOW env vars,
    # which depend on the execution environment
    expected_environment = {"SRUN_CPUS_PER_TASK": 100}
    actual_environment = result.pop("Environment")
    assert all(
        actual_environment[key] == value
        for key, value in expected_environment.items()
    )

    assert result == expected


def test_create_job_description_python(
    example_project_path, example_project, example_config_for_python
):
    entry_point = example_project.get_entry_point("main")
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"
    expected = {
        "Executable": (
            "precommand compute node && "
            "source /venv/bin/activate && python main.py whatever && "
            "postcommand compute node"
        ),
        "Arguments": [],
        "Project": "test-project",
        "Resources": {"Queue": "batch"},
        "RunUserPrecommandOnLoginNode": True,
        "RunUserPostcommandOnLoginNode": True,
        "Stderr": "mantik.log",
        "Stdout": "mantik.log",
    }
    result = backend.create_job_description(
        entry_point=entry_point,
        parameters=parameters,
        storage_dir=storage_dir,
        config=example_config_for_python,
    )

    # Removing Environment for assertion since it contains additional MLFLOW
    # env vars, which depend on the execution environment
    result.pop("Environment", None)

    assert result == expected


def test_ml_project_command_validation():
    entry_point = _project_spec.EntryPoint(
        name="main",
        parameters={
            "optional": {"default": "test", "type": "string"},
        },
        command=(
            "python main.py "
            "{optional} --nproc-per-node=$(${{SLURM_STEP_GPUS: -1}} + 1 )"
        ),
    )
    parameters = {"optional": "whatever"}
    storage_dir = "test-dir"

    backend._create_arguments(
        entry_point=entry_point,
        parameters=parameters,
        storage_dir=storage_dir,
    )


@pytest.mark.parametrize(
    ("entry_point", "user_parameters", "expected"),
    [
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {incorrect-parameter} {optional}",
            ),
            {"required": "whatever"},
            "Mismatch between entry point parameter names and parameter "
            "placeholders in the command: ['incorrect-parameter', 'required']. "
            "Please revise the MLproject file for "
            "typos or inconsistencies between parameter names and their "
            "corresponding placeholders in the command.",
        ),
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "optional": {"default": "test", "type": "string"},
                },
                command=(
                    "python main.py "
                    "{optional} --nproc-per-node=$(${SLURM_STEP_GPUS: -1} + 1 )"
                ),
            ),
            {"optional": "whatever"},
            "Entry point command contains improperly formatted environment "
            "variable expansions: ['${SLURM_STEP_GPUS: -1}']. Ensure "
            "expansions use exactly two opening and closing braces, "
            "e.g. ${{ENV_VAR}}.",
        ),
    ],
    ids=[
        "incorrect parameter in command with optional parameter given",
        "expansion variable given with single curly braces",
    ],
)
def test_ml_project_command_validation_fails(
    entry_point, user_parameters, expected, expect_raise_if_exception
):
    storage_dir = "test-dir"

    with expect_raise_if_exception(
        exceptions.MLprojectFileValidationError()
    ) as e:
        backend._create_arguments(
            entry_point=entry_point,
            parameters=user_parameters,
            storage_dir=storage_dir,
        )
    result = str(e.value)
    assert result == expected


@pytest.mark.parametrize(
    ("entry_point", "user_parameters"),
    [
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {required} {optional}",
            ),
            {"required": "whatever"},
        ),
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {required} {optional}",
            ),
            {"required": "whatever", "optional": "whatever"},
        ),
    ],
    ids=[
        "required parameter given, optional parameter not given",
        "required and optional parameter given",
    ],
)
def test_validate_parameters_placeholders_entry_point(
    entry_point, user_parameters
):
    backend._validate_parameters_placeholders_entry_point(
        entry_point=entry_point, user_parameters=user_parameters
    )


@pytest.mark.parametrize(
    ("entry_point", "user_parameters", "expected"),
    [
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {incorrect-parameter} {optional}",
            ),
            {"required": "whatever"},
            "Mismatch between entry point parameter names and parameter "
            "placeholders in the command: ['incorrect-parameter', 'required']. "
            "Please revise the MLproject file for "
            "typos or inconsistencies between parameter names and their "
            "corresponding placeholders in the command.",
        ),
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {required} {optional}",
            ),
            {"incorrect-parameter": "whatever", "optional": "whatever"},
            "Mismatch between entry point parameters and entered parameters: "
            "['incorrect-parameter', 'required']. Please revise the MLproject "
            "file or your submit command for typos or inconsistencies",
        ),
    ],
    ids=[
        "typo in user parameter with optional parameter given",
        "incorrect parameter in command with optional parameter given",
    ],
)
def test_validate_parameters_placeholders_entry_point_fails(
    entry_point, user_parameters, expected, expect_raise_if_exception
):
    with expect_raise_if_exception(
        exceptions.MLprojectFileValidationError()
    ) as e:
        backend._validate_parameters_placeholders_entry_point(
            entry_point=entry_point, user_parameters=user_parameters
        )
    result = str(e.value)
    assert result == expected


def test_environment_variable_expansion_validation():
    broken_entry_point = _project_spec.EntryPoint(
        name="main",
        parameters={},
        command=(
            "python main.py "
            "--nproc-per-node=$(( ${{SLURM_STEP_GPUS: -1}} + 1 ))"
        ),
    )

    backend._validate_env_var_expansion_in_entry_point(
        entry_point=broken_entry_point
    )


@pytest.mark.parametrize(
    ("env_var_expansion", "env_var_expansion_list"),
    [
        ("$(( ${SLURM_STEP_GPUS: -1} + 1 ))", "['${SLURM_STEP_GPUS: -1}']"),
        (
            "$(( ${{{SLURM_STEP_GPUS: -1}}} + 1 ))",
            "['${{{SLURM_STEP_GPUS: -1}}}']",
        ),
        (
            "$(( ${{{SLURM_STEP_GPUS: -1}} + 1 ))",
            "['${{{SLURM_STEP_GPUS: -1}}']",
        ),
    ],
    ids=[
        "Single opening and closing curly braces",
        "Matching number of opening and closing curly braces, "
        "but incorrect number",
        "Not matching numbers of opening and closing curly braces",
    ],
)
def test_environment_variable_expansion_fails(
    env_var_expansion, env_var_expansion_list, expect_raise_if_exception
):
    broken_entry_point = _project_spec.EntryPoint(
        name="main",
        parameters={},
        command=f"python main.py --nproc-per-node={env_var_expansion}",
    )
    expected = (
        "Entry point command contains improperly formatted environment "
        f"variable expansions: {env_var_expansion_list}. Ensure "
        "expansions use exactly two opening and closing braces, "
        "e.g. ${{ENV_VAR}}."
    )
    with expect_raise_if_exception(
        exceptions.MLprojectFileValidationError()
    ) as e:
        backend._validate_env_var_expansion_in_entry_point(
            entry_point=broken_entry_point
        )
    result = str(e.value)
    assert result == expected
