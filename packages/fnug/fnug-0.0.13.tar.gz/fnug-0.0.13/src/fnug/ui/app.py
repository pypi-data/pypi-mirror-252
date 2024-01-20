import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from textual import events, on
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal
from textual.geometry import Size
from textual.scrollbar import ScrollBar, ScrollDown, ScrollTo, ScrollUp
from textual.widgets import Footer

from fnug.config import ConfigRoot
from fnug.terminal_emulator import TerminalEmulator
from fnug.ui.components.lint_tree import LintTree, LintTreeDataType
from fnug.ui.components.terminal import Terminal


@dataclass
class TerminalInstance:
    """A collection of tasks and emulator for a terminal."""

    emulator: TerminalEmulator
    reader_task: asyncio.Task[None]
    run_task: asyncio.Task[None]


class FnugApp(App[None]):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "app.tcss"

    BINDINGS: ClassVar[list[BindingType]] = [Binding("escape", "quit", "Quit", show=False)]

    terminals: ClassVar[dict[str, TerminalInstance]] = {}
    active_terminal_id: str | None = None
    display_task: asyncio.Task[None] | None = None
    update_ready = asyncio.Event()

    def __init__(self, config: ConfigRoot, cwd: Path | None = None):
        super().__init__()
        self.cwd = (cwd or Path.cwd()).resolve()
        self.config = config

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Horizontal(id="main"):
            yield LintTree(self.config, cwd=self.cwd, id="lint-tree")
            yield Terminal(id="terminal")
            yield ScrollBar()
        yield Footer()

    @property
    def _active_terminal_emulator(self) -> TerminalInstance | None:
        if self.active_terminal_id is None:
            return None

        return self.terminals[self.active_terminal_id]

    @property
    def _lint_tree(self) -> LintTree:
        return self.query_one("#lint-tree", LintTree)

    @property
    def _terminal(self) -> Terminal:
        return self.query_one("#terminal", Terminal)

    @property
    def _scrollbar(self) -> ScrollBar:
        return self.query_one("ScrollBar", ScrollBar)

    @on(LintTree.NodeHighlighted, "#lint-tree")
    def _switch_terminal(self, event: LintTree.NodeHighlighted[LintTreeDataType]):
        if self.display_task is not None:
            self.display_task.cancel()
            self._terminal.clear()
        if event.node.data:
            self.display_task = asyncio.create_task(self._display_terminal(event.node.data.id))

    @on(LintTree.RunCommand, "#lint-tree")
    def _action_run_command(self, event: LintTree.RunCommand):
        if event.node.data is not None:
            self._run_command(event.node.data)

    @on(LintTree.StopCommand, "#lint-tree")
    def _action_stop_command(self, event: LintTree.RunCommand):
        if event.node.data:
            self._stop_command(event.node.data.id)

    @on(LintTree.RunAllCommand, "#lint-tree")
    def _run_all(self, event: LintTree.RunAllCommand):
        cursor_id = getattr(self._lint_tree.cursor_node, "id", None)

        for node in event.nodes:
            if node.data is not None:
                self._run_command(node.data, background=cursor_id != node.id)

    @on(LintTree.Resize, "#lint-tree")
    async def _tree_resize(self, event: LintTree.Resize):
        await self._on_resize()

    @on(ScrollDown)
    def _scroll_down(self, event: ScrollTo) -> None:
        if self._active_terminal_emulator is not None:
            self._active_terminal_emulator.emulator.scroll("down")
            self.update_ready.set()

    @on(ScrollUp)
    def _scroll_up(self, event: ScrollTo) -> None:
        if self._active_terminal_emulator is not None:
            self._active_terminal_emulator.emulator.scroll("up")
            self.update_ready.set()

    async def _display_terminal(self, command_id: str):
        scrollbar = self._scrollbar
        terminal = self.terminals.get(command_id)
        if terminal is None:
            scrollbar.window_virtual_size = 0
            return

        ui = self._terminal
        self.active_terminal_id = command_id
        task = ui.attach_emulator(terminal.emulator, self.update_ready, scrollbar)
        ui.update_scrollbar(scrollbar)
        await task

    def _run_command(self, command: LintTreeDataType, background: bool = False):
        if command.type != "command":
            return

        tree = self._lint_tree
        tree.update_status(command.id, "running")

        te = TerminalEmulator(self._terminal_size(), self.update_ready)

        async def run_shell():
            cwd = self.cwd
            if command.command and command.command.cwd:
                cwd = cwd / command.command.cwd

            if command.command and await te.run_shell(command.command.cmd, cwd):
                tree.update_status(command.id, "success")
            else:
                tree.update_status(command.id, "failure")

        if command.id in self.terminals:
            self.terminals[command.id].run_task.cancel()
            self.terminals[command.id].reader_task.cancel()

        self.terminals[command.id] = TerminalInstance(
            emulator=te,
            reader_task=asyncio.create_task(te.reader()),
            run_task=asyncio.create_task(run_shell()),
        )
        if not background and self.display_task is not None:
            self.display_task.cancel()
        if not background:
            self.display_task = asyncio.create_task(self._display_terminal(command.id))
        self.update_ready.set()

    def _stop_command(self, command_id: str):
        tree = self._lint_tree

        if command_id in self.terminals:
            self.terminals[command_id].emulator.clear()
            self.terminals[command_id].run_task.cancel()
            self.terminals[command_id].reader_task.cancel()
            self.update_ready.set()
            tree.update_status(command_id, "pending")

    def _terminal_size(self) -> Size:
        scrollbar_width = 1
        return Size(
            width=self.size.width - self._lint_tree.outer_size.width - scrollbar_width, height=self.size.height - 1
        )

    def _on_mount(self):
        self.call_after_refresh(self._on_resize)

    async def _on_resize(self, event: events.Resize | None = None) -> None:
        size = self._terminal_size()
        scrollbar = self._scrollbar
        scrollbar.window_size = size.height
        scrollbar.window_virtual_size = 0

        for terminal in self.terminals.values():
            self._scrollbar.window_size = size.height
            terminal.emulator.dimensions = size
