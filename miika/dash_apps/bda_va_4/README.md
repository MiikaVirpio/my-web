# ✨Visualization: Assignment 4

Given CSV data for data access permissions, how can you visualize data? I went for heatmap having text labels of permissions. There is a lot of combinations:

$$ comb = Emp^2Perm! $$

where employee matrix cells are all possible combination of permissions between the employees. In our test data case:

$$ 10^2*3*2*1$$

[Visualization at live site](https://miika.virpio.fi/dash-apps/bda-va-4)

## Code brakedown

### [dash_launcher.py](dash_launcher.py)

The `app` from this file is named and is usable with Django tag in the template provided the DjangoDash class is used. Otherwise the Dash app works as usual.

### [make_dataset.py](make_dataset.py)

Here the raw data is loaded and cleaned for visualization.

### [dash_layout.py](dash_layout.py)

This where the html / bootstrap components for the Dash app are built and where ids for input and output are defined. For html allergic pythonista this is quite a sleek way of creating web content.

### [plotter.py](plotter.py)

All things Plotly in this file.

