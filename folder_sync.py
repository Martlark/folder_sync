import logging
from pathlib import Path

import click

logger = logging.getLogger('folder_sync')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def should_copy(target_file, source_file):
    if not source_file.is_file():
        return False

    if not target_file.exists():
        return True
    if target_file.stat().st_mtime < source_file.stat().st_mtime:
        return True

    return False


@click.command()
@click.option('--source', help='source folder(s)', type=click.Path(dir_okay=True, file_okay=False, exists=True),
              multiple=True, required=True)
@click.option('--extension', help='glob definition default=**/*.jsx', default='**/*.jsx')
@click.option('--target', help='target folders(s)', type=click.Path(dir_okay=True, file_okay=False), multiple=True,
              required=True)
def reconcile(target, source, extension):
    files_checked = 0
    files_updated = 0
    for t in target:
        target_path = Path(t)
        target_path.mkdir(exist_ok=True)

        if not extension.startswith('**/'):
            extension = f"**/{extension}"

        for s in source:
            logger.debug('source', s)
            for p in Path(s).glob(extension):
                files_checked += 1
                rel = p.relative_to(s)
                logger.debug(p.is_file(), p, rel)
                target_file = target_path / rel
                logger.debug('target_file', target_file)
                logger.debug(f'mkdir: {target_file.parent}')
                target_file.parent.mkdir(exist_ok=True)
                if should_copy(target_file, p):
                    files_updated += 1
                    logger.info(f'updating: {target_file}')
                    target_file.write_text(p.read_text())

    logger.info(f'checked: {files_checked} updated: {files_updated}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reconcile()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
