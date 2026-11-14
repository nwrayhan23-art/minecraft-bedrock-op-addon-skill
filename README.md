# Minecraft Bedrock OP Add-On Builder Skill

An Agent Skill for helping an AI coding agent create, validate, debug, document, and package **Minecraft: Bedrock Edition Add-Ons**—with an emphasis on powerful utility abilities and Android-friendly controls.

## What it helps with

- Behavior Packs and Resource Packs
- Custom utility items, blocks, recipes, entities, effects, animations, and particles
- OP-style non-weapon abilities: mobility, survival, exploration, building, mining, and farming
- JavaScript / TypeScript with the Minecraft Bedrock Script API
- `manifest.json`, UUIDs, pack dependencies, localization, and project structure
- Static validation and `.mcpack` / `.mcaddon` packaging workflows
- Android Bedrock import and touch-control considerations

## Install / use

1. Upload this repository or folder to GitHub.
2. Give your AI agent the skill folder, or install it using the skill-loading mechanism supported by that agent.
3. The skill entry point is `SKILL.md`.
4. Keep the official documentation links current; Minecraft schemas and Script API versions change over time.

> This is an AI instruction skill, not a Minecraft Add-On itself. It guides an agent to create the actual Add-On project.

## Included files

```text
.
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
│   ├── project-layout.md
│   └── release-checklist.md
├── examples/
│   └── ability-brief.md
└── scripts/
    └── validate_pack.py
```

## Static validation

Requires Python 3.9+ and uses only the Python standard library:

```bash
python scripts/validate_pack.py path/to/MyAddon
```

The validator performs structural checks; it is not a replacement for Minecraft's own content validation or testing in a real Bedrock world.

## Official references

- [Minecraft Bedrock Creator Documentation](https://learn.microsoft.com/minecraft/creator/)
- [Add-On development workflow](https://learn.microsoft.com/minecraft/creator/documents/addondevelopmentworkflow?view=minecraft-bedrock-stable)
- [Comprehensive pack contents](https://learn.microsoft.com/minecraft/creator/documents/comprehensivepackcontents?view=minecraft-bedrock-stable)
- [Functions introduction](https://learn.microsoft.com/minecraft/creator/documents/functionsintroduction?view=minecraft-bedrock-stable)
- [Script API introduction](https://learn.microsoft.com/minecraft/creator/documents/scripting/introduction?view=minecraft-bedrock-stable)
- [Script API reference](https://learn.microsoft.com/minecraft/creator/scriptapi/?view=minecraft-bedrock-stable)
- [Manifest reference](https://learn.microsoft.com/minecraft/creator/reference/content/addonsreference/packmanifest?view=minecraft-bedrock-stable)
- [Microsoft Minecraft samples](https://github.com/microsoft/minecraft-samples)

## License

MIT. See [LICENSE](LICENSE).
