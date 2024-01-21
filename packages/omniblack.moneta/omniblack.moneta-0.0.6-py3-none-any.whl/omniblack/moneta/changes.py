from calendar import month_abbr
from contextlib import contextmanager
from datetime import datetime
from importlib.resources import files
from os import environ, makedirs
from os.path import join
from re import compile
from string import Template
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import NamedTuple

from more_itertools import unique_everseen
from sh import git
from fs.path import isparent, combine

from omniblack.repo import find_packages, find_root, Package

from .yaml import yaml
from .display_diff import Diff, Severity
from .read_change import Change
from .app import app

# a git command to use when doing read operations
info_git = git.bake('--no-pager', '--no-optional-locks')

release_branch = 'next'


author_info_re = compile(r'(?P<name>.+) \<(?P<email>.+)\>')


def read_text(pkg, resource):
    return files(pkg).joinpath(resource).read_text()


class Author(NamedTuple):
    name: str
    email: str


NULL = '\0'


def find_parent_package(path: str, packages: list[Package]):
    for pkg in packages:
        if isparent(pkg.path, path):
            return pkg


def get_packages(root: str) -> tuple[dict[str, Package], set[Package]]:
    all_pkgs = find_packages(root)
    pkg_by_name = {
        pkg.name: pkg
        for pkg in all_pkgs
    }
    packages = set(all_pkgs)

    return (pkg_by_name, packages)


def get_files(root: str):
    cmd = info_git(
        'diff-index',
        # z mean don't munge the path, and use NULL as a seperator
        '-z',
        '--name-only',

        # setting no renames will make git show us both modified paths
        '--no-renames',
        release_branch,
        _cwd=root,
    )

    return [
        combine(root, path)
        for path in cmd.split(NULL)
        if path
    ]


def get_author(root: str):
    author_ident = info_git.var('GIT_AUTHOR_IDENT', _cwd=root)
    author_ident = author_ident.strip()
    capture = author_info_re.match(author_ident)
    return Author(capture['name'], capture['email'])


def get_active_branch(root: str):
    stdout = info_git('rev-parse', 'HEAD', abbrev_ref=True, _cwd=root)
    return stdout.strip()


@contextmanager
def temp_file(root: str, prefix: str, suffix: str):
    file_manager = NamedTemporaryFile(
        mode='w+',
        dir=root,
        suffix=suffix,
    )

    with file_manager as file:
        yield file


def edit_file(file: str):
    command = (
        environ.get('EDITOR', 'vim'),
        file.name,
    )

    run(
        command,
        stdin=None,
        stdout=None,
        stderr=None,
    )


def comment(text: str):
    if text:
        return f'% {text}\n'
    else:
        return '%\n'


def frontmatter(file: str, data: dict):
    file.write('---\n')

    yaml.dump(data=data, stream=file)

    file.write('---\n')


def get_messages(changes: list[Change], active_branch: str, root: str):
    explainer_template = read_text(__package__, 'message_explainer.txt')

    template = Template(explainer_template)

    for change in changes:
        with temp_file(root, change.name, suffix='.md') as msg_file:
            msg_file.write('\n')
            explainer = template.substitute(
                package=change.name,
                branch=active_branch,
            )

            msg_file.writelines(
                comment(line)
                for line in explainer.splitlines()
            )
            msg_file.seek(0)

            edit_file(msg_file)

            msg = [
                line
                for line in msg_file.readlines()
                if not line.startswith('%')
            ]

            change.message = msg


def get_diff(root: str, pkg: Package):
    return info_git(
        'diff-index',
        '--no-color',
        '--patch',
        release_branch,
        pkg.path,
        _cwd=root,
    )


@app.command
def changes(target_pkgs: list[str]):
    """
    Prepare change files.


    Open a TUI to author change files for any packages
    that have changed between HEAD and the release branch.

    Args:
        target_pkgs: packages to publish changes for
    """
    root = find_root()

    now = datetime.today()

    active_branch = get_active_branch(root)
    author = get_author(root)
    (pkg_by_name, packages) = get_packages(root)

    if target_pkgs:
        changed_packages = (
            pkg_by_name[pkg_name]
            for pkg_name in target_pkgs
        )
    else:
        changed_files = get_files(root)
        changed_packages = (
            find_parent_package(file, packages)
            for file in changed_files
        )

    changed_packages = (
        pkg
        for pkg in unique_everseen(changed_packages)
        if pkg is not None
    )

    changes = (
        Diff.get_level(pkg, get_diff(root, pkg))
        for pkg in changed_packages
    )

    changes = tuple(
        change
        for change in changes
        if change.severity != Severity.none
    )

    missing_messages = tuple(
        change
        for change in changes
        if not change.message
    )

    get_messages(missing_messages, active_branch, root)

    changes_dir = join(root, 'changes', str(now.year))

    makedirs(changes_dir, exist_ok=True)

    changes = tuple(
        change
        for change in changes
        if change.message
    )

    paths = []
    for change in changes:
        month_str = month_abbr[now.month].lower()
        time_str = f'{now.hour:02}:{now.minute:02}'
        date_str = f'{month_str}-{now.day:02}T{time_str}'
        name = f'{change.name}-{date_str}.md'
        path = combine(changes_dir, name.replace('/', '-'))
        paths.append(path)

        with open(path, 'x') as file:
            frontmatter(file=file, data=dict(
                author=author.name,
                email=author.email,
                date=now,
                severity=change.severity,
                package=change.name
            ))

            file.write(change.message + '\n')

    git.add(*paths, verbose=True, _fg=True)
