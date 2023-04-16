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

