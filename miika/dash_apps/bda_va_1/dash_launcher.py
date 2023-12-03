from dash import Input, Output
from ..dash_helpers import make_dash_app
from .make_dataset import gdp_dataset
from .dash_layout import gdp_layout
from .plotter import gdp_plot

# Create the named DjangoDash app
app = make_dash_app("bda_va_1")
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