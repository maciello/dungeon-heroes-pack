# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.7", "typer>=0.12"]
# ///
"""Generate the relic tooltip resource pack from the pack's own spell and effect data.

Spell Engine builds a relic's tooltip line from the lang key
`spell.<namespace>.<spell>.description`. The mod ships fixed text for it, which goes
stale as soon as this pack retunes chances, durations, stack caps or effect attributes.
This script derives the text from:
  - global_packs/required_data/DungeonHeroes_Relics.zip   (spell definitions)
  - config/relics/effects.json, config/more_relics/effects.json   (effect attributes)
and writes global_packs/required_resources/DungeonHeroes_RelicTooltips.zip.

  uv run tools/relic_tooltips.py build   # regenerate the zip
  uv run tools/relic_tooltips.py check   # exit 1 if the zip is stale
  uv run tools/relic_tooltips.py show    # print the generated lines
"""

from __future__ import annotations

import io
import json
import re
import zipfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import typer
from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parent.parent
SPELLS_ZIP = ROOT / "global_packs/required_data/DungeonHeroes_Relics.zip"
EFFECT_FILES = [
    ROOT / "config/relics/effects.json",
    ROOT / "config/more_relics/effects.json",
]
OUT_ZIP = ROOT / "global_packs/required_resources/DungeonHeroes_RelicTooltips.zip"
NAMESPACES = ("relics_rpgs", "more_relics")

# Spell Engine reads the description with I18n.translate(key), which runs String.format,
# so a literal percent sign must be written "%%". Set to "%" if tooltips show "%%".
PERCENT_ESCAPE = "%%"
RESOURCE_PACK_FORMAT = 34  # Minecraft 1.21.1
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

# Spell Engine defaults (SpellEngine Spell.java): status effect duration 10s, apply_mode SET,
# refresh_duration true. First ADD gives amplifier max(inc-1, 0); cap N means N+1 stacks.
DEFAULT_EFFECT_SECONDS = 10.0


class Model(BaseModel):
    model_config = ConfigDict(extra="ignore")


class Trigger(Model):
    type: str
    chance: float | None = None
    spell: dict[str, Any] | None = None
    impact: dict[str, Any] | None = None
    effect: dict[str, Any] | None = None
    damage: dict[str, Any] | None = None
    target_conditions: list[dict[str, Any]] = Field(default_factory=list)


class Remove(Model):
    id: str


class StatusEffect(Model):
    effect_id: str | None = None
    duration: float = DEFAULT_EFFECT_SECONDS
    amplifier: int = 0
    amplifier_cap: int | None = None
    apply_mode: str = "SET"
    refresh_duration: bool = True
    remove: Remove | None = None


class Action(Model):
    type: str
    status_effect: StatusEffect | None = None
    min_power: float | None = None
    max_power: float | None = None
    heal: dict[str, Any] | None = None
    damage: dict[str, Any] | None = None


class Impact(Model):
    action: Action
    chance: float | None = None
    attribute: str | None = None


class Cloud(Model):
    time_to_live_seconds: float
    impact_tick_interval: int | None = None
    volume: dict[str, Any] = Field(default_factory=dict)


class Deliver(Model):
    type: str
    clouds: list[Cloud] = Field(default_factory=list)
    stash_effect: dict[str, Any] | None = None


class Target(Model):
    type: str
    area: dict[str, Any] = Field(default_factory=dict)


class Passive(Model):
    triggers: list[Trigger]


class Cooldown(Model):
    duration: float = 0.0


class Cost(Model):
    cooldown: Cooldown = Field(default_factory=Cooldown)


class AreaImpact(Model):
    radius: float


class Spell(Model):
    active: dict[str, Any] | None = None
    passive: Passive | None = None
    target: Target | None = None
    deliver: Deliver | None = None
    impacts: list[Impact] = Field(default_factory=list)
    area_impact: AreaImpact | None = None
    cost: Cost = Field(default_factory=Cost)

    @property
    def effects(self) -> list[StatusEffect]:
        return [
            i.action.status_effect
            for i in self.impacts
            if i.action.type == "STATUS_EFFECT"
            and i.action.status_effect
            and i.action.status_effect.effect_id
        ]


class Attr(Model):
    attribute: str
    value: float
    operation: str


class Effect(Model):
    attributes: list[Attr] = Field(default_factory=list)


class Ctx(BaseModel):
    spell_id: str
    spell: Spell
    effects: dict[str, Effect]


# ---------------------------------------------------------------- phrasing helpers

SCHOOLS_BASE = {"arcane", "fire", "frost", "healing", "lightning", "soul"}
SCHOOLS_ALL = SCHOOLS_BASE | {"air", "earth", "nature", "water"}
ATTR_NAMES = {
    "minecraft:generic.attack_damage": "attack damage",
    "minecraft:generic.attack_speed": "attack speed",
    "minecraft:generic.armor": "armor",
    "minecraft:generic.armor_toughness": "armor toughness",
    "minecraft:generic.max_health": "max health",
    "minecraft:generic.movement_speed": "movement speed",
    "minecraft:generic.scale": "size",
    "more_rpg_classes:lifesteal_modifier": "lifesteal",
    "more_rpg_classes:spell_vampire": "spell vamp",
    "more_rpg_classes:rage_modifier": "rage power",
    "ranged_weapon:damage": "ranged damage",
    "ranged_weapon:haste": "ranged haste",
    "spell_engine:damage_taken": "damage taken",
    "spell_engine:evasion_chance": "evasion chance",
    "spell_engine:healing_taken": "healing received",
    "spell_power:haste": "spell haste",
    "spell_power:critical_chance": "spell crit chance",
    "spell_power:critical_damage": "spell crit damage",
}


def num(v: float) -> str:
    return f"{round(v, 4):g}"


def pct(v: float) -> str:
    return f"{num(v * 100)}%"


def secs(v: float) -> str:
    return f"{num(v)}s"


def join_and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def join_or(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " or " + items[-1]


def school_phrase(schools: set[str]) -> str:
    if schools == SCHOOLS_BASE:
        return "spell power"
    if schools == SCHOOLS_ALL:
        return "spell power (all schools)"
    missing = sorted(SCHOOLS_ALL - schools)
    if len(schools) >= 8 and missing:
        return f"spell power (all schools except {join_and(missing)})"
    names = sorted(schools)
    return f"{join_and(names)} spell power"


def amount(attr: Attr, scale: float = 1.0) -> str:
    v = attr.value * scale
    sign = "+" if v >= 0 else "-"
    if attr.operation == "ADD_VALUE":
        return f"{sign}{num(abs(v))}"
    return f"{sign}{pct(abs(v))}"


def effect_phrase(ctx: Ctx, effect_id: str, scale: float = 1.0) -> str:
    """'+1% attack speed, ranged haste and spell haste' from the effect's attributes."""
    groups: dict[str, list[str]] = {}
    schools: dict[str, set[str]] = {}
    for a in ctx.effects[effect_id].attributes:
        if (
            a.attribute.startswith("spell_power:")
            and a.attribute.split(":")[1] in SCHOOLS_ALL
        ):
            schools.setdefault(amount(a, scale), set()).add(a.attribute.split(":")[1])
        else:
            groups.setdefault(amount(a, scale), []).append(ATTR_NAMES[a.attribute])
    for amt, s in schools.items():
        groups.setdefault(amt, []).insert(0, school_phrase(s))
    parts = [f"{amt} {join_and(names)}" for amt, names in groups.items()]
    # two single-name groups read best as "A and B"; otherwise "A, B and C" would be ambiguous
    return (
        join_and(parts)
        if all(len(n) == 1 for n in groups.values())
        else ", ".join(parts)
    )


def hit_text(t: Trigger) -> tuple[str, str]:
    """('hit', 'melee') | ('when', 'you take damage') for one trigger."""
    spell = t.spell or {}
    impact_type = (t.impact or {}).get("impact_type")
    magic = spell.get("archetype") == "MAGIC"
    if t.type == "MELEE_IMPACT":
        return "hit", "melee"
    if t.type == "ARROW_IMPACT":
        return "hit", "arrow"
    if t.type == "SPELL_IMPACT_ANY":
        return "hit", "magic spell" if magic else "spell"
    if t.type == "SPELL_IMPACT_SPECIFIC" and impact_type == "DAMAGE":
        return "hit", "damaging magic spell" if magic else "damaging spell"
    if t.type == "DAMAGE_TAKEN":
        direct = "!#dungeon_heroes:dot" in str((t.damage or {}).get("damage_type", ""))
        return (
            "when",
            "you take direct damage (not damage over time)"
            if direct
            else "you take damage",
        )
    if t.type == "SHIELD_BLOCK":
        return "when", "you block with a shield"
    if t.type == "EVASION":
        return "when", "you evade an attack"
    if t.type == "ROLL":
        return "when", "you roll"
    raise ValueError(f"unmapped trigger {t.type} impact={impact_type}")


def trigger_clause(triggers: list[Trigger]) -> str:
    """'20% chance on melee, arrow or spell hit' / 'Whenever ...'. One shared chance only."""
    chances = {t.chance for t in triggers}
    assert len(chances) == 1, f"mixed trigger chances {chances}"
    chance = chances.pop()
    hits: list[str] = []
    whens: list[str] = []
    for t in triggers:
        kind, text = hit_text(t)
        (hits if kind == "hit" else whens).append(text)
    hit_part = f"{join_or(hits)} hit" if hits else ""
    when_part = join_or(whens)
    if chance is None:
        if hit_part and when_part:
            return f"Whenever you land a {hit_part} or {when_part}"
        return (
            f"Whenever you land a {hit_part}" if hit_part else f"Whenever {when_part}"
        )
    if hit_part and when_part:
        return f"{pct(chance)} chance on {hit_part} or when {when_part}"
    return (
        f"{pct(chance)} chance on {hit_part}"
        if hit_part
        else f"{pct(chance)} chance when {when_part}"
    )


def stack_clause(e: StatusEffect) -> str:
    assert e.apply_mode == "ADD" and e.amplifier_cap is not None and e.amplifier == 1
    stacks = e.amplifier_cap + 1
    refresh = (
        "each stack refreshes the duration"
        if e.refresh_duration
        else "stacks do not extend the duration"
    )
    return f"Stacks up to {stacks} times; {refresh}."


# ---------------------------------------------------------------- describers

Describer = Callable[[Ctx], str]


def passive_buff(ctx: Ctx) -> str:
    """Passive whose impacts apply one effect to the wearer (optionally stacking)."""
    sp = ctx.spell
    (e,) = sp.effects
    assert sp.passive and sp.deliver is None and len(sp.impacts) == 1
    clause = trigger_clause(sp.passive.triggers)
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    if e.apply_mode == "ADD":
        return f"Passive: {clause} to gain a stack of {eff} for {secs(e.duration)}. {stack_clause(e)}"
    return f"Passive: {clause} to gain {eff} for {secs(e.duration)}."


def passive_stacking_always(ctx: Ctx) -> str:
    """Stacking passive with no proc chance (fires on every matching event)."""
    sp = ctx.spell
    (e,) = sp.effects
    assert sp.passive
    clause = trigger_clause(sp.passive.triggers)
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    return f"Passive: {clause}, gain a stack of {eff} for {secs(e.duration)}. {stack_clause(e)}"


def active_buff(ctx: Ctx) -> str:
    sp = ctx.spell
    (e,) = sp.effects
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    return f"Use: Gain {eff} for {secs(e.duration)}."


def area_buff(ctx: Ctx) -> str:
    sp = ctx.spell
    assert (
        sp.target and sp.target.type == "AREA" and sp.target.area.get("include_caster")
    )
    (e,) = sp.effects
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    return f"Use: You and nearby allies gain {eff} for {secs(e.duration)}."


def zone_buff(ctx: Ctx) -> str:
    sp = ctx.spell
    assert sp.deliver and sp.deliver.type == "CLOUD" and len(sp.deliver.clouds) == 1
    cloud = sp.deliver.clouds[0]
    (e,) = sp.effects
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    radius = num(cloud.volume["radius"])
    return f"Use: Create a {radius}-block zone for {secs(cloud.time_to_live_seconds)}. Allies inside gain {eff}."


def area_health_buff(ctx: Ctx) -> str:
    sp = ctx.spell
    heal = sp.impacts[1]
    assert (
        heal.action.type == "HEAL" and heal.attribute == "minecraft:generic.max_health"
    )
    assert sp.target and sp.target.area.get("include_caster")
    e = sp.effects[0]
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    coef = heal.action.heal["spell_power_coefficient"]  # type: ignore[index]
    return f"Use: You and nearby allies gain {eff} for {secs(e.duration)} and are healed for {pct(coef)} of max health."


def active_heal_max_health(ctx: Ctx) -> str:
    (imp,) = ctx.spell.impacts
    assert imp.action.type == "HEAL" and imp.attribute == "minecraft:generic.max_health"
    coef = imp.action.heal["spell_power_coefficient"]  # type: ignore[index]
    return f"Use: Heal for {pct(coef)} of your max health."


def stun_perk(verb: str) -> Describer:
    def describe(ctx: Ctx) -> str:
        sp = ctx.spell
        assert sp.passive and sp.area_impact
        (e,) = sp.effects
        clause = trigger_clause(sp.passive.triggers)
        return (
            f"Passive: {clause} to {verb} the target and enemies within "
            f"{num(sp.area_impact.radius)} blocks for {secs(e.duration)}."
        )

    return describe


def lesser_use_damage(ctx: Ctx) -> str:
    """Remove the old buff, then SET amplifier k with chance c_k in order: last success wins."""
    sp = ctx.spell
    assert sp.passive and [t.type for t in sp.passive.triggers] == ["MELEE_IMPACT"]
    sets = [
        i
        for i in sp.impacts
        if i.action.status_effect and i.action.status_effect.apply_mode == "SET"
    ]
    levels = [
        (i.action.status_effect.amplifier, i.chance if i.chance is not None else 1.0)
        for i in sets
    ]  # type: ignore[union-attr]
    probs = {}
    for idx, (amp, c) in enumerate(levels):
        later = 1.0
        for _, c2 in levels[idx + 1 :]:
            later *= 1 - c2
        probs[amp] = c * later
    assert max(probs.values()) - min(probs.values()) < 1e-3, (
        f"levels not uniform: {probs}"
    )
    eid = sets[0].action.status_effect.effect_id  # type: ignore[union-attr]
    unit = ctx.effects[eid].attributes[0]
    lo, hi = amount(unit, min(probs) + 1), amount(unit, max(probs) + 1)
    step = pct(unit.value)
    dur = sets[0].action.status_effect.duration  # type: ignore[union-attr]
    return f"Passive: Every melee hit grants a random {lo} to {hi} attack damage ({step} steps) for {secs(dur)}, replacing the previous bonus."


def lesser_use_ranged(ctx: Ctx) -> str:
    """Trigger: dungeon_heroes:sneak_ready (dh_addon fires it after SNEAK_READY_TICKS=20 of sneaking)."""
    sp = ctx.spell
    assert sp.passive and sp.passive.triggers[0].effect == {
        "id": "dungeon_heroes:sneak_ready"
    }
    (e,) = sp.effects
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    return f"Passive: After sneaking for 1s, gain {eff} until you stop sneaking."


def trance(ctx: Ctx) -> str:
    """Proc starts a stash effect; each stash trigger then adds one stack (consume 0)."""
    sp = ctx.spell
    assert sp.passive and sp.deliver and sp.deliver.type == "STASH_EFFECT"
    stash = sp.deliver.stash_effect or {}
    assert stash.get("consume") == 0
    (e,) = sp.effects
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    clause = trigger_clause(sp.passive.triggers)
    event = join_or([hit_text(Trigger.model_validate(t))[1] for t in stash["triggers"]])
    stacks = (e.amplifier_cap or 0) + 1
    duration = stash.get("duration", DEFAULT_EFFECT_SECONDS)
    return (
        f"Passive: {clause} to enter a trance for {secs(duration)}. "
        f"Each {event} hit during it adds a stack of {eff}, up to {stacks} stacks."
    )


def evasion_attack(ctx: Ctx) -> str:
    sp = ctx.spell
    assert sp.passive and sp.deliver and sp.deliver.type == "STASH_EFFECT"
    stash_id = sp.deliver.stash_effect["id"]  # type: ignore[index]
    eff = effect_phrase(ctx, stash_id)
    clause = trigger_clause(sp.passive.triggers)
    stash = sp.deliver.stash_effect or {}
    assert stash.get("consume", 1) == 1, "stash must be consumed by the first melee hit"
    duration = stash.get("duration", DEFAULT_EFFECT_SECONDS)
    return f"Passive: {clause} to gain {eff} on your next melee attack (within {secs(duration)})."


def roll_damage(ctx: Ctx) -> str:
    (imp,) = ctx.spell.impacts
    a = imp.action
    return f"Passive: Rolling deals {num(a.min_power)}-{num(a.max_power)} damage to nearby enemies."  # type: ignore[arg-type]


def defense_block(ctx: Ctx) -> str:
    (imp,) = ctx.spell.impacts
    a = imp.action
    coef = a.heal["spell_power_coefficient"]  # type: ignore[index]
    return f"Passive: Blocking with a shield heals you for {pct(coef)} of your spell power (counted as at least {num(a.min_power)})."  # type: ignore[arg-type]


def heal_danger(ctx: Ctx) -> str:
    sp = ctx.spell
    (imp,) = sp.impacts
    a = imp.action
    t = sp.passive.triggers[0]  # type: ignore[union-attr]
    below = t.target_conditions[0]["health_percent_below"]
    coef = a.heal["spell_power_coefficient"]  # type: ignore[index]
    return (
        f"Passive: Healing a target below {pct(below)} health triggers a bonus heal of {pct(coef)} "
        f"of your spell power (counted as at least {num(a.min_power)})."  # type: ignore[arg-type]
    )


def healing_cleanse(ctx: Ctx) -> str:
    t = ctx.spell.passive.triggers[0]  # type: ignore[union-attr]
    return f"Passive: {pct(t.chance)} chance when your healing spell hits a target with a harmful effect to remove one random harmful effect from it."  # type: ignore[arg-type]


def liandrys(ctx: Ctx) -> str:
    sp = ctx.spell
    (e,) = sp.effects
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    clause = trigger_clause(sp.passive.triggers)  # type: ignore[union-attr]
    return f"Passive: {clause} to afflict the target with {eff} for {secs(e.duration)}. {stack_clause(e)}"


def frozen_heart(ctx: Ctx) -> str:
    sp = ctx.spell
    (e,) = sp.effects
    eff = effect_phrase(ctx, e.effect_id)  # type: ignore[arg-type]
    clause = trigger_clause(sp.passive.triggers)  # type: ignore[union-attr]
    return f"Passive: {clause} to give nearby enemies {eff} for {secs(e.duration)}."


def kircheis(ctx: Ctx) -> str:
    sp = ctx.spell
    assert sp.deliver and sp.deliver.type == "CLOUD"
    cloud = sp.deliver.clouds[0]
    (imp,) = sp.impacts
    coef = imp.action.damage["spell_power_coefficient"]  # type: ignore[index]
    tick = (cloud.impact_tick_interval or 20) / 20
    every = "every second" if tick == 1 else f"every {secs(tick)}"
    clause = trigger_clause(sp.passive.triggers)  # type: ignore[union-attr]
    return (
        f"Passive: {clause} to create a field of lightning arcs at the target ({num(cloud.volume['radius'])}-block radius, "
        f"{secs(cloud.time_to_live_seconds)}) that deals {pct(coef)} of your ranged physical spell power to enemies inside {every}."
    )


# Spells deliberately not overridden (stock text stays), with the reason.
SKIPPED = {
    "more_relics:superior_mejais_soulstealer": "stash (10s) and impact (20s) durations disagree; re-delivery on later kills unverified",
    "more_relics:greater_madreds_bloodrazor": "stash damage scaled by target max health; wording unverified",
    "more_relics:greater_sunfire_cape": "stash aura on EFFECT_TICK scaled by max health; wording unverified",
    "more_relics:superior_shurelyas_battlesong": "six SET impacts with falling duration and rising amplifier; runtime outcome unverified",
}

DESCRIBERS: dict[str, Describer] = {
    "relics_rpgs:lesser_use_dex": passive_buff,
    "relics_rpgs:lesser_use_damage": lesser_use_damage,
    "relics_rpgs:lesser_use_ranged": lesser_use_ranged,
    "relics_rpgs:lesser_use_health": active_heal_max_health,
    "relics_rpgs:lesser_use_spell_haste": active_buff,
    "relics_rpgs:lesser_use_spell_power": active_buff,
    "relics_rpgs:lesser_proc_arcane_fire": passive_buff,
    "relics_rpgs:lesser_proc_frost_healing": passive_buff,
    "relics_rpgs:lesser_proc_spell_crit": passive_buff,
    "relics_rpgs:lesser_proc_crit_damage": passive_buff,
    "relics_rpgs:medium_proc_attack_damage": passive_buff,
    "relics_rpgs:medium_proc_attack_speed": passive_buff,
    "relics_rpgs:medium_proc_defense": passive_buff,
    "relics_rpgs:medium_proc_evasion": passive_buff,
    "relics_rpgs:medium_proc_ranged_damage": passive_buff,
    "relics_rpgs:medium_proc_spell_haste": passive_buff,
    "relics_rpgs:medium_proc_spell_power": passive_buff,
    "relics_rpgs:greater_perk_melee_stun": stun_perk("stun"),
    "relics_rpgs:greater_perk_spell_stun": stun_perk("stun"),
    "relics_rpgs:greater_perk_ranged_levitate": stun_perk("levitate"),
    "relics_rpgs:greater_perk_roll_damage": roll_damage,
    "relics_rpgs:greater_perk_defense_block": defense_block,
    "relics_rpgs:greater_perk_heal_danger": heal_danger,
    "relics_rpgs:greater_perk_healing_cleanse": healing_cleanse,
    "relics_rpgs:greater_perk_evasion_attack": evasion_attack,
    "relics_rpgs:greater_proc_physical_trance": trance,
    "relics_rpgs:greater_proc_spell_trance": trance,
    "relics_rpgs:superior_use_area_attack_damage": area_buff,
    "relics_rpgs:superior_use_area_defense_health": area_health_buff,
    "relics_rpgs:superior_use_zone_healing_taken": zone_buff,
    "relics_rpgs:superior_use_zone_spell_power": zone_buff,
    "more_relics:lesser_proc_air_water": passive_buff,
    "more_relics:lesser_proc_earth_nature": passive_buff,
    "more_relics:lesser_use_rage_power": passive_stacking_always,
    "more_relics:medium_perk_rage": passive_buff,
    "more_relics:medium_proc_lifesteal": passive_buff,
    "more_relics:greater_frozen_heart": frozen_heart,
    "more_relics:greater_kircheis_shard": kircheis,
    "more_relics:greater_liandrys_torment": liandrys,
}


# ---------------------------------------------------------------- IO


def load_spells() -> dict[str, Spell]:
    spells: dict[str, Spell] = {}
    with zipfile.ZipFile(SPELLS_ZIP) as z:
        for name in sorted(z.namelist()):
            m = re.fullmatch(r"data/([a-z_]+)/spell/([a-z_]+)\.json", name)
            if m and m.group(1) in NAMESPACES:
                spells[f"{m.group(1)}:{m.group(2)}"] = Spell.model_validate(
                    json.loads(z.read(name))
                )
    return spells


def load_effects() -> dict[str, Effect]:
    effects: dict[str, Effect] = {}
    for f in EFFECT_FILES:
        for eid, body in json.loads(f.read_text())["effects"].items():
            effects[eid] = Effect.model_validate(body)
    return effects


def generate() -> dict[str, dict[str, str]]:
    """namespace -> {lang_key: text}. Raises on spells that are neither described nor skipped."""
    spells, effects = load_spells(), load_effects()
    unknown = sorted(set(spells) - set(DESCRIBERS) - set(SKIPPED))
    if unknown:
        raise SystemExit(f"spells without a describer or skip reason: {unknown}")
    stale = sorted((set(DESCRIBERS) | set(SKIPPED)) - set(spells))
    if stale:
        raise SystemExit(
            f"describers for spells missing from {SPELLS_ZIP.name}: {stale}"
        )
    out: dict[str, dict[str, str]] = {ns: {} for ns in NAMESPACES}
    for spell_id, describe in DESCRIBERS.items():
        ns, path = spell_id.split(":")
        text = describe(Ctx(spell_id=spell_id, spell=spells[spell_id], effects=effects))
        out[ns][f"spell.{ns}.{path}.description"] = text.replace("%", PERCENT_ESCAPE)
    return out


def build_zip(lang: dict[str, dict[str, str]]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:

        def put(name: str, data: str) -> None:
            info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)

        put(
            "pack.mcmeta",
            json.dumps(
                {
                    "pack": {
                        "pack_format": RESOURCE_PACK_FORMAT,
                        "description": "Dungeon Heroes relic tooltips",
                    }
                },
                indent=2,
            )
            + "\n",
        )
        for ns, entries in lang.items():
            put(
                f"assets/{ns}/lang/en_us.json",
                json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
            )
    return buf.getvalue()


app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def show() -> None:
    """Print the generated tooltip lines."""
    for entries in generate().values():
        for key, text in entries.items():
            typer.echo(f"{key}\n    {text.replace(PERCENT_ESCAPE, '%')}")
    for spell_id, why in SKIPPED.items():
        typer.echo(f"[skipped] {spell_id}: {why}")


@app.command()
def build() -> None:
    """Write the resource pack zip."""
    OUT_ZIP.parent.mkdir(parents=True, exist_ok=True)
    OUT_ZIP.write_bytes(build_zip(generate()))
    typer.echo(f"wrote {OUT_ZIP.relative_to(ROOT)}")


@app.command()
def check() -> None:
    """Exit 1 when the committed zip differs from what the data produces."""
    fresh = build_zip(generate())
    if not OUT_ZIP.exists() or OUT_ZIP.read_bytes() != fresh:
        typer.echo("relic tooltips are stale: run `just relic-tooltips`", err=True)
        raise typer.Exit(1)
    typer.echo("relic tooltips up to date")


if __name__ == "__main__":
    app()
