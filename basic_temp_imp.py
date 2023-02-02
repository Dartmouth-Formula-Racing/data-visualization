# Go to http://127.0.0.1:8050/

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("dataviz_temperatures_sample.csv") # read csv file
df = df.drop(columns=df.columns[0], axis=1) # drop useless column
df['Timestamp'] = pd.to_datetime(df['Timestamp']) # convert time values to datetime format
df = df.pivot_table(values='Value', index='Timestamp',
                    columns='Variable').sort_values('Timestamp').reset_index() # organize data

fig = px.line(df, x='Timestamp',
              y=['Inverter1_Temperatures1_ModA','Inverter1_Temperatures1_ModB']) # plot using ploty express
fig.update_layout(xaxis_title="Time (H)", yaxis_title="Temperature (C)") # change axis labels

app.layout = html.Div(children=[
    html.H1(children='Basic Temperature Plot', style={'textAlign': 'center'}), # title for browser page

    html.Div(children='Time (x) vs. Temperature Sensor Data (y) Graph.', style={'textAlign': 'center'}), # sub-title

    dcc.Graph(id='graph1', figure=fig)]) # graph location on dashboard

if __name__ == '__main__':
    app.run_server(debug=True) # allows browser to refresh upon new changes

