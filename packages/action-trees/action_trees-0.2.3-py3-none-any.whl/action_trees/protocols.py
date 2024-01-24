""" action protocols """
from __future__ import annotations
import asyncio
from typing import Protocol
from .action_item import ActionState


class ActionItemProtocol(Protocol):
    """interface for action items"""

    def start(self) -> asyncio.Task:
        """start action item, if not already started, always return reference
        to main task"""

    async def cancel(self) -> None:
        """asynchronously cancel the action item"""

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...

    def get_exception(self) -> BaseException | None:
        """get exception if any"""

    @property
    def state(self) -> ActionState:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def parent(self) -> ActionItemProtocol | None:
        """get parent (if any)"""

    def add_child(self, child: ActionItemProtocol) -> None:
        """add child"""

    def get_child(self, name: str) -> ActionItemProtocol:
        """get child by name"""

    def remove_child(self, name: str) -> None:
        """remove child by name"""

    @property
    def children(self) -> list[ActionItemProtocol]:
        """get children"""
