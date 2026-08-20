# Cauldron Color Calculator

A helper tool for automatically calculating and rendering dye mixing results in water-logged cauldrons in Minecraft.

## Features

- **Mixing preview**: Real-time display of color changes in the cauldron as dyes are selected.
- **Version support**: Supports BE1, BE3, BE4, BE5, BE6, BE7. (BE5 and BE7 are identical; BE2 is omitted as no water level can be displayed in this version.)
- **Water level support**: Supports water levels 2-6. (Levels 0-1 are not visible from this perspective and are therefore omitted.)
- **Intelligent sequence calculation**: Input a target color and the program automatically calculates the optimal dye sequence. (Genetic algorithm)
- **Batch rendering**: Renders all valid dye sequences within a specified length range at once. The validity of sequences follows the latest proposals on dyed cauldron render naming in the zh.minecraft.wiki forums: Diff/1457167 and amendments Diff/1457170 and Diff/1457173.
- **Image export**: Exports the current cauldron state as a PNG image. The naming convention follows the latest proposals on dyed cauldron render naming in the zh.minecraft.wiki forums: Diff/1457167 and amendments Diff/1457170 and Diff/1457173.
- **Multi-language support**: Simplified Chinese, Traditional Chinese, English, Japanese.

## Usage

### Manual Rendering

1. Select the game version (BE1, BE3, BE4, BE5, BE6, BE7)
2. Select the water level (Level 2-6)
3. Click dye buttons to add them to the sequence
4. Watch the cauldron color change in real time
5. Export the current state as an image

### Batch Rendering

In the "Batch Render" dialog, set:
- Sequence length range
- Target version
- Target water level

The program will automatically generate all valid combinations and export them as images.

## Asset Copyright Notice

The texture files used in this program (the `textures/` directory) are the property of **Mojang Studios / Microsoft** and are used for non-commercial purposes only, in accordance with the [Minecraft End User License Agreement](https://www.minecraft.net/terms).

This program is an unofficial fan tool and is **not affiliated with Mojang Studios or Microsoft**.

## Dependencies

- Python 3.13.5
- Pillow
- NumPy
- Tkinter (included with Python)

## Run

python CauldronCalculator.py

## Acknowledgments

- Mojang Studios for creating the game Minecraft
- All players and Wiki contributors who provided feedback and suggestions
