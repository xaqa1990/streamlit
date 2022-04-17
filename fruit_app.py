import streamlit as st
import matplotlib.pyplot as plt


# Set a title for your app
st.title("Fruit Purchase Summary")

# Set tile of the app and header of the sidebar

st.sidebar.header('Inputs')

# Select the fruit you want to show in the chart
fruit_list = ['Apple', 'Orange', 'Pear', 'Banana']
selected_fruit = st.sidebar.multiselect("Please select the fruit: ", fruit_list)

if len(selected_fruit) == 0:
    st.write("Please select your fruits.")
    st.write()

# Generate lists to store the prices and amounts of selected fruits
fruit_price_list = []
fruit_amount_list = []


# Generate the sliders for fruit prices and fruit amounts
for sf in selected_fruit:
    fruit_price = st.sidebar.slider(f"{sf} Price", 0.00, 10.00)
    st.write(f"{sf} Price is {fruit_price}.")

    fruit_amount = st.sidebar.slider(f"{sf} Amount", 0.00, 100.00)
    st.write(f"You purchased {fruit_amount} pounds of {sf}.")

    fruit_price_list.append(fruit_price)
    fruit_amount_list.append(fruit_amount)


# Select from the fruit price bar chart and fruit amount pie chart
chart = st.sidebar.selectbox("Would you like to view the bar chart of fruit price or the pie chart of fruit amount?", ["", "Fruit Price Bar Chart", "Fruit Amount Pie Chart"])

if chart == "Fruit Price Bar Chart":
    # Plot the bar chart
    if sum(fruit_price_list) == 0:
        st.write("Please adjust the fruit price first.")
    else:
        # Select the color for the bar chart
        colors = ["Orange", "Blue", "Yellow", "Green"]
        selected_color = st.sidebar.radio('Please select the color for your bar chart:', colors)
        
        fig, ax = plt.subplots()
        ax.bar(selected_fruit,fruit_price_list, color = selected_color)
        ax.set_xlabel("Fruits")
        ax.set_ylabel("Price")
        st.pyplot(fig)
elif chart == "Fruit Amount Pie Chart":
    # Plot the pie chart
    if sum(fruit_amount_list) == 0:
        st.write("Please adjust the fruit amount first.")
    else:
        fig, ax = plt.subplots()
        ax.pie(fruit_amount_list,labels = selected_fruit)
        st.pyplot(fig)

