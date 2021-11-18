from abc import ABC, abstractmethod
from typing import Any, Callable


class Pager(ABC):
    """Base class for a pager."""

    @abstractmethod
    def show(self, content: str) -> None:
        """Show content in pager.

        Args:
            content (str): Content to be displayed.
        """


class SystemPager(Pager):
    """Uses the pager installed on the system."""

    _pager: Callable[[Any, str], Any] = lambda self, content: __import__("pydoc").pager(
        content
    )

    def show(self, content: str) -> None:
        """Use the same pager used by pydoc."""
        self._pager(content)
