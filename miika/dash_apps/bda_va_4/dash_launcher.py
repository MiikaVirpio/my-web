from dash import Input, Output
from ..dash_helpers import make_dash_app
from .make_dataset import make_dataset
from .dash_layout import app_layout
from .plotter import plot_graph

# Create the named DjangoDash app
app = make_dash_app("bda_va_4")
# Load data to dataframe and get employees and permissions
df, employees, permissions = make_dataset()
# Create Dash layout
app.layout = app_layout(df, employees, permissions) # type: ignore
# Callback methods
@app.callback(
    # Outputs updated Plotly figure
    Output(component_id="graph", component_property="figure"),
    # Takes in the countries selected in the multi dropdown
    Input(component_id="employee-dropdown", component_property="value"),
)
def update_graph(employees):
    graph = plot_graph(df, employees, permissions)
    return graph