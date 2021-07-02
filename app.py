from datetime import date
import dash
import dash_core_components as dcc
#import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
app = dash.Dash(__name__)


app.css.config.serve_locally = False

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin123',
    database='adatscience'
 )
mycursor= mydb.cursor(dictionary=True) 




def generate_table(dataframe, max_rows=50):
    return html.Div(html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns]) ] +
        # Body
        [html.Td([
            html.Tr(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    ), className="sum_div")
       

def current_quarter():
    
    curYear =  date.today().year
    curMonth = date.today().month
    prevYear = date.today().year - 1
    if(curMonth//3 == 1):
        curQtr = 'Q'+str(1)+'-'+str(curYear)
        prevQtr = 'Q'+str(4)+'-'+str(prevYear)
    elif(curMonth//3 == 2):
        #qutr = 'Q'+str(2)+'-'+str(curYear)
        #prevQtr = 'Q'+str(1)+'-'+str(curYear)
        curQtr = 'Q'+str(1)+'-'+str(curYear)
        prevQtr = 'Q'+str(4)+'-'+str(prevYear)
        
    elif(curMonth//3 == 3):
        curQtr = 'Q'+str(3)+'-'+str(curYear)
        prevQtr = 'Q'+str(2)+'-'+str(curYear)
    elif(curMonth//3 == 4):
        curQtr = 'Q'+str(4)+'-'+str(curYear)
        prevQtr = 'Q'+str(3)+'-'+str(curYear)
    else:
        curQtr = 'Q'+str(4)+'-'+str(prevYear)
        prevQtr = 'Q'+str(3)+'-'+str(prevYear)
    
    sql = "SELECT 	SUM(market_value) as mv, SUM(IF(change_type = 'new',1, 0)) AS new,SUM(IF(change_type = 'addition',1, 0)) AS addition,"
    sql += " SUM(if(change_type = 'reduction',1, 0)) AS reduction, SUM(IF(change_type = 'soldall',1, 0)) AS soldall "
    sql += " FROM stocksdata where quarter_year = '"+curQtr+"'"
    
    mycursor.execute(sql)
    result = mycursor.fetchone()
    
    ######
    sql1 = "SELECT SUM(market_value) as pmv FROM stocksdata where quarter_year = '"+prevQtr+"'"
    mycursor.execute(sql1)
    result1 = mycursor.fetchone()
    
    valPr = valPrint(result1['pmv'], result['mv'])
    result['pmv'] = str(valPr['pmvVal'])+'Billion'
    result['mv'] = str(valPr['mvVal'])+'Billion'
    return result

def previous_quarter():

    curYear =  date.today().year
    prevMonth = date.today().month
    prevYear = date.today().year - 1
    
    if(prevMonth//3 == 1): #Mar - May
        curQtr = 'Q'+str(4)+'-'+str(prevYear)
        prevQtr = 'Q'+str(3)+'-'+str(prevYear)
    elif(prevMonth//3 == 2): #Jun-Aug
       # curQtr = 'Q'+str(1)+'-'+str(curYear)
       # prevQtr = 'Q'+str(4)+'-'+str(prevYear)
       curQtr = 'Q'+str(4)+'-'+str(prevYear)
       prevQtr = 'Q'+str(3)+'-'+str(prevYear)
        
    elif(prevMonth//3 == 3): # Sep-Nov
        curQtr = 'Q'+str(2)+'-'+str(curYear)
        prevQtr = 'Q'+str(1)+'-'+str(curYear)
        
    else: # Dec-Feb
        curQtr = 'Q'+str(3)+'-'+str(curYear)
        prevQtr = 'Q'+str(2)+'-'+str(curYear)
        
    sql = "SELECT 	SUM(market_value) as mv, SUM(IF(change_type = 'new',1, 0)) AS new,SUM(IF(change_type = 'addition',1, 0)) AS addition,"
    sql += " SUM(if(change_type = 'reduction',1, 0)) AS reduction, SUM(IF(change_type = 'soldall',1, 0)) AS soldall "
    sql += " FROM stocksdata where quarter_year = '"+curQtr+"'"
    
    mycursor.execute(sql)
    result = mycursor.fetchone()
    
    ######
    sql1 = "SELECT SUM(market_value) as pmv FROM stocksdata where quarter_year = '"+prevQtr+"'"
    mycursor.execute(sql1)
    result1 = mycursor.fetchone()
    
    valPr = valPrint(result1['pmv'], result['mv'])
    result['pmv'] = str(valPr['pmvVal'])+'Billion'
    result['mv'] = str(valPr['mvVal'])+'Billion'
    return result  
    
    

    
def pre_previous_quarter():
    curYear =  date.today().year
    prevMonth = date.today().month
    prevYear = date.today().year - 1
    
    if(prevMonth//3 == 1): #Mar - May
        curQtr = 'Q'+str(3)+'-'+str(prevYear)
        prevQtr = 'Q'+str(2)+'-'+str(prevYear)
    elif(prevMonth//3 == 2): #Jun-Aug
        #qutr = 'Q'+str(4)+'-'+str(prevYear) ####### data is not available  #######
        #prevQtr = 'Q'+str(3)+'-'+str(prevYear)
        curQtr = 'Q'+str(3)+'-'+str(prevYear)
        prevQtr = 'Q'+str(2)+'-'+str(prevYear)
        
    elif(prevMonth//3 == 3): # Sep-Nov
        curQtr = 'Q'+str(1)+'-'+str(curYear)
        prevQtr = 'Q'+str(4)+'-'+str(prevYear)
    else:# Dec-Feb
        curQtr = 'Q'+str(2)+'-'+str(curYear)
        prevQtr = 'Q'+str(1)+'-'+str(curYear)
    
    
    
    
    sql = "SELECT 	SUM(market_value) as mv, SUM(IF(change_type = 'new',1, 0)) AS new,SUM(IF(change_type = 'addition',1, 0)) AS addition,"
    sql += " SUM(if(change_type = 'reduction',1, 0)) AS reduction, SUM(IF(change_type = 'soldall',1, 0)) AS soldall "
    sql += " FROM stocksdata where quarter_year = '"+curQtr+"'"
    
    mycursor.execute(sql)
    result = mycursor.fetchone()
    
    
    ######
    sql1 = "SELECT SUM(market_value) as pmv FROM stocksdata where quarter_year = '"+prevQtr+"'"
    mycursor.execute(sql1)
    result1 = mycursor.fetchone()
    
    valPr = valPrint(result1['pmv'], result['mv'])
    result['pmv'] = str(valPr['pmvVal'])+'Billion'
    result['mv'] = str(valPr['mvVal'])+'Billion'
    return result
    
def repeat(letter, times):
    str1 = ''
    for i in range(times):
        str1 = str1+letter
        
    return str1

def valPrint(pmv, mv):
    ########  PMV Calculation #############
    
    pmvVal = int(pmv)
    lenPmv = len(str(pmvVal))
    modPmv = str(lenPmv%2)
    if(modPmv == '0'):
        lenmn = 3
    else:
        lenmn = 2
    cntPmvLen = lenPmv - lenmn
    calc = repeat('0',cntPmvLen)
    divPmv = '1'+calc
    divPmvVal = int(divPmv)
    
    ########  MV Calculation #############
    mvVal = int(mv)
    lenMv = len(str(mvVal))
    modMv = str(lenMv%2)
    if(modMv == '0'):
        lenmin = 3
    else:
        lenmin = 2
    cntMvLen = lenMv - lenmin
    calc = repeat('0',cntMvLen)
    divMv = '1'+calc
    divMvVal = int(divMv)
    
    value = {}
    value['pmvVal'] = round(pmvVal/divPmvVal,2)
    value['mvVal'] = round(mvVal/divMvVal,2)
    return value
                
    
def index():
    fstqtr = current_quarter()
    secqtr = previous_quarter()
    thirdqtr =  pre_previous_quarter()
    data = {'13F Summary' : ['Market Value', '',fstqtr['mv'],], 'Q1_2021' : ['Prior Market value','',fstqtr['pmv']],'.' : ['New Purchases','',fstqtr['new']],'' : ['Additional Purchases','',fstqtr['addition']],'  ' : ['Sold Out Of','',fstqtr['soldall']],' . ' : ['Reducing Holding in','',fstqtr['reduction']]}
    data1 = {'13F Summary' : ['Market Value','', secqtr['mv'], ], 'Q4_2020' : ['Prior Market Value','',secqtr['pmv'], ],' .' : ['New Purchases','',secqtr['new']],'' : ['Additional Purchases','',secqtr['addition']],'  ' : ['Sold Out of','',secqtr['soldall']],' . ' : ['Reducing Holding in','',secqtr['reduction']]}
    data2 = {'13F Summary' : ['Market Value','', thirdqtr['mv'], ], 'Q3_2020' : ['Prior Market Value','',thirdqtr['pmv'], ],' .' : ['New Purchases','',thirdqtr['new']],'' : ['Additional Purchases','',thirdqtr['addition']],'  ' : ['Sold Out of','',thirdqtr['soldall']],' . ' : ['Reducing Holding in','',thirdqtr['reduction']]}
    
    

    df1 = pd.DataFrame(data)
    df2 = pd.DataFrame(data1)
    df3 = pd.DataFrame(data2)
    
    sql1 = "SELECT * FROM stocksdata where quarter_year = 'Q1-2021'"
    mycursor.execute(sql1)
    result = mycursor.fetchall()
    
    pd.options.plotting.backend = "plotly"
    file_data = pd.read_csv('E:/csvdata_data/csv/combine.csv')
    df = pd.DataFrame(file_data)
    
    #df = pd.DataFrame([[ij for ij in i] for i in result])
    #df.to_json()
    #df.rename(columns={0: "sector", 1: "percent_of_portfolio", 2: "qtr_first_owned"}, inplace=True);
    #x = df["qtr_first_owned"]
   
    pl = df.pivot_table(
        index='Qtr first owned',
        columns='sector',
        values='% of Portfolio',
        aggfunc='sum',
    ).plot.bar(title= 'Bar Graph')
     
    bubble = bubbleGraph()
    max_buys_stocks = bubble['max_buys_stocks']
    max_sells_stocks = bubble['max_sells_stocks']
    
    linear = linearGraph()
    max_gainer = linear['max_gainer']
    max_losers = linear['max_losers']
    
    app.layout = html.Div(style={'background-color':'#FFF','color':'#000'},children=[
        html.H1(children='Summary Tables'),
        generate_table(df1), 
        generate_table(df2), generate_table(df3),
        dcc.Graph(
              
              id='combinegraph',
              figure=pl,
              style={'float':'left','width':'100%'}
           ),
           
        dcc.Graph(
              id='graph_bought',
              figure= max_buys_stocks,
              style={'float':'left','width':'40%'}              
              
           ),
        dcc.Graph(
              id='graph_sold',
              figure= max_sells_stocks,
              style={'float':'left','width':'40%','margin-left':'300px'}              
              
           ),
        dcc.Graph(
             id='testgraphone',
             figure= max_gainer,
             style={'float':'left','width':'40%'}             
           ), 
        dcc.Graph(
             id='testgraphtwo',
             figure= max_losers ,
             style={'float':'left','width':'40%','margin-left':'300px'},
             
           )
                    
    ])
    
    
def bubbleGraph():
    pd.options.plotting.backend = "plotly"
    file_data = pd.read_csv('E:/csvdata_data/csv/combine.csv')
    df = (pd.DataFrame(file_data)[['Symbol', 'Stock', '% of Portfolio', 'Previous % of Portfolio']].fillna(0)).rename(columns={"Symbol": "Sticker"})
    
    df["% Change"] = df["% of Portfolio"] - df["Previous % of Portfolio"]
    sells = (df.where(df["% Change"] < 0).dropna()).sort_values(by=["% Change"],ascending=True).head(10)
    buys = (df.where(df["% Change"] >= 0).dropna()).sort_values(by=["% Change"],ascending=False).head(10)
    max_buys_stocks = px.scatter(buys, x="Sticker", y="% Change", title = 'Maximum bought stocks',
                     color="Sticker", 
                     size='% Change',
                     hover_name="Stock",
                     hover_data=['% Change','Sticker']) 
                    
    max_sells_stocks = px.scatter(sells, x="Sticker", y="% Change", title= 'Maximum sold stocks',
                    color="Sticker",
                    size=-sells['% Change'],
                    hover_name="Stock",
                    hover_data=['% Change','Sticker'])
    result = {}
    result['max_buys_stocks'] = max_buys_stocks
    result['max_sells_stocks'] = max_sells_stocks
    
    return result
    
def linearGraph():
        
    file_data = pd.read_csv('E:/csvdata_data/csv/combine.csv')
    file_data.head()


    # In[7]:


    file_data['% Price_Change'] = round((file_data['Recent Price']-file_data['Avg Price'])/file_data['Recent Price']*100,3)
    file_data.head()


    # In[8]:


    top_losers = file_data.sort_values(by='% Price_Change', ascending = False)
    top_losers= top_losers.head(10)
    top_losers


    # In[9]:


    max_losers = px.area(top_losers, x='Symbol', y='% Price_Change', title='Biggest Losers', labels=False)
    max_losers


    # In[11]:


    top_gainer = file_data.sort_values(by='% Price_Change', ascending = True)
    top_gainer= top_gainer.head(10)
    top_gainer


    # In[12]:


    max_gainer = px.area(top_gainer, x='Symbol', y='% Price_Change', title='Top Gainer', labels=True)
    result = {}
    result['max_gainer'] = max_gainer 
    result['max_losers'] = max_losers
    return result
         
    # app.layout = html.Div(children=[
        # html.H2(children='Summary Tables'),
        # dcc.Graph(
              # id='example-graph',
              # figure= max_buys_stocks  
              
           # ),
        # dcc.Graph(
              # id='example-graph1',
              # figure= max_sells_stocks  
              
           # )
    # ])
            
index() 
          



if __name__ == '__main__':
    app.run_server(port=8050,debug=True)