import argparse
import os
import pathlib
from typing import Mapping, Iterator, Callable

from . import ENTRY_DATA
from gather.commands import add_argument
from commander_data import COMMAND


@ENTRY_DATA.register(
    add_argument("--no-dry-run", action="store_true", default=True),
    add_argument("--container", required=True),
    add_argument("--host", required=True),
    add_argument("--user", required=True),
)
def sshirc(args: argparse.Namespace) -> None:  # pragma: no cover
    execlp = getattr(args, "execlp", os.execlp)
    command = list(
        COMMAND.ssh(
            o=["ServerAliveInterval=5", "ServerAliveCountMax=2"],
            t=f"{args.user}@{args.host}",
        )
        .sudo.docker.exec(i=None, t=None, u=args.user)(args.container)
        .tmux.at
    )
    execlp(command[0], *command)


def parse_environment(
    env_path: pathlib.Path,
) -> Iterator[tuple[str, str]]:  # pragma: no cover
    try:
        content = env_path.read_text()
    except OSError:
        content = ""
    for line in content.replace(";", "\n").splitlines():
        line = line.split("#", 1)[0]
        line = line.strip()
        if line == "":
            continue
        try:
            key, value = line.split("=", 1)
        except ValueError:
            continue
        yield key, value


def is_agent_up(env: Mapping[str, str], safe_run: Callable) -> bool:  # pragma: no cover
    try:
        pid = env["SSH_AGENT_PID"]
    except KeyError:
        return False
    results = safe_run(COMMAND.ps(e=None, f=None, width=1000))
    lines = iter(results.stdout.splitlines())
    fields = next(lines).split()
    for a_line in lines:
        if "<defunct>" in a_line:
            continue
        values = dict(zip(fields, a_line.split()))
        if values["PID"] == pid:
            return True
    return False


def bring_up_agent(env_path: pathlib.Path, run: Callable) -> None:  # pragma: no cover
    results = run(COMMAND.ssh_agent, capture_output=True)
    agent_output = results.stdout
    agent_output = agent_output.replace("echo ", "# echo ")
    env_path.write_text(agent_output)


@ENTRY_DATA.register(
    add_argument("--no-dry-run", action="store_true", default=False),
    add_argument(
        "--env-path", default=pathlib.Path.home() / ".ssh" / "agent-environment"
    ),
    name="ssh-agent-env",
)
def ssh_agent_env(args: argparse.Namespace) -> None:  # pragma: no cover
    args.env_path = pathlib.Path(args.env_path)
    env = dict(parse_environment(args.env_path))
    if not is_agent_up(env, args.safe_run):
        bring_up_agent(args.env_path, args.run)
    print(args.env_path.read_text())
