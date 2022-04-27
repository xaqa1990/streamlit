import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd


df_bos = pd.read_csv("boston.csv")

df_bos.rename(columns={"Lat":"lat", "Lon": "lon"}, inplace= True)

category_list = []


for c in df_bos.Category:
    if c.lower().strip() not in category_list:
        category_list.append(c.lower().strip())
st.write(category_list)

sub_df_list = []

for c in category_list:
    sub_df = df_bos[df_bos["Category"].str.lower().str.strip() == c]
    sub_df_list.append(sub_df)

layer_list = []

for sub_df in sub_df_list:
    layer = pdk.Layer(type = 'ScatterplotLayer',
                  data=sub_df,
                  get_position='[lon, lat]',
                  get_radius=300,
                  get_color=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)],
                  pickable=True
                  )
    layer_list.append(layer)

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

        st.pydeck_chart(map)


