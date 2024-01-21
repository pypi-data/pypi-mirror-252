from os.path import relpath as relative_path

from rich.syntax import Syntax
from textual.app import App
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer, Rule, Static, TextArea

from .parse_diff import parse_diff, Severity, ChangeInfo


class DiffChange(Widget):

    def __init__(self, change):
        self.change = change
        classes = None

        classes = self.change.change

        super().__init__(classes=classes)
        self.border_title = self.change.full_title

    def compose(self):
        if self.change.lines:
            text = '\n'.join(self.change.lines)
            yield Static(
                Syntax(text, 'diff', padding=1),
                shrink=True,
                expand=True,
            )


class Editor(TextArea):
    pass


class Diff(App):
    CSS_PATH = 'diff.tcss'

    BINDINGS = [
        Binding('q', 'none', 'No Change'),
        # Binding('h', 'help', 'Show help screen'),
        Binding('i', 'insert', 'Enter insert mode'),
        Binding('p', 'patch', 'Patch Change'),
        Binding('m', 'minor', 'Minor Change', key_display='m'),
        Binding('M', 'major', 'Major Change'),
    ]

    current_pkg = reactive('')

    def compose(self):
        self.static = Static(self.current_pkg.name, classes='header')
        yield self.static
        yield Rule()

        with VerticalScroll():
            for change in self.changes:
                yield DiffChange(change)

        yield Rule()
        self.editor = Editor(language='markdown', theme='vscode_dark')
        yield self.editor

        yield Footer()

    def action_patch(self):
        self.exit(Severity.patch)

    def action_minor(self):
        self.exit(Severity.minor)

    def action_major(self):
        self.exit(Severity.major)

    def action_none(self):
        self.exit(Severity.none)

    def action_insert(self):
        self.editor.focus()

    def exit(self, severity=Severity.none):
        super().exit(ChangeInfo(
            relative_path(self.current_pkg.path, self.current_pkg.root_dir),
            severity,
            self.editor.text,
        ))

    @classmethod
    def get_level(cls, pkg, diff):
        self = cls()
        self.current_pkg = pkg
        self.changes = tuple(parse_diff(diff))
        return self.run()
