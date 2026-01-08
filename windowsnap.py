#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WindowSnap - Smart Window Layout Manager
=========================================
Save and restore window positions and sizes with keyboard shortcuts.
Perfect for managing multiple monitor setups and different work contexts.

Author: Team Brain / Forge
License: MIT
"""

import os
import json
import sys
import platform
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding issues
if platform.system() == "Windows":
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
    except:
        pass  # If it fails, continue anyway

# Platform-specific imports
if platform.system() == "Windows":
    import win32gui
    import win32con
    import win32process
    import psutil
elif platform.system() == "Darwin":  # macOS
    try:
        from AppKit import NSWorkspace, NSScreen
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID,
        )
    except ImportError:
        print("macOS: Please install pyobjc: pip install pyobjc-framework-Quartz")
        sys.exit(1)
elif platform.system() == "Linux":
    import subprocess


class WindowSnap:
    """Main WindowSnap application class."""

    def __init__(self):
        """Initialize WindowSnap with config directory."""
        self.config_dir = Path.home() / ".windowsnap"
        self.config_dir.mkdir(exist_ok=True)
        self.layouts_dir = self.config_dir / "layouts"
        self.layouts_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.load_config()

    def load_config(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
                self.config = {"default_profile": "default"}
        else:
            self.config = {"default_profile": "default"}
            self.save_config()

    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_windows_windows(self):
        """Get all windows on Windows OS."""
        windows = []

        def callback(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return
            if not win32gui.GetWindowText(hwnd):
                return

            # Get window rectangle
            try:
                rect = win32gui.GetWindowRect(hwnd)
                x, y, right, bottom = rect
                width = right - x
                height = bottom - y

                # Get process name
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                except:
                    process_name = "Unknown"

                window_data = {
                    "title": win32gui.GetWindowText(hwnd),
                    "process": process_name,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "hwnd": hwnd,
                }
                windows.append(window_data)
            except Exception as e:
                pass  # Skip windows that cause errors

        win32gui.EnumWindows(callback, None)
        return windows

    def get_macos_windows(self):
        """Get all windows on macOS."""
        windows = []
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID
        )

        for window in window_list:
            title = window.get("kCGWindowName", "")
            owner = window.get("kCGWindowOwnerName", "")
            bounds = window.get("kCGWindowBounds", {})

            if title and bounds:
                windows.append(
                    {
                        "title": title,
                        "process": owner,
                        "x": int(bounds.get("X", 0)),
                        "y": int(bounds.get("Y", 0)),
                        "width": int(bounds.get("Width", 0)),
                        "height": int(bounds.get("Height", 0)),
                    }
                )

        return windows

    def get_linux_windows(self):
        """Get all windows on Linux (using wmctrl)."""
        try:
            output = subprocess.check_output(
                ["wmctrl", "-lGp"], universal_newlines=True
            )
            windows = []

            for line in output.strip().split("\n"):
                parts = line.split(None, 9)
                if len(parts) >= 10:
                    window_id, desktop, pid, x, y, w, h, host, title = (
                        parts[0],
                        parts[1],
                        parts[2],
                        parts[3],
                        parts[4],
                        parts[5],
                        parts[6],
                        parts[7],
                        parts[9],
                    )

                    # Get process name
                    try:
                        process = psutil.Process(int(pid))
                        process_name = process.name()
                    except:
                        process_name = "Unknown"

                    windows.append(
                        {
                            "title": title,
                            "process": process_name,
                            "x": int(x),
                            "y": int(y),
                            "width": int(w),
                            "height": int(h),
                            "window_id": window_id,
                        }
                    )

            return windows
        except FileNotFoundError:
            print("Error: wmctrl not found. Install with: sudo apt install wmctrl")
            return []
        except Exception as e:
            print(f"Error getting Linux windows: {e}")
            return []

    def get_all_windows(self):
        """Get all windows for the current platform."""
        system = platform.system()

        if system == "Windows":
            return self.get_windows_windows()
        elif system == "Darwin":
            return self.get_macos_windows()
        elif system == "Linux":
            return self.get_linux_windows()
        else:
            print(f"Unsupported platform: {system}")
            return []

    def save_layout(self, profile_name="default"):
        """Save current window layout to a profile."""
        windows = self.get_all_windows()

        if not windows:
            print("[X] No windows found to save!")
            return False

        # Remove platform-specific IDs (hwnd, window_id) for portability
        for window in windows:
            window.pop("hwnd", None)
            window.pop("window_id", None)

        layout = {
            "profile_name": profile_name,
            "timestamp": datetime.now().isoformat(),
            "platform": platform.system(),
            "window_count": len(windows),
            "windows": windows,
        }

        layout_file = self.layouts_dir / f"{profile_name}.json"

        try:
            with open(layout_file, "w") as f:
                json.dump(layout, f, indent=2)

            print(f"[OK] Saved layout '{profile_name}' with {len(windows)} windows")
            self.list_windows_in_layout(windows)
            return True
        except Exception as e:
            print(f"[X] Error saving layout: {e}")
            return False

    def restore_layout_windows(self, windows):
        """Restore window layout on Windows OS."""
        restored = 0
        failed = 0

        # Get current windows
        current_windows = self.get_windows_windows()

        for saved_window in windows:
            # Try to find matching window by process and title
            matched = False

            for current_window in current_windows:
                # Match by process name and similar title
                if (
                    saved_window["process"] == current_window["process"]
                    and saved_window["title"] in current_window["title"]
                ):
                    # Restore window position
                    try:
                        hwnd = current_window["hwnd"]
                        win32gui.SetWindowPos(
                            hwnd,
                            win32con.HWND_TOP,
                            saved_window["x"],
                            saved_window["y"],
                            saved_window["width"],
                            saved_window["height"],
                            win32con.SWP_SHOWWINDOW,
                        )
                        restored += 1
                        matched = True
                        break
                    except Exception as e:
                        print(f"Warning: Could not restore {saved_window['title']}: {e}")
                        failed += 1
                        matched = True
                        break

            if not matched:
                failed += 1

        return restored, failed

    def restore_layout_linux(self, windows):
        """Restore window layout on Linux (using wmctrl)."""
        restored = 0
        failed = 0

        current_windows = self.get_linux_windows()

        for saved_window in windows:
            matched = False

            for current_window in current_windows:
                if (
                    saved_window["process"] == current_window["process"]
                    and saved_window["title"] in current_window["title"]
                ):
                    try:
                        window_id = current_window["window_id"]
                        # Move and resize window
                        subprocess.run(
                            [
                                "wmctrl",
                                "-i",
                                "-r",
                                window_id,
                                "-e",
                                f"0,{saved_window['x']},{saved_window['y']},"
                                f"{saved_window['width']},{saved_window['height']}",
                            ],
                            check=True,
                        )
                        restored += 1
                        matched = True
                        break
                    except Exception as e:
                        print(f"Warning: Could not restore {saved_window['title']}: {e}")
                        failed += 1
                        matched = True
                        break

            if not matched:
                failed += 1

        return restored, failed

    def restore_layout(self, profile_name="default"):
        """Restore window layout from a profile."""
        layout_file = self.layouts_dir / f"{profile_name}.json"

        if not layout_file.exists():
            print(f"[X] Layout '{profile_name}' not found!")
            print(f"Available layouts: {self.list_layouts()}")
            return False

        try:
            with open(layout_file, "r") as f:
                layout = json.load(f)

            windows = layout["windows"]
            print(f"Restoring layout '{profile_name}' ({len(windows)} windows)...")

            system = platform.system()

            if system == "Windows":
                restored, failed = self.restore_layout_windows(windows)
            elif system == "Linux":
                restored, failed = self.restore_layout_linux(windows)
            elif system == "Darwin":
                print("[!] macOS window restoration requires additional permissions.")
                print("Use AppleScript or Accessibility API (not implemented in basic version)")
                return False
            else:
                print(f"[X] Unsupported platform: {system}")
                return False

            print(f"[OK] Restored {restored} windows, {failed} not found/failed")
            return True

        except Exception as e:
            print(f"[X] Error restoring layout: {e}")
            return False

    def list_layouts(self):
        """List all saved layouts."""
        layouts = list(self.layouts_dir.glob("*.json"))
        return [layout.stem for layout in layouts]

    def list_windows_in_layout(self, windows):
        """Print a nice list of windows."""
        print("\nWindows in this layout:")
        for i, window in enumerate(windows, 1):
            # Safely handle unicode characters in titles
            title = window['title'][:50]
            process = window['process']
            try:
                print(f"  {i}. {process}: {title}")
            except UnicodeEncodeError:
                # Fallback: encode as ASCII with replace
                title_safe = title.encode('ascii', 'replace').decode('ascii')
                process_safe = process.encode('ascii', 'replace').decode('ascii')
                print(f"  {i}. {process_safe}: {title_safe}")
            print(f"     Position: ({window['x']}, {window['y']}) "
                  f"Size: {window['width']}x{window['height']}")

    def delete_layout(self, profile_name):
        """Delete a saved layout."""
        layout_file = self.layouts_dir / f"{profile_name}.json"

        if layout_file.exists():
            layout_file.unlink()
            print(f"[OK] Deleted layout '{profile_name}'")
            return True
        else:
            print(f"[X] Layout '{profile_name}' not found!")
            return False


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="WindowSnap - Smart Window Layout Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  windowsnap save work          # Save current layout as 'work'
  windowsnap restore work       # Restore 'work' layout
  windowsnap list               # List all saved layouts
  windowsnap delete old_layout  # Delete a layout
        """,
    )

    parser.add_argument(
        "action",
        choices=["save", "restore", "list", "delete", "current"],
        help="Action to perform",
    )
    parser.add_argument(
        "profile", nargs="?", default="default", help="Profile name (default: 'default')"
    )

    args = parser.parse_args()

    snap = WindowSnap()

    if args.action == "save":
        snap.save_layout(args.profile)

    elif args.action == "restore":
        snap.restore_layout(args.profile)

    elif args.action == "list":
        layouts = snap.list_layouts()
        if layouts:
            print(f"Saved layouts ({len(layouts)}):")
            for layout in layouts:
                layout_file = snap.layouts_dir / f"{layout}.json"
                with open(layout_file) as f:
                    data = json.load(f)
                    timestamp = data.get("timestamp", "Unknown")
                    count = data.get("window_count", 0)
                    print(f"  * {layout} ({count} windows, saved: {timestamp[:10]})")
        else:
            print("No saved layouts found. Create one with: windowsnap save <name>")

    elif args.action == "delete":
        snap.delete_layout(args.profile)

    elif args.action == "current":
        windows = snap.get_all_windows()
        if windows:
            print(f"Currently open windows ({len(windows)}):")
            snap.list_windows_in_layout(windows)
        else:
            print("No windows found.")


if __name__ == "__main__":
    main()
