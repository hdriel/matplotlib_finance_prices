# matplotlib Finance graph line prices

### Python , matplotlib

## Description

A nice project where I learned more in depth about matplotlib, and the implementation of stock chart with indicators
When running a project, i inputed before SD stock, but you can change it as you wish , or remove the marker # to random a stock from the file of list stock I published here

```python
stockName = 'SD'
#stockName, Symbols = getRandomSymbol()
#if stockName not in Symbols: print('Notice! the Symbol {0} isn\'t in the symbol list!'.format(stockName))

```

then you can change or set the period of time to import data, and setup the bayAt param : 
* -1 
* number >= 0
* 'random' 

```python
GraphIt(stockName, bayAt='random', times = '7m')
```

the program import data from the internet (quandl database) and save it in csv file 

```
Generate file data of stock: 'SD'
Between the times: start 2017-10-23 - end 2018-05-23
File 'SD.csv' created!
random bayAt price:  19.06
```

then plot the graphs, you can zoom it and so on... 

Installing required packages

```python
pip install numpy 
pip install matplotlib
pip install pandas==0.21.0
pip install pandas_datareader
pip install beatifulsoup4
pip install scikit_learn
pip install sklearn
```

___

The program running will give you the following images:

<div width=100%>
<img src="https://profile.fcdn.co.il/images2/0__05b05cfa0ddc3e.jpg" width="700" style="padding:1px;
                   border:1px solid #021a40; 
                  display: block;
                  margin-left: auto;
                  margin-right: auto "> 

<img src="https://profile.fcdn.co.il/images2/0__05b05cfac1ba2f.jpg" width="700" style="padding:1px;
                   border:1px solid #021a40; 
                  display: block;
                  margin-left: auto;
                  margin-right: auto "> 
</div>


Enjoy...
