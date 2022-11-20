import base64
import io
import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd

CSV_PATH = "strong3110884325819117787.csv"
df = pd.read_csv(CSV_PATH, delimiter=";")

df['Date'] = pd.to_datetime(df['Date'])
df.set_index(['Date'], inplace=True, drop=True)

dash.register_page(__name__, path='/')

def calculate_gym_time(df):
    df['Workout Duration'] = pd.to_timedelta(df['Workout Duration'])
    time = df.resample(rule='D')['Workout Duration'].max().to_frame()
    time = df["Workout Duration"].sum()

layout = html.Div(children=[
    html.H1(children='Welcome'),
    html.Div(children='''
        This application is for visualizing exercise data from Strong gym app (add link to play store).
    '''),
    html.H2("Upload CSV File"),
    dcc.Upload(
        id="upload-data",
        children=html.Div(
            ["Drag and drop or click to select a file to upload."]),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
        multiple=False,
    ),
    ],style={"max-width": "500px"})

def parse_contents(filename, contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')), delimiter=";")
        return df

@callback(
    Output("memory", "data"),
    Output("upload-data", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")], prevent_initial_call=True, suppress_callback_exceptions=True,
)
def update_output(name, data):
    data = parse_contents(name, data).reset_index().to_json(orient="split")
    name = f"Uploaded successfully: {name}"
    return data, name