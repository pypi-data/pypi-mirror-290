from click.testing import CliRunner
from agentfud_password_manager.commands.cmd_info import cli


def test_it_returns_version_info():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert "password_manager_version" in result.output
    assert "agentfud@gmail.com" in result.output
    assert result.exit_code == 0
