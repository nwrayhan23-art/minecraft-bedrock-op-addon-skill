# Bedrock Add-On project layout notes

A combined project usually has one Behavior Pack and one Resource Pack. Each pack has its own `manifest.json`, header UUID, module UUID(s), and version. The exact directories depend on the content being built; create only what is needed and verify every path against the current official reference.

## Typical Behavior Pack content

- `blocks/`
- `entities/`
- `items/`
- `recipes/`
- `functions/` (for `.mcfunction` files)
- `loot_tables/`
- `spawn_rules/`
- `scripts/`
- `texts/`

## Typical Resource Pack content

- `textures/`
- `models/`
- `entity/`
- `animations/`
- `animation_controllers/`
- `render_controllers/`
- `particles/`
- `sounds/`
- `texts/`

The list is illustrative, not a schema. Some folders are required only by particular features. Folder naming can be case-sensitive in tools and must match the Creator documentation.

## Manifest reminders

- Each pack header UUID must be unique.
- Each module UUID must be unique and different from the header UUID.
- Pack dependencies refer to the required pack's **header UUID**, with a compatible version.
- Script modules require a valid script entry point and a documented Script API dependency.
- Use the manifest format and fields supported by the target stable Bedrock version.

## References

- https://learn.microsoft.com/minecraft/creator/documents/comprehensivepackcontents?view=minecraft-bedrock-stable
- https://learn.microsoft.com/minecraft/creator/reference/content/addonsreference/packmanifest?view=minecraft-bedrock-stable

- Functions tutorial: https://learn.microsoft.com/minecraft/creator/documents/functionsintroduction?view=minecraft-bedrock-stable
