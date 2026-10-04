# Server setup (admin)

The server installs and updates the pack itself on every start, from this repo. You never copy mods by hand.

## Requirements

- **Java 21** on the server.
- **RAM:** 8 GB for the server process (6 GB boots; more players need more).
- **Disk:** about 1 GB for mods and libraries, plus the world.
- **Fabric server** for Minecraft **1.21.1**, loader **0.19.5**. The pack's `pack.toml` lists the exact versions.

## How it works

The server starts with [start.sh](start.sh) and a pack link:

```
bash start.sh <PACK_URL>
```

1. It runs [packwiz-installer-bootstrap](https://github.com/packwiz/packwiz-installer-bootstrap) with `-g -s server <PACK_URL>`:
   - `-g` = no window (servers have no screen).
   - `-s server` = server mods only. Client-only mods (minimaps, shaders, …) are skipped.
   - It downloads only files that changed, and it removes mods that the pack removed.
2. Then it starts Minecraft.

`PACK_URL` for players' version:
```
https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/main/pack.toml
```
A test server can use branch `dev` instead of `main`, or a tag like `v1.0.0` to stay on one version.

## Pterodactyl

1. Create the server with the **Fabric** egg (not a CurseForge modpack egg: the pack runs on Fabric, CurseForge is only one of its download sites):
   - Docker image: **java 21**
   - `MC_VERSION` = `1.21.1`
   - `LOADER_VERSION` = `0.19.5`
2. **Files:** upload these 2 files to the server root (next to `server.jar`):
   - [packwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar)
   - [start.sh](https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/main/docs/start.sh)
3. **Admin → Servers → your server → Startup → Startup Command:**
   ```
   bash start.sh https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/main/pack.toml
   ```
   Do not use `&&` in the startup command. The panel runs it without a shell, so Minecraft starts before the pack update.
4. **Backups:** set the backup limit to 1 or more.
5. **Start.** The first start downloads about 1 GB. The console must show:
   - `Finished successfully!` (pack update, before Minecraft)
   - ``Data pack `dungeon_heroes` loaded successfully!``
   - `Done (…)! For help, type "help"`

## Plain Linux (no panel)

1. In an empty folder, download the Fabric server launcher, the bootstrap and the start script:
   ```
   curl -o fabric-server.jar https://meta.fabricmc.net/v2/versions/loader/1.21.1/0.19.5/1.1.2/server/jar
   curl -LO https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar
   curl -O https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/main/docs/start.sh
   ```
2. Write `eula=true` into `eula.txt` (this accepts Mojang's EULA).
3. Start:
   ```
   bash start.sh https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/main/pack.toml
   ```
   Memory: `SERVER_MEMORY` in MiB (default 8192).

## Updates

- A new pack version is live when a new release `v…` appears under [Releases](https://github.com/maciello/dungeon-heroes-pack/releases). Its notes say what changed.
- **Make a backup first**, then restart the server. It pulls the new version on start.
- Players get the same version at their next launch.

Versions follow MAJOR.MINOR.PATCH:

| bump | means | do |
|---|---|---|
| MAJOR | a mod was removed, or the Minecraft/Fabric version changed | **backup required**: the world loses that mod's blocks and items |
| MINOR | a mod was added or updated | backup recommended |
| PATCH | only settings or data changed | restart |

## Roll back

- **World:** restore the backup from before the update.
- **Mods:** in the startup command, replace `main` with the old tag, for example `https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/v1.0.0/pack.toml`, and restart. Players must use the same version, so tell the host to roll back the pack too.

## Never put in this repo

`server.properties`, `ops.json`, `whitelist.json`, RCON or other passwords, IP addresses. They stay on the server only.

## Troubleshooting

| console shows | fix |
|---|---|
| `Update process failed` before Minecraft starts | Check the pack link (open it in a browser: it must show text starting with `name = "Dungeon Heroes"`). |
| Minecraft starts first, the pack never updates | The startup command has `&&` in it. Use `bash start.sh <PACK_URL>`. |
| `NoClassDefFoundError: net/minecraft/class_…` | A client-only mod got onto the server. Report it to the pack host with the mod name from the log. |
| Server starts but players get "mod mismatch" | Server and players run different pack versions. Restart the server, players relaunch. |
