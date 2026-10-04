# Dungeon Heroes (RPG Series)

A Minecraft 1.21.1 RPG modpack: classes, spells, bosses, dungeons. It updates itself every time you start the game.

**Running the server?** See [docs/SERVER.md](docs/SERVER.md).

---

## Before you start

You need:

- A PC with **16 GB RAM** (the game uses 8 GB) and about **3 GB** of free disk space.
- **Minecraft Java Edition** bought on your Microsoft account.
- The **server address** and an **invite** from the host. Ask them.

## Step 1: Install Java 21

Minecraft 1.21.1 needs Java 21. The launcher does not install it for you.

- **Windows / macOS:** go to <https://adoptium.net/temurin/releases/?version=21>, download the **JRE 21** installer for your system, and run it. Click *Next* until it is done.
- **Linux:** install the `openjdk-21-jre` package (Ubuntu/Debian/Mint) or `jre21-openjdk` (Arch). Or use Adoptium like above.

## Step 2: Install PolyMC

1. Go to <https://polymc.org/download/>.
2. **Windows:** download the **Installer (.exe)** and run it.
   **macOS:** download the macOS file, unpack it, and move PolyMC to *Applications*.
   **Linux:** download the **AppImage**, make it executable (right-click → *Properties → Allow executing*), and start it.
3. Start PolyMC. The first-start window asks for language and Java:
   - Click **Auto-detect** and pick the entry that says **21**.
   - Leave memory as it is. The pack sets its own.

## Step 3: Add your Microsoft account

1. In PolyMC, click **Accounts** (top right) → **Manage Accounts** → **Add Microsoft**.
2. A browser page opens. Log in with the account that owns Minecraft.
3. Back in PolyMC, your name appears. Close the window.

## Step 4: Add the pack (one time)

1. Click **Add Instance** (top left).
2. On the left, click **Import from zip**.
3. Paste this link into the field and click **OK**:
   ```
   https://github.com/maciello/dungeon-heroes-pack/releases/download/instance/DungeonHeroes-main.zip
   ```
4. A new instance **Dungeon Heroes** appears.

## Step 5: First start

1. Select **Dungeon Heroes** and click **Launch**.
2. A window **Updating modpack** opens and downloads about 1100 files. The first time takes a few minutes. Wait.
3. If it asks to update the Minecraft or Fabric version, click **Yes**. If the game does not start after that, click **Launch** again.
4. The game opens. The first start is slow (it loads about 340 mods).

## Step 6: Join the server

1. Click **Multiplayer → Add Server**.
2. Enter the address from the host. Click **Done**, then **Join Server**.

---

## Updates

You do nothing. Each launch checks for a new pack version and downloads only what changed.

If the server kicks you with a mod mismatch, close the game and launch again.

## Problems

| problem | fix |
|---|---|
| "Java" error when you click Launch | Right-click the instance → **Edit → Settings → Java** → tick *Java installation* → **Auto-detect** → pick **21**. |
| Game crashes with "out of memory" | Same place → *Memory* → set **Maximum memory** to 8192 MB or more. |
| Download failed | Click **Launch** again. It continues where it stopped. |
| A window asks you to download a file by hand | Tell the host. Do not download mods from other sites. |
| Cannot connect to the server | Check the address and your invite with the host. |

## Good to know

- Your own settings (keys, video, sound) are yours. Updates never change them.
- Mod settings that come with the pack can reset when the pack updates.
- Do not add or remove mods in this instance. Your game must match the server.
- The pack version shows in the *Updating modpack* window. All versions: [Tags](https://github.com/maciello/dungeon-heroes-pack/tags).
