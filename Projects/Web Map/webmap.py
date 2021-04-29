import folium
import pandas,io
 
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
data_json = io.open("world.json",'r',encoding='utf-8-sig').read()


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'
 
# base map layer, openstreet map  
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="OpenStreetMap")

# marker layer
fgv = folium.FeatureGroup(name = "Volcanoes")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=150, height=100)
#   fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = color_producer(el))))
    fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=6, popup=folium.Popup(iframe),
    fill_color=color_producer(el),color='grey',fill_opacity=0.7))



# adding a GeoJson polygon layer and cholropeth map
fgp = folium.FeatureGroup(name = "Population")
fgp.add_child(folium.GeoJson(data=data_json,style_function=lambda x: {'fillColor':'green' if x['properties']
['POP2005'] < 10000000 else 'yellow' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' }))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map.html")