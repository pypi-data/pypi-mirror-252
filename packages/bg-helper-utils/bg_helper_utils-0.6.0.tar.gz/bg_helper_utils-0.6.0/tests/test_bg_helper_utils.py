#!/usr/bin/env python

"""Tests for `bg_helper_utils` package."""


import unittest
from click.testing import CliRunner

from bg_helper_utils import bg_helper_utils
from bg_helper_utils import cli


class TestBg_helper_utils(unittest.TestCase):
    """Tests for `bg_helper_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'bg_helper_utils.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
