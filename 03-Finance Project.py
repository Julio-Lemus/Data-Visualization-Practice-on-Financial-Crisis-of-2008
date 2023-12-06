#!/usr/bin/env python
# coding: utf-8

# # Finance Data Project 
# 
# In this data project we will focus on exploratory data analysis of stock prices. Keep in mind, this project is just meant to practice your visualization and pandas skills, it is not meant to be a robust financial analysis or be taken as financial advice.
# ____
# We'll focus on bank stocks and see how they progressed throughout the [financial crisis](https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%9308) all the way to early 2016.

# ## Get the Data
# 
# *Note: [You'll need to install pandas-datareader for this to work!](https://github.com/pydata/pandas-datareader) Pandas datareader allows you to [read stock information directly from the internet](http://pandas.pydata.org/pandas-docs/stable/remote_data.html) Use these links for install guidance (**pip install pandas-datareader**), or just follow along with the video lecture.*

# ## Data
# 
# We need to get data using pandas datareader. We will get stock information for the following banks:
# *  Bank of America
# * CitiGroup
# * Goldman Sachs
# * JPMorgan Chase
# * Morgan Stanley
# * Wells Fargo
# 
# ** Figure out how to get the stock data from Jan 1st 2006 to Jan 1st 2016 for each of these banks. Set each bank to be a separate dataframe, with the variable name for that bank being its ticker symbol. This will involve a few steps:**
# 1. Use datetime to set start and end datetime objects.
# 2. Figure out the ticker symbol for each bank.
# 2. Figure out how to use datareader to grab info on the stock.
# 
# ** Use [this documentation page](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html) for hints and instructions (it should just be a matter of replacing certain values. Use google finance as a source, for example:**
#     
#     # Bank of America
#     BAC = data.DataReader("BAC", 'google', start, end)
# 
# ### WARNING: MAKE SURE TO CHECK THE LINK ABOVE FOR THE LATEST WORKING API.

# In[ ]:


get_ipython().system('pip install yfinance')


# In[2]:


from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import yfinance as yf
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


yf.pdr_override()
start = datetime.date(2006, 1, 1)
end = datetime.date(2016, 1, 1)
# Bank of America
BAC = data.get_data_yahoo('BAC', start, end)
 
# CitiGroup
C = data.get_data_yahoo('C', start, end)
 
# Goldman Sachs
GS = data.get_data_yahoo('GS', start, end)
 
# JPMorgan Chase
JPM = data.get_data_yahoo('JPM', start, end)
 
# Morgan Stanley
MS = data.get_data_yahoo('MS', start, end)
 
# Wells Fargo
WF = data.get_data_yahoo('WFC', start, end)


# In[4]:


MS.head()


# ** Create a list of the ticker symbols (as strings) in alphabetical order. Call this list: tickers**

# In[5]:


tickers = ["BAC", "C", "GS", "JPM", "MS", "WF"]


# ** Use pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks. Set the keys argument equal to the tickers list. Also pay attention to what axis you concatenate on.**

# In[6]:


bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WF], axis=1, keys=tickers)
bank_stocks.head()


# In[7]:


bank_stocks.columns.names = ['Bank Ticker','Stock Info']


# ** Check the head of the bank_stocks dataframe.**

# In[8]:


bank_stocks.head()


# # EDA
# 
# Let's explore the data a bit! Documentation on [Multi-Level Indexing](http://pandas.pydata.org/pandas-docs/stable/advanced.html) and [Using .xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html).
# 
# ** What is the max Close price for each bank's stock throughout the time period?**

# In[9]:


bank_stocks.xs(key="Close", axis=1, level="Stock Info").max()


# ** Create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. returns are typically defined by:**
# 
# $$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$

# In[10]:


returns = pd.DataFrame()


# ** We can use pandas pct_change() method on the Close column to create a column representing this return value. Create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.**

# In[11]:


for tick in tickers:
    returns[tick + " Return"] = bank_stocks[tick]['Close'].pct_change()


# In[12]:


returns.head()


# ** Create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?**

# In[13]:


import seaborn as sns


# In[14]:


sns.pairplot(returns[1:])


# * See solution for details about Citigroup behavior....

# ** Using this returns DataFrame, figure out on what dates each bank stock had the best and worst single day returns. You should notice that 4 of the banks share the same day for the worst drop, did anything significant happen that day?**

# In[15]:


returns.idxmin()


# ** You should have noticed that Citigroup's largest drop and biggest gain were very close to one another, did anythign significant happen in that time frame? **

# ** Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015?**

# In[16]:


returns.std()


# In[17]:


returns.loc['2015-01-01': '2015-12-31'].std()


# ** Create a distplot using seaborn of the 2015 returns for Morgan Stanley **

# In[18]:


sns.distplot(returns["MS Return"].loc['2015-01-01': '2015-12-31'], color='green', bins=50)


# ** Create a distplot using seaborn of the 2008 returns for CitiGroup **

# In[19]:


sns.distplot(returns["C Return"].loc['2008-01-01': '2008-12-31'], color='red', bins=100)


# ____
# # More Visualization
# 
# A lot of this project will focus on visualizations. Feel free to use any of your preferred visualization libraries to try to recreate the described plots below, seaborn, matplotlib, plotly and cufflinks, or just pandas.
# 
# ### Imports

# In[ ]:


get_ipython().system('pip install plotly cufflinks')


# In[21]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()


# ** Create a line plot showing Close price for each bank for the entire index of time. (Hint: Try using a for loop, or use [.xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html) to get a cross section of the data.)**

# In[22]:


for tick in tickers:
    bank_stocks[tick]["Close"].plot(label=tick, figsize=(12,4))
    
plt.legend()


# In[23]:


bank_stocks.head()


# In[24]:


bank_stocks.xs(key="Close", axis=1, level="Stock Info").iplot()


# ## Moving Averages
# 
# Let's analyze the moving averages for these stocks in the year 2008. 
# 
# ** Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**

# In[25]:


plt.figure(figsize=(12,4))
BAC["Close"].loc['2008-01-01' : '2008-12-01'].rolling(window=30).mean().plot(label='30 Day Moving Average')
BAC["Close"].loc['2008-01-01' : '2008-12-01'].plot(label='BAC Close', color='green')
plt.legend()


# ** Create a heatmap of the correlation between the stocks Close Price.**

# In[26]:


sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)


# ** Optional: Use seaborn's clustermap to cluster the correlations together:**

# In[27]:


sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)


# # Part 2 (Optional)
# 
# In this second part of the project we will rely on the cufflinks library to create some Technical Analysis plots. This part of the project is experimental due to its heavy reliance on the cuffinks project, so feel free to skip it if any functionality is broken in the future.

# ** Use .iplot(kind='candle) to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016.**

# In[28]:


bac15 = BAC[["Open", "High", "Low", "Close"]].loc['2015-01-01':'2016-01-01']
bac15.iplot(kind='candle')
# BAC.head()


# ** Use .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015.**

# In[29]:


MS["Close"].loc['2015-01-01' : '2016-01-01'].ta_plot(study='sma', periods=[13, 21, 55])


# **Use .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015.**

# In[30]:


BAC["Close"].loc['2015-01-01' : '2016-01-01'].ta_plot(study='boll')


# # Great Job!

# In[ ]:




