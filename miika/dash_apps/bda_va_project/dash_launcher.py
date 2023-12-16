from dash import Input, Output
from ..dash_helpers import make_dash_app
from .make_dataset import stock_data
from .dash_layout import app_layout
from .plotter import plot_scatter, plot_lines, plot_sunburst, plot_trader

app = make_dash_app("bda_va_project")
df, prices = stock_data()
app.layout = app_layout(df) # type: ignore
# Callback functions
# Market cap buttons
@app.callback(
    Output(component_id="company-dropdown", component_property="value"),
    Input(component_id="category-radio", component_property="value"),
)
def update_companies(category):
    if category == "All":
        return df["name"]
    elif category == "Small Cap":
        return df.loc[df["mcap"] < 300, "name"]
    elif category == "Mid Cap":
        return df.loc[(df["mcap"] >= 300) & (df["mcap"] < 1000), "name"]
    elif category == "Large Cap":
        return df.loc[df["mcap"] >= 1000, "name"]
    elif category == "Empty":
        return []
# Scatter graph callback
@app.callback(
    Output(component_id="scatter-graph", component_property="figure"),
    Input(component_id="company-dropdown", component_property="value"),
    Input(component_id="x-radio", component_property="value"),
    Input(component_id="y-radio", component_property="value"),
    Input(component_id="size-radio", component_property="value"),
    Input(component_id="color-radio", component_property="value"),
)
def update_scatter(companies, x_column, y_column, size_column, color_column):
    scatter_graph = plot_scatter(df, companies, x_column, y_column, size_column, color_column)
    return scatter_graph
# Lines graph callback
@app.callback(
    Output(component_id="lines-graph", component_property="figure"),
    Input(component_id="company-dropdown", component_property="value"),
)
def update_lines(companies):
    lines_graph = plot_lines(df, prices, companies)
    return lines_graph
# Sunburst graph callback
@app.callback(
    Output(component_id="sunburst-graph", component_property="figure"),
    Input(component_id="company-dropdown", component_property="value"),
)
def update_sunburst(companies):
    sunburst_graph = plot_sunburst(df, companies)
    return sunburst_graph
# Trader graph callback
@app.callback(
    Output(component_id="trader-graph", component_property="figure"),
    Input(component_id="trader-company-dropdown", component_property="value"),
)
def update_trader_graph(company):
    trader_graph = plot_trader(df, prices, company)
    return trader_graph