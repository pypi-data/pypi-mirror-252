from omniblack.repo import find_root
from os import chmod
from os import makedirs
from os.path import join


hook_exec_name = 'changes'
run_module = 'exec python -m'


def install():
    root = find_root()

    hook_dir = join(root, 'devtools', 'git_hooks', 'pre-commit')
    makedirs(hook_dir, exist_ok=True)
    hook_file = join(hook_dir, hook_exec_name)
    with open(hook_file, 'x') as file:
        file.write('#! /usr/bin/sh\n')
        file.write(
            f'{run_module} {__package__}.{hook_exec_name}'
        )

    # user read/execute
    # group/other readonly
    chmod(hook_file, 0o544)
