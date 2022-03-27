<!-- https://pyweek.readthedocs.io/en/latest/help.html#how-to-submit-your-entry -->
# Mirror Mirror

When Commander Leto receives a letter from the Prince of the Snailfish,
she discovers that the infamous criminal stealing all of the stars in
the galaxy is none other than a version of herself from another dimension!
Can she retrieve the stars before her evil twin escapes with them and restore balance to the universe?

## Installing requirements

To download the required PyPI packages, run:

```sh
pip install -r requirements.txt
```

from this directory.

The game has been tested on Windows and MacOS with Python 3.10, but should also work with Python 3.9.

## Running the game

To play the game, run:

```sh
python -m EvilTwin
```

also from this directory, or run the `run_game.py` script.

## Controls

• Arrow keys or WASD to choose your direction of movement.

• `r` to restart level.

• ESC will take you back to the previous page.

• Press keys or click to speed through the intro.

## Make Your Own Level

• Running the included `LevelEditor.py` file (in the `GameTools` folder) in a terminal will open a level editor.

• The editor consists of three main components:

    • The currently open level
    • The tile pallete
    • The toolbar

• The toolbar lets you select from a few functions:

    • Brush - Allows you to paint a tile across the level

    • R_Sel (Rect Selector) - Allows you to select a rectangle and paint it. 
      (There's a little green indicator for your first corner, drag and release)

    • Remove Items - Allows you to remove items from the level.
      Items are anything with a transparent background, plus the player start, enemy start, switch and stars.

    • Player, Enemy, Star, Switch - Allows you to place these items on the level.

    • Play - Opens the main game window in parallel. You can test your levels while editing, 
      just use `Save_to` and go to menu and back within the main game window.

    • Load_from - Allows you to load a level from a file. 
      Enter a number into the terminal when prompted to load the level, 
      or generate a new level if that number doesn't exist.
      (You can use this to edit levels from the main game O_O)
      If you make a new level, start from level numbers 12+ to avoid clashes, 
      and you should be able to access your new level from the main game.

    • Save - Saves the current level to the levels folder, under the name you used in `Load_from`.

• Other stuff:

    • Middle-clicking a tile in the main level area will select the tile to paint with.
    • Left/middle-clicking on a tile in the palette will automatically switch you to brush/rect mode, 
      and select the tile to paint with.
    • The boulder item and the blue hatched tile are special, 
      representing walls that will appear/disppear post-switch activation respectively.
## Artwork

• The tiles and player animations were made by Laurie Noel (`@LaurieNoelArt`), taken from her `itch.io` page, where they are freely available.

• The 8-bit game font is by `AbasCreative` on `fontspace.com`.

• The evil twin animations were made by us, based on the player animations.

• The rest of the art was made purely by us.

## Who is "us"?

• `applе#2775`

• `Cheeki#0376`

• `Ning1253#1269`
