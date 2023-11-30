from django_plotly_dash import DjangoDash
from dash import callback, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from .make_dataset import gdp_dataset
from .dash_layout import gdp_layout
from .plotter import gdp_plot

# Theming Dash
# Choose theme from https://hellodash.pythonanywhere.com/
theme = "VAPOR"
# Stylesheet with the .dbc class to style dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = DjangoDash("bda_va_1", external_stylesheets=[getattr(dbc.themes, theme), dbc.icons.FONT_AWESOME, dbc_css])
load_figure_template(theme)
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