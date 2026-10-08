# Rules for agents in this repo

Players download `main`. A push to `main` goes straight into their game.

- Never push to `main`. Only the release step (`just release`, run by the pack owner) writes `main`.
- Never push to `dev`. `just publish` writes `dev` from the source game instance.
- To make a change: push a branch `claude/<topic>` and open a pull request into `dev`. The pack owner merges and releases it.
- Every publish copies `config/`, `datapacks/`, `global_packs/`, `scripts/` and `mods/` from the source game instance. A change there that is only in this repo is lost. Name each such file in the pull request.
- Generated files: run the generator (`just --list`), commit its output, and name the command in the pull request.
