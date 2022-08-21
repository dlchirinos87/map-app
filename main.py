import folium
import pandas

data = pandas.read_csv("Volcanoes.csv")
latitude = list(data["LAT"])
longitude = list(data["LON"])
elevation = list(data["ELEV"])
name = list(data["NAME"])


def color_designator(eleva):
    if eleva < 1000:
        return 'green'
    elif 1000 <= eleva < 3000:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location=[38.58, -99.09], zoom_start=4, tiles="Stamen Terrain")

ftvolcanogroup = folium.FeatureGroup(name="Volcanoes")
ftpopulationgroup = folium.FeatureGroup(name="Population")

for lat, lon, elv, nm in zip(latitude, longitude, elevation, name):
    ftvolcanogroup.add_child(folium.CircleMarker(location=(lat, lon), radius=5, popup=f"{nm} {elv} mts",
                                                 fill_color=color_designator(elv), color='grey', fill_opacity=0.7))

ftpopulationgroup.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='UTF-8-sig').read(),
                                           style_function=lambda x: {'fillColor': 'green' if x["properties"]["POP2005"]
                                           < 10000000 else "yellow" if 10000000 <= x["properties"]["POP2005"] < 20000000
                                           else "red"}))

map.add_child(ftvolcanogroup)
map.add_child(ftpopulationgroup)
map.add_child(folium.LayerControl())

map.save("Map.html")
