# ruff: noqa: D100, D101, D102, D103, D104, D107
from __future__ import annotations

from dataclasses import replace
from typing import Sequence

from redux import BaseAction, Immutable, InitAction, InitializationActionError


class IconState(Immutable):
    symbol: str
    color: str
    priority: int
    id: str | None


class StatusIconsState(Immutable):
    icons: Sequence[IconState]


class StatusIconsRegisterAction(BaseAction):
    icon: str
    color: str = 'white'
    priority: int = 0
    id: str | None = None


IconAction = StatusIconsRegisterAction | InitAction


def reducer(state: StatusIconsState | None, action: IconAction) -> StatusIconsState:
    if state is None:
        if isinstance(action, InitAction):
            return StatusIconsState(icons=[])
        raise InitializationActionError(action)
    if isinstance(action, StatusIconsRegisterAction):
        return replace(
            state,
            icons=sorted(
                [
                    *[
                        icon_status
                        for icon_status in state.icons
                        if icon_status.id != action.id or icon_status.id is None
                    ],
                    IconState(
                        symbol=action.icon,
                        color=action.color,
                        priority=action.priority,
                        id=action.id,
                    ),
                ],
                key=lambda entry: entry.priority,
            ),
        )
    return state
