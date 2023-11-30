from dash import html, dcc
import dash_bootstrap_components as dbc

def gdp_layout(df):
    layout = dbc.Container(
        [
            dbc.Row([html.H1("Countries GDP over past 50 years", className="text-center")], className="mt-4"),
            dbc.Row([dcc.Graph(id="gdp-graph", figure={})]),
            dbc.Row([
                dbc.Label("Select Countries"),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": i, "value": i} for i in df.columns],
                    value=["United States", "China", "Japan", "Germany", "India"],
                    multi=True
                )
            ]),
            dbc.Row([html.P("Source: World Bank - https://data.worldbank.org")], className="my-4"),
        ],
        fluid=True,
        className="dbc",
    )
    return layout