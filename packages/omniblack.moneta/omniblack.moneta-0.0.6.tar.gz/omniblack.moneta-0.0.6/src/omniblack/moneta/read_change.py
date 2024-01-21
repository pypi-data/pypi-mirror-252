from io import StringIO
from dataclasses import dataclass
from datetime import datetime

from .parse_diff import Severity
from .yaml import yaml


@dataclass
class Change:
    author: str
    email: str
    date: datetime
    severity: Severity
    package: str
    message: str
    path: str

    @classmethod
    def from_yaml(cls, change_path, data, msg):
        return cls(
            author=data['author'],
            email=data['email'],
            date=data['date'],
            severity=Severity[data['severity']],
            package=data['package'],
            message=msg.strip(),
            path=change_path,
        )


def read_change(change_path):
    with open(change_path) as file:
        lines = ''
        line_iter = iter(file)
        next(line_iter)  # Ignore the first frontmatter marker
        for line in file:
            if line.strip() == '---':
                break
            else:
                lines += line

        msg = file.read()

    stream = StringIO(lines)
    data = yaml.load(stream)
    return Change.from_yaml(change_path, data, msg)
