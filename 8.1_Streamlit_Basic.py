import streamlit as st
from matplotlib import pyplot as plt
import numpy as np


# https://docs.streamlit.io/library/api-reference

# Set a title for your app
st.title("Welcome to my first app!")

# Write into your app

# Write text
st.text("I can write text here!")
a,b,c = 1,2,3
st.text(f"The variables are a = {a:<2.2f}, b = {b:< 2.1f}")
st.write("I'm writing text using a different method!")
st.success("I'm writing text using a different method!")


# Write data
langs = ['C', 'C++', 'Java', 'Python', 'PHP']
students = [23,17,35,29,12]
student_info = {"001": "Olivia",
                "002": "Paul",
                "003": "Allen",
                "004": "Katie",
                "005": "Tad"
                }
st.write(langs)
st.write(student_info)
st.success(langs)
st.success(student_info)

# Radio buttons
radio_language = st.radio("Please select a language:", ("Python", "Java", "C++"))
st.write(f"The language you chose from radio button is {radio_language}")

# Single selection box
signle_language = st.selectbox("Please select a language:", ("Python", "Java", "C++"))
st.write(f"The language you chose from single selection box is {signle_language}")

# Multi selection box
multi_language = st.multiselect("Please select the languages you like:",["Python", "Java","C++"])
st.write(f"The language you chose from multi-selection box is {multi_language}")


# Slider
number = st.slider('Pick a number', 0.00, 50.00)
st.write(f"The number you picked is {number}")

size = st.select_slider('Pick a size', ['S', 'M', 'L'])
st.write(f"The size you picked is {size}")


# Input
name = st.text_input("What's your name? ")
age = st.number_input("What's your age? ", 0.00, 100.00)
st.write(f"The age of {name} is {age}.")


# Write image
st.image("Python.png",width = 100)


# Write a matplotlib figure
fig, ax = plt.subplots() # If you have only one axis in your figure
ax.pie(students, labels = langs, autopct='%.1f%%')
st.pyplot(fig)
#st.write(fig)


# Sidebar
st.sidebar.header("I'm the sidebar")
fruit = st.sidebar.radio("Please select a fruit:", ("Apple", "Orange", "Peach"))
st.sidebar.write(f"The fruit you chose from the sidebar radio button is {fruit}")


# Balloons!
#st.balloons()


