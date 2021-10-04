import logging
import os
from pathlib import Path
from shutil import copy2

import click

logger = logging.getLogger('folder_sync')
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
logger.addHandler(logging.StreamHandler())


def should_copy(target_file, source_file):
    if not source_file.is_file():
        return False

    if not target_file.exists():
        return True
    if target_file.stat().st_mtime < source_file.stat().st_mtime:
        return True

    return False


def sync_file(target_file, source_file):
    copy2(source_file, target_file)


@click.command()
@click.option('--source', help='source folder(s), if different from --target', type=click.Path(dir_okay=True, file_okay=False, exists=True),
              multiple=True, default=None)
@click.option('--pattern', help='glob definition default=**/*.jsx', default='**/*.jsx')
@click.option('--target', help='target folders(s)', type=click.Path(dir_okay=True, file_okay=False, exists=True), multiple=True,
              required=True)
def reconcile(target, source, pattern):
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
            logger.debug('source', s)
            for p in Path(s).glob(pattern):
                files_checked += 1
                rel = p.relative_to(s)
                logger.debug(p.is_file(), p, rel)
                target_file = target_path / rel
                logger.debug('target_file', target_file)
                if not target_file.parent.exists():
                    logger.info(f'mkdir: {target_file.parent}')
                    target_file.parent.mkdir(exist_ok=True)
                if should_copy(target_file, p):
                    files_updated += 1
                    logger.info(f'updating: {target_file}')
                    sync_file(target_file, p)

    logger.info(f'checked: {files_checked} updated: {files_updated}')

if __name__ == "__main__":
    reconcile()