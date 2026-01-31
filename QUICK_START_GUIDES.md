# 🪟 WindowSnap - Quick Start Guides

5-minute guides for each Team Brain agent.

---

## 🔥 Forge Quick Start (5 min)

```bash
# 1. Verify installation
python windowsnap.py --help

# 2. Save orchestration layout
python windowsnap.py save forge_orchestrate

# 3. Restore when needed
python windowsnap.py restore forge_orchestrate
```

**Recommended Layouts:** forge_orchestrate, forge_review, forge_planning

---

## ⚡ Atlas Quick Start (5 min)

```bash
# 1. Verify installation
python -c "from windowsnap import WindowSnap; print('[OK]')"

# 2. Save dev layout
python windowsnap.py save atlas_dev

# 3. Restore at session start
python windowsnap.py restore atlas_dev
```

**Recommended Layouts:** atlas_dev, atlas_test, atlas_docs

---

## 🐧 Clio Quick Start (5 min)

```bash
# 1. Install wmctrl
sudo apt install wmctrl

# 2. Verify
wmctrl -l

# 3. Save layout
python3 windowsnap.py save clio_dev

# 4. Restore
python3 windowsnap.py restore clio_dev
```

**Recommended Layouts:** clio_dev, clio_deploy, clio_bch

---

## 🌐 Nexus Quick Start (5 min)

```python
import platform
from windowsnap import WindowSnap
snap = WindowSnap()
print(f"Platform: {platform.system()}")
snap.restore_layout("nexus_dev")
```

**Recommended:** Create platform-specific layouts (nexus_dev_windows, etc.)

---

## 🆓 Bolt Quick Start (5 min)

```bash
# Non-interactive restore for scripts
python windowsnap.py restore bolt_standard

# Batch operations
for layout in work testing docs; do
    python windowsnap.py restore $layout
done
```

**Cost:** Zero API calls - 100% local operation

---

## 📚 Resources

- [README.md](README.md) - Full documentation
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [CHEAT_SHEET.txt](CHEAT_SHEET.txt) - Quick reference

---

**Built by:** ATLAS (Team Brain)
