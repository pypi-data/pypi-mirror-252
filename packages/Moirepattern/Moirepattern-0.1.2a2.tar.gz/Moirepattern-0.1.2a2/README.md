# Moirepattern

Moirepattern is a Python library that enables the creation of moire patterns. Currently, it can generate simple moire patterns by controlling the angle and distance between interferences, and these can be added to form new moire patterns. Additionally, cylinder-shaped moire patterns are supported. In the future, it is planned to have construction operations that would allow the user to make any shape, in 2 or 3 dimensions, and several predefined geometries.

## Installation

You can install Moirepattern via pip using the following command:

```bash
pip install Moirepattern
```
## Initializing a Moire Object

To start creating moire patterns, you first need to initialize a Moire object. This is done using the `Moire` constructor, which takes three parameters:

- `interference_distance`: This is the distance between two interference lines. In 3D cases, this represents the distance on the surface without distortion.

- `base_grid_gap`: This is the gap between the lines forming the base grid. The base grid is an equidistant grid overlaid to create the desired moire pattern.

- `angle`: This is the angle of the interference lines.

Here's an example of how to create a Moire object:

```python
moire = Moirepattern.Moire(interference_distance, base_grid_gap, angle)
```
In this code, `interference_distance`, `base_grid_gap`, and `angle` should be replaced with the values you want to use for your moire pattern.

## Usage

### Setting the Size

You can define the size of the moire pattern using the `set_size` method. This method takes two parameters:

- `x_size`: The size of the pattern in the x-direction.
- `y_size`: The size of the pattern in the y-direction.

Here's an example of how to set the size of a moire pattern:

```python
moire.set_size(x_size, y_size)
```
In this code, `x_size` and `y_size` should be replaced with the dimensions you want for your moire pattern.

### Creating a Moire Pattern

Generate the moire pattern by specifying the interference type. Currently, only "Simple" and "Cylinder" interference are supported.

```bash
moire.make("Simple")
```
## Construction operations

**Add**

You can add two moire patterns together to create a new one using the `add` method. This method takes two optional parameters: `space_factor` and `Autody` (which defaults to `True`).

```bash
moire_2 = Moirepattern.Moire(interference_distance, base_grid_gap, angle)
moire.add(moire_2) 
```
If Autody is set to True, the interference distance of moire_2 will be adjusted to align the interferences of the two moire patterns. It's generally not recommended to modify space_factor; it may be removed in future versions. The purpose of this variable is to generate extra lines for correct alignment.

After using the `add` method, the `moire` object becomes a compound moire. This means you cannot use the `add` method again on this object. Instead, you should use the `add_compound` method. Here's how you can use it:

```python
moire.add_compound(moire_2, space_factor)
```

In the above code, `moire_2` is the second moire pattern that you want to add to the compound moire. The `space_factor` parameter is optional and it's an integer.

# Visualizing Results

You can visualize the moire pattern using `moire.visualize()`. This will open a new window showing the 2 layers (base and interference grid). The base layer can be manipulated to see the movement of the pattern.

## Exporting Results

You can export the generated moire pattern and the base grid using the following methods:

- `export(filename)`: Exports the moire pattern to a file.
- `export_base(filename)`: Exports the base grid to a file.

## Accessing Lines

You can access the lines generated in the moire pattern using the `.poly` attribute, which returns an array containing arrays of points defining each line.

```python
lines = moire.poly
```
If the moire pattern is Simple, you can access the pattern gap with `moire.gap`, the first x coordinate where a line cuts the center with `moire.first_pos` and the last x coordinate with `moire.last_pos`.

Size can be accessed using `moire.xsize` and `moire.ysize`.

## Example Usage

```python
import Moirepattern as mp

moire = mp.Moire(10, 5, 30)
moire.set_size(800, 600)
moire.make("simple")
moire.export("moire_pattern.svg")
moire.export_base("base_grid.svg")

lines = moire.poly
print(lines)
```
## Changelog

Changelog introduced in v 0.0.2a1
