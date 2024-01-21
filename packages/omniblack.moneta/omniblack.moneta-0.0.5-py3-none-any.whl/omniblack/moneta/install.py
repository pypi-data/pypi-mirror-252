from omniblack.repo import find_root
from pathlib import Path


hook_exec_name = 'write_change'
run_module = 'exec python -m'


def install():
    root: Path = find_root()

    hook_dir = root/'devtools'/'git_hooks'/'pre-commit'
    hook_dir.mkdir(exist_ok=True, parents=True)
    hook_file = hook_dir/hook_exec_name
    with hook_file.open('x') as file:
        file.write('#! /usr/bin/sh\n')
        file.write(
            f'{run_module} {__package__}.{hook_exec_name}'
        )

    # user read/execute
    # group/other readonly
    hook_file.chmod(0o544)
