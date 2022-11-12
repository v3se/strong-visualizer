import dash
from dash import html, dcc

dash.register_page(__name__, path='/exercise_details')

layout = html.Div(children=[
    html.H1(children='Welcome'),

    html.Div(children='''
        This application is for visualizing exercise data from Strong gym app (add link to play store).
    '''),

])