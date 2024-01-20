# wunplots
Automating plot formatting

# Basic Usage

```python
from pathlib import Path

from wuncolors import ColorPalette, utils
from wunplots import Plotting

# See wuncolors package
palpath = Path(__file__)/"color_palette.toml"
colors = ColorPalette.from_toml(palpath, "example")

p = Plotting()

n = 1000
p.cycler_colors = utils.gradient(colors.all_colors("blue"), colors.all_colors("red"), n=n)
fig, ax = p.new(width=3, nrows=3, ncols=3)

for x in range(0, n):
    ax[0, 0].plot([x/n, x/n], [0, 1], label=x)

p.show()
```

It can also be used by creating a new class inheriting from Plotting with more attributes and it can contain all your plotting boilerplate code to be later re-used.
