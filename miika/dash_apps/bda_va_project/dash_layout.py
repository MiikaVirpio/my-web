from dash import html, dcc
import dash_bootstrap_components as dbc

CHOICE_LABELS = {
    "name": "Company name",
    "yf_ticker": "Ticker",
    "target": "Target price",
    "recommendation": "Inderes recommendation",
    "risk": "Inderes risk level",
    "revenue_2023": "Revenue (M)",
    "ebitda": "EBITDA (M)",
    "eps": "EPS",
    "dividend_ratio": "Dividend ratio",
    "margin": "EBITDA-%",
    "roe": "ROE",
    "mcap": "Market Capitalization (M)",
    "ev": "EV (M)",
    "equity_ratio": "Equity ratio",
    "sector": "Sector",
    "pb": "P/B",
    "peg": "PEG",
    "volume": "Volume (M)",
    "quick_ratio": "Quick ratio",
    "current_ratio": "Current ratio",
    "price": "Price",
    "pe": "P/E",
    "ev_ebitda": "EV/EBITDA",
    "vmc": "Average volume/MCAP",
}

PRICES = ["price", "target"]
INDICATORS = ["pe", "pb", "peg", "ev_ebitda", "roe", "dividend_ratio", "equity_ratio", "margin", "current_ratio", "quick_ratio", "vmc"]
CATEGORICALS = ["sector", "recommendation", "risk"]
SCALERS = ["mcap", "ev", "revenue_2023", "volume", "risk"]

def app_layout(df):
    layout = dbc.Container(
        [
            dbc.Row([
                dbc.RadioItems(
                    id="category-radio",
                    class_name="btn-group mb-2",
                    input_class_name="btn-check",
                    label_class_name="btn btn-outline-warning thick-btn",
                    label_checked_class_name="btn btn-warning",
                    options=[{"label": i, "value": i} for i in ["All", "Small Cap", "Mid Cap", "Large Cap", "Empty"]],
                    value="All",
                ),
                dbc.Label("Select Companies. Affects scatter, lines and sunburst charts"),
                dcc.Dropdown(
                    id="company-dropdown",
                    options=[{"label": i, "value": i} for i in df["name"]],
                    value=df["name"],
                    multi=True
                ),
            ], class_name="my-4"),
            dbc.Row([html.H1("4-Dimensional Interactive Scatter Screener", className="text-center")]),
            dbc.Row([html.P("Select axis, size and color parameters below. Use the hover tools on the right. Fiddle with axis to pan and scale. Legend click to hide, double click to solo.", className="text-center")]),
            dbc.Row([dcc.Graph(id="scatter-graph", figure={})]),
            dbc.Row([
                dbc.Label("Select x-axis:"),
                dbc.RadioItems(
                    id="x-radio",
                    class_name="btn-group",
                    input_class_name="btn-check",
                    label_class_name="btn btn-outline-danger thick-btn",
                    label_checked_class_name="btn btn-danger",
                    options=[{"label": CHOICE_LABELS[i], "value": i} for i in PRICES + INDICATORS],
                    value="price",
                ),]),
            dbc.Row([
                dbc.Label("Select y-axis:"),
                dbc.RadioItems(
                    id="y-radio",
                    class_name="btn-group",
                    input_class_name="btn-check",
                    label_class_name="btn btn-outline-success thick-btn",
                    label_checked_class_name="btn btn-success",
                    options=[{"label": CHOICE_LABELS[i], "value": i} for i in PRICES + INDICATORS],
                    value="pb",
                ),]),
            dbc.Row([
                dbc.Label("Select size parameter:"),
                dbc.RadioItems(
                    id="size-radio",
                    class_name="btn-group",
                    input_class_name="btn-check",
                    label_class_name="btn btn-outline-primary thick-btn",
                    label_checked_class_name="btn btn-primary",
                    options=[{"label": CHOICE_LABELS[i], "value": i} for i in SCALERS],
                    value="mcap",
                ),]),
            dbc.Row([
                dbc.Label("Select color parameter:"),
                dbc.RadioItems(
                    id="color-radio",
                    class_name="btn-group",
                    input_class_name="btn-check",
                    label_class_name="btn btn-outline-info thick-btn",
                    label_checked_class_name="btn btn-info",
                    options=[{"label": CHOICE_LABELS[i], "value": i} for i in CATEGORICALS],
                    value="sector",
                ),], class_name="mb-4"),
            dbc.Row([html.H1("Messy Indexed Stock Price Lines", className="text-center")]),
            dbc.Row([html.P("Year-To-Date return of selected companies. Legend shows if companies count < 30. Legend click to hide, double click to solo.", className="text-center")]),
            dbc.Row([dcc.Graph(id="lines-graph", figure={})], class_name="mb-2"),
            dbc.Row([html.H1("Sunburst of sector & indurstries", className="text-center")]),
            dbc.Row([html.P("Click sectors to navigate. Size based on market capitalization.", className="text-center")]),
            dbc.Row([dcc.Graph(id="sunburst-graph", figure={})], class_name="mb-2"),
            dbc.Row([html.H1("Traders view with all the bells and whistles", className="text-center")]),
            dbc.Row([html.P("Choose a company for YTD candle chart. Sip some maté and see the patterns!", className="text-center")]),
            dcc.Dropdown(
                    id="trader-company-dropdown",
                    options=[{"label": i, "value": i} for i in df["name"]],
                    value="Qt",
                ),
            dbc.Row([dcc.Graph(id="trader-graph", figure={})], class_name="mb-4"),
        ],
        fluid=True,
        class_name="dbc",
    )
    return layout