# 🪟 WindowSnap - Usage Examples

12 comprehensive examples for WindowSnap window layout manager.

## Example 1: Basic Usage
```bash
python windowsnap.py save work
python windowsnap.py restore work
```

## Example 2: Work vs Break
```bash
python windowsnap.py save work
python windowsnap.py save break
python windowsnap.py restore work  # Back to work
```

## Example 3: Multi-Monitor Setup
```bash
# Arrange windows across monitors, then save
python windowsnap.py save coding3mon
# Later restore
python windowsnap.py restore coding3mon
```

## Example 4: Gaming Layout
```bash
python windowsnap.py save gaming
python windowsnap.py restore work  # Back to productivity
```

## Example 5: List and Manage
```bash
python windowsnap.py list
python windowsnap.py delete old_layout
```

## Example 6: View Current Windows
```bash
python windowsnap.py current
```

## Example 7: System Tray Mode
```bash
python windowsnap_tray.py  # GUI in system tray
```

## Example 8: Startup Automation
```powershell
# Windows Task Scheduler
$action = New-ScheduledTaskAction -Execute "python" -Argument "windowsnap.py restore work"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "WindowSnap" -Action $action -Trigger $trigger
```

## Example 9: Team Brain Integration
```python
from windowsnap import WindowSnap
from synapselink import quick_send
snap = WindowSnap()
snap.restore_layout("focus")
quick_send("TEAM", "Context Switch", "Entering focus mode")
```

## Example 10: Error Recovery
```bash
python windowsnap.py restore nonexistent  # Shows available layouts
```

## Example 11: Multiple Dev Profiles
```bash
python windowsnap.py save dev-code
python windowsnap.py save dev-test
python windowsnap.py save dev-debug
```

## Example 12: Python API
```python
from windowsnap import WindowSnap
snap = WindowSnap()
windows = snap.get_all_windows()
snap.save_layout("my_layout")
snap.restore_layout("my_layout")
layouts = snap.list_layouts()
snap.delete_layout("old_layout")
```

---
**Built by:** ATLAS (Team Brain)
