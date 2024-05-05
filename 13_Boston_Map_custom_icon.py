import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd

st.title("Boston Map with Custom Icons")

# Write image
from PIL import Image

# Open your image using Image.open(file_path)
img = Image.open("Python.png")

# Show your image using st.image()
st.image(img, width= 150, caption= "Python Icon")

df_bos = pd.read_csv("boston.csv")

df_bos.rename(columns={"Lat":"lat", "Lon": "lon"}, inplace= True)

URL_list = [
    "https://upload.wikimedia.org/wikipedia/commons/f/f4/Graduation-cap-239875.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/e/ee/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Fountain_%E2%80%93_Tourism_%E2%80%93_White.png",
    "https://upload.wikimedia.org/wikipedia/commons/d/d8/Ejibon_Online_Shopping_Icon.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/01/Round_Landmark_Icon_Park.svg",


]

category_list = []


for c in df_bos.Category:
    if c.lower().strip() not in category_list:
        category_list.append(c.lower().strip())


sub_df_list = []

for c in category_list:
    sub_df = df_bos[df_bos["Category"].str.lower().str.strip() == c]
    sub_df_list.append(sub_df)

layer_list = []


for i in range(len(sub_df_list)):
    icon_data = {
        "url": URL_list[i],
        "width": 100,
        "height": 100,
        "anchorY": 100
        }

    # Add icons to your dataframe
    sub_df_list[i]["icon_data"]= None
    for j in sub_df_list[i].index:
        sub_df_list[i]["icon_data"][j] = icon_data

    # Create a layer with your custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                           data = sub_df_list[i],
                           get_icon="icon_data",
                           get_position='[lon,lat]',
                           get_size=4,
                           size_scale=10,
                           pickable=True)

    layer_list.append(icon_layer)

tool_tip = {"html": "Attracction Name:<br/> <b>{Name}</b> <br/> <b>{Category}</b>",
            "style": { "backgroundColor": "orange",
                        "color": "white"}
          }

view_state = pdk.ViewState(
                latitude=df_bos["lat"].mean(),
                longitude=df_bos["lon"].mean(),
                zoom=11,
                pitch=0)



category_list.insert(0,"")

selected_category = st.selectbox("Please select a category", category_list)


for i in range(len(category_list)):
    if selected_category == category_list[i]:
        if i == 0:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_state,
                layers=layer_list,
                tooltip= tool_tip
                )
        else:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_state,
                layers=[layer_list[i-1]],
                tooltip= tool_tip
                )

            sub_cat = sub_df_list[i-1]
            attr_names = list(sub_cat.Name)
            attr_names.insert(0,"")
            selected_attr_name = st.selectbox("Please select the attraction", attr_names)

            selected_attr = sub_cat[sub_cat["Name"] == selected_attr_name]
            st.write(selected_attr.iloc[:,0:-1])

        st.pydeck_chart(map)





