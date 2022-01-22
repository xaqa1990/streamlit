import streamlit as st
import matplotlib.pyplot as plt




# Set tile of the app and header of the sidebar

st.sidebar.header('Inputs')

# Select the fruit you want to show in the chart
fruit_list = ['Apple', 'Orange', 'Pear', 'Banana']
selected_fruit = st.sidebar.multiselect("Please select the fruit: ", fruit_list)
selected_fruit.sort()


# Generate the sliders for fruit prices




st.title(f'Fruit Price and amount')
# Generate a list of prices for selected fruit
price_list = []
amount_list = []

if "Apple" in selected_fruit:
    apple_value = st.sidebar.slider("Apple_price",0.00,10.00)
    price_list.append(apple_value)
    
    apple_amount = st.sidebar.slider("How many apples you need?",0,20)
    amount_list.append(apple_amount)

if "Banana" in selected_fruit:
    banana_value = st.sidebar.slider("Banana_price",0.00,10.00)
    price_list.append(banana_value)
    
    banana_amount = st.sidebar.slider("How many bananas you need?",0,20)
    amount_list.append(banana_amount)

if "Orange" in selected_fruit:
    orange_value = st.sidebar.slider("Orange_price",0.00,10.00)
    price_list.append(orange_value)
    
    orange_amount = st.sidebar.slider("How many oranges you need?",0,20)
    amount_list.append(orange_amount)

if "Pear" in selected_fruit:
    pear_value = st.sidebar.slider("Pear_price",0.00,10.00)
    price_list.append(pear_value)
    
    pear_amount = st.sidebar.slider("How many pears you need?",0,20)
    amount_list.append(pear_amount)


# Select the color for the bar chart
colors = {"red":"r","green":"g","yellow":"y","blue":"b"}
color_names = list(colors.keys())

selected_color_name = st.sidebar.radio('Color:', color_names)
selected_color = colors[selected_color_name]

# Plot the bar chart
fig, ax = plt.subplots()
ax.bar(selected_fruit,price_list, color = selected_color)
ax.set_xlabel("Fruits")
ax.set_ylabel("Price")
st.pyplot(fig)


fig, ax = plt.subplots()
ax.pie(amount_list, labels = selected_fruit)

st.pyplot(fig)
