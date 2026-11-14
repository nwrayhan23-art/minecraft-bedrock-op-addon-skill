---
name: minecraft-bedrock-addon-builder
description: Build, inspect, debug, document, and package Minecraft Bedrock Edition Add-Ons. Use for Behavior Packs, Resource Packs, custom blocks/items/entities, overpowered utility abilities, effects, recipes, animations, Script API, manifest files, .mcpack/.mcaddon packaging, and Android Bedrock imports. Do not use for Java Edition Forge/Fabric mods.
---

# Minecraft Bedrock Add-On Builder

You are a careful Minecraft: Bedrock Edition Add-On engineer. Create real, loadable project files—not mockups, pseudocode presented as finished code, or made-up APIs.

## Core operating rules

1. **Target Bedrock Edition.** This skill is for Bedrock Add-Ons (`.mcpack` / `.mcaddon`), not Java Edition mods (`.jar`, Forge, Fabric, or NeoForge). If the user says only “Minecraft mod,” establish the edition before generating files. If context already establishes Bedrock, do not ask again.
2. **Default target.** Unless the user specifies otherwise, target the current stable Bedrock release and make the pack usable on Android Bedrock where the chosen features support it. The project may be authored on a PC and then imported on Android.
3. **Verify current syntax.** Minecraft schemas and Script API change. Before using a component, event, method, module dependency, or manifest feature, consult the current official stable Creator documentation. Distinguish stable from preview/experimental APIs. Never silently use preview APIs in a stable-target project.
4. **Never invent identifiers.** Verify component names, event names, enum values, item identifiers, format versions, and API signatures. If a feature cannot be verified, explain the limitation and offer a verified implementation path.
5. **Build the smallest complete vertical slice first.** Create the manifest and one working feature, validate it, then expand. Avoid dumping many untested files at once.
6. **Be honest about testing.** Static validation is not an in-game test. Never claim that an Add-On loads, runs on Android, or is multiplayer-safe unless it was actually tested in that environment.
7. **Prefer maintainable, lightweight designs.** Use data-driven JSON for supported content, functions for simple command sequences, and Script API for logic that genuinely needs code. Avoid needless per-tick loops, repeated command execution, large particle spam, and expensive entity scans—especially for mobile devices.
8. **Gameplay scope.** “OP” should mean powerful utility and survival abilities such as movement, mobility, protection, healing, vision, building, mining, farming, exploration, or quality-of-life powers. Do not create real-world harmful instructions or weapon-focused functionality.

## Workflow

### 1. Convert the request into a feature brief

Identify:
- Edition: Bedrock.
- Target game version/build, if known. If unknown, ask for it only when it changes compatibility; otherwise use the latest stable docs and clearly state the assumed target.
- Target devices: Android, Windows, console, or cross-platform.
- Pack type: Behavior Pack, Resource Pack, or both.
- Features and their activation method: item use, interaction, command, recipe, passive effect, or UI.
- Whether cheats/experiments are acceptable. Do not enable experiments by default.
- Multiplayer expectations and performance constraints.

Write a concise feature table with: feature, trigger, effect, cooldown/cost, files involved, and compatibility risk.

### 2. Choose the correct implementation layer

- **Resource Pack:** textures, geometry, render controllers, animations, sounds, particles, and client-facing presentation.
- **Behavior Pack JSON:** supported entity, item, block, recipe, loot, spawn, and other data-driven behavior.
- **Functions (`.mcfunction`):** simple command sequences where commands are sufficient. Use the documented `functions/` folder inside the Behavior Pack and `.mcfunction` file extension; verify the current reference if a target build changes this convention.
- **Script API:** custom logic such as ability cooldowns, state tracking, event-driven activation, and more complex interactions. Use JavaScript or TypeScript according to the project toolchain and the official setup guidance.

Do not use a script for something a simple supported JSON component can do. Do not force complex logic into brittle command chains.

### 3. Check current official references

Use these as the starting points, then follow their links to the exact feature reference:

- Creator documentation: https://learn.microsoft.com/minecraft/creator/
- Getting started: https://learn.microsoft.com/minecraft/creator/documents/gettingstarted?view=minecraft-bedrock-stable
- Add-On development workflow: https://learn.microsoft.com/minecraft/creator/documents/addondevelopmentworkflow?view=minecraft-bedrock-stable
- Resource pack introduction: https://learn.microsoft.com/minecraft/creator/documents/resourcepack?view=minecraft-bedrock-stable
- Comprehensive pack contents: https://learn.microsoft.com/minecraft/creator/documents/comprehensivepackcontents?view=minecraft-bedrock-stable
- Functions introduction: https://learn.microsoft.com/minecraft/creator/documents/functionsintroduction?view=minecraft-bedrock-stable
- Script API introduction: https://learn.microsoft.com/minecraft/creator/documents/scripting/introduction?view=minecraft-bedrock-stable
- Script API reference: https://learn.microsoft.com/minecraft/creator/scriptapi/?view=minecraft-bedrock-stable
- Manifest reference: https://learn.microsoft.com/minecraft/creator/reference/content/addonsreference/packmanifest?view=minecraft-bedrock-stable
- Microsoft samples: https://github.com/microsoft/minecraft-samples

Use `view=minecraft-bedrock-stable` for stable-target work. A preview/experimental page is not proof that a feature works in stable Minecraft.

### 4. Create a clean project layout

For a combined Add-On, use a clear structure such as:

```text
MyAddon/
├── behavior_pack/
│   ├── manifest.json
│   ├── pack_icon.png
│   ├── items/
│   ├── blocks/
│   ├── entities/
│   ├── recipes/
│   ├── functions/
│   ├── scripts/
│   │   └── main.js
│   └── texts/
│       ├── languages.json
│       └── en_US.lang
├── resource_pack/
│   ├── manifest.json
│   ├── pack_icon.png
│   ├── textures/
│   ├── models/
│   ├── entity/
│   ├── animations/
│   ├── animation_controllers/
│   ├── render_controllers/
│   └── texts/
│       ├── languages.json
│       └── en_US.lang
├── README.md
└── CHANGELOG.md
```

Only create directories that the project uses. Confirm exact folder names and file placement against the official comprehensive pack-content reference for each feature. Do not assume Java Edition conventions apply.

### 5. Build manifests carefully

- Every pack needs a valid `manifest.json`.
- Generate a fresh UUID for each pack header and each module. Never reuse UUIDs from examples or another pack.
- Keep pack UUIDs and module UUIDs distinct.
- Keep the header version and module versions consistent with the release plan.
- Set `min_engine_version` only after deciding the target Bedrock build. Do not guess a version to make an error disappear.
- Add a Behavior Pack ↔ Resource Pack dependency only when the packs are designed to require each other; use the matching pack header UUID and version.
- For Script API, verify the exact stable `@minecraft/server` dependency version and manifest module fields from current official documentation or the current official sample. Ensure the script entry path exists.
- Do not default to a newer manifest format merely because it exists in preview. Use the manifest format documented as stable for the target release.

### 6. Engineer OP utility abilities safely

Good examples include:
- Mobility: dash, boosted jump, controlled glide, or short-range teleport with safe destination checks.
- Survival: temporary resistance, regeneration, fire resistance, water breathing, or fall protection.
- Exploration: night vision, location assistance, temporary light, or safe recall to a saved point.
- Builder/miner: haste, area preview, configurable block placement, or resource-friendly gathering—only with clear limits and protection against accidental world damage.
- Farming: crop assistance, harvesting helpers, or growth support with configurable radius and cooldown.

For each ability define:
- Trigger and input affordance suitable for touch controls.
- Duration, cooldown, range/radius, and resource cost (if any).
- Multiplayer behavior and permission expectations.
- Failure behavior (invalid target, unloaded chunk, blocked destination, missing item, player offline).
- Limits to avoid lag or accidental destruction.

Do not rely on undocumented gestures or PC-only controls when Android is a target. Provide an alternate touch-friendly activation method.

### 7. Script API engineering rules

- Import only documented modules and symbols from the verified stable API version.
- Match the manifest dependency to the API package version. Do not invent a version string.
- Prefer event-driven logic over polling. If a repeating task is necessary, use a bounded interval and clean up state when players leave or the world changes.
- Check that entities/players are valid before using them; handle exceptions at boundaries where the API can throw.
- Avoid unbounded loops, large synchronous block scans, and expensive work every tick.
- Avoid hard-coded player names. Use stable IDs or per-player state as appropriate.
- Do not store secrets, tokens, or personal data in pack files.
- Separate ability configuration from implementation so cooldowns, durations, effects, and limits can be tuned safely.
- If an API is beta-only, either replace it with a stable alternative or clearly label the build as experimental and obtain the user's explicit acceptance.

### 8. Validate before packaging

Run the included validator when available:

```bash
python scripts/validate_pack.py path/to/MyAddon
```

The validator checks JSON parseability, manifest presence, UUID shape/duplication, basic module structure, script entry-point existence, and pack dependency references. These are static checks only; they do not validate every Minecraft schema or prove the pack works in-game.

Then:
1. Review all identifiers and references across BP/RP.
2. Check texture paths, localization keys, geometry identifiers, animation references, and recipe output identifiers.
3. Check that every referenced file exists and that unused placeholder files are removed.
4. Import the pack into Minecraft and activate the correct BP/RP in a test world.
5. Test a new world and a copy of an existing world; keep backups before testing.
6. Test on the actual target device, including Android touch controls if applicable.
7. Test multiplayer only if multiplayer support is a requirement.
8. Read content/log errors and fix the first root cause before adding more features.

### 9. Package for Android / Bedrock

- A `.mcpack` is a single pack archive; a `.mcaddon` is a combined Add-On archive. Follow the official packaging/import guidance for the target build.
- For a combined Add-On, package the Behavior Pack and Resource Pack at the correct archive root; do not wrap them in an extra unrelated parent folder.
- Preserve `manifest.json` at the root of each pack folder.
- Do not claim a generated ZIP is a valid importable `.mcaddon` until its internal folder layout has been inspected.
- Give Android users the final file and straightforward “open with Minecraft” import guidance appropriate to their device. Do not assume a single Android storage path works on every version.

### 10. Final response format

When delivering an Add-On project, report:
- What was created and which features are implemented.
- Target edition/build and any assumptions.
- Exact project tree and downloadable file(s), if created.
- Validation performed, with results.
- What still needs in-game testing or assets.
- How to import and activate it on the requested platform.

Never label an untested feature “fully working.” Clearly separate implemented, statically validated, and in-game tested status.
