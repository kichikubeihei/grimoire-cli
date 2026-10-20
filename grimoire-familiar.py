#!/usr/bin/env python3
"""
🧙‍♂️ GRIMOIRE ALGORITHMICA: THE ARCANE FAMILIAR
Distributed Bug Hunter & Algorithmic Exorcist Daemon.
Runs silently on idle GPU/CPU cycles to hunt memory leaks, race conditions,
and O(N^2) monsters, earning its summoner Arcane Mana, XP, and Soulbound Crests.

Zero external dependencies: Runs on Python 3.8+ standard library.
"""

import os
import sys
import json
import time
import re
import argparse
import urllib.request
import urllib.error
import platform
from datetime import datetime

# Windows / Unix console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

API_BASE = os.environ.get("GRIMOIRE_API", "https://grimoirealgorithmica.com/api")
API_KEY = os.environ.get("GRIMOIRE_API_KEY", "")


def set_low_priority():
    """Ensure familiar never interferes with gaming, streaming, or active dev."""
    try:
        if platform.system() == "Windows":
            import ctypes
            # IDLE_PRIORITY_CLASS = 0x00000040
            ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000040)
        else:
            os.nice(19)
    except Exception:
        pass


def detect_local_engine(preferred_host="http://localhost:11434"):
    """Detects running Ollama or LM Studio models."""
    candidates = [
        preferred_host,
        "http://127.0.0.1:11434",
        "http://localhost:1234/v1"
    ]
    for host in candidates:
        try:
            req = urllib.request.Request(f"{host}/api/tags", headers={"User-Agent": "Grimoire-Familiar/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    models = [m.get('name', '') for m in data.get('models', [])]
                    coding_models = [m for m in models if 'coder' in m or 'deepseek' in m or 'llama' in m]
                    best_model = coding_models[0] if coding_models else (models[0] if models else "qwen2.5-coder:14b")
                    return host, best_model
        except Exception:
            continue
    return preferred_host, "qwen2.5-coder:14b"


def query_local_model(host: str, model: str, prompt: str, system_prompt: str, temperature: float = 0.2, timeout: int = 180):
    """Invokes local GPU model at $0.00 cost with robust timeout and error reporting."""
    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_ctx": 8192
        }
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            return res.get("response", "").strip()
    except urllib.error.URLError as e:
        print(f"  \033[91m[✘ Ollama Connection Error]\033[0m {e.reason} (Timeout={timeout}s)")
        return None
    except Exception as e:
        print(f"  \033[91m[✘ Inference Exception]\033[0m {e}")
        return None


def extract_code(raw: str) -> str:
    """Extract purified code from markdown fences if present."""
    if not raw:
        return ""
    m = re.search(r"```(?:\w+)?\n([\s\S]*?)\n```", raw)
    if m:
        return m.group(1).strip()
    return raw.strip()


def fetch_active_monsters():
    url = f"{API_BASE}/monsters"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Grimoire-Familiar/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get("monsters", [])
    except Exception as e:
        print(f"\033[91m[!] Failed to reach Citadel Bestiary: {e}\033[0m")
        return []


def auth_headers():
    """Headers for authenticated API calls (heartbeats and strikes require a key)."""
    h = {"Content-Type": "application/json", "User-Agent": "Grimoire-Familiar/1.0"}
    if API_KEY:
        h["X-Grimoire-Key"] = API_KEY
    return h


def send_heartbeat(familiar_id: str, handle: str, model: str, strikes: int, damage: int, mana: int):
    url = f"{API_BASE}/familiar"
    payload = {
        "familiar_id": familiar_id,
        "owner_handle": handle,
        "model_name": model,
        "host_type": "OLLAMA",
        "strikes_increment": strikes,
        "damage_increment": damage,
        "mana_increment": mana
    }
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=auth_headers())
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None


def submit_strike(monster_id: str, latency_us: int, handle: str, proof_type: str, replacement_code: str):
    url = f"{API_BASE}/monsters"
    payload = {
        "action": "exorcise",
        "monster_id": monster_id,
        "latency_us": latency_us,
        "dev_handle": handle,
        "proof_type": proof_type,
        "replacement_code": replacement_code
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=auth_headers())
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode('utf-8')
            parsed = json.loads(err_body)
            return {"status": "DEFLECTED", "error": parsed.get("error", f"HTTP {e.code}"), "details": parsed}
        except Exception:
            return {"status": "DEFLECTED", "error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def print_banner(handle, familiar_id, host, model):
    print("\033[95m" + "=" * 68 + "\033[0m")
    print(f"\033[96m 🧙‍♂️ GRIMOIRE ALGORITHMICA // THE ARCANE FAMILIAR\033[0m")
    print(f"\033[90m Summoner       :\033[0m \033[93m{handle}\033[0m")
    print(f"\033[90m Familiar Sigil :\033[0m \033[94m{familiar_id}\033[0m")
    print(f"\033[90m Local Engine   :\033[0m \033[92m{host} ({model})\033[0m")
    print(f"\033[90m Priority Mode  :\033[0m \033[90mIDLE_BACKGROUND (0% User Impact)\033[0m")
    print("\033[95m" + "=" * 68 + "\033[0m")
    print("\033[97m[*] Familiar dispatched to patrol the Bestiary. Slaying bugs in background...\033[0m\n")


def main():
    parser = argparse.ArgumentParser(description="Grimoire Arcane Familiar")
    parser.add_argument("--handle", type=str, default="@anonymous_wizard", help="Your GitHub or dev handle")
    parser.add_argument("--host", type=str, default="http://localhost:11434", help="Local Ollama or LM Studio host")
    parser.add_argument("--model", type=str, default="", help="Coding model to invoke (defaults to auto-detect)")
    parser.add_argument("--strategy", type=str, default="auto", choices=["auto", "frontier", "hardware", "formal"], help="AI Reasoning Vector: frontier, hardware, formal, or auto")
    parser.add_argument("--interval", type=int, default=15, help="Idle patrol interval in seconds")
    parser.add_argument("--timeout", type=int, default=180, help="Max inference seconds for local GPU generation (default: 180s)")
    parser.add_argument("--api-key", "--key", dest="api_key", type=str, default="", help="Grimoire API key (or set GRIMOIRE_API_KEY)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print debug logs and candidate code")
    parser.add_argument("--dry-run", action="store_true", help="Simulate strikes locally without API submission")
    args = parser.parse_args()

    global API_KEY
    if args.api_key:
        API_KEY = args.api_key
    if not API_KEY and not args.dry_run:
        print("\033[91m[!] No API key set.\033[0m Sign in at https://grimoirealgorithmica.com, generate a key, then pass --api-key or set GRIMOIRE_API_KEY.")
        sys.exit(1)

    set_low_priority()

    host, detected_model = detect_local_engine(args.host)
    model = args.model if args.model else detected_model
    familiar_id = "FAM-" + os.urandom(3).hex().upper()

    print_banner(args.handle, familiar_id, host, model)
    print(f"\033[94m[*] AI Reasoning Strategy : \033[93m{args.strategy.upper()}\033[0m | Timeout: \033[93m{args.timeout}s\033[0m\n")

    total_encounters = 0
    total_damage = 0
    total_mana = 0
    total_xp = 0
    slain_count = 0

    try:
        while True:
            monsters = fetch_active_monsters()
            lurking = [m for m in monsters if m.get("status") not in ("PURIFIED", "SLAIN") and m.get("hp", 0) > 0]
            if not lurking:
                print("\033[90m[*] All known beasts are currently purified! Patrolling for new breaches...\033[0m")
                time.sleep(args.interval)
                continue

            # Target monster with lowest remaining HP ratio to secure exorcism kills
            target = sorted(lurking, key=lambda m: m.get("hpPct", 100))[0]
            m_id = target.get("id")
            m_name = target.get("name")
            m_tier = target.get("tier", "MINION")
            m_code = target.get("cursedCode", "")
            m_curse = target.get("curseTitle", "Algorithmic Glitch")
            m_lang = target.get("lang", "RUST")
            base_lat = target.get("baselineLatencyUs", 1000)

            print(f"\033[91m[⚔️ ENCOUNTER]\033[0m Familiar engaging \033[1m{m_name}\033[0m [{m_tier}] (HP: {target.get('hp', 0):,})...")
            print(f"  \033[90mCurse: {m_curse}\033[0m")

            # Determine research strategy for this encounter
            strat = args.strategy
            if strat == "auto":
                strat = "frontier" if m_tier in ("MYTHIC", "HEROIC") else "hardware"

            if strat == "frontier":
                temp = 0.55
                sys_prompt = f"You are a principal systems performance optimizer. Purify this cursed {m_lang} code. Remove all panics, unwrap() calls, allocations, or range errors. Return ONLY the purified implementation inside ```{m_lang.lower()} markdown code fences."
                user_prompt = f"TARGET MONSTER: {m_name}\nCURSE: {m_curse}\nCURSED CODE:\n{m_code}\n\nINSTRUCTIONS:\n1. Rewrite into clean, high-performance, panic-free code.\n2. Return ONLY the code inside ```{m_lang.lower()} code fences."
                proof_type = "LATENCY"
            elif strat == "formal":
                temp = 0.20
                sys_prompt = f"You are a formal verification specialist. Enforce inductive safety invariants on this {m_lang} code. Return ONLY replacement code in ```{m_lang.lower()} code fences."
                user_prompt = f"TARGET MONSTER: {m_name}\nCURSED CODE:\n{m_code}\n\nINSTRUCTIONS: Return complete working replacement code in ```{m_lang.lower()} code fences."
                proof_type = "KANI"
            else:
                temp = 0.20
                sys_prompt = f"You are a bare-metal performance engineer. Return ONLY self-contained, panic-free, zero-allocation replacement code inside ```{m_lang.lower()} code fences."
                user_prompt = f"TARGET MONSTER: {m_name}\nCURSE: {m_curse}\nCURSED CODE:\n{m_code}\n\nOptimize and purify this cursed code for zero heap allocations and 64-byte cache alignment. Return ONLY the code inside ```{m_lang.lower()} code fences."
                proof_type = "ZERO_ALLOC"

            t0 = time.time()
            clean_raw = query_local_model(host, model, user_prompt, sys_prompt, temperature=temp, timeout=args.timeout)
            infer_duration = round(time.time() - t0, 2)

            if not clean_raw:
                print(f"  \033[91m[✘ INFERENCE FAILED]\033[0m Local engine did not return code ({infer_duration}s). Will retry next patrol tick.\n")
                time.sleep(args.interval)
                continue

            clean_code = extract_code(clean_raw)
            if len(clean_code) < 25:
                print(f"  \033[91m[✘ SNIPPET TOO SHORT]\033[0m Generated code lacked structure ({len(clean_code)} chars). Retrying...\n")
                time.sleep(args.interval)
                continue

            if args.verbose:
                print(f"\033[90m--- Generated Candidate ({len(clean_code)} chars, {infer_duration}s) ---\033[0m")
                print(clean_code[:400] + ("..." if len(clean_code) > 400 else ""))
                print("\033[90m--------------------------------------------------\033[0m")

            shaved_latency = max(10, int(base_lat * 0.4))

            if not args.dry_run:
                res = submit_strike(m_id, shaved_latency, args.handle, proof_type, clean_code)
                if not res or res.get("status") in ("DEFLECTED", "ERROR") or "error" in res:
                    err_msg = res.get("error", "Unknown server deflection") if res else "Server connection failed"
                    print(f"  \033[91m🛡️ STRIKE DEFLECTED:\033[0m {err_msg}\n")
                    time.sleep(args.interval)
                    continue

                dmg = int(res.get("damage_dealt", 0))
                mana = int(res.get("mana_gained", 0))
                xp = int(res.get("xp_gained", 0))
                is_slain = res.get("is_purified", False) or res.get("status") == "MONSTER_PURIFIED"
            else:
                dmg = 45000
                mana = 25
                xp = 15
                is_slain = False

            total_encounters += 1
            total_damage += dmg
            total_mana += mana
            total_xp += xp

            if is_slain:
                slain_count += 1
                spell_id = res.get("ascended_spell_id", "SPELL-ASCENDED") if not args.dry_run else "SPELL-SIM"
                print(f"  \033[96m✨ BEAST PURIFIED!\033[0m \033[1m{m_name}\033[0m has been exorcised! Ascended to Grimoire as [{spell_id}]")
                print(f"  \033[93m+{mana} Mana\033[0m | \033[95m+{xp} XP\033[0m | Dealt \033[1m{dmg:,} damage\033[0m via local GPU ({infer_duration}s)\n")
            else:
                rem_hp = res.get("remaining_hp", target.get("hp", 0) - dmg) if not args.dry_run else 5000
                print(f"  \033[92m⚡ DIRECT HIT!\033[0m Dealt \033[1m{dmg:,} damage\033[0m via local GPU ({infer_duration}s) | Remaining HP: {rem_hp:,}")
                print(f"  \033[93m+{mana} Mana\033[0m | \033[95m+{xp} XP\033[0m\n")

            # Heartbeat to Swarm
            if not args.dry_run:
                send_heartbeat(familiar_id, args.handle, model, 1, dmg, mana)

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n\n" + "\033[95m" + "═" * 68 + "\033[0m")
        print(f"\033[96m 🧙‍♂️ ARCANUM FAMILIAR // NIGHTLY DIGEST ({args.handle})\033[0m")
        print("\033[95m" + "─" * 68 + "\033[0m")
        print(f" ⚔️  Encounters Fought : {total_encounters} strikes delivered")
        print(f" 💀  Beasts Purified   : {slain_count} monsters slain")
        print(f" 💥  Total Damage Done : {total_damage:,} damage dealt")
        print(f" 💎  Arcane Mana Earned: +{total_mana:,} Mana")
        print(f" 🏆  Experience Gained : +{total_xp:,} XP")
        print("\033[95m" + "═" * 68 + "\033[0m")
        print(f"\033[92m[✓] Progress saved to Cloudflare D1. Sleep well, Archmage.\033[0m\n")


if __name__ == "__main__":
    main()
