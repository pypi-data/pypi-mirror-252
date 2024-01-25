import dataclasses
import logging
import pathlib
import typing as t
import uuid

import mantik.compute_backend.config._base as _base
import mantik.compute_backend.config._utils as _utils
import mantik.compute_backend.config.environment as _environment
import mantik.compute_backend.config.exceptions as _exceptions
import mantik.compute_backend.config.firecrest as _firecrest
import mantik.compute_backend.config.read as read
import mantik.compute_backend.config.resources as _resources
import mantik.compute_backend.credentials as _credentials
import mantik.utils.env as env

_PROJECT_ENV_VAR = "MANTIK_COMPUTE_BUDGET_ACCOUNT"
_UNICORE_AUTH_SERVER_URL_ENV_VAR = "MANTIK_UNICORE_AUTH_SERVER_URL"
APPLICATION_LOGS_FILE = "mantik.log"

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Config(_base.ConfigObject):
    """The backend config for the UNICORE MLflow backend."""

    user: str
    password: str
    project: str
    resources: _resources.Resources
    environment: t.Optional[_environment.Environment] = None
    exclude: t.Optional[t.List] = None
    unicore_api_url: t.Optional[str] = None
    firecrest: t.Optional[_firecrest.Firecrest] = None

    @classmethod
    def _from_dict(
        cls, config: t.Dict, connection_id: t.Optional[uuid.UUID] = None
    ) -> "Config":
        """

        Parameters
        ----------
        config : t.Dict
            the possible keys to specify inside the config dictionary are:
            REQUIRED:
                - UnicoreApiUrl : str
                    URL to the API of the UNICORE HPC used.

                The other required field MANTIK_USERNAME, MANTIK_PASSWORD
                and MANTIK_PROJECT are inferred from the environment.
            OPTIONAL:
                - Resources : dict
                    Dict of parameters specifying the resources
                    to request on the remote system.
                    More info can be found here:
                    https://sourceforge.net/p/unicore/wiki/Job_Description/
                - Environment : dict
                    Used to build a environment.Environment.
                - Exclude : list
                    List of files or file-patterns
                    that are not sent with the job


        Returns
        -------
        mantik.unicore._config.core.Config

        """
        (
            unicore_api_url,
            firecrest,
            credentials,
        ) = _get_unicore_or_firecrest_and_credentials(
            config=config,
            connection_id=connection_id,
        )
        project = env.get_required_env_var(_PROJECT_ENV_VAR)

        # Read remaining config sections.
        resources = _utils.get_required_config_value(
            name="Resources",
            value_type=_resources.Resources.from_dict,
            config=config,
        )
        environment = _utils.get_optional_config_value(
            name="Environment",
            value_type=_environment.Environment.from_dict,
            config=config,
        )
        exclude = _utils.get_optional_config_value(
            name="Exclude",
            value_type=list,
            config=config,
        )

        return cls(
            unicore_api_url=unicore_api_url,
            firecrest=firecrest,
            user=credentials.username,
            password=credentials.password,
            project=project,
            resources=resources,
            environment=environment,
            exclude=exclude,
        )

    def __post_init__(self):
        if self.environment is None:
            self.environment = _environment.Environment()

        # set SRUN_CPUS_PER_TASK to CPUsPerNode if not explicitly set
        self.environment = self.environment.set_srun_cpus_per_task_if_unset(
            self.resources
        )

        if self.firecrest is not None and (
            self.environment.pre_run_command_on_login_node is not None
            or self.environment.post_run_command_on_login_node is not None
        ):
            raise _exceptions.ConfigValidationError(
                "Pre-/PostRunCommandOnLoginNode not supported by firecREST"
            )

    @classmethod
    def from_filepath(
        cls, filepath: pathlib.Path, connection_id: t.Optional[uuid.UUID] = None
    ) -> "Config":
        """Initialize from a given file."""
        return cls._from_dict(
            read.read_config(filepath), connection_id=connection_id
        )

    @property
    def files_to_exclude(self) -> t.List[str]:
        return self.exclude or []

    def _to_dict(self) -> t.Dict:
        environment = (
            self.environment.to_dict() if self.environment is not None else {}
        )
        return {
            "Project": self.project,
            "Resources": self.resources,
            # Write stderr/stdout to given file to allow access to logs
            "Stdout": APPLICATION_LOGS_FILE,
            "Stderr": APPLICATION_LOGS_FILE,
            **environment,
        }

    def to_job_description(self, arguments: str) -> t.Dict:
        """Convert to UNICORE job description."""
        environment = (
            self.environment.to_job_description(arguments)
            if self.environment is not None
            else {}
        )
        return {
            **self.to_dict(),
            **environment,
        }

    def execution_environment_given(self) -> bool:
        return (
            self.environment is not None and self.environment.execution_given()
        )

    def add_env_vars(self, env_vars: t.Dict) -> None:
        self.environment.add_env_vars(env_vars)


def _get_unicore_or_firecrest_and_credentials(
    config: t.Dict, connection_id: t.Optional[uuid.UUID] = None
) -> t.Tuple[
    t.Optional[str], t.Optional[_firecrest.Firecrest], _credentials.HpcRestApi
]:
    # Read UNICORE or firecREST info.
    unicore_api_url = _utils.get_optional_config_value(
        name="UnicoreApiUrl",
        value_type=str,
        config=config,
    )
    firecrest = _utils.get_optional_config_value(
        name="Firecrest",
        value_type=_firecrest.Firecrest.from_dict,
        config=config,
    )

    # Check that either UnicoreApiUrl or Firecrest section given
    if unicore_api_url is None and firecrest is None:
        raise _exceptions.ConfigValidationError(
            "Either UnicoreApiUrl or Firecrest details must be provided"
        )
    elif unicore_api_url is not None and firecrest is not None:
        raise _exceptions.ConfigValidationError(
            "Either UnicoreApiUrl or Firecrest details must be provided, "
            "but both are given"
        )

    # Read either UNICORE or firecREST credentials
    if unicore_api_url is not None:
        credentials = _credentials.HpcRestApi.from_unicore_env_vars(
            connection_id
        )
    elif firecrest is not None:
        credentials = _credentials.HpcRestApi.from_firecrest_env_vars(
            connection_id
        )
    else:
        raise RuntimeError("Neither UnicoreApiUrl nor Firecrest section given")

    return unicore_api_url, firecrest, credentials
