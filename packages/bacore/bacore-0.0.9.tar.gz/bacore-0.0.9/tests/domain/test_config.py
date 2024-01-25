"""Tests for domain.config module."""
import pytest
from bacore.domain import config

pytestmark = pytest.mark.domain


class TestProjectInfo:
    """Tests for ProjectInfo entity."""

    def test_name(self):
        """Test name."""
        p = config.ProjectInfo(name="bacore")
        assert p.name == "bacore"

    def test_name_must_not_contain_spaces(self):
        """Test name_must_not_contain_spaces."""
        with pytest.raises(ValueError):
            config.ProjectInfo(name="ba core")


class TestSystemInfo:
    """Test for SystemInfo."""

    def test_os(self):
        """Test os. (Darwin is macOS.)"""
        system_info = config.SystemInfo(os="Darwin")
        assert system_info.os in ["Darwin", "Linux", "Windows"]

    def test_os_must_be_supported(self):
        """Test os_must_be_supported."""
        with pytest.raises(ValueError):
            config.SystemInfo(os="AS/400")
