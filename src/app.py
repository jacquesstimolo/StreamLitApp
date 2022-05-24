# Standard imports
import pandas as pd
import json

# matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
#plotly
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st



# st.title("MPG")
# df = pd.read_csv("mpg.csv")



df = pd.read_csv('data/renewable_power_plants_CH.csv', encoding="unicode_escape")


with open('data/georef-switzerland-kanton.geojson') as json_file:
    cantons = json.load(json_file)





# Basic set-up of the page:
# First the checkbox to show the data frame
if st.sidebar.checkbox('Show dataframe'):
    st.header("dataframe")
    st.dataframe(df.head())


# Then the radio botton for the plot type
# show_plot = st.sidebar.radio(
#     label='Choose Plot type', options=['Matplotlib', 'Plotly'])


# st.header("Highway Fuel Efficiency")
# years = ["All"]+sorted(pd.unique(df['year']))
# year = st.sidebar.selectbox("choose a Year", years)   # Here the selection of the year.
# car_classes = ['All'] + sorted(pd.unique(df['class']))
# car_class = st.sidebar.selectbox("choose a Class", car_classes)  # and the selection of the class.


# show_means = st.sidebar.radio(
#     label='Show Class Means', options=['Yes', 'No'])


# st.subheader(f'Fuel efficiency vs. engine displacement for {year}')


# With these functions we wrangle the data and plot it.
def mpg_mpl(year, car_class, show_means):
    fig, ax = plt.subplots()
    if year == 'All':
        group = df
    else:
        group = df[df['year'] == year]
    if car_class != 'All':
        st.text(f'plotting car class: {car_class}')
        group = group[group['class'] == car_class]
    group.plot('displ', 'hwy', marker='.', linestyle='', ms=12, alpha=0.5, ax=ax, legend=None)
    if show_means == "Yes":
        means = df.groupby('class').mean()
        for cc in means.index:
            ax.plot(means.loc[cc, 'displ'], means.loc[cc, 'hwy'], marker='.', linestyle='', ms=12, alpha=1, label=cc)
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1))
    ax.set_xlim([1, 8])
    ax.set_ylim([10, 50])
    plt.close()
    return fig


def mpg_plotly(year, car_class, show_means):
    if year == 'All':
        group = df
    else:
        group = df[df['year'] == year]
    if car_class != 'All':
        group = group[group['class'] == car_class]
    fig = px.scatter(group, x='displ', y='hwy', opacity=0.5, range_x=[1, 8], range_y=[10, 50])
    if show_means == "Yes":
        means = df.groupby('class').mean().reset_index()
        fig = px.scatter(means, x='displ', y='hwy', opacity=0.5, color='class', range_x=[1, 8], range_y=[10, 50])
        fig.add_trace(go.Scatter(x=group['displ'], y=group['hwy'], mode='markers', name=f'{year}_{car_class}',
                                 opacity=0.5, marker=dict(color="RoyalBlue")))
    return fig
  

# if show_plot == 'Plotly':
#     st.plotly_chart(mpg_plotly(year, car_class, show_means))
    
# else:
#     st.pyplot(mpg_mpl(year, car_class, show_means))






# Adding ID to data:
def modify_cantons(canton):
    dict_cantons = {
        'Genève' : 'GE',
        'Schaffhausen' : 'SH',
        'Uri' : 'UR',
        'Bern' : 'BE',
        'Fribourg' : 'FR',
        'Aargau' : 'AG',
        'Graubünden' : 'GR',
        'Luzern' : 'LU',
        'Basel-Stadt' : 'BS',
        'Ticino' : 'TI',
        'Obwalden' : 'OW',
        'Appenzell Ausserrhoden' : 'AR',
        'Solothurn' : 'SO',
        'Schwyz' : 'SZ',
        'Jura' : 'JU',
        'St. Gallen' : 'SG',
        'Valais' : 'VS',
        'Thurgau' : 'TG',
        'Vaud' : 'VD',
        'Basel-Landschaft' : 'BL',
        'Zürich' : 'ZH',
        'Nidwalden' : 'NW',
        'Glarus' : 'GL',
        'Neuchâtel' : 'NE',
        'Zug' : 'ZG',
        'Appenzell Innerrhoden' : 'AI'
    }

    for i in range(len(cantons['features'])):
        cantons['features'][i]['id'] = dict_cantons[cantons['features'][i]['properties']['kan_name']]
    return cantons


cantons = modify_cantons(cantons)


st.markdown('> For the first analysis I will just take the the sum of the electrical capacity for each type of energy-harversting method, that for each canton.')

df1 = df.copy()
df1 = df1.groupby('canton').electrical_capacity.sum().reset_index()
st.dataframe(df1)


fig = go.Figure(go.Choroplethmapbox(geojson=cantons, locations=df1.canton, z=df1.electrical_capacity,
                                    colorscale="Viridis", 
                                    marker_opacity=0.5, marker_line_width=0))


fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=6, mapbox_center = {"lat": 46.484, "lon": 8.1336})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


st.plotly_chart(fig)


st.markdown('---')
st.markdown('### Observations:')
st.markdown('> I noticed that big cantons also have a high electricity capacity. Hence: I will divide the elecricity by the area of each canton to obtain the el-cap per square-km. With the hope that this will partially eliminate the factor of the canton-size.')


st.markdown('> I know yet that there are still a lot of factor as the location: After some thinking I hypothesized that the location also plays a big role.')
st.markdown('- Cantons in the South have access to other kind of resources such as Hydro-power, due to them beeing near the Alps.')
st.markdown(' - Cantons in the Center-North are in a plane, hence they can take advantage of the wind and sun for example.')

st.markdown('> My hypothesis was confirmed after looking at the following article (given from in the exercise) Source: https://www.uvek-gis.admin.ch/BFE/storymaps/EE_Elektrizitaetsproduktionsanlagen/?lang=en')

st.markdown('> Yet it is really hard to take count of such factors, hence I will ignore them.')
st.markdown('---')



dict_areas = {
    'GE' : 282.3,
    'SH' : 298.4,
    'UR' : 1076.3,
    'BE' : 5959.4,
    'FR' : 1671.4,
    'AG' : 1404.0,
    'GR' : 7105.0,
    'LU' : 1493.3,
    'BS' : 37.0,
    'TI' : 2812.3,
    'OW' : 490.6,
    'AR' : 242.9,
    'SO' : 790.4,
    'SZ' : 908.0,
    'JU' : 838.6,
    'SG' : 2030.7,
    'VS' : 5224.8,
    'TG' : 991.5,
    'VD' : 3212.2,
    'BL' : 517.7,
    'ZH' : 1728.9,
    'NW' : 275.9,
    'GL' : 685.4,
    'NE' : 802.3,
    'ZG' : 238.7,
    'AI' : 172.4
}

func = lambda row: row.electrical_capacity / dict_areas[row.canton]

df1['el_cap_by_area'] = df.apply(func, axis=1)
st.dataframe(df1)


fig = go.Figure(go.Choroplethmapbox(geojson=cantons, locations=df1.canton, z=df1.el_cap_by_area,
                                    colorscale="Viridis", 
                                    marker_opacity=0.5, marker_line_width=0))


fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=6, mapbox_center = {"lat": 46.484, "lon": 8.1336})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


st.plotly_chart(fig)

st.markdown('---')
st.markdown('### Observations:')
st.markdown('> Now that completely changes the situation... We see that Aargau and Glarus have a lot more electrical capacity per km2 compared to the other cantons, all other cantons have more or less of the same electrical capasity per km2')


dict_habitants = {
    'GE' : 419000,
    'SH' : 74000,
    'UR' : 35000,
    'BE' : 950000,
    'FR' : 243000,
    'AG' : 556000,
    'GR' : 186000,
    'LU' : 352000,
    'BS' : 186000,
    'TI' : 315000,
    'OW' : 33000,
    'AR' : 53000,
    'SO' : 247000,
    'SZ' : 133000,
    'JU' : 69000,
    'SG' : 455000,
    'VS' : 281000,
    'TG' : 230000,
    'VD' : 632000,
    'BL' : 263000,
    'ZH' : 1242000,
    'NW' : 39000,
    'GL' : 38000,
    'NE' : 167000,
    'ZG' : 102000,
    'AI' : 15000
}


func = lambda row: row.electrical_capacity / dict_habitants[row.canton]

df1['el_cap_by_habit'] = df.apply(func, axis=1)
st.dataframe(df1)


fig = go.Figure(go.Choroplethmapbox(geojson=cantons, locations=df1.canton, z=df1.el_cap_by_habit,
                                    colorscale="Viridis", 
                                    marker_opacity=0.5, marker_line_width=0))


fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=6, mapbox_center = {"lat": 46.484, "lon": 8.1336})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


st.plotly_chart(fig)