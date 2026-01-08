#!/usr/bin/env python3
"""
WindowSnap System Tray Application
===================================
Provides a system tray icon with quick access to WindowSnap features.

Author: Team Brain / Forge
License: MIT
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PyQt5.QtWidgets import (
        QApplication,
        QSystemTrayIcon,
        QMenu,
        QAction,
        QInputDialog,
        QMessageBox,
    )
    from PyQt5.QtGui import QIcon
    from PyQt5.QtCore import Qt
except ImportError:
    print("Error: PyQt5 not installed!")
    print("Install with: pip install PyQt5")
    sys.exit(1)

from windowsnap import WindowSnap


class WindowSnapTray:
    """System tray application for WindowSnap."""

    def __init__(self):
        """Initialize the system tray application."""
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        self.snap = WindowSnap()
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setToolTip("WindowSnap - Window Layout Manager")
        
        # Create a simple icon (text-based for portability)
        # In production, you'd use a proper icon file
        self.tray_icon.setIcon(self.app.style().standardIcon(
            self.app.style().SP_ComputerIcon
        ))
        
        # Create context menu
        self.create_menu()
        
        # Show the tray icon
        self.tray_icon.show()
        
        # Show startup message
        self.tray_icon.showMessage(
            "WindowSnap",
            "Window layout manager is running!\nRight-click for options.",
            QSystemTrayIcon.Information,
            3000
        )

    def create_menu(self):
        """Create the context menu for the tray icon."""
        menu = QMenu()
        
        # Save layout submenu
        save_menu = QMenu("💾 Save Layout", menu)
        
        save_default_action = QAction("Save as 'default'", save_menu)
        save_default_action.triggered.connect(lambda: self.save_layout("default"))
        save_menu.addAction(save_default_action)
        
        save_custom_action = QAction("Save as... (custom name)", save_menu)
        save_custom_action.triggered.connect(self.save_layout_custom)
        save_menu.addAction(save_custom_action)
        
        menu.addMenu(save_menu)
        
        # Restore layout submenu
        restore_menu = QMenu("🔄 Restore Layout", menu)
        self.populate_restore_menu(restore_menu)
        menu.addMenu(restore_menu)
        
        menu.addSeparator()
        
        # Current windows
        current_action = QAction("📺 Show Current Windows", menu)
        current_action.triggered.connect(self.show_current_windows)
        menu.addAction(current_action)
        
        # Manage layouts
        manage_action = QAction("🗂️ Manage Layouts", menu)
        manage_action.triggered.connect(self.manage_layouts)
        menu.addAction(manage_action)
        
        menu.addSeparator()
        
        # About
        about_action = QAction("ℹ️ About WindowSnap", menu)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        # Quit
        quit_action = QAction("❌ Quit", menu)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)

    def populate_restore_menu(self, menu):
        """Populate the restore menu with available layouts."""
        menu.clear()
        
        layouts = self.snap.list_layouts()
        
        if layouts:
            for layout in layouts:
                action = QAction(f"Restore '{layout}'", menu)
                action.triggered.connect(lambda checked, l=layout: self.restore_layout(l))
                menu.addAction(action)
        else:
            no_layouts_action = QAction("(No saved layouts)", menu)
            no_layouts_action.setEnabled(False)
            menu.addAction(no_layouts_action)

    def save_layout(self, profile_name):
        """Save current window layout."""
        success = self.snap.save_layout(profile_name)
        
        if success:
            self.tray_icon.showMessage(
                "Layout Saved",
                f"Successfully saved layout '{profile_name}'",
                QSystemTrayIcon.Information,
                2000
            )
            # Refresh the menu
            self.create_menu()
        else:
            QMessageBox.warning(
                None,
                "Save Failed",
                f"Could not save layout '{profile_name}'"
            )

    def save_layout_custom(self):
        """Save layout with custom name."""
        name, ok = QInputDialog.getText(
            None,
            "Save Layout",
            "Enter layout name:",
            text="work"
        )
        
        if ok and name:
            self.save_layout(name)

    def restore_layout(self, profile_name):
        """Restore a window layout."""
        success = self.snap.restore_layout(profile_name)
        
        if success:
            self.tray_icon.showMessage(
                "Layout Restored",
                f"Successfully restored layout '{profile_name}'",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            QMessageBox.warning(
                None,
                "Restore Failed",
                f"Could not restore layout '{profile_name}'"
            )

    def show_current_windows(self):
        """Show information about current windows."""
        windows = self.snap.get_all_windows()
        
        if windows:
            message = f"Currently open windows ({len(windows)}):\n\n"
            for i, window in enumerate(windows[:10], 1):  # Show first 10
                message += f"{i}. {window['process']}: {window['title'][:40]}...\n"
            
            if len(windows) > 10:
                message += f"\n... and {len(windows) - 10} more windows"
            
            QMessageBox.information(
                None,
                "Current Windows",
                message
            )
        else:
            QMessageBox.information(
                None,
                "Current Windows",
                "No windows found."
            )

    def manage_layouts(self):
        """Show layout management dialog."""
        layouts = self.snap.list_layouts()
        
        if not layouts:
            QMessageBox.information(
                None,
                "Manage Layouts",
                "No saved layouts yet.\n\nCreate one with 'Save Layout'."
            )
            return
        
        message = f"Saved layouts ({len(layouts)}):\n\n"
        for layout in layouts:
            layout_file = self.snap.layouts_dir / f"{layout}.json"
            import json
            with open(layout_file) as f:
                data = json.load(f)
                count = data.get('window_count', 0)
                timestamp = data.get('timestamp', 'Unknown')[:19]
                message += f"• {layout} ({count} windows)\n  Saved: {timestamp}\n\n"
        
        QMessageBox.information(
            None,
            "Manage Layouts",
            message
        )

    def show_about(self):
        """Show about dialog."""
        about_text = """
<h2>WindowSnap</h2>
<p><b>Smart Window Layout Manager</b></p>
<p>Save and restore window positions with ease!</p>
<br>
<p><b>Features:</b></p>
<ul>
<li>Save unlimited window layouts</li>
<li>Restore layouts with one click</li>
<li>Works across reboots</li>
<li>Cross-platform support</li>
</ul>
<br>
<p><b>Usage:</b></p>
<ul>
<li>Right-click tray icon for options</li>
<li>Save Layout: Capture current windows</li>
<li>Restore Layout: Apply saved layout</li>
</ul>
<br>
<p>Created by Team Brain<br>
License: MIT</p>
        """
        
        msg = QMessageBox()
        msg.setWindowTitle("About WindowSnap")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        msg.setIconPixmap(self.app.style().standardIcon(
            self.app.style().SP_ComputerIcon
        ).pixmap(64, 64))
        msg.exec_()

    def quit_app(self):
        """Quit the application."""
        self.tray_icon.hide()
        QApplication.quit()

    def run(self):
        """Run the application."""
        return self.app.exec_()


def main():
    """Main entry point."""
    tray_app = WindowSnapTray()
    sys.exit(tray_app.run())


if __name__ == "__main__":
    main()
