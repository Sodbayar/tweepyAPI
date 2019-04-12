from pymongo import MongoClient
import folium

client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']
#collection.remove({})

tweets_iterator = collection.find()

mymap = folium.Map(location=[39.50, -98.35], zoom_start=4)

for tweet in tweets_iterator:

    if tweet['coordinates']:
        folium.CircleMarker(location=list(reversed(tweet['coordinates']['coordinates'])), radius=2).add_to(mymap)


mymap.save('map.html')
#display(mymap)
