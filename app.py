#--------------------------------------------
# LIBRARIES:
#--------------------------------------------
# Standard imports
from audioop import reverse
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


#--------------------------------------------
# DATA:
#--------------------------------------------
df = pd.read_csv('renewable_power_plants_CH.csv')

with open('georef-switzerland-kanton.geojson') as json_file:
    cantons = json.load(json_file)

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

df2 = pd.DataFrame()
df2.index = list(dict_areas.keys())
df2['names'] = dict_cantons.keys()
df2['areas (km2)'] = dict_areas.values()
df2['habitants'] = dict_habitants.values()


types_energy = df.energy_source_level_2.unique().tolist()





#--------------------------------------------
# CHECK-BOXES:
#--------------------------------------------

show_hist = False
if st.sidebar.checkbox('Hide Histograms'):
    show_hist = True


show_dfs = False
if st.sidebar.checkbox('Hide dataframe'):
    show_dfs = True


reverse = []
for i in range(len(types_energy)-1, -1, -1):
    reverse.append(types_energy[i])

enegry_type = st.sidebar.radio(
    label='Types of Renewable Energy for last map-plot:', options=[el for el in reverse])



#--------------------------------------------
# DATA-FRAMES:
#--------------------------------------------
# Set ID:
for i in range(len(cantons['features'])):
    cantons['features'][i]['id'] = dict_cantons[cantons['features'][i]['properties']['kan_name']]


df1 = df.copy()
df1 = df1[['canton', 'electrical_capacity', 'energy_source_level_2']]
df1.groupby('canton').electrical_capacity.sum()




#--------------------------------------------
# PLOTS:
#--------------------------------------------
def division(series, div):
    series = series.tolist()
    div = div.tolist()

    res = []
    for i in range(len(series)):
        res.append(series[i] / div[i])

    return pd.DataFrame(res)



def dependent_plot(keyword):
    df_aux = df[df.energy_source_level_2 == keyword]
    df_aux.groupby('canton').energy_source_level_2.sum()

    fig4 = go.Figure(go.Choroplethmapbox(geojson=cantons, locations=df.canton, z=df_aux.electrical_capacity,
                                    colorscale="Viridis", 
                                    marker_opacity=0.5, marker_line_width=0))
    fig4.update_layout(mapbox_style="carto-positron",
                    mapbox_zoom=6, mapbox_center = {"lat": 46.484, "lon": 8.1336})
    fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig4


#--------------------------------------------
# PAGE:
#--------------------------------------------
c1, c2 = st.columns((1, 3, ))

st.header('Mini-Project')
st.header('Clean Energy Sources in Switzerland')


if not show_dfs:
    st.markdown('#### Data set to analyze:')
    st.dataframe(df)
    st.markdown('#### Data about Switzerland:')
    st.dataframe(df2.sort_values(by='areas (km2)', ascending=False))
 

if not show_hist:
    st.markdown('### Data about Switzerland:')
    sns.barplot(data = df2, x='names', y='areas (km2)', color='blue')
    plt.xticks(rotation=90)
    plt.title('Area of each Canton')
    st.pyplot(plt.gcf())
    sns.barplot(data = df2, x='names', y='habitants', color='blue')
    plt.title('Number of Habitants of each Canton')
    st.pyplot(plt.gcf())

if not show_dfs:
    st.markdown('### Data Sets:')
    st.markdown('(source: https://de.statista.com/statistik/daten/studie/942738/umfrage/flaeche-der-schweiz-nach-kantonen/)')



st.markdown('> For the first analysis I will just take the the sum of the electrical capacity for each type of energy-harversting method, that for each canton.')


if not show_dfs:
    st.markdown('### Dataframe of elecrtical capacity per Canton:')
    st.dataframe(sum_el_cap_n)


# First Histo:
fig = sns.barplot(data=sum_el_cap.sort_values(by = 'electrical_capacity', ascending=True), x='canton', y='electrical_capacity', color='blue')
# fig.set_yscale('log')
fig = plt.xticks(rotation=90)
plt.xlabel('Cantons')
plt.ylabel('Electrical Capacity')
plt.title('Electrical Capacity of each Canton', fontsize=15)

if not show_hist:
    st.pyplot(plt.gcf())

st.plotly_chart(fig1)

st.markdown('---')
st.markdown('### Observations:')
st.markdown('> I noticed that big cantons also have a high electricity capacity. Hence: I will divide the elecricity by the area of each canton to obtain the el-cap per square-km. With the hope that this will partially eliminate the factor of the canton-size.')

st.markdown('> I know yet that there are still a lot of factor as the location: After some thinking I hypothesized that the location also plays a big role.')
st.markdown('- Cantons in the South have access to other kind of resources such as Hydro-power, due to them beeing near the Alps.')
st.markdown(' - Cantons in the Center-North are in a plane, hence they can take advantage of the wind and sun for example.')

st.markdown('> My hypothesis was confirmed after looking at the following article (given from in the exercise) Source: https://www.uvek-gis.admin.ch/BFE/storymaps/EE_Elektrizitaetsproduktionsanlagen/?lang=en')

st.markdown('> Yet it is really hard to take count of such factors, hence I will ignore them.')

st.markdown('#### (I will map those out on the last map!)')
st.markdown('---')


if not show_dfs:
    st.markdown('### Dataframe of elecrtical capacity per km2:')
    st.dataframe(sum_el_cap_area[['canton', 'el_cap_by_area']].sort_values(by='el_cap_by_area', ascending=False))

st.plotly_chart(fig2)

st.markdown('---')
st.markdown('### Observations:')
st.markdown('> Now that completely changes the situation... We see that Aargau and Glarus have a lot more electrical capacity per km2 compared to the other cantons, all other cantons have more or less of the same electrical capasity per km2')


if not show_dfs:
    st.markdown('### Dataframe of elecrtical capacity per canton-habitant:')
    st.dataframe(sum_el_cap_habit[['canton', 'el_cap_by_habit']].sort_values(by='el_cap_by_habit', ascending=False))

st.plotly_chart(fig3)


st.markdown('---')
st.header('Last Map-Plot:')
text = f'For Type of Renewable Energy: {enegry_type.upper()}'
st.header(text)
st.plotly_chart(dependent_plot(enegry_type))