#!/usr/bin/env python3
"""
WindowSnap - Comprehensive Test Suite
======================================
Tests for the WindowSnap window layout manager.

Run with: python test_windowsnap.py

Author: ATLAS (Team Brain)
For: Logan Smith / Metaphy LLC
Date: January 31, 2026
"""

import unittest
import tempfile
import shutil
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))
from windowsnap import WindowSnap


class TestWindowSnapInitialization(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization_creates_directories(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            config_dir = Path(self.temp_dir) / ".windowsnap"
            layouts_dir = config_dir / "layouts"
            self.assertTrue(config_dir.exists())
            self.assertTrue(layouts_dir.exists())

    def test_initialization_creates_default_config(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            config_file = Path(self.temp_dir) / ".windowsnap" / "config.json"
            self.assertTrue(config_file.exists())
            with open(config_file) as f:
                config = json.load(f)
            self.assertEqual(config.get('default_profile'), 'default')

    def test_config_is_loaded(self):
        config_dir = Path(self.temp_dir) / ".windowsnap"
        config_dir.mkdir(parents=True)
        (config_dir / "layouts").mkdir()
        test_config = {"default_profile": "work", "custom_setting": "value"}
        with open(config_dir / "config.json", "w") as f:
            json.dump(test_config, f)
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            self.assertEqual(snap.config.get('default_profile'), 'work')
            self.assertEqual(snap.config.get('custom_setting'), 'value')


class TestLayoutManagement(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".windowsnap"
        self.layouts_dir = self.config_dir / "layouts"
        self.layouts_dir.mkdir(parents=True)
        with open(self.config_dir / "config.json", "w") as f:
            json.dump({"default_profile": "default"}, f)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_layout_creates_file(self):
        mock_windows = [{"title": "Test", "process": "python.exe", "x": 100, "y": 100, "width": 800, "height": 600}]
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            with patch.object(snap, 'get_all_windows', return_value=mock_windows):
                result = snap.save_layout("test_profile")
                self.assertTrue(result)
                self.assertTrue((self.layouts_dir / "test_profile.json").exists())

    def test_save_layout_no_windows(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            with patch.object(snap, 'get_all_windows', return_value=[]):
                result = snap.save_layout("empty_profile")
                self.assertFalse(result)

    def test_list_layouts(self):
        for name in ['work', 'gaming', 'coding']:
            with open(self.layouts_dir / f"{name}.json", "w") as f:
                json.dump({"profile_name": name, "windows": []}, f)
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            layouts = snap.list_layouts()
            self.assertEqual(len(layouts), 3)
            self.assertIn('work', layouts)

    def test_list_layouts_empty(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            layouts = snap.list_layouts()
            self.assertEqual(layouts, [])

    def test_delete_layout(self):
        layout_file = self.layouts_dir / "to_delete.json"
        with open(layout_file, "w") as f:
            json.dump({"profile_name": "to_delete", "windows": []}, f)
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            self.assertTrue(layout_file.exists())
            result = snap.delete_layout("to_delete")
            self.assertTrue(result)
            self.assertFalse(layout_file.exists())

    def test_delete_nonexistent_layout(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            result = snap.delete_layout("nonexistent")
            self.assertFalse(result)


class TestRestoreLayout(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".windowsnap"
        self.layouts_dir = self.config_dir / "layouts"
        self.layouts_dir.mkdir(parents=True)
        with open(self.config_dir / "config.json", "w") as f:
            json.dump({"default_profile": "default"}, f)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_restore_nonexistent_layout(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            result = snap.restore_layout("nonexistent")
            self.assertFalse(result)


class TestWindowDetection(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".windowsnap"
        self.layouts_dir = self.config_dir / "layouts"
        self.layouts_dir.mkdir(parents=True)
        with open(self.config_dir / "config.json", "w") as f:
            json.dump({"default_profile": "default"}, f)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_all_windows_windows(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            mock_windows = [{"title": "Test", "process": "test.exe", "x": 0, "y": 0, "width": 100, "height": 100}]
            with patch('windowsnap.platform.system', return_value='Windows'):
                with patch.object(snap, 'get_windows_windows', return_value=mock_windows):
                    result = snap.get_all_windows()
                    self.assertEqual(result, mock_windows)

    def test_get_all_windows_unsupported(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            with patch('windowsnap.platform.system', return_value='UnknownOS'):
                result = snap.get_all_windows()
                self.assertEqual(result, [])


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".windowsnap"
        self.layouts_dir = self.config_dir / "layouts"
        self.layouts_dir.mkdir(parents=True)
        with open(self.config_dir / "config.json", "w") as f:
            json.dump({"default_profile": "default"}, f)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_multiple_windows_same_process(self):
        mock_windows = [
            {"title": "Doc 1", "process": "notepad.exe", "x": 0, "y": 0, "width": 400, "height": 300},
            {"title": "Doc 2", "process": "notepad.exe", "x": 400, "y": 0, "width": 400, "height": 300},
        ]
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            with patch.object(snap, 'get_all_windows', return_value=mock_windows):
                result = snap.save_layout("multi")
                self.assertTrue(result)
                with open(self.layouts_dir / "multi.json") as f:
                    layout = json.load(f)
                self.assertEqual(layout['window_count'], 2)

    def test_negative_coordinates(self):
        mock_windows = [{"title": "Left", "process": "app.exe", "x": -1920, "y": 0, "width": 800, "height": 600}]
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            with patch.object(snap, 'get_all_windows', return_value=mock_windows):
                result = snap.save_layout("multi_mon")
                self.assertTrue(result)
                with open(self.layouts_dir / "multi_mon.json") as f:
                    layout = json.load(f)
                self.assertEqual(layout['windows'][0]['x'], -1920)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".windowsnap"
        self.layouts_dir = self.config_dir / "layouts"
        self.layouts_dir.mkdir(parents=True)
        with open(self.config_dir / "config.json", "w") as f:
            json.dump({"default_profile": "default"}, f)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_list_delete_workflow(self):
        with patch.object(Path, 'home', return_value=Path(self.temp_dir)):
            snap = WindowSnap()
            mock_windows = [{"title": "Win", "process": "app.exe", "x": 0, "y": 0, "width": 800, "height": 600}]
            with patch.object(snap, 'get_all_windows', return_value=mock_windows):
                result = snap.save_layout("test")
                self.assertTrue(result)
                layouts = snap.list_layouts()
                self.assertIn("test", layouts)
                result = snap.delete_layout("test")
                self.assertTrue(result)
                layouts = snap.list_layouts()
                self.assertNotIn("test", layouts)


def run_tests():
    print("=" * 70)
    print("WINDOWSNAP - Test Suite")
    print("=" * 70)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in [TestWindowSnapInitialization, TestLayoutManagement, TestRestoreLayout, 
                TestWindowDetection, TestEdgeCases, TestIntegration]:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}, Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print("[OK] All tests passed!" if result.wasSuccessful() else "[X] Some tests failed!")
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_tests())
