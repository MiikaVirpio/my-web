# ✨Visualization: Assignment 1

First assignment for visualization. Dash app did not work well with Google Colab and Heroku had removed free deployment. Render would be option today. Ended up using hosting I already have for several sites and forgot to ins and outs of Django through that.

[Visualization at live site](https://miika.virpio.fi/dash-apps/bda-va-1)

## Code brakedown

### [dash_launcher.py](dash_launcher.py)

The `app` from this file is named and is usable with Django tag in the template provided the DjangoDash class is used. Otherwise the Dash app works as usual.

### [make_dataset.py](make_dataset.py)

Here the raw data is loaded and cleaned for visualization.

### [dash_layout.py](dash_layout.py)

This where the html / bootstrap components for the Dash app are built and where ids for input and output are defined. For html allergic pythonista this is quite a sleek way of creating web content.

### [plotter.py](plotter.py)

All things Plotly in this file. It can go quite verbose so there might be opportunity to split premade definitions, like `legend_top_left()` or `arrow(x,y,text,direction)`.

