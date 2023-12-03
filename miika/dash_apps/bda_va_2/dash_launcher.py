from dash import Input, Output
from ..dash_helpers import make_dash_app
from .make_dataset import make_dataset
from .dash_layout import app_layout
from .plotter import plot_structure, plot_monthly

# Create the named DjangoDash app
app = make_dash_app("bda_va_2")
# Load data to dataframe
df = make_dataset()
# Create Dash layout
app.layout = app_layout(df) # type: ignore
# Callback methods
@app.callback(
    # Outputs updated Plotly figures
    Output(component_id="structure-graph", component_property="figure"),
    Output(component_id="monthly-graph", component_property="figure"),
    # Takes in the countries selected in the multi dropdown
    Input(component_id="segment-checklist", component_property="value"),
)
def update_graph(segments):
    structure_graph = plot_structure(df, segments)
    monthly_graph = plot_monthly(df, segments)
    return structure_graph, monthly_graph