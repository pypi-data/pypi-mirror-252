from py_git_auto_version.settings.auto_version import PyGitAutoVersionSettings
from py_git_auto_version.settings.github import GitHubActionEnvVars
from py_git_auto_version.version_generators import generate_version_string_for_scenario


def for_toml():
    github_ = GitHubActionEnvVars.generate_failover_env_then_dotenv()
    auto_version_ = PyGitAutoVersionSettings.generate_failover_try_env_then_dotenv_then_defaults()
    return generate_version_string_for_scenario(
            auto_version_settings=auto_version_,
            github_action_env_vars=github_
    )
