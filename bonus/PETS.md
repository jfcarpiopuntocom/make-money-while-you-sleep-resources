# Bonus: a little pet that keeps you company

My free status-line pets put a tiny animal at the bottom of your Claude Code window. It blinks, breathes, dozes off, and changes its face when Claude is working or something went wrong. There are 24 to choose from. It is just for fun, and it costs nothing.

- **claude-pets** (English): https://github.com/jfcarpiopuntocom/claude-pets
- **claude-mascotas** (Spanish edition): https://github.com/jfcarpiopuntocom/claude-mascotas

## Install claude-pets (English)

Start your studio (double-click `2-Start-My-Studio.bat`), then type these three lines into Claude Code, one at a time, pressing Enter after each:

```
/plugin marketplace add jfcarpiopuntocom/claude-pets
/plugin install pets@claude-pets
/pets:setup
```

When Claude Code shows a menu or asks you to confirm, choose to install. The kitty comes first.

To pick another pet:

```
/pets            (list all 24, numbered)
/pets 22         (by number, 1 to 24)
/pets octopus    (by name)
/pets random     (let fate decide)
```

If another plugin already uses `/pets`, type `/pets:pets` instead.

To remove it: `/pets:remove`, then `/plugin uninstall pets@claude-pets`. Your old status line comes back.

## Install claude-mascotas (Spanish)

```
/plugin marketplace add jfcarpiopuntocom/claude-mascotas
/plugin install mascotas@claude-mascotas
/mascotas:setup
```

To pick another one: `/mascota` (the list), `/mascota 22`, `/mascota pulpo`, `/mascota azar`. If another plugin already uses `/mascota`, type `/mascotas:mascota`. To remove it: `/mascotas:quitar`, then `/plugin uninstall mascotas@claude-mascotas`.

## Prefer the terminal window?

These lines do the same install without opening Claude Code first (the pets README lists them):

```
claude plugin marketplace add jfcarpiopuntocom/claude-pets
claude plugin install pets@claude-pets
```

Then open Claude Code and ask it: "run the pets setup command". For the Spanish edition, use `claude-mascotas` and `mascotas@claude-mascotas`, then ask for "el comando setup de mascotas".

## Get new pets automatically (optional)

Type `/plugin`, go to **Marketplaces**, choose `claude-pets` (or `claude-mascotas`) and pick **Enable auto-update**. You only do this once.

## If you get stuck

The pets need a small free program called Node on your computer. If you see a message about Node, or the pet does not appear, paste this to Claude:

"I installed the pets plugin but the pet does not show. Check what is missing, explain it in plain words, and help me fix it one step at a time, asking before each step."
