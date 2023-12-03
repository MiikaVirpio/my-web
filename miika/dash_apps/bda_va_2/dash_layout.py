from dash import html, dcc
import dash_bootstrap_components as dbc

def app_layout(df):
    layout = dbc.Container(
        [
            dbc.Row([html.H1("Segments, sales and discounts", className="text-center")], class_name="mt-4"),
            dbc.Row([
                dbc.Col([dcc.Graph(id="structure-graph", figure={})], md=6),
                dbc.Col([dcc.Graph(id="monthly-graph", figure={})], md=6),            
            ]),
            dbc.Row([
                dbc.Label("Select segments"),
                dbc.Checklist(
                    id="segment-checklist",
                    class_name="checklist btn-group mb-4",
                    input_class_name="btn-check",
                    label_class_name="btn btn-outline-warning",
                    label_checked_class_name="btn btn-warning",
                    options=[{"label": i, "value": i} for i in df["Segment"].unique()],
                    value=["Government","Small Business"],
                )
            ], class_name="mb-4"),
        ],
        fluid=True,
        class_name="dbc",
    )
    return layout