import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

#main df dropping rows with neg and NA CO2 value, sort by year
co2_production = pd.read_csv("/Users/antruong/Downloads/Bridge Programs/C-Women/Python - Final Project/clean-co2-data.csv", usecols=['country', 'year','region', 'iso_code', 'Industry', 'CO2 Value'])
co2_production = co2_production[co2_production['CO2 Value'] >= 0]\
.dropna(subset=['CO2 Value']).sort_values('year').reset_index(drop=True) 
co2_production['year']=co2_production['year'].astype(int)
co2_production

#pie_chart function presenting CO2 Industry breakdown 
def pie_chart(selected_year, selected_country):
    filters=co2_production[(co2_production['year'] == selected_year) & (co2_production['country'] == selected_country)&(co2_production['CO2 Value'] >= 0)]
    grouped_df = filters.groupby('Industry')['CO2 Value'].sum().reset_index()

    fig = px.pie(grouped_df, values='CO2 Value', names='Industry',
                 color_discrete_sequence=['#D1495B', '#EDAE49', '#009ab2', '#4D7CA9', '#003D5B'])
    fig.update_layout (
        autosize=False,
        width=280,
        height=210, 
        title_text=f'''CO2 EMISSION BY INDUSTRY <br> ({selected_country} - {selected_year})''', 
        title_x=1,  
        title_y=.9,
        legend=dict(
        {"itemsizing": "constant", "itemwidth": 30},x=1.1)
        ,title_font_color='#FFD166'
        ,title_font_size=12
        ,legend_font_size=10,font_size=10,
        paper_bgcolor='rgba(0, 0, 0, 0)',font={'color':'#c9c9c9'},
        margin=dict(l=5, r=5, b=5, t=50))
    
    fig.update_traces(hovertemplate="Industry: %{label} <br>CO2: %{value:,.2f}")
    return fig

#create df for scatter_geo map without Industry column
map_df=co2_production[co2_production['CO2 Value'] >= 0]\
    .groupby(['country','year'],as_index=False)\
    .agg({'region':'first','iso_code':'first',
        'CO2 Value':'sum'})\
    .sort_values('year')\
    .reset_index(drop=True)
map_df #df for scatter_geo

#scatter_geo map
def setup_layout(fig):
    fig.update_layout(
        autosize=False,
        height=680, width=1280,
        title_text=f'GLOBAL CO2 PRODUCTION',
        title_x=0.5,
        title_y=0.9,
        legend=dict(
            title_text="Continent",
            x=0.05,
            y=0.45,
        ),
        title_font_color='#FFD166',
        title_font_size=25,

        geo=dict(
            bgcolor='#393433',
            lakecolor='rgb(17,17,17)',
            landcolor='black',
            showlakes=True,
            showland=True,
            subunitcolor='#506784'),
        paper_bgcolor='#393433',
        font={'color': '#FFD166'},
        annotations=[
        dict(
            text=f'NORTH <br>AMERICA',
            align='center',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.34,
            y=0.68,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#666666',size=12)),
        dict(
            text=f'SOUTH <br>AMERICA',
            align='center',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.4,
            y=0.4,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#666666',size=12)),
        dict(
            text=f'ASIA',
            align='center',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.68,
            y=0.65,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#666666',size=12)),
        dict(
            text=f'AFRICA',
            align='center',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.54,
            y=0.5,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#666666',size=12)),
        dict(
            text=f'EUROPE',
            align='center',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.55,
            y=0.78,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#666666',size=12)),
        dict(
            text=f'OCEANIA',
            align='center',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.73,
            y=0.35,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#666666',size=12)),
        dict(
            text=f'(1920-2022)',
            align='center',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=1.05,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#FFD166',size=18)),
        dict(
            text='Emissions Unit: <b>Million tons</b>',
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.265,
            y=1,
            xanchor='center',
            yanchor='bottom',
            font=dict(color='#FFD166',size=12))])
    fig.update_layout(margin=dict(l=5, r=5, t=150, b=0))
    return fig

def scatter_geo(df):
    hover_text = [f"Continent: {region}<br>Year: {year}<br>CO2: {co2:,.2f}"
                 for region, year, co2 in zip(
                      df['region'], 
                      df['year'], 
                      df['CO2 Value'])] #list comprehensive

    fig = px.scatter_geo(df,
                         locations="iso_code",
                         hover_name="country", size="CO2 Value",
                         animation_frame="year", size_max=90,
                         color_discrete_sequence=['#ffcc00', '#ef476f',
                                                  '#06d6a0', '#073b4c', '#118ab2'],
                         projection='equirectangular',
                         hover_data={
                             'year': False,'iso_code':False,'CO2 Value':False,'':hover_text},
                        
                         basemap_visible=True)
    fig = setup_layout(fig)
    
    return fig

#create Dash app
app = Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    dcc.Graph(figure=scatter_geo(map_df),id='scattergeo'),
    html.Div(id='piechart'), 
    html.Div(id="hide-button")
])

@app.callback(
    [Output('piechart', 'children'),
     Output('hide-button', 'children')],
    [Input('scattergeo', 'clickData')]
)
def display_pie_chart(clickData):
    if clickData and 'points' in clickData:
        point = clickData['points'][0]
        selected_country = point.get('hovertext', '')
        selected_year = point.get('customdata', [])[0]
  

        piechart = dcc.Graph(figure=pie_chart(selected_year, selected_country),
        style={
            "position": "absolute",
            "left": f"{130}px", #Adjust as needed
            "bottom": f"{170}px", #Adjust as needed
            "zIndex": 1,
            "display": "block"  # Set display to block to show the piechart
        })
        
        hide_button=html.Button('Hide/Show', n_clicks=0,
        style = {
            "position": "absolute",
            "left": f"{260}px", #Adjust as needed
            "bottom": f"{130}px", #Adjust as needed
            "zIndex": 1,
            "color": "#a9a9a9",
            "backgroundColor": "#696261",
            "display": "block",
            'fontSize':9,'borderRadius':5})

        return piechart,hide_button
    else:
        return [dash.no_update] * 2

@app.callback(
    [Output('piechart', 'style')],
    [Input('hide-button', 'n_clicks')]
)
def hide_chart(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return [{"display": "none"}]
    elif n_clicks and n_clicks % 2 == 0:
        return [{"display": "block"}]
    else:
        return [dash.no_update]

if __name__ == '__main__':
    app.run_server(debug=True)
