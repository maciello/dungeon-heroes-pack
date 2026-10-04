# Server setup (admin)

The server installs and updates the pack itself on every start, from this repo. You never copy mods by hand.

## Requirements

- **Java 21** on the server.
- **RAM:** 8 GB for the server process (6 GB boots; more players need more).
- **Disk:** about 1 GB for mods and libraries, plus the world.
- **Fabric server** for Minecraft **1.21.1**, loader **0.19.5**. The pack's `pack.toml` lists the exact versions.

## How it works

On every start, the server runs [packwiz-installer-bootstrap](https://github.com/packwiz/packwiz-installer-bootstrap) before Minecraft:

```
java -jar packwiz-installer-bootstrap.jar -g -s server <PACK_URL>
```

- `-g` = no window (servers have no screen).
- `-s server` = server mods only. Client-only mods (minimaps, shaders, …) are skipped.
- It downloads only files that changed, and it removes mods that the pack removed.

`PACK_URL` for players' version:
```
https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/main/pack.toml
```
A test server can use branch `dev` instead of `main`, or a tag like `v1.0.0` to stay on one version.

## Pterodactyl

1. Create the server with a **Fabric** egg: Minecraft **1.21.1**, loader **0.19.5**, Java 21 image.
2. **Files:** download [packwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar) and upload it to the server root (next to the server jar).
3. **Startup → Variables:** add `PACK_URL` with the link above. (If your egg does not allow new variables, put the link straight into the command.)
4. **Startup → Command:**
   ```
   java -jar packwiz-installer-bootstrap.jar -g -s server {{PACK_URL}} && java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar {{SERVER_JARFILE}} nogui
   ```
5. **Backups:** set the backup limit to 1 or more.
6. **Start.** The first start downloads about 1 GB. The console must show:
   - ``Data pack `dungeon_heroes` loaded successfully!``
   - `Done (…)! For help, type "help"`

## Plain Linux (no panel)

1. Download the Fabric server launcher for Minecraft 1.21.1, loader 0.19.5:
   ```
   curl -o fabric-server.jar https://meta.fabricmc.net/v2/versions/loader/1.21.1/0.19.5/1.1.2/server/jar
   ```
2. Put `packwiz-installer-bootstrap.jar` next to it.
3. Write `eula=true` into `eula.txt` (this accepts Mojang's EULA).
4. Start script (`start.sh`):
   ```
   java -jar packwiz-installer-bootstrap.jar -g -s server https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/main/pack.toml \
     && java -Xmx8G -jar fabric-server.jar nogui
   ```

## Updates

- A new pack version is live when a new tag `v…` appears under [Tags](https://github.com/maciello/dungeon-heroes-pack/tags).
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
- **Mods:** set `PACK_URL` to the old tag, for example `https://raw.githubusercontent.com/maciello/dungeon-heroes-pack/v1.0.0/pack.toml`, and restart. Players must use the same version, so tell the host to roll back the pack too.

## Never put in this repo

`server.properties`, `ops.json`, `whitelist.json`, RCON or other passwords, IP addresses. They stay on the server only.

## Troubleshooting

| console shows | fix |
|---|---|
| `Update process failed` before Minecraft starts | Check `PACK_URL` (open it in a browser: it must show text starting with `name = "Dungeon Heroes"`). |
| `NoClassDefFoundError: net/minecraft/class_…` | A client-only mod got onto the server. Report it to the pack host with the mod name from the log. |
| Server starts but players get "mod mismatch" | Server and players run different pack versions. Restart the server, players relaunch. |
