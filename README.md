# 🪟 WindowSnap - Smart Window Layout Manager

**Never manually resize windows again!** WindowSnap saves and restores your perfect window layouts with a single click.

Perfect for:
- 🖥️ Multiple monitor setups
- 💼 Different work contexts (coding, design, research)
- 🎮 Gaming vs. productivity layouts
- 🔄 Quick context switching

---

## ✨ Features

- **💾 Save Layouts** - Capture all window positions and sizes
- **🔄 Restore Layouts** - Apply saved layouts instantly
- **📋 Multiple Profiles** - Work, Gaming, Coding, etc.
- **🖱️ System Tray** - Quick access from your taskbar
- **🌍 Cross-Platform** - Windows, macOS, Linux
- **⚡ Lightning Fast** - No configuration needed
- **🎯 Smart Matching** - Finds windows even after restart

---

## 📥 Installation

### Requirements

- **Python 3.7+**
- **pip** (Python package manager)

### Step 1: Install Python Dependencies

#### Windows:
```bash
pip install pywin32 psutil PyQt5
```

#### macOS:
```bash
pip install pyobjc-framework-Quartz PyQt5
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt install wmctrl
pip install psutil PyQt5
```

### Step 2: Download WindowSnap

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/WindowSnap.git
cd WindowSnap

# Or download ZIP and extract
```

### Step 3: Run WindowSnap

#### Command Line Mode:
```bash
python windowsnap.py save work    # Save current layout
python windowsnap.py restore work # Restore layout
```

#### System Tray Mode (GUI):
```bash
python windowsnap_tray.py
```

---

## 🚀 Quick Start Guide

### Using Command Line

**1. Save your current window layout:**
```bash
python windowsnap.py save work
```

**2. Change your window positions (try different apps/positions)**

**3. Restore the saved layout:**
```bash
python windowsnap.py restore work
```

**4. List all saved layouts:**
```bash
python windowsnap.py list
```

**5. See currently open windows:**
```bash
python windowsnap.py current
```

### Using System Tray (GUI)

**1. Start the tray application:**
```bash
python windowsnap_tray.py
```

**2. Right-click the WindowSnap icon in your system tray**

**3. Use the menu to:**
   - 💾 Save Layout → Save current window positions
   - 🔄 Restore Layout → Choose a saved layout
   - 📺 Show Current Windows → See what's open
   - 🗂️ Manage Layouts → View all saved layouts

---

## 📖 Complete Usage Examples

### Example 1: Work vs. Break Layout

```bash
# Setup your perfect work layout (code editor, terminal, browser)
python windowsnap.py save work

# Setup your break layout (music, chat, web)
python windowsnap.py save break

# Switch between them anytime:
python windowsnap.py restore work
python windowsnap.py restore break
```

### Example 2: Multi-Monitor Coding Setup

```bash
# Arrange windows:
# - Monitor 1: VS Code (left), Terminal (right)
# - Monitor 2: Browser with docs (full screen)
# - Monitor 3: Slack (left), Email (right)

python windowsnap.py save coding

# Later, restore it all with one command:
python windowsnap.py restore coding
```

### Example 3: Gaming Mode

```bash
# Setup your gaming layout (game, Discord, music)
python windowsnap.py save gaming

# Back to productivity:
python windowsnap.py restore work
```

---

## 🛠️ Advanced Usage

### Automatic Layout on Startup

**Windows (Task Scheduler):**
```powershell
# Create a task that runs on login:
$action = New-ScheduledTaskAction -Execute "python" `
    -Argument "`"C:\path\to\windowsnap.py`" restore work"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "WindowSnap" -Action $action -Trigger $trigger
```

**Linux (Autostart):**
```bash
# Add to ~/.config/autostart/windowsnap.desktop
[Desktop Entry]
Type=Application
Exec=python /path/to/windowsnap.py restore work
Name=WindowSnap
```

**macOS (Launch Agent):**
```bash
# Create ~/Library/LaunchAgents/com.windowsnap.plist
# (see documentation for full plist format)
```

### Creating Desktop Shortcuts

**Windows:**
1. Right-click Desktop → New → Shortcut
2. Location: `python C:\path\to\windowsnap.py restore work`
3. Name it "Restore Work Layout"

**Linux:**
```bash
# Create ~/.local/share/applications/windowsnap-work.desktop
[Desktop Entry]
Name=Work Layout
Exec=python /path/to/windowsnap.py restore work
Type=Application
```

---

## 🎯 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `save <profile>` | Save current layout | `windowsnap.py save work` |
| `restore <profile>` | Restore saved layout | `windowsnap.py restore work` |
| `list` | List all saved layouts | `windowsnap.py list` |
| `current` | Show current windows | `windowsnap.py current` |
| `delete <profile>` | Delete a saved layout | `windowsnap.py delete old` |

**Default Profile:** If you don't specify a profile name, "default" is used.

---

## 📂 File Locations

WindowSnap stores all data in your home directory:

```
~/.windowsnap/
├── config.json          # Configuration
└── layouts/             # Saved layouts
    ├── default.json
    ├── work.json
    └── gaming.json
```

**Windows:** `C:\Users\YourName\.windowsnap\`  
**Linux/Mac:** `/home/username/.windowsnap/`

---

## ⚙️ Platform-Specific Notes

### Windows
- ✅ Full support for all features
- Uses Win32 API for window management
- No additional software needed

### macOS
- ⚠️ Window restoration requires accessibility permissions
- Basic window detection works
- Full restoration may need additional setup

### Linux
- ✅ Full support with `wmctrl` installed
- Install: `sudo apt install wmctrl`
- Works with most window managers (X11)

---

## 🐛 Troubleshooting

### "No windows found"
- **Check if apps are running:** WindowSnap can only save visible windows
- **Run as admin (Windows):** Some system windows require elevation
- **Check wmctrl (Linux):** Run `wmctrl -l` to verify it works

### "Could not restore window"
- **App must be running:** WindowSnap matches by process name
- **Window title changed:** Some apps change titles (normal, some windows may not match)
- **Permissions:** Check if you have permission to move that window

### "Layout not found"
- **Check available layouts:** Run `python windowsnap.py list`
- **Case sensitive:** Profile names are case-sensitive
- **Check file location:** Verify `~/.windowsnap/layouts/` exists

### System Tray Icon Not Showing
- **PyQt5 installed?** Run `pip install PyQt5`
- **Try running as:** `python windowsnap_tray.py`
- **Check system tray settings:** Ensure apps can show tray icons

---

## 🔒 Privacy & Security

- ✅ **All data stored locally** - No cloud, no network calls
- ✅ **No telemetry** - Zero tracking or analytics
- ✅ **Open source** - Full code transparency
- ✅ **No admin needed** - Runs with normal user permissions

WindowSnap only stores:
- Window titles
- Process names
- Window positions and sizes

**No sensitive data like window contents, passwords, or personal information is captured.**

---

## 🤝 Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🌟 Support

If you find WindowSnap useful, please:
- ⭐ Star this repository
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features via GitHub Discussions
- 📢 Share with friends who need better window management!

---

## 🎉 Example Workflow

```bash
# Morning: Start your workday
python windowsnap.py restore work
# → Opens: VS Code, 3 terminals, browser with docs, Slack

# Lunch break
python windowsnap.py restore break
# → Opens: Spotify, YouTube, casual browsing

# Afternoon: Deep focus coding
python windowsnap.py restore focus
# → Opens: Just code editor fullscreen + terminal

# Evening: Gaming time
python windowsnap.py restore gaming
# → Opens: Game, Discord, Twitch

# Before bed: Save tomorrow's layout
python windowsnap.py save tomorrow
```

---

**Created by Team Brain**  
**Part of the Holy Grail Automation Project**  

Enjoy your perfectly organized windows! 🎯
