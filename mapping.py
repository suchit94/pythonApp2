#import libraries here:
import folium
import pandas

#open file and assign to variable here:
data = pandas.read_csv("Volcanoes.txt")

#python lists of all longitudinal and latitudinal coordinates and elevations saved to variables:
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
name = list(data["NAME"])

#create function to determine the color of the marker here:
def markerColor(elevation):
    if elevation > 0 and elevation < 2000:
        return "green"
    elif elevation > 2000 and elevation < 3000:
        return "orange"
    else:
        return "red"

#add base map here:
map = folium.Map(location=[42.022814, -114.118327], zoom_start=4, tiles="Stamen Terrain")

#add a marker (children) to the map using a for loop here:
fgv = folium.FeatureGroup(name="Volcanoes") 
for lt, ln, elv, nm in zip(lat, lon, elev, name):
    fgv.add_child(folium.CircleMarker(
        location=[lt,ln], 
        radius=6, #size of circle
        popup= "NAME: " + nm + " ELEVATION: " + str(elv) + "m",
        fill_color=markerColor(elv),
        color='none', #border color
        fill_opacity=0.7)) #transparency 

#add polygon layer which will display shading of each country here: 
fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
#GREEN if pop is < 10mil, ORANGE if pop is > 10mil and < 20mil, RED if pop is > 20mil
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv) #add this feature group to our final map
map.add_child(fgp) #add this feature group to our final map
map.add_child(folium.LayerControl()) #MUST BE PLACED AFTER THE FEATURE GROUPS FOR VOLCANOES AND POPULATION

#save map here:
map.save("Map1.html")
