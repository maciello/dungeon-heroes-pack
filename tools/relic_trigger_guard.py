# /// script
# requires-python = ">=3.12"
# dependencies = ["typer>=0.12"]
# ///
"""Keep relic passives from triggering on other passives' impacts, their own included.

Spell Engine fires SPELL_IMPACT_ANY / SPELL_IMPACT_SPECIFIC after every performed impact,
passive spells and status-effect impacts included, with no recursion guard. A relic whose
own impact matches its own trigger re-rolls its chance on every proc (a chain), and relics
can set each other off. `spell.type = ACTIVE` restricts those triggers to spells the
player casts. Applies to every PASSIVE spell in NAMESPACES of
global_packs/required_data/DungeonHeroes_Relics.zip.

  uv run tools/relic_trigger_guard.py apply   # add the guard, rewrite the zip
  uv run tools/relic_trigger_guard.py check   # exit 1 if any trigger lacks it
"""

from __future__ import annotations

import io
import json
import re
import zipfile
from pathlib import Path
from typing import Any

import typer

ROOT = Path(__file__).resolve().parent.parent
SPELLS_ZIP = ROOT / "global_packs/required_data/DungeonHeroes_Relics.zip"
NAMESPACES = ("relics_rpgs", "more_relics")
IMPACT_EVENTS = ("SPELL_IMPACT_ANY", "SPELL_IMPACT_SPECIFIC")
SPELL_PATH = re.compile(r"data/([a-z_]+)/spell/[a-z_]+\.json")


def unguarded(spell: dict[str, Any]) -> list[dict[str, Any]]:
    """Impact triggers of a PASSIVE spell whose `spell` condition does not pin ACTIVE."""
    if spell.get("type") != "PASSIVE":
        return []
    triggers = spell.get("passive", {}).get("triggers", [])
    return [
        t
        for t in triggers
        if t.get("type") in IMPACT_EVENTS
        and (t.get("spell") or {}).get("type") != "ACTIVE"
    ]


def scan(z: zipfile.ZipFile) -> dict[str, dict[str, Any]]:
    """entry name -> parsed spell, for the spells that need the guard."""
    found: dict[str, dict[str, Any]] = {}
    for name in z.namelist():
        m = SPELL_PATH.fullmatch(name)
        if m and m.group(1) in NAMESPACES:
            spell = json.loads(z.read(name))
            if unguarded(spell):
                found[name] = spell
    return found


def dump(spell: dict[str, Any], original: bytes) -> bytes:
    text = json.dumps(spell, indent=1, ensure_ascii=False)
    return (text + ("\n" if original.endswith(b"\n") else "")).encode()


app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def check() -> None:
    """Exit 1 when a relic impact trigger can match passive-spell impacts."""
    with zipfile.ZipFile(SPELLS_ZIP) as z:
        bad = scan(z)
    for name, spell in bad.items():
        kinds = ", ".join(t["type"] for t in unguarded(spell))
        typer.echo(f"{name}: {kinds}", err=True)
    if bad:
        typer.echo("unguarded triggers: run `just relic-trigger-guard`", err=True)
        raise typer.Exit(1)
    typer.echo("relic impact triggers are guarded")


@app.command()
def apply() -> None:
    """Pin `spell.type = ACTIVE` on every unguarded impact trigger; rewrite the zip."""
    with zipfile.ZipFile(SPELLS_ZIP) as src:
        todo = scan(src)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                data = src.read(info)
                if info.filename in todo:
                    spell = todo[info.filename]
                    for t in unguarded(spell):
                        t.setdefault("spell", {})["type"] = "ACTIVE"
                    data = dump(spell, data)
                dst.writestr(info, data, compress_type=info.compress_type)
    SPELLS_ZIP.write_bytes(buf.getvalue())
    typer.echo(f"guarded {len(todo)} spells in {SPELLS_ZIP.relative_to(ROOT)}")


if __name__ == "__main__":
    app()
