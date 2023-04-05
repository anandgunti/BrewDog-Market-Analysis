#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


pip install 


# In[2]:


trade = pd.read_csv("Trade.csv") #importing trade master file 
tr = pd.read_csv("trade res.csv")#importing the additional file for trade classification


# # Selecting the required data from Master file and Rearranging the data

# ###### The dataset (trade_pivot) below is used for representing the Trade across continents

# In[3]:


pivot = trade.pivot_table('Y2020', ['Area','Item'], 'Element') #selecting the required variables using pivot table
trade_pivot = pivot.reset_index()


# ###### The dataset (trpivot) below is used for representing the Classfications of Trade and Distribution of Trade

# In[4]:


pivot = tr.pivot_table('Value', ['Area','Element'], ['Item']) #selecting the required variables for representing trade classification
trpivot = pivot.reset_index()


# # Adding continents to the countries 
# 

# In[5]:



north_america = ['Canada', 'United States of America','Antigua and Barbuda', 'Bahamas', 'Barbados', 'Cuba', 'Dominica',
       'Dominican Republic', 'Grenada', 'Guadeloupe', 'Haiti', 'Jamaica',
       'Martinique', 'Puerto Rico', 'Saint Kitts and Nevis',
       'Saint Lucia', 'Saint Vincent and the Grenadines',
       'Trinidad and Tobago']
south_america = ['Argentina', 'Bolivia (Plurinational State of)', 'Brazil', 'Chile',
       'Colombia', 'Ecuador', 'French Guyana', 'Guyana', 'Paraguay',
       'Peru', 'Suriname', 'Uruguay',
       'Venezuela (Bolivarian Republic of)','Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras',
       'Mexico', 'Nicaragua', 'Panama']


north_africa = ['Algeria', 'Egypt', 'Libya', 'Morocco', 'Sudan', 'Sudan (former)',
       'Tunisia','Botswana', 'Eswatini', 'Lesotho', 'Namibia', 'South Africa','Burundi', 'Comoros', 'Djibouti', 'Eritrea', 'Ethiopia',
       'Ethiopia PDR', 'Kenya', 'Madagascar', 'Malawi', 'Mauritius',
       'Mozambique', 'Réunion', 'Rwanda', 'Seychelles', 'Somalia',
       'South Sudan', 'Uganda', 'United Republic of Tanzania', 'Zambia',
       'Zimbabwe','Benin', 'Burkina Faso', 'Cabo Verde', "Côte d'Ivoire", 'Gambia',
       'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali',
       'Mauritania', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone',
       'Togo','Angola', 'Cameroon', 'Central African Republic', 'Chad', 'Congo',
       'Democratic Republic of the Congo', 'Equatorial Guinea', 'Gabon',
       'Sao Tome and Principe']

east_asia = ['China, Hong Kong SAR', 'China, Macao SAR', 'China, mainland',
       'China, Taiwan Province of',
       "Democratic People's Republic of Korea", 'Japan', 'Mongolia',
       'Republic of Korea']
west_asia = ['Armenia', 'Azerbaijan', 'Bahrain', 'Cyprus', 'Georgia', 'Iraq',
       'Israel', 'Jordan', 'Kuwait', 'Lebanon', 'Oman', 'Palestine',
       'Qatar', 'Saudi Arabia', 'Syrian Arab Republic', 'Türkiye',
       'United Arab Emirates', 'Yemen']
central_asia = ['Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan',
       'Uzbekistan']
south_asia = ['Afghanistan', 'Bangladesh', 'Bhutan', 'India',
       'Iran (Islamic Republic of)', 'Maldives', 'Nepal', 'Pakistan',
       'Sri Lanka']
south_east_asia = ['Brunei Darussalam', 'Cambodia', 'Indonesia',
       "Lao People's Democratic Republic", 'Malaysia', 'Myanmar',
       'Philippines', 'Singapore', 'Thailand', 'Timor-Leste', 'Viet Nam']


east_europe = ['Belarus', 'Bulgaria', 'Czechia', 'Czechoslovakia', 'Hungary',
       'Poland', 'Republic of Moldova', 'Romania', 'Russian Federation',
       'Slovakia', 'Ukraine', 'USSR']
west_europe = ['Austria', 'Belgium', 'Belgium-Luxembourg', 'France', 'Germany',
       'Luxembourg', 'Netherlands', 'Switzerland']
north_europe = ['Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'Iceland',
       'Ireland', 'Latvia', 'Lithuania', 'Norway', 'Sweden',
       'United Kingdom of Great Britain and Northern Ireland']
south_europe = ['Albania', 'Bosnia and Herzegovina', 'Croatia', 'Greece', 'Italy',
       'Malta', 'Montenegro', 'North Macedonia', 'Portugal', 'Serbia',
       'Serbia and Montenegro', 'Slovenia', 'Spain', 'Yugoslav SFR']

oceania = ['Cook Islands', 'Fiji', 'French Polynesia',
       'Kiribati', 'Marshall Islands', 'Micronesia (Federated States of)',
       'Nauru', 'New Caledonia', 'Niue',
       'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tokelau', 'Tonga',
       'Tuvalu', 'Vanuatu','Kiribati', 'Marshall Islands', 'Micronesia (Federated States of)',
       'Nauru','Fiji', 'New Caledonia', 'Papua New Guinea', 'Solomon Islands',
       'Vanuatu','Australia', 'New Zealand']


# In[6]:


def GetConti(counry):
    if counry in east_asia or counry in west_asia or counry in south_asia or counry in central_asia or counry in south_east_asia:
        return "Asia"
    elif counry in east_europe or counry in west_europe or counry in north_europe or counry in south_europe:
        return "Europe"
    elif counry in north_africa:
        return "Africa"
    elif counry in north_america:
        return "North America"
    elif counry in south_america:
        return "South America"
    else:
        return "Oceania"


# In[7]:


trade_pivot['Regions'] = trade_pivot['Area'].apply(lambda x: GetConti(x)) # Calling the function and appending the continents(Regions)

trpivot['Regions'] = trpivot['Area'].apply(lambda x: GetConti(x)) # Calling the function and appending the continents(Regions)

trade_clean = trade_pivot.fillna(0) #Replacing the null values with 0

trclean = trpivot.fillna(0) #Replacing the null values with 0


# ###### Normalizing and Generating  The Data Required For Data Visualization 

# In[8]:


trade_clean['Export Value'] = trade_clean['Export Value']/1000000 #Converting trade value in terms of one Billion USD from 1000 USD

trade_clean['Import Value'] = trade_clean['Import Value']/1000000 #Converting trade value in terms of one Billion USD from 1000 USD

trade_clean['Export Quantity'] = trade_clean['Export Quantity']/1000000 #Converting trade Quantity in terms of million tonnes from 1 tonne

trade_clean['Import Quantity'] = trade_clean['Import Quantity']/1000000 #Converting trade Quantity in terms of million tonnes from 1 tonne

trade_clean['Net_trade'] = trade_clean['Export Value'] - trade_clean['Import Value'] #Net trade calculation and appending to DataFrame


# In[9]:


trclean.iloc[:,2:8] = trclean.iloc[:,2:8]/100000


# # Trade Data Visualization

# In[10]:


import panel as pn
import hvplot.pandas 
import matplotlib.pyplot as plt


# ## Interactive Design using Panel  

# In[11]:


idf = trade_clean.interactive()


# #### Function for visualization of Import and Export parameters

# In[12]:


def Trade_fxn(yaxis,graph,label): ##Three positional arguments Y axis input , kind of graph (ex: line,bar,scatter) and label  
                        
     
    #creating widgets for graphs and visualization
    
    yaxis_col = pn.widgets.RadioButtonGroup( name='Y axis', 
     options=yaxis,
    button_type='success'
    )  
    
    continents = ['Asia', 'Europe', 'Africa', 'North America', 'South America','Oceania']
    
    #Data pipeline - Attaching the related data 
    data_pipeline = (
        idf[   
            (idf.Regions.isin(continents)) 
        ]
        .groupby(['Regions'])[yaxis_col].sum()
        .to_frame()
        .reset_index() 
    ) 
    
    
    #plotting the graph using hvplot 
    
    trade_plot = data_pipeline.hvplot(x = 'Regions', y=yaxis_col ,kind = graph, rot =45,
                                      
                                      color=("#fd7f6f"),ylabel = label,width=450,height = 450)
    return trade_plot


# #### Data Visualization of Trade Categories across continents

# In[14]:


idfs = trclean.interactive()


# In[15]:


def items_fxn(items,graph): ##Two positional arguments : Y axis input and kind of graph (ex: line,bar,scatter) 
                        
     
    #creating widgets for graphs and visualization
    
    yaxis_col = pn.widgets.Select(name='Category', options=items)
    trade = ['Import Value','Export Value']

    #Data pipeline - Attaching the related data 
    
    data_pipeline = (
        idfs[   
            (idfs.Element.isin(trade)) 
        ]
        .groupby(['Element','Regions'])[yaxis_col].sum()
        .to_frame()
        .reset_index() 
    )
    
     #plotting the graph using hvplot 
    
    data_plot = data_pipeline.hvplot(x = 'Element', by = 'Regions', y=yaxis_col ,alpha = 13,kind = graph,
                                     title="Trade parameters in a category  ",width=400,grid=True,
                                     color=(['#10a735','#118fa4','#ffa600','#13b6da','#bc5090','#ff6361']),invert = True)
    
    return data_plot


# #### Function for Data Visualization  of Trade Distribution (Import and Export Quantities and Values)

# In[16]:


def distribution():
    j = trade_clean.hvplot.hexbin(x='Import Quantity' , y='Export Quantity', width=500, height=500, logz=True,invert = True)
    return display(j)


# ##### Total Trade as a percentage across Regions

# In[17]:


total_trade = trade_pivot.pivot_table( ['Export Value','Import Value'],['Regions']).reset_index()
    
total_trade['Total'] =((total_trade.iloc[:,2] + total_trade.iloc[:,2])/((total_trade.iloc[:,2] + total_trade.iloc[:,2]).sum())*100) .round()
total_trade[['Regions','Total']]


#                 Table 4.a Percantage of Trade across Regions

# # 

# # Data Visualization Insights

# In[18]:


d = Trade_fxn(['Export Quantity'],'bar','Trade in  Million Tonnes  (Export Quantity)') #calling the function by using variables in list format. Variables = Import Value','Export Value','Import Quantity','Export Quantity'
e = Trade_fxn(['Export Value'],'bar','Trade in  Billion USD  (Export Value') #calling the function by using variables in list format. Variables = Import Value','Export Value','Import Quantity','Export Quantity'
f = Trade_fxn(['Import Quantity'],'bar','Trade in  Million Tonnes  (Export Quantity') #calling the function by using variables in list format. Variables = Import Value','Export Value','Import Quantity','Export Quantity'
g = Trade_fxn(['Import Value'],'bar','Trade in  Billion USD  (Export Value)') #calling the function by using variables in list format. Variables = Import Value','Export Value','Import Quantity','Export Quantity'


# In[19]:


display((d+e),(f+g)) 


#                                 Graph 4.1 Trade parameters across Regions

# In[20]:


distribution()


#                                     Graph 4.2 Trade Quantity Distribution

# In[21]:


a =items_fxn(['Cereals'],'bar')
b =items_fxn(['Other food'],'bar')
c =items_fxn(['Pulses'],'bar')

d =items_fxn(['Vegetable Oil and Fat',],'bar')
e =items_fxn(['Dairy Products and Eggs',],'bar')


# In[22]:


display(a+b, c+d,e)


#                                Graph 4.3 Trade categories across the Regions with Trade parameters

# # Work in progress

# In[ ]:





# In[ ]:


data_plot = total_trade.hvplot.bar(x = 'Regions', y=['Total'] ,alpha = 13,
                                     title="Trade parameters in a category  ",height=1000,grid=True,
                                     color=(['#ff6361']))


# In[ ]:


data_plot


# In[ ]:


a= trade_clean.groupby(['Area'])['Item'].count().reset_index()


# In[20]:


trade_pivot


# In[ ]:




