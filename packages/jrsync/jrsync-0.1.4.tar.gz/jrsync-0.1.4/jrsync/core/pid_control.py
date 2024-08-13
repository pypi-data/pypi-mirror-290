import os
from pathlib import Path

BASE_PID_NAME = ".pid"
ROOT_DIR = Path(__file__).parent.parent.resolve()


def another_instance_in_execution(pid_file: Path) -> bool:
    """Try to find pid associated to name to check if there is another instance in execution"""
    if not pid_file.exists():
        return False

    with pid_file.open() as f:
        pid = int(f.read().strip())
        return pid_is_running(pid)


def get_pid_file(run_name=None):
    pid_dir = str(Path(__file__).parent.absolute())
    pid_file = f"{pid_dir}/.pid"
    if run_name:
        pid_file = f"{pid_file}_{run_name}"
    return pid_file


def pid_is_running(pid: int) -> bool:
    """Check For the existence of a unix pid. 0 signal has no effect on the process"""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def write_pid(pid_file: Path):
    pid = str(os.getpid())
    pid_file.write_text(pid)


def get_exec_permission(name: str = "", dr: Path = ROOT_DIR) -> bool:
    """
    Function to check if an instance has the permission to be executed.
    Only an instance in execution can be associated to name
    """
    pid_file = dr / (BASE_PID_NAME + name)

    if another_instance_in_execution(pid_file):
        return False

    write_pid(pid_file)
    return True
