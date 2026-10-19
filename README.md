# Grimoire Algorithmica — Arcane Familiar CLI (`grimoire-cli`)

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Platform: Mac | Linux | Windows](https://img.shields.io/badge/Platform-Mac%20%7C%20Linux%20%7C%20Windows-blue.svg)]()
[![Backend: Grimoire Algorithmica](https://img.shields.io/badge/Grimoire%20MMO-Live-amber.svg)](https://grimoirealgorithmica.com)

The **Arcane Familiar** is a lightweight, zero-impact background daemon for [Grimoire Algorithmica](https://grimoirealgorithmica.com). It runs on your workstation during idle hours, connects to your local GPU/CPU Ollama instances, exorcises cursed code monsters in the Bestiary, and synchronizes your earned Arcane Mana and speedup telemetry back to your verified profile on the global leaderboard.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8+ (`python3 --version`)
- *(Optional)* [Ollama](https://ollama.ai) running locally for AI-powered autonomous monster hunting (`qwen2.5-coder`, `deepseek-r1`, or `llama3.2`).

### 1. Clone & Run
```bash
git clone https://github.com/kichikubeihei/grimoire-cli.git
cd grimoire-cli
python3 grimoire-familiar.py --handle @your_handle
```

### 2. Authenticated Scribe Mode (Optional)
If you have a developer API key (`grim_free_*` or `grim_pro_*`) from [grimoirealgorithmica.com](https://grimoirealgorithmica.com):
```bash
python3 grimoire-familiar.py --handle @your_handle --api-key grim_free_your_key_here
```
Or export it as an environment variable:
```bash
export GRIMOIRE_API_KEY="grim_free_your_key_here"
python3 grimoire-familiar.py --handle @your_handle
```

---

## 🎮 Features
- **0% Gaming / Work Impact**: Automatically yields CPU/GPU resources and runs at lowest OS scheduling priority (`nice 19` / `IDLE_PRIORITY_CLASS`).
- **Autonomous Bestiary Exorcism**: Pulls unoptimized code bugs and benchmarks algorithmic optimizations in microseconds.
- **Mana Harvester**: Accumulates Arcane Mana per microsecond of execution speedup shaved.
- **Morning Report**: Displays a terminal summary of overnight monster kills, speedups, and leaderboard progression when you wake up.

---

## 📜 License
MIT License. Copyright (c) 2026 Grimoire Algorithmica.
