# Import required libraries
from re import A
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.io as pio
# Read the launch data into pandas dataframe
spacex_df = pd.read_csv("dashboard_data.csv")
# background template layout
pio.templates.default = "simple_white"

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options = [
                                    {'label': 'All Sites', 'value': 'ALL'}, 
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, 
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                             value = 'ALL',
                                             placeholder = 'Choose a Launch Site here:', 
                                             searchable = True, 
                                             style = {'font-size': 20}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart'), 
                                         style = {'width': '100%'}),
                                html.Br(),

                                html.P("Payload range (Kg):", style = {'font-size': 20}),
                                # TASK 3: Add a slider to select payload range
                                #id to be payload-slider
                                dcc.RangeSlider(id='payload-slider', min = 0, step = 1000, max = 10_000, 
                                                value = [min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'), 
                                         style = {'width': '100%'}), 
                                html.Br(),
                                ])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'), 
    Input(component_id = 'site-dropdown', component_property = 'value'))
def get_pie_chart(entered_site):
    # filtered dataframes    
    if entered_site != 'ALL':
        filtered_data = spacex_df[spacex_df.iloc[:, 2] == entered_site]
        
        fig = px.pie(filtered_data, 'class', facet_col = 'Launch Site', 
                     height = 700, width = 1850)
        fig.update_traces(textinfo='percent+label', legendgrouptitle_font_size = 1, textfont_size = 18)
        fig.update_layout(hoverlabel_font_size = 20, annotations = [
            dict(text = f'Total Success Launches by Site {entered_site}', 
                y = 1.05, font_size = 30)])
        return fig
    else:
        fig = px.pie(spacex_df, 'Launch Site', 'class', title = 'Total Success Launches by Site', 
                     height = 700, width = 1850)
        fig.update_traces(textinfo='percent+label', textfont_size = 18)
        fig.update_layout(hoverlabel_font_size = 20, title_font_size = 30)
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'), 
    [Input(component_id = 'site-dropdown', component_property = 'value'), 
    Input(component_id = 'payload-slider', component_property = 'value')])
def get_scatterPlot(entered_site, entered_range):
    if entered_site != 'ALL':
        filtered_df = spacex_df[spacex_df.iloc[:, 2] == entered_site]
        filtered_df = filtered_df[filtered_df.iloc[:, 4].between(entered_range[0], entered_range[1], inclusive = 'both')]
        fig = px.scatter(filtered_df, 'Payload Mass (kg)', 'class', 
               color = 'Booster Version Category', title = f'Correlation between Payload and Success for Site {entered_site}')
        fig.update_layout(hoverlabel_font_size = 20, title_font_size = 30, font_size = 18)
        return fig
    else:
        slider_df = spacex_df[spacex_df.iloc[:, 4].between(entered_range[0], entered_range[1], inclusive = 'both')]
        fig = px.scatter(slider_df, 'Payload Mass (kg)', 'class',
               color = 'Booster Version Category', title = 'Correlation between Payload and Success for all Sites')
        fig.update_layout(hoverlabel_font_size = 20, title_font_size = 30, font_size = 18)
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)