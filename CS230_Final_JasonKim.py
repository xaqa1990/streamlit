import streamlit as st
import matplotlib.ticker
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import google_streetview.api
from PIL import Image

# Link to website: https://share.streamlit.io/jbkim01/cs230/main/CS230Final.py
# Jason Kim
# CS230-5
# Final Project: Cambridge Properties

# Change the layout of the page from "narrow" to "wide"
st.set_page_config(layout="wide")

st.title("Cambridge Properties")

# Create a dataframe of properties from the Cambridge property database
df_cambridge_properties = pd.read_csv('Cambridge_Property_Database_FY2022_8000_sample.csv')
df_property_info = df_cambridge_properties.loc[:, ["Address", "Latitude", "Longitude", "PropertyClass", "LandArea",
                                                   "ResidentialExemption", "BuildingValue", "LandValue", "AssessedValue",
                                                   "SalePrice", "SaleDate", "Exterior_Style", "Exterior_occupancy", "Interior_LivingArea",
                                                   "Interior_Bedrooms", "Interior_FullBaths", "Interior_HalfBaths",
                                                   "Condition_YearBuilt", "Parking_Open", "Parking_Covered", "Parking_Garage"]]
df_property_info = df_property_info[(df_property_info.PropertyClass.str.lower().isin(["sngl-fam-res", "two-fam-res", "three-fm-res",
                                                                                      "4-8-unit-apt", ">8-unit-apt", "condominium",
                                                                                      "cndo lux", "condo-bldg"])) &
                                    (df_property_info.SalePrice > 100000)]
df_property_info.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)
property_types = ["Single Family", "Two Family", "Three Family", "4+ Unit", "Condominium"]


def previous_page(page):
    if page > 1:
        page -= 1
    return page


def next_page(page, num_pages):
    if page < num_pages:
        page += 1
    return page


def adjust_prop_type(prop_type):
    for a in range(len(prop_type)):
        if prop_type[a] == "Single Family":
            prop_type[a] = "sngl-fam-res"
        elif prop_type[a] == "Two Family":
            prop_type[a] = "two-fam-res"
        elif prop_type[a] == "Three Family":
            prop_type[a] = "three-fm-res"
        elif prop_type[a] == "4+ Unit":
            prop_type[a] = "4-8-unit-apt"
        prop_type[a] = prop_type[a].lower()
    if "4-8-unit-apt" in prop_type:
        prop_type.append(">8-unit-apt")
    if "condominium" in prop_type:
        prop_type.append("cndo lux")
        prop_type.append("condo-bldg")
    return prop_type


def create_map(current):
    view_state = pdk.ViewState(latitude=current["lat"].mean(), longitude=current["lon"].mean(), zoom=11.5, pitch=0)

    layer = pdk.Layer('ScatterplotLayer',
                      data=current,
                      get_position='[lon, lat]',
                      get_radius=100,
                      get_color=[255, 0, 255],
                      pickable=True)

    tool_tip = {"html": "<b>{Address}</b>", "style": {"backgroundColor": "orange", "color": "white"}}

    display_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tool_tip
        )
    return display_map


def units_sold_chart(df_info):
    dict_sold_by_year = {}
    for every_year in range(2000, 2022):
        dict_sold_by_year[every_year] = 0
    df_units_by_year = df_info.loc[:, ["Address", "SaleDate"]]
    df_units_by_year = df_units_by_year.dropna()
    for indexA, rowA in df_units_by_year.iterrows():
        year = int(str(rowA["SaleDate"])[-4:])
        if year >= 2000:
            if year in dict_sold_by_year:
                dict_sold_by_year[year] += 1
    dict_sold_by_year = dict(sorted(dict_sold_by_year.items()))
    x_year = dict_sold_by_year.keys()
    y_units = dict_sold_by_year.values()
    figure, chart = plt.subplots()
    chart.plot(x_year, y_units)
    chart.set_xlabel("Year")
    chart.set_ylabel("# of Units Sold")
    random_columns = st.columns([0.7, 1])
    with random_columns[0]:
        st.pyplot(figure)


def median_price_chart(df_info):
    dict_median_price_year = {}
    for every_year in range(2000, 2022):
        dict_median_price_year[every_year] = []
    df_price_by_year = df_info.loc[:, ["SalePrice", "SaleDate"]]
    for indexB, rowB in df_price_by_year.iterrows():
        year = int(str(rowB["SaleDate"])[-4:])
        if year >= 2000:
            if year in dict_median_price_year:
                price = rowB["SalePrice"]
                dict_median_price_year[year].append(price)
    x_year = list(dict_median_price_year.keys())
    y_price = []
    for keyB in list(dict_median_price_year.keys()):
        prices_list = sorted(list(dict_median_price_year[keyB]))
        len_prices = len(prices_list)
        if len_prices % 2 != 0:
            m = int((len_prices+1)/2 - 1)
            y_price.append(prices_list[m])
        else:
            m1 = int(len_prices/2 - 1)
            m2 = int(len_prices/2)
            y_price.append((prices_list[m1]+prices_list[m2])/2)
    figure, chart = plt.subplots()
    chart.plot(x_year, y_price)
    chart.set_xlabel("Year")
    chart.set_ylabel("Sales Price")
    chart.ticklabel_format(useOffset=False, style="plain")
    chart.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda a, p: format(int(a), ',')))
    random_columns = st.columns([0.7, 1])
    with random_columns[0]:
        st.pyplot(figure)


def price_sqft_chart(df_info):
    dict_sqft_year = {}
    for every_year in range(2000, 2022):
        dict_sqft_year[every_year] = []
    df_price_by_year = df_info.loc[:, ["SalePrice", "SaleDate", "Interior_LivingArea"]]
    for indexC, rowC in df_price_by_year.iterrows():
        year = int(str(rowC["SaleDate"])[-4:])
        if year >= 2000:
            if year in dict_sqft_year:
                if rowC["Interior_LivingArea"] > 0:
                    price_sqft = rowC["SalePrice"]/rowC["Interior_LivingArea"]
                    dict_sqft_year[year].append(price_sqft)
    x_year = list(dict_sqft_year.keys())
    y_sqft = []
    for keyB in list(dict_sqft_year.keys()):
        total_sqft = 0
        count = 0
        sqft_list = list(dict_sqft_year[keyB])
        for sqft in sqft_list:
            total_sqft += sqft
            count += 1
        if count == 0:
            avg_sqft = 0
        else:
            avg_sqft = total_sqft / count
        y_sqft.append(avg_sqft)
    figure, chart = plt.subplots()
    chart.plot(x_year, y_sqft)
    chart.set_xlabel("Year")
    chart.set_ylabel("Price/Square Foot")
    chart.ticklabel_format(useOffset=False, style="plain")
    chart.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda a, p: format(int(a), ',')))
    random_columns = st.columns([0.7, 1])
    with random_columns[0]:
        st.pyplot(figure)


# Charts
st.sidebar.header("Market Trends")
chart_list = ["[No Chart Selected]", "# Units Sold by Year", "# Units Sold by Year by Property Type", "Median Sale Price by Year", "Average Price/SqFt by Year"]
selected_chart = st.sidebar.selectbox("Select a chart: ", chart_list)
if selected_chart == "# Units Sold by Year":
    st.header(selected_chart)
    units_sold_chart(df_property_info)
elif selected_chart == "# Units Sold by Year by Property Type":
    chart_property_select = st.sidebar.radio("Select", property_types)
    if chart_property_select == "Single Family":
        df_chart = df_property_info[df_property_info.PropertyClass == "SNGL-FAM-RES"]
    elif chart_property_select == "Two Family":
        df_chart = df_property_info[df_property_info.PropertyClass == "TWO-FAM-RES"]
    elif chart_property_select == "Three Family":
        df_chart = df_property_info[df_property_info.PropertyClass == "THREE-FM-RES"]
    elif chart_property_select == "4+ Unit":
        df_chart = df_property_info[(df_property_info.PropertyClass == "4-8-UNIT-APT") | (df_property_info.PropertyClass == ">8-UNIT-APT")]
    elif chart_property_select == "Condominium":
        df_chart = df_property_info[(df_property_info.PropertyClass == "CONDOMINIUM") | (df_property_info.PropertyClass == "CNDO LUX") | (df_property_info.PropertyClass == "CONDO-BLDG")]
    else:
        df_chart = df_property_info
    st.header(selected_chart + ": " + chart_property_select)
    units_sold_chart(df_chart)
elif selected_chart == "Median Sale Price by Year":
    st.header(selected_chart)
    median_price_chart(df_property_info)
elif selected_chart == "Average Price/SqFt by Year":
    st.header(selected_chart)
    price_sqft_chart(df_property_info)
else:
    # Search bar
    with st.form("my_form"):
        searchbar = st.columns([2.5, 1.5, 1, 1])
        searchbar_bottom = st.columns([3, 0.1, 2.4, 0.5])
        with searchbar[0]:
            # st.header("Search by Address")
            search_address = st.text_input("Search by Address")
        with searchbar[1]:
            # st.header("Property Type")
            selected_types = st.multiselect("Property Type", property_types)
        with searchbar[2]:
            # st.header("Bedrooms")
            num_bdrm = st.number_input("Bedrooms", 1, 10)
        with searchbar[3]:
            # st.header("Bathrooms")
            num_bth = st.number_input("Bathrooms", 1, 10)
        with searchbar_bottom[0]:
            # st.header("Price Range")
            min_price, max_price = st.slider('Price', 100000, 3000000, (500000, 2000000))
        with searchbar_bottom[2]:
            # st.header("More Filters")
            with st.expander("Filter"):
                st.write("Square Footage")
                min_ft = st.number_input("Min", 0, 99999)
                max_ft = st.number_input("Max", 0, 100000)
                if min_ft > max_ft or max_ft == 0:
                    sq_ft_bool = False
                    if max_ft > 0:
                        st.write("Please input valid minimum and maximum square footage")
                else:
                    sq_ft_bool = True
                st.write("Land Size")
                min_land = st.number_input("Min", 0, 499999)
                max_land = st.number_input("Max", 0, 500000)
                if min_land > max_land or max_land == 0:
                    land_size_bool = False
                    if max_land > 0:
                        st.write("Please input valid minimum and maximum land size")
                else:
                    land_size_bool = True
                # st.write("Year Built")
                # year_built = st.number_input("House built after:", 1800, 2022)
        # Every form must have a submit button.
        with searchbar_bottom[3]:
            submitted = st.form_submit_button("Submit")
            if submitted:
                for key in st.session_state.keys():
                    del st.session_state[key]
                if "search_bool" not in st.session_state:
                    st.session_state.search_bool = True

# Search results
if "search_bool" in st.session_state:
    # If the "Search Address" text input is empty, use the filters to search through the dataframe
    if search_address.strip() == "":
        # Create 'search_result' from filters
        search_result = df_property_info[(df_property_info.AssessedValue >= min_price) & (df_property_info.AssessedValue <= max_price)
                                         & (df_property_info.Interior_Bedrooms == num_bdrm)
                                         & (df_property_info.Interior_FullBaths + df_property_info.Interior_HalfBaths == num_bth)]
        # If property types are selected, adjust 'search_result' accordingly
        if selected_types:
            selected_types = adjust_prop_type(selected_types)
            search_result = search_result[(search_result.PropertyClass.str.lower().isin(selected_types))]
        else:
            selected_types = adjust_prop_type(property_types)
            search_result = search_result[(search_result.PropertyClass.str.lower().isin(selected_types))]
        # If square footage is determined, adjust 'search_result' accordingly
        if sq_ft_bool:
            search_result = search_result[(search_result.Interior_LivingArea >= min_ft) & (search_result.Interior_LivingArea <= max_ft)]
        # If land size is determined, adjust 'search_result' accordingly
        if land_size_bool:
            search_result = search_result[(search_result.LandArea >= min_land) & (search_result.LandArea <= max_land)]
        # If no houses meet the criteria, display "Nothing here"
        # if search_result.empty:
        #    st.write("Nothing here")
        # else:
        #    st.write(search_result)
    # If street address inputted
    else:
        search_result = df_property_info[df_property_info["Address"].str.lower() == search_address.strip().lower()]
    # Pages of search results
    if search_result.empty:
        st.write("No results found :(")
    else:
        page_and_map = st.columns([0.5, 0.5, 1])
        page_buttons = st.columns([0.15, 0.2, 2])
        if (len(search_result) / 10) == (len(search_result) // 10):
            pages = (len(search_result) // 10)
        else:
            pages = (len(search_result) // 10) + 1
        with page_buttons[0]:
            if st.button("Previous"):
                st.session_state.current_page = previous_page(st.session_state.current_page)
        with page_buttons[1]:
            if st.button("Next"):
                st.session_state.current_page = next_page(st.session_state.current_page, pages)
        if "current_page" not in st.session_state:
            st.session_state.current_page = 1
        map_result = search_result.iloc[(st.session_state.current_page*10-10):(st.session_state.current_page*10), :]
        map_result = map_result.loc[:, ["Address", "lat", "lon", "BuildingValue", "LandValue", "AssessedValue", "Interior_LivingArea",
                                        "Interior_Bedrooms", "Interior_FullBaths", "Interior_HalfBaths", "LandArea"]]
        st.write("Page ", st.session_state.current_page, " of ", pages)
        st.write("Found ", len(search_result), " properties")
        for index, row in map_result.iterrows():
            with page_and_map[0]:
                location = str(row['lat']) + "," + str(row['lon'])
                # Define parameters for street view api
                params = [{
                    'size': '300x300',  # max 640x640 pixels
                    'location': location,
                    'key': 'AIzaSyAaDdrsYSJrwVBdjj7n6yqBwPyW6XlY8yw'
                }]

                # Create a results object
                results = google_streetview.api.results(params)
                # Download images to directory 'downloads'
                results.download_links('downloads')
                f = open("downloads/metadata.json", "r")
                metadata = str(f.readline())
                if metadata == '[{"status": "ZERO_RESULTS"}]':
                    st.image("https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930", width=300)
                else:
                    image = Image.open('downloads/gsv_0.jpg')
                    st.image(image)
                    image.close()
                f.close()
            with page_and_map[1]:
                st.subheader(f"${row['AssessedValue']:,.0f}")
                st.write(f"{row['Interior_Bedrooms']:.0f} bed {(row['Interior_FullBaths'] + row['Interior_HalfBaths']):.0f} bath {row['Interior_LivingArea']:,d} sqft")
                st.write(str(row['Address']))
                st.write("Cambridge, MA")
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                st.write('')
                st.write('')
        with page_and_map[2]:
            cambridge_map = create_map(map_result)
            st.pydeck_chart(cambridge_map)
else:
    st.write("")
