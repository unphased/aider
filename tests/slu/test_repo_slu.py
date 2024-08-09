import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from aider.io import InputOutput
from aider.repo import GitRepo

class TestGitRepoSLU(unittest.TestCase):

    def setUp(self):
        self.mock_io = InputOutput()
        self.git_repo = GitRepo(self.mock_io, [], None)
        self.git_repo.repo = Mock()
        self.git_repo.root = '/path/to/repo'

    def test_normalize_path(self):
        self.git_repo.normalized_path = {}
        result = self.git_repo.normalize_path('/path/to/repo/file.txt')
        self.assertEqual(result, 'file.txt')

        # Test caching
        self.assertEqual(self.git_repo.normalize_path('/path/to/repo/file.txt'), 'file.txt')

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_relative_to')
    def test_path_in_repo(self, mock_is_relative_to, mock_resolve):
        mock_resolve.return_value = Path('/path/to/repo/file.txt')
        mock_is_relative_to.return_value = True
        self.assertTrue(self.git_repo.path_in_repo('file.txt'))

        mock_is_relative_to.return_value = False
        self.assertFalse(self.git_repo.path_in_repo('outside_file.txt'))

