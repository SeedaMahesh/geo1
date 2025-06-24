from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GOOGLE_API_KEY = "AIzaSyBKPmRn0P4ZCgCSKdTb2Hqd-n3ICHTdwUg"  

def find_nearest_metro(lat, lng):
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}&rankby=distance&type=subway_station&key={GOOGLE_API_KEY}"
    )
    resp = requests.get(url).json()
    if resp['status'] == 'OK' and resp['results']:
        metro = resp['results'][0]
        return {
            'name': metro['name'],
            'address': metro.get('vicinity', ''),
            'lat': metro['geometry']['location']['lat'],
            'lng': metro['geometry']['location']['lng']
        }
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    user_lat = request.form.get('lat')
    user_lng = request.form.get('lng')
    destination = request.form.get('destination', '')

    source_metro = dest_metro = None
    dest_lat = dest_lng = None

    if request.method == 'POST' and user_lat and user_lng and destination:
        # Find user's nearest metro
        source_metro = find_nearest_metro(user_lat, user_lng)
        # Geocode destination
        geo_url = (
            f"https://maps.googleapis.com/maps/api/geocode/json"
            f"?address={destination}&key={GOOGLE_API_KEY}"
        )
        geo_resp = requests.get(geo_url).json()
        if geo_resp['status'] == 'OK':
            dest_loc = geo_resp['results'][0]['geometry']['location']
            dest_lat, dest_lng = dest_loc['lat'], dest_loc['lng']
            dest_metro = find_nearest_metro(dest_lat, dest_lng)
        else:
            dest_metro = None

    return render_template(
        'main.html',
        user_lat=user_lat,
        user_lng=user_lng,
        destination=destination,
        source_metro=source_metro,
        dest_metro=dest_metro,
        dest_lat=dest_lat,
        dest_lng=dest_lng
    )

@app.route('/map', methods=['POST'])
def map_page():
    user_lat = request.form['user_lat']
    user_lng = request.form['user_lng']
    source_lat = request.form['source_lat']
    source_lng = request.form['source_lng']
    dest_lat = request.form['dest_lat']
    dest_lng = request.form['dest_lng']
    destination_lat = request.form['destination_lat']
    destination_lng = request.form['destination_lng']
    return render_template(
        'map.html',
        user_lat=user_lat,
        user_lng=user_lng,
        source_lat=source_lat,
        source_lng=source_lng,
        dest_lat=dest_lat,
        dest_lng=dest_lng,
        destination_lat=destination_lat,
        destination_lng=destination_lng,
        google_key=GOOGLE_API_KEY
    )

if __name__ == '__main__':
    app.run(debug=True)