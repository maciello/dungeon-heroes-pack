default:
    @just --list

# Regenerate relic tooltips from the spell/effect data, then refresh the packwiz index.
relic-tooltips:
    uv run tools/relic_tooltips.py build
    packwiz refresh

# Fail if the committed relic tooltip pack no longer matches the data.
relic-tooltips-check:
    uv run tools/relic_tooltips.py check

# Print the generated relic tooltip lines.
relic-tooltips-show:
    uv run tools/relic_tooltips.py show

# Pin impact triggers of relic passives to ACTIVE spells (no self/cross triggering), then refresh the index.
relic-trigger-guard:
    uv run tools/relic_trigger_guard.py apply
    packwiz refresh

# Fail if a relic impact trigger can match passive-spell impacts.
relic-trigger-guard-check:
    uv run tools/relic_trigger_guard.py check
