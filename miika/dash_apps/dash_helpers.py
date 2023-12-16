import json
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.io as pio
# Old python on server
from importlib_resources import files
# Fresh python local. Comment for server.
#from importlib.resources import files

VAPOR_SEQUENCE = [
    "#6F42C1",
    "#EA39B8",
    "#3CF281",
    "#1BA2F6",
    "#FFC107",
    "#E44C55",
    "#44D9E8",
]

def make_dash_app(name):
    """Create a DjangoDash app with the given name and return a DjangoDash object.

    Args:
        name (str): Name of the Dash app.

    Returns:
        DjangoDash: DjangoDash app object.
    """
    # Theming Dash
    # Stylesheet with the .dbc class to style dcc, DataTable and AG Grid components with a Bootstrap theme
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    app = DjangoDash(name, external_stylesheets=[dbc.themes.VAPOR, dbc.icons.FONT_AWESOME, dbc_css])
    # inject the bootstrap figure template into plotly
    with (files("dash_bootstrap_templates") / "templates" / "vapor.json").open() as f: # type: ignore
                template = json.load(f)
    pio.templates["VAPOR"] = template
    return app