import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

#path = "/Users/ax/Documents/Bentley/teaching/CS230/Spring2023/spring2023_in_class/Charts/"
dfpct = pd.read_csv('cars_pct.csv', index_col='Country')
print(dfpct)


# Remove all the NaN data using df.dropna()
dfpct.dropna(inplace= True)


# Show the data in simple lines with df.plot()
# Each column becomes one line, row indexes become the x-axis
dfpct.plot()
st.pyplot()

# Transpose the dataset using df.transpose() if needed
dfpct = dfpct.transpose()
dfpct.plot()
st.pyplot()

# Order the x-axis if needed using df.sort_index()
dfpct.sort_index(inplace=True)
dfpct.plot()
st.pyplot()


# Show the plot


# Show the plot in streamlit


# Plot only Iceland, Sweden, Netherlands, Denmark, Switzerland from 2015 - 2018
df_new = dfpct.loc["2015":"2018", "Iceland":"Denmark"]
df_new.plot()
#st.pyplot()


# Add a label for x axis using plt.xlabel()
plt.xlabel("Year")

# Add a label for y axis using plt.ylabel()
plt.ylabel("Percentage")

# Add a title for the plot using plt.title()
plt.title("Car Percentage")

#Add/Change legend using plt.legend(labels = ["line 1", "line 2"])
st.pyplot()



df_sales = pd.read_csv(path + 'cars_sales.csv', index_col='Country')
print(df_sales)

# Show the bar chart of all sales in Germany using df.plot(kind = "bar"/"barh")
df_sales.loc["Germany"].plot(kind = "bar")
st.pyplot()

df_sales.loc["Germany"].plot(kind = "bar", color = ["red", "yellow", "green", "blue"])
st.pyplot()

df_sales.loc["Germany"].plot(kind = "barh")
st.pyplot()

# Show the bar chart for all countries in 2020
df_sales.loc[:,"2020"].plot(kind = "bar")
st.pyplot()

# Show the bar chart for all countries in 2020 with sales ordered
df_sales.loc[:,"2020"].sort_values().plot(kind = "bar")
st.pyplot()

# Show the cluster bar chart for Germany, Norway, France
df_sales
df_sales.loc[["Germany", "Norway", "France"]].plot(kind = "bar")
st.pyplot()

df_sales=df_sales.transpose()
df_sales[["Germany", "Norway", "France"]].plot(kind = "bar")

st.pyplot()

# Show the stacked bar chart for Germany, Norway, France
df_sales[["Germany", "Norway", "France"]].plot(kind = "bar", stacked = True)
st.pyplot()


# Show the sales distrubution in year 2020

df_sales.loc["2020"].plot(kind = "pie")
st.pyplot()

df_sales["France"].plot(kind = "pie")
st.pyplot()

# To show the percentage of each category using df.plot(kind = "pie", autopct = "%.1f%%")
'''
autopct = '%.1f' # display the percentage value to 1 decimal place
autopct = '%.2f' # display the percentage value to 2 decimal places
autopct = '%.1f%%' # display the percentage value to 1 decimal places with the percentage sign
autopct = '%.2f%%' # display the percentage value to 2 decimal places with the percentage sign
'''


# To show the absolute value of each category (optional)
#df.plot(kind = "pie", autopct = lambda p: '{:.0f}'.format(p * sum(df) / 100))
