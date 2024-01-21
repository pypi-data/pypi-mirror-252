import re
from dataclasses import dataclass, field
from enum import Enum
from io import StringIO, TextIOBase
from os.path import basename

from ruamel.yaml import yaml_object

from .yaml import yaml

str_tag = 'tag:yaml.org,2002:str'


@yaml_object(yaml)
class Severity(Enum):
    none = 'none'
    patch = 'patch'
    minor = 'minor'
    major = 'major'

    @property
    def index(self):
        cls = self.__class__

        if not hasattr(cls, '_Severity__member_to_index'):
            cls.__member_to_index = {
                member: index
                for index, member in enumerate(cls)
            }

        return cls.__member_to_index[self]

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(str_tag, node.value)

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.index > other.index

        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.index >= other.index

        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.index < other.index

        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.index <= other.index

        return NotImplemented


@dataclass
class ChangeInfo:
    name: str
    severity: Severity
    _message: str

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, new_value):
        self._message = new_value.strip()


@dataclass
class ChangedFile:
    old_path: str
    new_path: str
    lines: list[str] = field(default_factory=list)

    @property
    def change(self):
        if self.old_path is None:
            return 'added'
        elif self.new_path is None:
            return 'removed'
        elif self.old_path != self.new_path:
            return 'renamed'
        else:
            return 'modified'

    @property
    def full_title(self):
        match self.change:
            case 'added':
                return f'New file: {self.new_path}'
            case 'removed':
                return f'Removed file: {self.old_path}'
            case 'renamed':
                return f'Renamed {self.old_path} -> {self.new_path}'
            case 'modified':
                return f'Changed {self.old_path}'

    @property
    def tab_title(self):
        match self.change:
            case 'renamed':
                old_path = basename(self.old_path)
                new_path = basename(self.new_path)
                return f'{old_path} -> {new_path}'
            case 'added' | 'modified':
                return basename(self.new_path)
            case 'removed':
                return basename(self.old_path)


def parse_header(line_iter):
    next_line = next(line_iter)

    if next_line.startswith('new file mode'):
        next(line_iter)

    old_path_line = next(line_iter)
    *_, old_path = old_path_line.split(' ')
    old_path = old_path.removeprefix('a/').strip()

    new_path_line = next(line_iter)
    *_, new_path = new_path_line.split(' ')
    new_path = new_path.removeprefix('b/').strip()

    if old_path == '/dev/null':
        old_path = None
    else:
        old_path

    if new_path == '/dev/null':
        new_path = None

    return ChangedFile(old_path=old_path, new_path=new_path)


def parse_diff(file: TextIOBase):
    change = None

    if isinstance(file, str):
        file = StringIO(file)

    line_iter = (line.removesuffix('\n') for line in iter(file))
    for line in line_iter:
        first_word, *_ = re.split(r'\s+', line)
        match first_word:
            case 'diff':
                if change is not None:
                    yield change

                change = parse_header(line_iter)

            case _:
                change.lines.append(line)

    if change is not None:
        yield change
