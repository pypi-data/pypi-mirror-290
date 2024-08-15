import subprocess
import pytest

from src.conda_export_history_versions.parse_conda_env import (
    export_yaml,
    get_conda_env_export,
    get_conda_list,
    run_command,
    update_dependencies,
)


@pytest.mark.usefixtures("mocker")
class TestParseCondaEnv:
    def test_run_command_success(self, mocker):
        mock_run = mocker.patch("subprocess.run")
        mock_result = mocker.Mock()
        mock_result.stdout = "Command output"
        mock_run.return_value = mock_result

        result = run_command(["test", "command"])
        assert result == "Command output"
        mock_run.assert_called_once_with(
            ["test", "command"], capture_output=True, text=True, check=True
        )

    def test_run_command_failure(self, mocker):
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["test"], stderr="Error message"
        )

        with pytest.raises(subprocess.CalledProcessError):
            run_command(["test", "command"])

    def test_get_conda_env_export_with_env_name(self, mocker):
        mock_run_command = mocker.patch(
            "src.conda_export_history_versions.parse_conda_env.run_command"
        )
        mock_run_command.return_value = "name: test_env\ndependencies:\n  - python=3.8"
        result = get_conda_env_export("test_env")
        assert result == {"name": "test_env", "dependencies": ["python=3.8"]}
        mock_run_command.assert_called_once_with(
            ["conda", "env", "export", "--from-history", "-n", "test_env"]
        )

    def test_get_conda_list_without_env_name(self, mocker):
        mock_run_command = mocker.patch(
            "src.conda_export_history_versions.parse_conda_env.run_command"
        )
        mock_run_command.return_value = '[{"name": "python", "version": "3.8.0"}]'
        result = get_conda_list()
        assert result == [{"name": "python", "version": "3.8.0"}]
        mock_run_command.assert_called_once_with(["conda", "list", "--json"])

    def test_update_dependencies(self):
        env_dict = {"dependencies": ["python", "numpy"]}
        conda_list = [
            {"name": "python", "version": "3.8.0"},
            {"name": "numpy", "version": "1.21.0"},
            {"name": "pandas", "version": "1.3.0"},
        ]
        result = update_dependencies(env_dict, conda_list)
        assert result == {"dependencies": ["numpy==1.21.0", "python==3.8.0"]}

    def test_export_yaml(self, mocker):
        data = {"name": "test_env", "dependencies": ["python==3.8.0", "numpy==1.21.0"]}
        mock_file = mocker.mock_open()
        mocker.patch("builtins.open", mock_file)
        export_yaml(data, "test_env.yml")
        mock_file.assert_called_once_with("test_env.yml", "w")
        mock_file().write.assert_called_once_with(
            "name: test_env\ndependencies:\n  - python==3.8.0\n  - numpy==1.21.0\n"
        )
