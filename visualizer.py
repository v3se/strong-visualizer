import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
load_figure_template('Darkly')
pd.set_option('display.max_columns', None)
CSV_PATH = "strong3110884325819117787.csv"
df = pd.read_csv(CSV_PATH, delimiter=";")
load_figure_template("darkly")

def calculate_max(df):
    if df.empty == True:
        return 0
    else:
        df['ONERM'] = (df['Weight'] / (1.0278 - 0.0278 *
                       (df['Reps'] + (10 - df['RPE'].fillna(10)))))
        return df


def get_best_set(name):
    df_temp = df.loc[df['Exercise Name'] == name]

# for date, new_df in df_temp.groupby(level=0):
#     calculate_max(new_df)
    #df.loc[datetime.date(2021, 9, 11)]


def get_excercise_names(df):
    return df['Exercise Name'].unique()

def create_rm_fig(value, new_df):
    new_df = new_df.loc[new_df['Exercise Name'] == value].resample(rule='D')['ONERM'].max().to_frame()
    print(new_df)
    fig = go.Scatter(x=new_df.index, y=new_df['ONERM'], mode="lines+markers", name=value, connectgaps=True)

    return fig

def main():
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(['Date'], inplace=True, drop=True)
    new_df = calculate_max(df)
    #new_df.groupby(by=[new_df.index, new_df['Exercise Name']]).max()
    #new_df = new_df.loc[new_df['Exercise Name'] == 'Bench Press (Barbell)'].resample(rule='D')['ONERM'].max()

    app.layout = html.Div([
        dcc.Dropdown(get_excercise_names(
            df), ['Bench Press (Barbell)'], id='rm-dropdown', multi=True),
        html.Br(),
        html.Div([
            dcc.Graph(id="graph")
        ])

    ])

    @app.callback(
        Output(component_id='graph', component_property='figure'),
        Input(component_id='rm-dropdown', component_property='value')
    )
    def update_output(value):
        fig = make_subplots(len(value), 1, subplot_titles=value, vertical_spacing = 0.1, row_heights=[400 for i in value])
        for index, exercise in enumerate(value):
            print(index, exercise)
            fig.append_trace(create_rm_fig(exercise, new_df), row=index+1, col=1)
        subplot_height=len(value)*400
        fig.update_layout(height=subplot_height, title_text="One Rep Max")
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Weight') 
        return fig

    if __name__ == '__main__':
        app.run_server(debug=True)
    # print(df)
    # print(df.columns.tolist())


if __name__ == "__main__":
    main()
