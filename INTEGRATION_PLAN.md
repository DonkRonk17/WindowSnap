# 🪟 WindowSnap - Integration Plan

## 🎯 Integration Goals

This document outlines how WindowSnap integrates with Team Brain agents and tools.

---

## 🤖 AI Agent Integration

| Agent | Use Case | Priority |
|-------|----------|----------|
| Forge | Session context management | HIGH |
| Atlas | Tool building workspace | HIGH |
| Clio | Linux development | MEDIUM |
| Nexus | Cross-platform testing | MEDIUM |
| Bolt | Automated setup | LOW |

### Forge Quick Start
```python
from windowsnap import WindowSnap
snap = WindowSnap()
snap.restore_layout("forge_orchestrate")
```

### Atlas Quick Start
```python
from windowsnap import WindowSnap
snap = WindowSnap()
snap.restore_layout("atlas_dev")
```

### Clio Quick Start
```bash
sudo apt install wmctrl
python3 windowsnap.py restore clio_dev
```

---

## 🔗 Tool Integrations

### With AgentHealth
```python
from agenthealth import AgentHealth
from windowsnap import WindowSnap
health = AgentHealth()
snap = WindowSnap()
health.log_activity("AGENT", "layout_switch", {"profile": "work"})
snap.restore_layout("work")
```

### With SynapseLink
```python
from synapselink import quick_send
from windowsnap import WindowSnap
snap = WindowSnap()
snap.restore_layout("focus")
quick_send("TEAM", "Context Switch", "Entering focus mode")
```

### With SessionReplay
```python
from sessionreplay import SessionReplay
from windowsnap import WindowSnap
replay = SessionReplay()
snap = WindowSnap()
session_id = replay.start_session("AGENT", task="Work")
snap.save_layout("session_start")
replay.log_event(session_id, "layout_saved", {"profile": "session_start"})
```

### With TaskQueuePro
```python
from taskqueuepro import TaskQueuePro
from windowsnap import WindowSnap
queue = TaskQueuePro()
snap = WindowSnap()
# Map task types to layouts
TASK_LAYOUTS = {"code": "dev_layout", "test": "test_layout"}
```

---

## 🚀 Adoption Roadmap

### Week 1: Core Adoption
- All agents test basic save/restore
- Create agent-specific layouts

### Week 2-3: Integration
- Add to session startup routines
- Test with other Team Brain tools

### Week 4+: Optimization
- Collect efficiency metrics
- Implement improvements

---

## 📊 Success Metrics

- Agents using WindowSnap: Target 5/5
- Layout profiles created: Target 15+
- Time saved per switch: ~30 seconds

---

**Last Updated:** January 31, 2026
**Maintained By:** ATLAS (Team Brain)
