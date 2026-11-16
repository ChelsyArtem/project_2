import time
import pandas as pd
import geopandas as gpd
import folium
from geopandas.tools import geocode

df = pd.read_excel("map_dataset.xlsx")

m = folium.Map(
    location=[55.7558, 37.6173],
    zoom_start=10,
    tiles='CartoDB positron',
    attr='&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors &copy; <a href="https://carto.com">CARTO</a>'
)

for i in range(len(df)):
    addr = df['address'][i]
    popup = df['shortName'][i]

    gdf = geocode(addr, provider='nominatim', user_agent='my_map_app_v2')


    if not gdf.empty and not gdf['geometry'].is_empty.iloc[0]:
        point = gdf['geometry'].iloc[0]
        lat, lon = point.y, point.x

        folium.Marker(
            location=[lat, lon],
            popup=popup,
            tooltip=addr,
            icon=folium.Icon(color='red', icon='home'),
        ).add_to(m)

    time.sleep(1.1)

m.save('map_500.html')