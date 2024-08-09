import unittest
from unittest.mock import patch
from pathlib import Path

from aider.main import get_git_root, resolve_config_path

class TestMain(unittest.TestCase):

    @patch('git.Repo')
    def test_get_git_root(self, mock_repo):
        # Test when git repo is found
        mock_repo.return_value.working_tree_dir = '/path/to/repo'
        result = get_git_root('/path/to/start')
        self.assertEqual(result, '/path/to/repo')

        # Test when no git repo is found
        mock_repo.side_effect = git.InvalidGitRepositoryError
        result = get_git_root('/path/to/start')
        self.assertIsNone(result)

    @patch('pathlib.Path.exists')
    def test_resolve_config_path(self, mock_exists):
        # Test when git_root is None
        result = resolve_config_path('.aider.conf.yml', None)
        self.assertEqual(result, str(Path('.aider.conf.yml').resolve()))

        # Test when git_root exists but config file doesn't exist in git root
        mock_exists.return_value = False
        result = resolve_config_path('.aider.conf.yml', '/path/to/git/root')
        self.assertEqual(result, str(Path('.aider.conf.yml').resolve()))

        # Test when git_root exists and config file exists in git root
        mock_exists.return_value = True
        result = resolve_config_path('.aider.conf.yml', '/path/to/git/root')
        self.assertEqual(result, str(Path('/path/to/git/root/.aider.conf.yml')))
