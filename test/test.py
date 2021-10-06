import shutil
import unittest
from pathlib import Path

from click.testing import CliRunner

from py_sync import cli


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_folder = Path("temp")
        if self.temp_folder.is_dir():
            shutil.rmtree(self.temp_folder)
        self.temp_folder.mkdir()

    def tearDown(self) -> None:
        if self.temp_folder.is_dir():
            shutil.rmtree(self.temp_folder)

    def make_dir(self, dir_name):
        folder = Path(self.temp_folder / dir_name)
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def assertSameFile(self, sf, tf):
        self.assertEqual(Path(sf).read_text(), Path(tf).read_text())
        self.assertEqual(Path(sf).stat().st_mtime, Path(tf).stat().st_mtime)

    def test_no_args(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        self.assertEqual(result.exit_code, 2, result.output)  # add assertion here
        self.assertIn('requires --target or --syncfiles option', result.output, result.output)

    def test_sync_one_folder(self):
        runner = CliRunner()
        folder_source = Path(self.temp_folder / ".test_source")
        folder_target = Path(self.temp_folder / ".test_target")
        file_name = "temp.jsx"
        s = Path(
            folder_source
        )
        s.mkdir(parents=True, exist_ok=True)
        t = Path(
            folder_target
        )
        t.mkdir(parents=True, exist_ok=True)
        sf = Path(s / file_name)
        sf.write_text('hello')
        result = runner.invoke(cli, [f'--target', t, f'--source', s])
        self.assertEqual(result.exit_code, 0, result.output)  # add assertion here
        self.assertSameFile(sf, Path(t / file_name))

    def test_sync_one_folder_pattern(self):
        runner = CliRunner()
        folder_source = Path(self.temp_folder / ".test_source")
        folder_target = Path(self.temp_folder / ".test_target")
        file_name = "temp.txt"
        s = Path(
            folder_source
        )
        s.mkdir(parents=True, exist_ok=True)
        t = Path(
            folder_target
        )
        t.mkdir(parents=True, exist_ok=True)
        sf = Path(s / file_name)
        tf = Path(t / file_name)
        sf.write_text('hello')

        result = runner.invoke(cli, [f'--target', t, f'--source', s, '--pattern', '**/*.jsx'])
        self.assertEqual(result.exit_code, 0, result.output)  # add assertion here
        self.assertFalse(tf.is_file())

        result = runner.invoke(cli, [f'--target', t, f'--source', s, '--pattern', '**/*.txt'])
        self.assertEqual(result.exit_code, 0, result.output)  # add assertion here
        self.assertTrue(tf.is_file())

    def test_sync_only_target_folder(self):
        runner = CliRunner()
        folder_target_1 = Path(self.temp_folder / ".test_target_1")
        folder_target_2 = Path(self.temp_folder / ".test_target_2")
        file_name_1 = "temp_1.jsx"
        file_name_2 = "temp_2.jsx"
        t1 = Path(
            folder_target_1
        )
        t1.mkdir(parents=True, exist_ok=True)
        t2 = Path(
            folder_target_2
        )
        t2.mkdir(parents=True, exist_ok=True)
        sf_1 = Path(t1 / file_name_1)
        sf_2 = Path(t2 / file_name_2)
        sf_1.write_text('hello_1')
        sf_2.write_text('hello_2')

        result = runner.invoke(cli, [f'--target', t2, f'--target', t1])

        self.assertEqual(result.exit_code, 0, result)  # add assertion here
        self.assertSameFile(sf_1, Path(t2 / file_name_1))
        self.assertSameFile(sf_2, Path(t1 / file_name_2))

    def test_syncfiles(self):
        runner = CliRunner()
        t1 = self.make_dir(".test_target_1")
        t2 = self.make_dir(".test_target_2")
        t3 = self.make_dir(".test_target_3")
        file_name_1 = "temp_1.jsx"

        sf_1 = Path(t1 / file_name_1)
        sf_2 = Path(t2 / file_name_1)
        sf_3 = Path(t3 / file_name_1)
        sf_1.write_text('hello_1')

        result = runner.invoke(cli, [f'--syncfiles', f'{sf_1},{sf_2},{sf_3}'])

        self.assertEqual(result.exit_code, 0, result.output)  # add assertion here
        self.assertSameFile(sf_1, Path(t2 / file_name_1))
        self.assertSameFile(sf_1, Path(t2 / file_name_1))
        self.assertSameFile(sf_1, Path(t3 / file_name_1))

        # sync_file should create the folder
        shutil.rmtree(t2)
        self.assertFalse(t2.is_dir())

        file_name_3 = "temp_3.jsx"

        sf_1 = Path(t1 / file_name_3)
        sf_2 = Path(t2 / file_name_3)
        sf_3 = Path(t3 / file_name_3)
        sf_3.write_text('hello_2')

        result = runner.invoke(cli, [f'--syncfiles', f'{sf_1},{sf_2},{sf_3}'])

        self.assertEqual(result.exit_code, 0, result.output)  # add assertion here
        self.assertSameFile(sf_1, Path(t2 / file_name_3))
        self.assertSameFile(sf_1, Path(t2 / file_name_3))
        self.assertSameFile(sf_1, Path(t3 / file_name_3))

    def test_target_folder_and_sync(self):
        runner = CliRunner()
        t1 = self.make_dir("test_target_1")
        t2 = self.make_dir(".test_target_2")
        file_name_1 = "temp_1.jsx"
        file_name_2 = "temp_2.jsx"

        tf_1 = Path(t1 / file_name_1)
        tf_2 = Path(t2 / file_name_2)
        tf_1.write_text('hello_1')
        tf_2.write_text('hello_2')

        s1 = self.make_dir(".test_syncfiles_1")
        s2 = self.make_dir(".test_syncfiles_2")
        s3 = self.make_dir(".test_syncfiles_3")
        sf_name_1 = "flong.pootle"

        sf_1 = Path(s1 / sf_name_1)
        sf_2 = Path(s2 / sf_name_1)
        sf_3 = Path(s3 / sf_name_1)
        sf_1.write_text('hello_1')

        result = runner.invoke(cli, [f'--target', t2, f'--target', t1, f'--syncfiles', f'{sf_1},{sf_2},{sf_3}'])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertSameFile(sf_1, Path(s2 / sf_name_1))
        self.assertSameFile(sf_1, Path(s2 / sf_name_1))
        self.assertSameFile(sf_1, Path(s3 / sf_name_1))

        self.assertSameFile(tf_1, Path(t2 / file_name_1))
        self.assertSameFile(tf_2, Path(t1 / file_name_2))

        if __name__ == '__main__':
            unittest.main()
