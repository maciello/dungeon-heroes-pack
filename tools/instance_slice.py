# /// script
# requires-python = ">=3.12"
# dependencies = ["typer>=0.12"]
# ///
"""Slice the game data the passives toolchain reads (build.py registries, gear_check.jar_data,
build_kits.scan) out of a PolyMC instance: every mod jar and the Minecraft client jar are
rewritten with only the entries below, same file names. Models, lang, spells, equipment sets,
weapon attributes, spell/item tags, Skill Tree category files; no classes, textures or sounds.

  uv run tools/instance_slice.py            # default PolyMC paths of passives/build.py
  uv run tools/instance_slice.py --instance "<.../minecraft>" --client-jar "<.../minecraft-1.21.1-client.jar>"

Output tar layout (extract onto the PolyMC paths build.py hard-codes):
  mods/<jar>                                                         -> <instance>/mods/
  libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar  -> ~/.local/share/PolyMC/
"""

from __future__ import annotations

import io
import re
import tarfile
import zipfile
from pathlib import Path
from typing import Annotated

import typer

POLYMC = Path.home() / ".local/share/PolyMC"
INSTANCE = POLYMC / "instances/Dungeon Heroes (RPG Series)/minecraft"
CLIENT_JAR = (
    POLYMC / "libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar"
)
CLIENT_MEMBER = "libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar"

KEEP = re.compile(
    r"""
    assets/[^/]+/models/item/.+\.json
  | assets/[^/]+/lang/en_us\.json
  | data/[^/]+/(?:weapon_attributes|equipment_set|spell)/.+\.json
  | data/[^/]+/tags/(?:spell|items?)/.+\.json
  | data/skill_tree_rpgs/puffish_skills/categories/\w+/(?:category|experience)\.json
  | resourcepacks/mrpgc_skill_tree_changes/data/skill_tree_rpgs/puffish_skills/categories/.+\.json
    """,
    re.VERBOSE,
)


def slim(jar: Path) -> tuple[bytes, int] | None:
    """(slim jar bytes, kept entry count); None when the file is not a zip."""
    try:
        src = zipfile.ZipFile(jar)
    except zipfile.BadZipFile:
        return None
    buf = io.BytesIO()
    kept = 0
    with src, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            if KEEP.fullmatch(info.filename):
                dst.writestr(info.filename, src.read(info))
                kept += 1
    return buf.getvalue(), kept


def add(tar: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    tar.addfile(info, io.BytesIO(data))


def main(
    instance: Annotated[
        Path, typer.Option(help="PolyMC instance's minecraft/ folder")
    ] = INSTANCE,
    client_jar: Annotated[
        Path, typer.Option(help="minecraft-1.21.1-client.jar")
    ] = CLIENT_JAR,
    out: Annotated[Path, typer.Option(help="output archive")] = Path(
        "instance_slice.tar.gz"
    ),
) -> None:
    jars = sorted((instance / "mods").glob("*.jar"))
    if not jars:
        raise typer.BadParameter(f"no mod jars in {instance / 'mods'}")
    if not client_jar.is_file():
        raise typer.BadParameter(f"no client jar at {client_jar}")
    with tarfile.open(out, "w:gz") as tar:
        for jar in jars:
            if (s := slim(jar)) is None:
                typer.echo(f"skip (not a zip): {jar.name}", err=True)
                continue
            add(tar, f"mods/{jar.name}", s[0])
        mc = slim(client_jar)
        assert mc is not None, f"{client_jar} is not a zip"
        add(tar, CLIENT_MEMBER, mc[0])
    typer.echo(
        f"{len(jars)} mod jars + client jar -> {out} ({out.stat().st_size / 1e6:.1f} MB)"
    )


if __name__ == "__main__":
    typer.run(main)
