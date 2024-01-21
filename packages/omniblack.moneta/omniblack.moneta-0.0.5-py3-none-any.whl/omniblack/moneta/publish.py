from sys import stderr
from glob import glob
from os.path import join, relpath as relative_to
from omniblack.repo import find_packages, find_root
from tomlkit import dump

from rich import print

from sh import ErrorReturnCode_128, git, twine

from .app import app
from .read_change import read_change

info_git = git.bake('--no-pager', '--no-optional-locks')


def get_changes(pkg):
    changes_dir = join(pkg.root_dir, 'changes')
    newest_tag = get_newest_tag(pkg)
    rel_pkg = relative_to(pkg.path, pkg.root_dir)

    if newest_tag is not None:
        new_changes = info_git(
            'diff-index',
            '--no-color',
            '--name-only',
            '--diff-filter=A',
            newest_tag,
            changes_dir,
            _cwd=pkg.root_dir,
        )

        change_files = new_changes.split('\n')
    else:
        change_files = glob(join(changes_dir, '**', '*.md'), recursive=True)

    changes = (
        read_change(change_file)
        for change_file in change_files
    )

    return [
        change
        for change in changes
        if change.package == rel_pkg
    ]


def get_newest_tag(pkg):
    name = relative_to(pkg.path, pkg.root_dir)

    try:
        return info_git.describe(
            tags=True,
            match=name + '-*',
            _cwd=pkg.root_dir,
        )
    except ErrorReturnCode_128:
        return None


@app.command
def publish():
    """
    Create a release commit including pending changes to packages.
    """
    root_dir = find_root()

    pkg_to_change = {
        pkg: get_changes(pkg)
        for pkg in find_packages(root_dir, iter=True)
        if pkg.py
    }

    pkg_to_change = {
        pkg: changes
        for pkg, changes in pkg_to_change.items()
        if changes
    }

    new_versions = tuple(
        publish_pkg(pkg, changes)
        for pkg, changes in pkg_to_change.items()
    )

    if not new_versions:
        print('[red]No changes to publish[/]', file=stderr)
        return 1

    commit_lines = [
        pkg_commit_message(pkg, new_version, changes)
        for pkg, new_version, changes in new_versions
    ]

    commit_lines[0:-1] = [
        line + '\n'
        for line in commit_lines[0:-1]
    ]

    commit_message = 'Bump Packages:\n\n' + '\n'.join(commit_lines)

    git.commit(message=commit_message, _cwd=root_dir, verbose=True, _fg=True)

    for pkg, version, _ in new_versions:
        tag = f'{pkg.rel_path}-{version}'
        git.tag(tag, _fg=True)
        print(f'[blue]Created tag[/] [green]{tag}[/]')

    git.push(verbose=True, _fg=True)

    all_dist_files = []
    print('[blue]Uploading[/]:')

    for pkg, *_ in new_versions:
        dist_files = glob(join(pkg.path, 'dist', '*'))
        all_dist_files.extend(dist_files)
        for file in dist_files:
            print(f'  [green]{file}[/]')

    twine.upload(*all_dist_files, non_interactive=True, _fg=True, verbose=True)


def pkg_commit_message(pkg, new_version, changes):
    lines = [f'* {pkg.rel_path} {pkg.version} -> {new_version}']
    lines.extend([
        (' ' * 2) + f'* {relative_to(change.path, pkg.root_dir)}'
        for change in changes
    ])

    return '\n'.join(lines)


def prepare_message(msg: str):
    lines = msg.splitlines()
    lines[0] = f'* {lines[0]}'
    lines[1:] = (
        f'  {line}'
        for line in lines[1:]
    )

    return '\n'.join(lines)


def publish_pkg(pkg, changes):
    if len(changes) != 1:
        severity = max(
            change.severity
            for change in changes
        )
    else:
        change = changes[0]
        severity = change.severity

    new_version = pkg.version.bump(severity.name)
    if pkg.py:
        man = pkg.py.manifest
        man['project']['version'] = str(new_version)
        with open(pkg.py.path, 'w') as man_file:
            dump(man, man_file)

        git.add(pkg.py.path, _cwd=pkg.root_dir, verbose=True, _fg=True)

    return pkg, new_version, changes


if __name__ == '__main__':
    publish()
