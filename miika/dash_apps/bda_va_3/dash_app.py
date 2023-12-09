from dash import Dash, html
import dash_cytoscape as cyto

# Given raw data
# Political system
political_system = """
US -> Strong democracy
China -> Strong communism
India -> Strong democracy
UK -> Strong democracy
Russia -> Weak democracy
Germany -> Strong democracy
Japan -> Strong democracy
Pakistan -> Weak democracy
Hungary -> Weak communism
"""
# Annual defense spending
defense_spending = """
US 801bn $
China 293bn $
India 76 bn $
UK 68 bn $
Russia 65 bn $
Germany 56 bn $
Japan 54 bn $
Pakistan 12 bn $
Hungary 8 bn $
"""
# Strategic relations
relations = """
[Hungary, Russia, Weak Allies]
[US, UK, Strong Allies]
[India, Pakistan, Strong Adversary]
[China, Japan, Strong Adversary]
[US, Japan, Strong Allies]
[India, China, Weak Adversary]
[China, US, Weak Adversary]
[China, UK, Weak Adversary]
[China, Russia, Strong Allies]
[India, Japan, Weak Allies]
[Germany, US, Strong Allies]
[Hungary, Germany, Weak Allies]
[India, US, Weak Allies]
[Pakistan, US, Weak Allies]
[Russia, Germany, Weak Adversary]
"""

app = Dash(__name__)

styles = [
    {"selector": "node", "style": {"content": "data(label)"}},
    {"selector": ".heavy-communist", "style": {"background-color": "red"}},
    {"selector": ".heavy-capitalist", "style": {"background-color": "blue"}},
    {"selector": ".light-communist", "style": {"background-color": "pink"}},
    {"selector": ".light-capitalist", "style": {"background-color": "lightblue"}},
    {"selector": ".heavy_allies", "style": {"line-color": "green"}},
    {"selector": ".light_allies", "style": {"line-color": "lightgreen"}},
    {"selector": ".heavy_adversaries", "style": {"line-color": "orange"}},
    {"selector": ".light_adversaries", "style": {"line-color": "yellow"}},
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='cyto-va-3',
        layout={'name': 'cose'},
        style={'width': '1200px', 'height': '800px'},
        stylesheet=styles,
        elements=[
            # Nodes.
            # Node size reflects defense spending (80px = 800bn $ etc.).
            # Node color reflects political system.
            {'data': {'id': 'US', 'label': 'US'}, 'classes': 'heavy-capitalist', 'style': {'width': '80px', 'height': '80px'}},
            {'data': {'id': 'China', 'label': 'China'}, 'classes': 'heavy-communist', 'style': {'width': '30px', 'height': '30px'}},
            {'data': {'id': 'India', 'label': 'India'}, 'classes': 'heavy-capitalist', 'style': {'width': '7px', 'height': '7px'}},
            {'data': {'id': 'UK', 'label': 'UK'}, 'classes': 'heavy-capitalist', 'style': {'width': '7px', 'height': '7px'}},
            {'data': {'id': 'Russia', 'label': 'Russia'}, 'classes': 'light-capitalist', 'style': {'width': '7px', 'height': '7px'}},
            {'data': {'id': 'Germany', 'label': 'Germany'}, 'classes': 'heavy-capitalist', 'style': {'width': '6px', 'height': '6px'}},
            {'data': {'id': 'Japan', 'label': 'Japan'}, 'classes': 'heavy-capitalist', 'style': {'width': '5px', 'height': '5px'}},
            {'data': {'id': 'Pakistan', 'label': 'Pakistan'}, 'classes': 'light-capitalist', 'style': {'width': '1px', 'height': '1px'}},
            {'data': {'id': 'Hungary', 'label': 'Hungary'}, 'classes': 'light-communist', 'style': {'width': '1px', 'height': '1px'}},
            # Edges
            {'data': {'source': 'Hungary', 'target': 'Russia'}, 'classes': 'light_allies'},
            {'data': {'source': 'US', 'target': 'UK'}, 'classes': 'heavy_allies'},
            {'data': {'source': 'India', 'target': 'Pakistan'}, 'classes': 'heavy_adversaries'},
            {'data': {'source': 'China', 'target': 'Japan'}, 'classes': 'heavy_adversaries'},
            {'data': {'source': 'US', 'target': 'Japan'}, 'classes': 'heavy_allies'},
            {'data': {'source': 'India', 'target': 'China'}, 'classes': 'light_adversaries'},
            {'data': {'source': 'China', 'target': 'US'}, 'classes': 'light_adversaries'},
            {'data': {'source': 'China', 'target': 'UK'}, 'classes': 'light_adversaries'},
            {'data': {'source': 'China', 'target': 'Russia'}, 'classes': 'heavy_allies'},
            {'data': {'source': 'India', 'target': 'Japan'}, 'classes': 'light_allies'},
            {'data': {'source': 'Germany', 'target': 'US'}, 'classes': 'heavy_allies'},
            {'data': {'source': 'Hungary', 'target': 'Germany'}, 'classes': 'light_allies'},
            {'data': {'source': 'India', 'target': 'US'}, 'classes': 'light_allies'},
            {'data': {'source': 'Pakistan', 'target': 'US'}, 'classes': 'light_allies'},
            {'data': {'source': 'Russia', 'target': 'Germany'}, 'classes': 'light_adversaries'}, 
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)