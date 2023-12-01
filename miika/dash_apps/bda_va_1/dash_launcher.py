import os
import json
from django_plotly_dash import DjangoDash
from dash import Input, Output
import dash_bootstrap_components as dbc
if os.getenv('OVH_APP_ENGINE_VERSION', None) == "3.8":
    from importlib_resources import files
else:
    from importlib.resources import files
import plotly.io as pio
from .make_dataset import gdp_dataset
from .dash_layout import gdp_layout
from .plotter import gdp_plot

# Theming Dash
# Stylesheet with the .dbc class to style dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = DjangoDash("bda_va_1", external_stylesheets=[dbc.themes.VAPOR, dbc.icons.FONT_AWESOME, dbc_css])
# inject the bootstrap figure template into plotly
with (files("dash_bootstrap_templates") / "templates" / "vapor.json").open() as f: # type: ignore
            template = json.load(f)
pio.templates["VAPOR"] = template
# Load data to dataframe
df = gdp_dataset()
# Create Dash layout
app.layout = gdp_layout(df) # type: ignore
# Callback methods
@app.callback(
    # Outputs updated Plotly figure
    Output(component_id="gdp-graph", component_property="figure"),
    # Takes in the countries selected in the multi dropdown
    Input(component_id="country-dropdown", component_property="value"),
)
def update_graph(countries):
    fig = gdp_plot(df, countries)
    return fig