# Release checklist

## Before release

- [ ] Bedrock Edition and target build are stated.
- [ ] All manifest files parse as JSON.
- [ ] Every UUID is valid and unique across the project.
- [ ] All pack dependencies reference the intended pack header UUID and version.
- [ ] Script entry paths exist and the `@minecraft/server` dependency matches the verified API version.
- [ ] All JSON identifiers and cross-pack references have been checked.
- [ ] Textures, geometry, animations, sounds, and localization files referenced by JSON exist.
- [ ] No preview/experimental API is used in a stable build unless explicitly accepted.
- [ ] No placeholder assets or TODO code are presented as complete.
- [ ] Runtime work is bounded and suitable for the target device.

## Test

- [ ] Import into a disposable test world.
- [ ] Activate the correct Behavior Pack and Resource Pack.
- [ ] Test each feature trigger and its failure cases.
- [ ] Test mobile/touch input when Android is a target.
- [ ] Check content/log errors.
- [ ] Test multiplayer if promised.
- [ ] Keep a backup before testing an existing world.

## Package

- [ ] `.mcpack` / `.mcaddon` archive structure has been inspected.
- [ ] `manifest.json` is at the root of each pack folder inside the archive.
- [ ] Combined pack dependencies and version numbers are correct.
- [ ] Final release notes state what was and was not tested.
