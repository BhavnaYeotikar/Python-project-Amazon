#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


# # DATA CLEANING

# In[ ]:


#Reading Data


# In[3]:


df = pd.read_csv("Amazon sale report (1).csv")


# In[ ]:


#Dataframe


# In[5]:


df


# #Datatype of Columns

# In[7]:


df.dtypes


# In[ ]:


#Delete the unnecessary Columns


# In[9]:


df=df.drop(["Unnamed: 22", "currency"], axis=1)
df


# In[10]:


df=df.drop(columns=["ship-country"], axis=1)
df


# In[11]:


df=df.drop(columns=["Sales Channel "], axis=1)
df


# In[ ]:


#Extracted the data from 01-04-2022 to 29-06-2022


# In[12]:


df["Date"]=pd.to_datetime(df["Date"])
s = "2022-04-01"
e = "2022-06-29"
df=df.query('Date>=@s and Date<=@e')
df


# In[13]:


df.dtypes


# In[ ]:


# Dropped duplicate records 


# In[14]:


df.drop_duplicates(subset=["ASIN", "Order ID"], inplace=True)
df


# In[ ]:


#Fill null values


# In[15]:


values={"Courier Status": "Unknown", "promotion-ids": "No Promotion", "Amount":0, "ship-city": "Others", "ship-state": "Others","ship-postal-code":"Others"}
df=df.fillna(value=values)
df


# In[ ]:


#Renaming Column


# In[44]:


df=df.rename(columns={'B2B':'Customer_type'})
df


# In[ ]:


#Checking if There is any null value


# In[18]:


df['Customer_type'].isnull().sum()


# In[ ]:


#Renaming Amount column


# In[19]:


df=df.rename(columns={'Amount':'Order_amount'})
df


# In[ ]:





# In[ ]:


#Replace the values of Customer column


# In[21]:


df['Customer_type']=df['Customer_type'].map({True: 'Business' ,False: 'Customer'})
df


# In[ ]:


#Conversion of currency


# In[22]:


exchange_rate = 0.0120988
df['Order_amount'] = (df['Order_amount'].apply(lambda x: x * exchange_rate)).round(2)
df


# In[ ]:


#Extracting Month from Date


# In[23]:


df['Month']=df['Date'].dt.month_name()
df


# In[24]:


df.head()


# In[25]:


list(df.head())


# In[ ]:


#Changing the position of columns


# In[26]:


df=df[['index',
 'Order ID',
 'Date', 'Month',
 'Status',
 'Fulfilment',
 'ship-service-level',
 'Style',
 'SKU',
 'Category',
 'Size',
 'ASIN',
 'Courier Status',
 'Qty',
 'Order_amount',
 'ship-city',
 'ship-state',
 'ship-postal-code',
 'promotion-ids',
 'Customer_type',
 'fulfilled-by',
 ]]
df


# In[27]:


df.head(3)


# In[28]:


size=df['Size'].unique()
size


# In[29]:


size=['XS','S','M','L','XL', 'XXL','3XL', '4XL', '5XL','6XL',
       'Free']


# In[30]:


df.isna().any()


# In[ ]:


#Checking unique values of city


# In[31]:


df['ship-city'].unique()


# In[ ]:


#Changing city names into title case


# In[32]:


df['ship-city']=df['ship-city'].str.title()
df.head(3)


# In[ ]:


#Changing State names into title case


# In[33]:


df['ship-state']=df['ship-state'].str.title()
df['ship-state'].unique()


# In[ ]:


#Cleaning names


# In[34]:


df['ship-state']=df['ship-state'].replace({'Apo':'Andra Pradesh','Pb': 'Punjab', 'Rj': 'Rajasthan', 'Ar': 'Arunachal Pradesh', 'Nl': 'Nagaland'})
df


# # Data Analysis

# In[ ]:


#Categories by Order amount


# In[35]:


df1 = df.groupby('Category', as_index=False)['Order_amount'].sum()
df1['percent'] = ((df1['Order_amount'] / df1['Order_amount'].sum()) * 100).round(2)
df1



# In[ ]:


#sales by customer type


# In[111]:


grouped_df = df.groupby(['Customer_type', 'Category'], as_index=False)['Order_amount'].sum()

grouped_df


# In[ ]:


#Insight: Customer sales amount is greater than business sales amount


# In[ ]:


#Checking Order categories of higest sales


# In[36]:


df2= df1.nlargest(3, 'percent')
df2


# In[ ]:


#Largest sales categories are Set, Kurta, and Sarees this are strongest points


# In[46]:


import matplotlib.pyplot as plt

categories = df2['Category']
percentages = df2['percent']  # Replace with your actual percentage data

plt.xlabel('Category')
plt.ylabel('Percentage of Sale')
plt.title('Category of highest Sales')

# Use plt.bar() to create a bar chart
plt.bar(categories, percentages, width=0.2, color='blue')

plt.show()


# In[ ]:


#Checking Order categories of minimum sales


# In[37]:


df3= df1.nsmallest(3, 'percent')
df3


# In[ ]:


#Lowest sales categories are Dupatta, Saree and bottom we should focus on promotion of this products.


# In[38]:


import matplotlib.pyplot as plt

categories = df3['Category']
percentages = df3['percent']  # Replace with your actual percentage data

plt.xlabel('Category')
plt.ylabel('Percentage of Sale')
plt.title('Category of Lowest Sales')

# Use plt.bar() to create a bar chart
plt.bar(categories, percentages, width=0.2, color='red')

plt.show()


# In[ ]:


#Sales by considering cancelled orders


# In[51]:


df5=df[df['Status']!='Cancelled']
df6 = df5.groupby('Category', as_index=False)['Order_amount'].sum()
df6['percent'] = ((df6['Order_amount'] / df6['Order_amount'].sum()) * 100).round(2)
df6


# #Insights: Cancelled order amount we have calculated which is matter of concern we should reduce days of cancellation or return products so that the cancellation of orders will have control we should also check the qualities of products that are cancelled most like set and kurta and get appropriate reviews on that.

# In[ ]:





# In[ ]:





# In[39]:





# In[ ]:


#Highest sales by considering cancelled orders


# In[112]:


dfl= df6.nlargest(3, 'percent')
dfl


# In[ ]:





# In[ ]:


#Lowest sales by considering cancelled orders


# In[69]:


dfs= df6.nsmallest(3, 'percent')
dfs


# In[ ]:





# In[ ]:


#State wise Lowest Sales


# In[114]:


import plotly.express as px

df8 = df[df['Category'].isin(df7['Category'])]
grouped_df = df8.groupby(['ship-state', 'Category'], as_index=False)['Order_amount'].sum()

fig = px.bar(grouped_df, x='ship-state', y='Order_amount', color='Category', barmode='group',
             title='Sales of bottom three products', labels={'Order_amount': 'Sales', 'ship-state': 'State', 'Category': 'Products'})
fig.update_layout(xaxis_title='States', yaxis_title='Total sales')
fig.show()



# #Insights: we should focus on states where sales and minimum like arunachal pradesh, New delhi  and arrange offline promotion campaigns over there or some offers should be introduce on first order so that people will have an idea of quality of product and sales will get increased.

# In[ ]:


#State and month wise revenue collection


# In[60]:


sort_order=['April','May','June']
df12=df.groupby(['ship-state','Month'],as_index=False)['Order_amount'].sum()
df12=df12.sort_values('Order_amount')
df12


# In[ ]:


We should focus on the months when sales is minimum and arrange some offer or deals on products when there will be no any festival or anything.


# In[77]:


import pandas as pd
import plotly.express as px
df['promotion Status']=df['promotion-ids'].apply(lambda x:'No Promotion' if x=='No Promotion' else 'with Promotion')
sales=df.groupby(['Category','Promotion Status'])['Order_amount'].sum().reset_index()
fig=px.line(sales,x='Category',y='Order_amount',color='Promotion Status', title='sales',
           labels={'Order_amount':'Total sales', 'Category':'Category'})
fig.show()
                                                                      


# #with promotion sales improved for categories like saree, set and top so we should focus on promotion of this products.

# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




