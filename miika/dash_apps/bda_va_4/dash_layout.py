from dash import html, dcc
import dash_bootstrap_components as dbc

def app_layout(df, employees, permissions):
    layout = dbc.Container(
        [
            dbc.Row([html.H1("Data permission matrix", className="text-center")], class_name="mt-4"),
            dbc.Row([
                dbc.Col([dcc.Graph(id="graph", figure={})], md=12),      
            ]),
            dbc.Row([
                dbc.Label("Select Employees"),
                dcc.Dropdown(
                    id="employee-dropdown",
                    options=[{"label": i, "value": i} for i in employees],
                    value=employees,
                    multi=True
                )
            ]),
        ],
        fluid=True,
        class_name="dbc",
    )
    return layout