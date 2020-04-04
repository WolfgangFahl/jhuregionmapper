'''
Created on 2020-04-04

@author: wf
'''
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from jhu.jhu import COVIDCases
import math

CONFIRMED="Confirmed"
DEATHS="Deaths"
RECOVERED="Recovered"
REGION='Country_Region'
LAT='Lat'
LON='Long_'
        
class WorldMap(object):
    '''
    map of the world with data
    '''

    def __init__(self, title):
        '''
        Constructor
        '''
        self.title = title
        
    def sample(self):
        df = px.data.gapminder().query("year==2007")
        fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                             hover_name="country", size="pop",
                             projection="natural earth")
        fig.show()  
        
    def addScatter(self,fig,df,title,column,color):   
        '''
        add a scatter plot for the given data
        '''
        hoverdata = df[REGION] + " - "+ [title+": " + str(v) for v in df[column].tolist()]
        normalized_data = [math.log(value+1)*4 for value in  df[column]]
  
        scatter = go.Figure(data=go.Scattergeo(
                lon = df[LON],
                lat = df[LAT],
            name = title,
                hovertext = hoverdata,
                marker = dict(
                    size =  normalized_data,
                    opacity = 0.5,
                    color = color,
                    line = dict(
                        width=0,
                        color='rgba(102, 102, 102)'
                    ),
                ),
                ))
        fig.add_trace(scatter.data[0])
        
    def directFromCSV(self,date):
        '''
        create  a scatter plot map directly from the daily CSV data
        see https://towardsdatascience.com/the-impact-of-covid-19-data-analysis-and-visualization-560e54262dc
        and https://github.com/SanthiyaDaniel/Impact-of-COVID-19
        '''
        url=COVIDCases.BASE_URL_REPORTS+date+".csv"
        print (url)
        df = pd.read_csv(url)
        fig = make_subplots()
        self.addScatter(fig,df,"Confirmed cases",CONFIRMED,'blue')
        self.addScatter(fig,df,'Deaths',DEATHS,'red')
        self.addScatter(fig,df,'Recovered',RECOVERED,'green')
        
        fig.update_layout(
                title = self.title,
            legend=dict(
                itemsizing = "constant",
                font=dict(
                    family="sans-serif",
                    size=20,
                    color="black"
                )
            )
        )
        fig.show()
        
