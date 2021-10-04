import logging
import os
import time
from pathlib import Path
from shutil import copy2

import click

logger = logging.getLogger('folder_sync')
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
logger.addHandler(logging.StreamHandler())


def should_copy(target_file: Path, source_file: Path) -> bool:
    """
    return true if source_file should be sent to target_file

    :param target_file:
    :param source_file:
    :return:
    """
    if not source_file.is_file():
        return False

    if not target_file.exists():
        return True
    if target_file.stat().st_mtime < source_file.stat().st_mtime:
        return True

    return False


def sync_file(target_file: Path, source_file: Path):
    """
    copy the file, preserving as many attributes as possible

    :param target_file:
    :param source_file:
    """
    copy2(source_file, target_file)


def run_forever(pattern, source, target, timed):
    """
    run in infinite loop, pausing, timed seconds each loop

    :param pattern:
    :param source:
    :param target:
    :param timed:
    """
    while True:
        reconcile(target, source, pattern)
        print('.', end=None)
        time.sleep(timed)


def reconcile(target, source, pattern):
    """
    sync all folders

    :param target:
    :param source:
    :param pattern:
    :return:
    """
    files_checked = 0
    files_updated = 0
    if not source:
        source = target

    for t in target:
        target_path = Path(t)
        target_path.mkdir(exist_ok=True)

        if not pattern.startswith('**/'):
            pattern = f"**/{pattern}"

        for s in source:
            logger.debug(f'source:{s}')
            for p in Path(s).glob(pattern):
                files_checked += 1
                rel = p.relative_to(s)
                logger.debug(f'{p.is_file()}, {p}, {rel}')
                target_file = target_path / rel
                logger.debug(f'target_file {target_file}')
                if not target_file.parent.exists():
                    logger.info(f'mkdir: {target_file.parent}')
                    target_file.parent.mkdir(exist_ok=True)
                if should_copy(target_file, p):
                    files_updated += 1
                    logger.info(f'updating: {target_file}')
                    sync_file(target_file, p)

    logger.info(f'checked: {files_checked} updated: {files_updated}')


@click.command()
@click.option('--source', help='source folder(s), if different from --target',
              type=click.Path(dir_okay=True, file_okay=False, exists=True),
              multiple=True, default=None)
@click.option('--pattern', help='glob definition default=**/*.jsx', default='**/*.jsx')
@click.option('--target', help='target folders(s)', type=click.Path(dir_okay=True, file_okay=False, exists=True),
              multiple=True,
              required=True)
@click.option('--timed', help='number of seconds to wait between checks', type=click.INT)
def cli(target, source, pattern, timed):
    if timed:
        run_forever(pattern, source, target, timed)
    else:
        reconcile(target, source, pattern)


if __name__ == "__main__":
    cli()
