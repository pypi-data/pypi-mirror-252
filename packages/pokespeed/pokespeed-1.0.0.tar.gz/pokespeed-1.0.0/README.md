# pokespeed

A command-line utility for calculating Pokemon speed tiers for a particular format.

To install from [PyPI]():
```
pip install pokespeed
```

To use, just run:
```
pokespeed
```

Or optionally supply the CSV location, Pikalytics URL (supplying a Pikalytics url like `https://www.pikalytics.com/pokedex/gen9vgc2023regulatione` will let you specify the format), or Pokemon level (50 for VGC):
```
pokespeed --out ./outspeed_benchmarks.csv --url https://ww.pikalytics.com --level 50
```

Then, view the resulting CSV file in your favorite spreadsheet viewer (e.g. Google Sheets) to see the generated output. Interpreting the output is relatively straightforward:
* Each row corresponds to a speed.
* Each column corresponds to a stat stage:
  * `-2` is two negative stat changes.
  * `-1` is a negative stat change (e.g. icy wind).
  * `+0` is no stat change.
  * `+1` is a positive stat change (e.g. dragon dance, choice scarf, speed booster energy).
  * `+2` is two positive stat changes (e.g. tailwind).
  * `-1 x2` is a negative stat change (e.g. icy wind) multiplied by 2 (e.g. tailwind).
  * `+1 x2` is a positive stat change (e.g. choice scarf) multiplied by 2 (e.g. tailwind).
* Each cell corresponds to the Pokemon you **outspeed** if you have that row's speed and you are under the effects of that column's speed modifier. (So the speed in the row isn't the speed that each of the listed Pokemon hit; it's the speed you need to outspeed them.)
  * `pokemon+` means `252+` in speed (e.g. timid or jolly).
  * `pokemon=` means `252` in speed (e.g. modest or adamant).
  * `+1 pokemon+` means `252+` in speed with a stat modifier of `+1` (these modifiers are exactly as in the columns).

For an example of what this tool's output looks like, see [here](https://docs.google.com/spreadsheets/d/11ml2mJ-k86F5jxlj2Ziav7uw73nNfJkA_19DEM1uDFM/edit?usp=sharing).
