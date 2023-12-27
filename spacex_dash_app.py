# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Add a dropdown list to enable Launch Site selection
                                html.Div([html.Label("Select Site:"),
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label': 'All Sites', 'value': 'All Sites'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                ],value='ALL',placeholder='select site',searchable=True)
                                ]),
                                # The default select value is for ALL sites
                                #dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                #  Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                #  Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',

                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                1000: '1000',2000:'2000',3000:'3000',4000:'4000',5000:'5000',6000:'6000',7000:'7000',8000:'8000',9000:'9000',10000:'10000'},
                                                value=[min_payload, max_payload]),
                                #dcc.RangeSlider(id='payload-slider',...)

                                #Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    df1 = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='count_class')
    df1 = df1.reset_index(drop=True)
    df2=df1[df1['class']==1]
    df3=df1[df1['Launch Site']== entered_site]
    if entered_site == 'All Sites':
        fig = px.pie(df2, values='count_class', 
        names='Launch Site', 
        title='pie chart')
        return fig
    else:
        fig1 = px.pie(df3,values='count_class',names='class',title='pie charts')
        return fig1
       
        # return the outcomes piechart for a selected site
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              [Input(component_id='site-dropdown',component_property='value'),Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,payload_range):
    selected_columns = ['Launch Site', 'class','Payload Mass (kg)','Booster Version Category']
    filtered_df = spacex_df[selected_columns]
    min_payload, max_payload = payload_range
    df4=filtered_df[filtered_df['Launch Site']== entered_site]
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= min_payload) & (filtered_df['Payload Mass (kg)'] <= max_payload)]
    df4= df4[(df4['Payload Mass (kg)'] >= min_payload) & (df4['Payload Mass (kg)'] <= max_payload)]
    if entered_site == 'All Sites':
        fig3 =px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color="Booster Version Category",title='scatter plot')
        return fig3
    else:
        empty_fig = px.scatter(df4,x='Payload Mass (kg)',y='class',color="Booster Version Category",title='No Data Selected')
        return empty_fig               
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Run the app
if __name__ == '__main__':
    app.run_server()

