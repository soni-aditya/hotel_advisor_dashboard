import pandas as pd
import streamlit as st
from data_manager import KeyStrings, DashboardDataManager
import extra_streamlit_components as stx
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

# ----- PAGE CONFIG (title bar)------
st.set_page_config(
    page_title="Hotel Advisor",
    page_icon=":hotel:",
    layout="wide",
    initial_sidebar_state="expanded",
)

data_manager = DashboardDataManager()
data_manager.get_filter_data()

# ---- SIDEBAR ----
st.sidebar.header("Apply Filters:")
st.sidebar.write("")
city = st.sidebar.multiselect(
    "Select the City:",
    options=data_manager.cities,
    default=data_manager.cities,
    key=KeyStrings.CITY_FILTER
)

st.sidebar.write("")
ratings = st.sidebar.selectbox(
    "Ratings:",
    (
        'All',
        '5',
        '4 and above',
        '3 and above',
        '2 and above',
        '1 and above',
    ),
    key=KeyStrings.RATINGS_FILTER
)

st.sidebar.write("")
price = st.sidebar.slider(
    "Maximum Hotel Price:",
    min_value=0,
    max_value=int(data_manager.max_price),
    value=int(data_manager.max_price),
    step=1000,
    key=KeyStrings.PRICE_FILTER,
)

st.sidebar.write("")
cuisine = st.sidebar.multiselect(
    "Cuisine:",
    options=data_manager.cuisines,
    key=KeyStrings.CUISINE_FILTER,
)

st.sidebar.write("")
nearby_places = st.sidebar.slider(
    "Nearby Places to Visit:",
    min_value=0,
    max_value=int(data_manager.max_nearby_places),
    value=int(data_manager.max_nearby_places),
    step=100,
    key=KeyStrings.NEARBY_PLACES_FILTER,
)

st.sidebar.write("")
nearby_restaurants = st.sidebar.slider(
    "Nearby Restaurants:",
    min_value=0,
    max_value=int(data_manager.max_restaurants_nearby),
    value=int(data_manager.max_restaurants_nearby),
    step=500,
    key=KeyStrings.NEARBY_RESTAURANTS_FILTER,
)

st.sidebar.write("")
total_reviews = st.sidebar.slider(
    "Total Reviews:",
    min_value=0,
    max_value=int(data_manager.max_review_count),
    value=int(data_manager.max_review_count),
    step=100,
    key=KeyStrings.REVIEWS_FILTER,
)

st.sidebar.write("")
amenities = st.sidebar.multiselect(
    "Amenities:",
    options=data_manager.amenities,
    default=data_manager.amenities[0],
    key=KeyStrings.AMENITIES_FILTER,
)

st.sidebar.write("")
languages = st.sidebar.multiselect(
    "Languages:",
    options=data_manager.languages,
    default=data_manager.languages[0],
    key=KeyStrings.LANGUAGES_FILTER
)

st.sidebar.write("")
hotel_classes = st.sidebar.multiselect(
    "Hotel Class:",
    options=data_manager.classes,
    default=data_manager.classes[0],
    key=KeyStrings.CLASS_FILTER
)
# setting the above filters
data_manager.set_filters(cities=city, rating=ratings, price=price, cuisine=cuisine, nearby_places=nearby_places,
                         nearby_restaurants=nearby_restaurants, total_reviews=total_reviews, amenities=amenities,
                         languages=languages, hotel_classes=hotel_classes)
data_manager.get_top_20_hotels()
# ----MAIN SECTION ----
st.header(":hotel: Cumulative Statistics")
st.markdown("##")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader(f"Total Hotels:\n{data_manager.data.shape[0]}")
    st.subheader(f"Top Cuisine:\n{data_manager.get_top_cusine()}")
    st.subheader(f"Top Language:\n{data_manager.get_top_language()}")

with middle_column:
    st.subheader(f"Average Rating:\n{round(data_manager.data.rating.mean(), 2)}")
    st.subheader(f"Places Nearby:\n{data_manager.get_nearby_places_avg()}")
    st.subheader(f"Hotel Class:\n{data_manager.get_class()}")
with right_column:
    st.subheader(f"Average Hotel Price:\n{round(data_manager.data.price.mean(), 2)}")
    st.subheader(f"Most Hotels are near\n{data_manager.get_restaurants()} Restaurant")

st.markdown("""---""")
st.markdown("## Top Hotels")
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="All Hotels", description=""),
    stx.TabBarItemData(id=2, title="Top 20 Hotels", description=""),
], default=1)
if chosen_id == '2':
    if len(data_manager.top_20) == 0:
        st.write("No Data")
    else:
        wc = WordCloud(background_color="white", width=1200, height=500).fit_words(data_manager.top_20)
        # Display the generated image:
        st.image(wc.to_array())
else:
    st.write(data_manager.get_df())
######################################################
cuisine_names, cuisine_counts = data_manager.get_cusines_for_donut()
cusines = px.pie(
    hole=0.35,
    labels=cuisine_counts,
    names=cuisine_names,
    values=cuisine_counts,
    title=f"Top {len(cuisine_names)} Cuisines",
)
class_name, class_counts = data_manager.get_classes_for_donut()
hotel_classes = px.pie(
    hole=0.2,
    labels=class_counts,
    names=class_name,
    values=class_counts,
    title=f'Hotel {len(class_name)} Classes',
)
left_column, right_column = st.columns(2)
with left_column:
    if len(cuisine_names) > 0:
        st.plotly_chart(cusines, use_container_width=True)
    else:
        st.write("No Data for Top Cuisines")
        st.markdown("##")
        st.markdown("##")
with right_column:
    if len(class_name) > 0:
        st.plotly_chart(hotel_classes, use_container_width=True)
    else:
        st.write("No Data regarding Top Classes")
        st.markdown("##")
        st.markdown("##")
st.markdown("##")

amenities_names, amenities_counts = data_manager.get_amenities_for_donut()
amenities = px.pie(
    hole=0.2,
    labels=amenities_counts,
    names=amenities_names,
    values=amenities_counts,
    title=f'Top {len(amenities_names)} Amenities'
)

language_names, language_counts = data_manager.get_languages_for_donut()
languages_donut = px.pie(
    hole=0.2,
    labels=language_counts,
    names=language_names,
    values=language_counts,
    title=f'Top {len(language_names)} Languages'
)
left_column, right_column = st.columns(2)
with left_column:
    if len(amenities_names) > 0:
        left_column.plotly_chart(amenities, use_container_width=True)
    else:
        st.write("No Data regarding Top Amenities")
        st.markdown("##")
        st.markdown("##")
with right_column:
    if len(language_names) > 0:
        st.plotly_chart(languages_donut, use_container_width=True)
    else:
        st.write("No Data regarding most used Languages")
        st.markdown("##")
        st.markdown("##")
st.markdown("##")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
