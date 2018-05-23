import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import csv
import re
import time
import random

##(26)      0        1              2            3            4              5          6               7                   8                      9                   10                 11               12               13               14                15                16                  17              18               19                20                 21             22             23                      24                 25                                 
themes = ['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test']
style.use(themes[4])


def getSymbolLists(companyListFile = 'secwiki_tickers.csv'):
    '''
        This function get name of the file in the currenct direction program
        the file should contain the first line with the labels: 'Ticker', 'Name', 'Sector', 'Industry'
        and return a dictionary of thes data (about some valid Tickers/Symbols on stocks)
    '''
    labels = ['Ticker', 'Name', 'Sector', 'Industry']
    df = {}
    for l in labels:  df[l] = []
    with open(companyListFile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for l in labels:
                try:
                    df[l].append(row[l])
                except:
                    print('Cannot file the title {0} in the first line of the file {1}'.format(l, companyListFile))
                    print('Exit program')
                    exit(0)
                    break
    return df

def getRandomSymbol():
    '''
        This function return tuple of a random symbol and the list of all the stocks
    '''
    df = getSymbolLists()
    Symbol = df['Ticker']
    Name = df['Name']
    Sector = df['Sector']
    Industry = df['Industry']

    rand_symbol = random.choice(Symbol)
    return (rand_symbol, Symbol)

    
def GraphIt(stockName,  bayAt = 'random', times = None ):
    '''
        This function get:
        *  stockName - need to be a valid ticker/symbol from 'quandl' database
        *  bayAt     - the price that you bought the stock 
        *  times     - get the peroid of time from now to back , like: '10y' (10 years) , '5m' (5 months)  or '30d' (30 days) (optinal as '10y')
                       a valid param times can be specific time like:
                       ( start = dt.datetime(2000,1,1) , end   = dt.datetime(2016,12,31) )
                                    '2000-01-01'                        '2016-12-31'
                               
        and plot the graphs functionalities of:
        +  line of the closep with gain or lose indication
    '''
    ## get data stock from internet to csv file
    def generateFile(stockName):
        print('Generate file data of stock: \'{0}\''.format(stockName))
        times_val = None
        if(type(times) is str):
            # get balid date tuple of 2 date (start, end=today)
            def getTimes(times):
                # regular expression to extract the interesting data from the string param
                timeReg    = re.compile('(\d+)\s?(\w)')
                match_time = timeReg.findall(times)
                today      = dt.date.today() 
                diffBy     = match_time[0][1]
                diffAmount = int(match_time[0][0])
                before = 0
                if  (diffBy in ['y', 'Y']):
                    before = relativedelta(months =+ 12*diffAmount)
                elif(diffBy in ['m', 'M']):
                    before = relativedelta(months =+ diffAmount)
                elif(diffBy in ['d', 'D']):
                    before = dt.timedelta(days=diffAmount)

                start = today - before
                return (start, today)
            
            times_val = getTimes(times)

        print('Between the times: start {0} - end {1}'.format(times_val[0], times_val[1]))
        if( (type(times_val) is tuple or type(times_val) is list)  and
             len(times_val) == 2 and
             type(times_val[0]) is dt.date and
             type(times_val[1]) is dt.date):

            start, end = times_val
            # should can be from : 'quandl' or 'google' or 'yahoo' , but for me work only quandl
            try:
                df = web.DataReader(stockName, 'quandl' , start, end) 
                df.iloc[::-1] # for order data that mack present it left to right
                df.to_csv(stockName+'.csv')
                print('File \'{0}.csv\' created!'.format(stockName))
            except:
                plt.close('all')
                print('There ins\'t name symbol \'{0}\' stock in quandl! try another else'.format(stockName))
                return
        else:
            print('Error: file did not crated...')
            print('Exit program')
            exit(0)
    

    ## convert date from string
    ## convert date from string
    ## the format should be composit from:
    ## %Y - full year. 2018
    ## %y - partial year. 18
    ## %m - number months
    ## %d - number days
    ## %H - hours
    ## %M - minuts
    ## %S - seconds
    ## the format can be use like: '%Y-%m-%d' from the date like '2018-05-23'
    def bytesdate2num(fmt, encoding='utf-8'):
        strconverter = mdates.strpdate2num(fmt)
        def bytesconverter(b):
            s = b.decode(encoding)
            return strconverter(s)
        return bytesconverter

    ## Read data from file to list
    ## I take only the 6 first data, but you cat take more as you wish
    def getData_list(stockName):
        labels = ['Date', 'Open', 'High', 'Low', 'Close','Volume'] #, 'ExDividend','SplitRatio','AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']
        df = []
        with open(stockName+'.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                strintLine = ''
                for l in labels:
                    strintLine = strintLine + row[l] + ',' # Comma separated! 
                strintLine = strintLine[:len(strintLine)-1]# cut the last Comma.
                df.append(strintLine)
        return df

    def show_graph(stockName, bayAt = 'random'):
        plt.close('all')
        
        ## get data from file.csv we allrady have
        try:
            df = getData_list(stockName)
            if(df == []):
                print('No data found in thes times, for the stock ' ,stockName )
                return
        except:
            print('there isn\'t file with name \'{0}.csv\''.format(stockName))
            return
            
        date , closep, highp, lowp, openp, volume = np.loadtxt(df,
                                                               delimiter=',',
                                                               unpack=True,
                                                               converters={0: bytesdate2num('%Y-%m-%d')})        

        ## create a fig - we save it in the end of the program(function)
        fig = plt.figure()
        
        ax = plt.subplot2grid((1,1),(0,0))
        ax.plot_date(date, closep, '-', label='Price', linewidth=1, color='b')
        ax.plot([],[],linewidth=5, label='lose', color='r', alpha=0.5)
        ax.plot([],[],linewidth=5, label='gain', color='g', alpha=0.5)

        if bayAt == 'random':
            bayAt = random.choice(closep)
            print('random bayAt price: ' , bayAt)
        if bayAt >= 0:
            ax.fill_between(date, closep, bayAt, where=(closep < bayAt), facecolor='r', alpha=0.5)
            ax.fill_between(date, closep, bayAt, where=(closep > bayAt), facecolor='g', alpha=0.5)
        else:
            ax.fill_between(date, closep, 0, alpha=0.3)
        
        for label in ax.xaxis.get_ticklabels():
                label.set_rotation(45)
        ax.grid(True, linestyle='--')

        ax.set_xlabel('Date')
        ax.xaxis.label.set_color('k')

        ax.set_ylabel('closing Price ($)')
        ax.yaxis.label.set_color('k')

        ax.spines['left'].set_color('c')
        ax.spines['left'].set_linewidth(2)
        ax.spines['right'].set_color('c')
        ax.spines['left'].set_linewidth(2)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.tick_params(axis='y', colors='#0033cc')
        ax.tick_params(axis='x', colors='#0033cc')

        ax.axhline(bayAt, color='k', linewidth=2)
        ax.set_yticks([0,25,50,75])
        
        plt.title(stockName+' Stock')
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0.4)
        plt.legend()
        plt.show()
        fig.set_size_inches((11, 8.5), forward=False)
        fig.savefig((''+ stockName + ' Stock.png'), dpi=500)
    ##############################################################

    ## run the function
    ## first check if the user want to override and loada new range data
    if(times is not None):
        print('there hasn\'t allrady a file data')
        generateFile(stockName)
    
    try:
        show_graph(stockName, bayAt = bayAt)
    except:
        ## if we have exception like Missing Data , we create a new data in range of ten years from now to back
        print('catch exception')
        times = '10y'
        generateFile(stockName)
        ## and try to load and show the graph again
        show_graph(stockName, bayAt = bayAt)
##---------------------------------------------------------------------------------------------------------
       
stockName = 'SD'
#stockName, Symbols = getRandomSymbol()
#if stockName not in Symbols: print('Notice! the Symbol {0} isn\'t in the symbol list!'.format(stockName))

GraphIt(stockName, bayAt='random', times = '7m') # bayAt= -1 ,times - to overide the old data enter the time you want
