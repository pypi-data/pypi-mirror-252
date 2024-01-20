"""Update manager module."""
from __future__ import annotations

import asyncio
import importlib.metadata
from pathlib import Path

import aiohttp
from kivy import shutil
from ubo_gui.constants import DANGER_COLOR, SECONDARY_COLOR, SUCCESS_COLOR
from ubo_gui.menu.types import ActionItem, Item

from ubo_app.constants import INSTALLATION_PATH
from ubo_app.logging import logger
from ubo_app.store import autorun, dispatch
from ubo_app.store.services.notifications import (
    Chime,
    Notification,
    NotificationsAddAction,
)
from ubo_app.store.update_manager_types import (
    SetLatestVersionAction,
    SetUpdateStatusAction,
    UpdateStatus,
    VersionStatus,
)
from ubo_app.utils.async_ import create_task

CURRENT_VERSION = importlib.metadata.version('ubo_app')


@autorun(lambda store: store.main.version.update_status)
async def check(status: UpdateStatus) -> None:
    """Check for updates."""
    if status != UpdateStatus.CHECKING:
        return

    logger.info('Checking for updates...')

    # Check PyPI server for the latest version
    import requests

    try:
        async with aiohttp.ClientSession() as session, session.get(
            'https://pypi.org/pypi/ubo-app/json',
            timeout=5,
        ) as response:
            if response.status != requests.codes.ok:
                logger.error('Failed to check for updates')
                return
            data = await response.json()
            latest_version = data['info']['version']

            # Compare the latest version with the current version
            if latest_version == CURRENT_VERSION:
                dispatch(
                    SetLatestVersionAction(latest_version=latest_version),
                    SetUpdateStatusAction(status=UpdateStatus.UP_TO_DATE),
                )
            else:
                dispatch(
                    SetLatestVersionAction(latest_version=latest_version),
                    SetUpdateStatusAction(status=UpdateStatus.OUTDATED),
                    NotificationsAddAction(
                        notification=Notification(
                            title='Update available!',
                            content=f"""Ubo v{latest_version
                                } is available. Go to the About menu to update.""",
                            color=SECONDARY_COLOR,
                            icon='system_update',
                            chime=Chime.DONE,
                        ),
                    ),
                )
    except requests.exceptions.RequestException as exception:
        logger.error('Failed to check for updates', exc_info=exception)
        dispatch(SetUpdateStatusAction(status=UpdateStatus.FAILED_TO_CHECK))
        return


check.subscribe(create_task)


@autorun(lambda store: store.main.version)
async def update(version: VersionStatus) -> None:
    """Update the Ubo app."""
    if version.update_status != UpdateStatus.UPDATING:
        return
    logger.info('Updating Ubo app...')

    async def download_files() -> None:
        target_path = Path(f'{INSTALLATION_PATH}/_update/')
        shutil.rmtree(target_path.parent, ignore_errors=True)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        process = await asyncio.create_subprocess_exec(
            '/usr/bin/env',
            'pip',
            'download',
            '--dest',
            target_path,
            'ubo-app[default]',
            'setuptools',
            'wheel',
        )
        await process.wait()
        if process.returncode != 0:
            msg = 'Failed to download packages'
            raise RuntimeError(msg)

    try:
        await download_files()

        await asyncio.sleep(3)

        process = await asyncio.create_subprocess_exec(
            '/usr/bin/env',
            'sudo',
            'reboot',
        )
        await process.wait()
    except Exception as exception:  # noqa: BLE001
        logger.error('Failed to update', exc_info=exception)
        dispatch(
            NotificationsAddAction(
                notification=Notification(
                    title='Failed to update',
                    content='Failed to update',
                    color=DANGER_COLOR,
                    icon='security_update_warning',
                    chime=Chime.FAILURE,
                ),
            ),
            SetUpdateStatusAction(status=UpdateStatus.CHECKING),
        )
        return


update.subscribe(create_task)


@autorun(lambda store: store.main.version)
def about_menu_items(version_status: VersionStatus) -> list[Item]:
    """Get the update menu items."""
    if version_status.update_status is UpdateStatus.CHECKING:
        return [
            ActionItem(
                label='Checking for updates...',
                action=lambda: None,
                icon='update',
                background_color='#00000000',
            ),
        ]
    if version_status.update_status is UpdateStatus.FAILED_TO_CHECK:
        return [
            ActionItem(
                label='Failed to check for updates',
                action=lambda: dispatch(
                    SetUpdateStatusAction(status=UpdateStatus.CHECKING),
                ),
                icon='security_update_warning',
                background_color=DANGER_COLOR,
            ),
        ]
    if version_status.update_status is UpdateStatus.UP_TO_DATE:
        return [
            ActionItem(
                label='Already up to date!',
                action=lambda: None,
                icon='security_update_good',
                background_color=SUCCESS_COLOR,
            ),
        ]
    if version_status.update_status is UpdateStatus.OUTDATED:
        return [
            ActionItem(
                label=f'Update to v{version_status.latest_version}',
                action=lambda: dispatch(
                    SetUpdateStatusAction(status=UpdateStatus.UPDATING),
                ),
                icon='system_update',
            ),
        ]
    if version_status.update_status is UpdateStatus.UPDATING:
        return [
            ActionItem(
                label='Updating...',
                action=lambda: None,
                icon='update',
                background_color='#00000000',
            ),
        ]
    return []
