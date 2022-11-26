from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
load_figure_template("darkly")

app.layout = html.Div([

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                ), style={'display': 'inline-block'}
            )
            for page in dash.page_registry.values()
        ]
    ),
    html.H1('Strong Gym Data Visualizer'),
    dcc.Store(id="memory", storage_type='session'),
	dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
