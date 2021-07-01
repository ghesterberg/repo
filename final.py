"""
Name: Grace Hesterberg
CS230: SN2F
Data: Volcanic Eruptions
URL: Link to your web application online (see extra credit)

Description: This program uses the Volcanic Eruptions dataset. It contains a map where a user can
click from a drop down menu to select a volcano, and the map with find that point on the map and
plot it with a label of the volcano name. Next, is a boxplot that displays the min, max, and average
elevations of all of the volcanoes together. Lastly there is a bar chart that displays the number of
volcanoes in each region with a multiselect box where users can select one or multiple regions to compare.
"""

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
import pydeck as pdk
import pandas as pd
import os


# Displays happy volcano image as well as the title of the web page
def display_heading():
    from PIL import Image
    img = Image.open('volcano_img.jpg')
    st.title('Volcanic Eruptions Across the Globe')
    st.image(img, width=480)


display_heading()


# Reads the data file and assigns it to the name 'volcanoes'
volcanoes = pd.read_csv(os.path.join('volcanoes.csv'))


# Map function
def volcano_map():
    st.subheader('Volcanic Eruptions Map')
    st.sidebar.write('Map', fontweight='bold')
    name_selection = st.sidebar.selectbox('Select the name of a volcano:', volcanoes['Volcano Name'])

    df = pd.DataFrame(volcanoes, columns={'Volcano Name', 'Latitude', 'Longitude'})
    df = df.rename(columns=dict(lat='Latitude', lon='Longitude'))
    name = df[df['Volcano Name'] == name_selection]
    st.write(name)

    view_map = pdk.ViewState(latitude=df['Latitude'].mean(),
                            longitude=df['Longitude'].mean(),
                            zoom=2,
                            pitch=0)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=name,
                       get_position=['Longitude', 'Latitude'],
                       get_radius=75000,
                       get_color=[0, 191, 255],
                       pickable=True)
    tool_tip = {"html": "Volcano Name:<br/> <b>{Volcano Name}</b> ",
                "style": {"backgroundColor": "deepskyblue", "color": "white"}}


    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                   initial_view_state=view_map,
                   layers=[layer1],
                   tooltip=tool_tip)
    st.pydeck_chart(map)


volcano_map()


# Boxplot function
def boxplot():
    boxplot_data = pd.DataFrame(volcanoes, columns={'Elevation (m)'})
    st.subheader('Boxplot of Volcano Elevations')
    c = ['lightcyan', 'deepskyblue', 'lightskyblue', 'cyan']

    c_dict = {'patch_artist': True,
              'boxprops': dict(color=c[1], facecolor=c[0]),
              'capprops': dict(color=c[1]),
              'flierprops': dict(color=c[1], markeredgecolor=c[1]),
              'medianprops': dict(color=c[1]),
              'whiskerprops': dict(color=c[1])}

    plt.title('Average Volcano Elevation', color='deepskyblue', fontweight='bold', fontfamily='monospace')
    plt.ylabel('Elevation (m)', color='deepskyblue', fontfamily='monospace')
    plt.xlabel('Volcanoes', color='deepskyblue', fontfamily='monospace')
    plt.boxplot(boxplot_data, **c_dict)
    st.pyplot(plt)


boxplot()


# Statistics function
def stats():
    stats = ['Mean', 'Median', 'Minimum', 'Maximum', 'Standard Deviation']
    st.sidebar.write(f'\n\n')
    st.sidebar.write(f'\n\n')
    st.sidebar.write('Statistics for Boxplot', fontweight='bold')
    stat = st.sidebar.radio('Select a statistics calculation: ', stats)

    mean = volcanoes['Elevation (m)'].mean()
    median = volcanoes['Elevation (m)'].median()
    min = volcanoes['Elevation (m)'].min()
    max = volcanoes['Elevation (m)'].max()
    std = volcanoes['Elevation (m)'].std()

    if stat == 'Mean':
        st.write(f'Mean:\t{mean:0.4f}')
    elif stat == 'Median':
        st.write(f'Median:\t{median:0.4f}')
    elif stat == 'Minimum':
        st.write(f'Minimum:\t{min:0.4f}')
    elif stat == 'Maximum':
        st.write(f'Maximum:\t{max:0.4f}')
    else:
        st.write(f'Standard Deviation:\t{std:0.4f}')


stats()


# Bar Chart function
def bar_chart():
    keys = ['Africa and Red Sea', 'Alaska', 'Antarctica', 'Atlantic Ocean', 'Canada and Western USA',
            'Hawaii and Pacific Ocean', 'Iceland and Arctic Ocean', 'Indonesia', 'Japan, Taiwan, Marianas',
            'Kamchatka and Mainland Asia', 'Kuril Islands', 'Mediterranean and Western Asia',
            'Melanesia and Australia', 'Middle East and Indian Ocean', 'México and Central America',
            'New Zealand to Fiji', 'Philippines and SE Asia', 'South America', 'West Indies']

    values = [121, 87, 33, 29, 65, 33, 36, 126, 134, 128, 44, 41, 73, 44, 110, 58, 51, 184, 16]

    st.subheader('Bar Chart of Volcanic Eruptions')
    st.sidebar.write(f'\n\n')
    st.sidebar.write(f'\n\n')
    st.sidebar.write('Bar Chart', fontweight='bold')
    regions = st.sidebar.multiselect("Select regions: ", keys, default='Africa and Red Sea')
    region = go.Bar(x=regions, y=values, showlegend=True)
    layout = go.Layout(title="Number of Volcanoes Per Region")
    data = [region]
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(marker_color='deepskyblue')
    fig.update_layout(font_family='monospace',
                      font_color='deepskyblue',
                      title_font_family='monospace',
                      legend_title_font_color='deepskyblue')
    fig.update_xaxes(title='Regions')
    fig.update_yaxes(title='Number of Volcanoes')
    st.plotly_chart(fig)


bar_chart()
