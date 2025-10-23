from __future__ import annotations

from typing import Dict, Optional, Type

import pygame


class GameState:
    """Base class for application states.

    Concrete states should override :meth:`enter`, :meth:`exit`,
    :meth:`handle_event`, :meth:`update`, and :meth:`draw` as needed.
    """

    def __init__(self, app: "GameApp") -> None:
        self.app = app

    def enter(self, **params) -> None:  # pragma: no cover - lifecycle hook
        pass

    def exit(self) -> None:  # pragma: no cover - lifecycle hook
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass


class StateMachine:
    """Orchestrates state transitions and lifecycle management."""

    def __init__(self, app: "GameApp") -> None:
        self.app = app
        self.states: Dict[str, GameState] = {}
        self.current: Optional[GameState] = None
        self.current_name: Optional[str] = None

    def register(self, name: str, state_cls: Type[GameState]) -> None:
        if name in self.states:
            raise ValueError(f"State '{name}' already registered")
        self.states[name] = state_cls(self.app)

    def switch(self, name: str, **params) -> None:
        if name not in self.states:
            raise KeyError(f"State '{name}' not registered")
        if self.current:
            self.current.exit()
        self.current_name = name
        self.current = self.states[name]
        self.current.enter(**params)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.current:
            self.current.handle_event(event)

    def update(self, dt: float) -> None:
        if self.current:
            self.current.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self.current:
            self.current.draw(surface)
