from flask import Flask, request, jsonify
import joblib
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
model = joblib.load('lease_price_model.joblib')
cityProvDict = {'British Columbia': ['Abbotsford, British Columbia', 'Burnaby, British Columbia', 'Campbell River, British Columbia', 'Chilliwack, British Columbia', 'Colwood, British Columbia', 'Comox, British Columbia', 'Coquitlam, British Columbia', 'Courtenay, British Columbia', 'Cranbrook, British Columbia', 'Dawson Creek, British Columbia', 'Duncan, British Columbia', 'Fort St John, British Columbia', 'Golden, British Columbia', 'Horseshoe Bay, British Columbia', 'Kamloops, British Columbia', 'Kelowna, British Columbia', 'Kitimat, British Columbia', 'Ladysmith, British Columbia', 'Lake Country, British Columbia', 'Langford, British Columbia', 'Langley, British Columbia', 'Maple Ridge, British Columbia', 'Mission, British Columbia', 'Nanaimo, British Columbia', 'New Westminster, British Columbia', 'North Cowichan, British Columbia', 'Parksville, British Columbia', 'Penticton, British Columbia', 'Port Alberni, British Columbia', 'Port Moody, British Columbia', 'Prince George, British Columbia', 'Richmond, British Columbia', 'Saanich, British Columbia', 'Sooke, British Columbia', 'Squamish, British Columbia', 'Summerland, British Columbia', 'Surrey, British Columbia', 'Tsawwassen, British Columbia', 'Vancouver, British Columbia', 'Vernon, British Columbia', 'Victoria, British Columbia', 'Wardner, British Columbia', 'West Kelowna, British Columbia', 'West Vancouver, British Columbia', 'White Rock, British Columbia'], 'Alberta': ['Airdrie, Alberta', 'Aldersyde, Alberta', 'Beaumont, Alberta', 'Beiseker, Alberta', 'Blackfalds, Alberta', 'Bonnyville, Alberta', 'Brooks, Alberta', 'Calgary, Alberta', 'Camrose, Alberta', 'Canmore, Alberta', 'Carmangay, Alberta', 'Chestermere, Alberta', 'Cochrane, Alberta', 'Cold Lake, Alberta', 'Crossfield, Alberta', 'Crowsnest Pass, Alberta', 'De Winton, Alberta', 'Drumheller, Alberta', 'Edmonton, Alberta', 'Fort McMurray, Alberta', 'Fort Saskatchewan, Alberta', 'Grande Prairie, Alberta', 'High River, Alberta', 'Leduc, Alberta', 'Lethbridge, Alberta', 'Medicine Hat, Alberta', 'Morinville, Alberta', 'Okotoks, Alberta', 'Olds, Alberta', 'Peace River, Alberta', 'Ponoka, Alberta', 'Priddis, Alberta', 'Red Deer, Alberta', 'Rocky View, Alberta', 'Sherwood Park, Alberta', 'Slave Lake, Alberta', 'Spruce Grove, Alberta', 'St. Albert, Alberta', 'Stony Plain, Alberta', 'Strathmore, Alberta', 'Sylvan Lake, Alberta', 'Wainwright, Alberta', 'Westlock, Alberta', 'Wetaskiwin, Alberta', 'Whitecourt, Alberta'], 'Ontario': ['Ajax, Ontario', 'Amherstview, Ontario', 'Ancaster, Ontario', 'Aurora, Ontario', 'Ayr, Ontario', 'Barrie, Ontario', 'Belleville, Ontario', 'Bolton, Ontario', 'Bradford, Ontario', 'Brampton, Ontario', 'Brantford, Ontario', 'Breslau, Ontario', 'Burlington, Ontario', 'Caledon, Ontario', 'Cambridge, Ontario', 'Carleton Place, Ontario', 'Chatham, Ontario', 'Clarington, Ontario', 'Collingwood, Ontario', 'Cornwall, Ontario', 'East Gwillimbury, Ontario', 'East York, Ontario', 'Fergus, Ontario', 'Fort Erie, Ontario', 'Georgina, Ontario', 'Gloucester, Ontario', 'Gravenhurst, Ontario', 'Grimsby, Ontario', 'Guelph, Ontario', 'Hamilton, Ontario', 'Hanover, Ontario', 'Huntsville, Ontario', 'Innisfil, Ontario', 'Kanata, Ontario', 'Kingston, Ontario', 'Kitchener, Ontario', 'LaSalle, Ontario', 'Leamington, Ontario', 'Lindsay, Ontario', 'Listowel, Ontario', 'London, Ontario', 'Lucan, Ontario', 'Markham, Ontario', 'Milton, Ontario', 'Mississauga, Ontario', 'Mount Forest, Ontario', 'Newmarket, Ontario', 'Niagara Falls, Ontario', 'North Bay, Ontario', 'North York, Ontario', 'Oakville, Ontario', 'Orangeville, Ontario', 'Orillia, Ontario', 'Oshawa, Ontario', 'Ottawa, Ontario', 'Owen Sound, Ontario', 'Paris, Ontario', 'Pelham, Ontario', 'Peterborough, Ontario', 'Pickering, Ontario', 'Port Colborne, Ontario', 'Port Elgin, Ontario', 'Richmond Hill, Ontario', 'Sarnia, Ontario', 'Sault Ste. Marie, Ontario', 'Scarborough, Ontario', 'St Thomas, Ontario', 'St. Catharines, Ontario', 'Stoney Creek, Ontario', 'Stratford, Ontario', 'Sudbury, Ontario', 'Tecumseh, Ontario', 'Thorold, Ontario', 'Thunder Bay, Ontario', 'Tilbury, Ontario', 'Tillsonburg, Ontario', 'Timmins, Ontario', 'Toronto, Ontario', 'Vanier, Ontario', 'Vaughan, Ontario', 'Waterloo, Ontario', 'Welland, Ontario', 'Whitby, Ontario', 'Whitchurch-Stouffville, Ontario', 'Windsor, Ontario', 'Woodstock, Ontario', 'Wyoming, Ontario'], 'Saskatchewan': ['Assiniboia, Saskatchewan', 'Lloydminster, Saskatchewan', 'Moose Jaw, Saskatchewan', 'Prince Albert, Saskatchewan', 'Regina, Saskatchewan', 'Saskatoon, Saskatchewan', 'Swift Current, Saskatchewan', 'Warman, Saskatchewan', 'Yorkton, Saskatchewan'], 'Nova Scotia': ['Bedford, Nova Scotia', 'Bridgewater, Nova Scotia', 'Digby, Nova Scotia', 'Glace Bay, Nova Scotia', 'Halifax, Nova Scotia'], 'Manitoba': ['Blumenort, Manitoba', 'Brandon, Manitoba', 'Headingley, Manitoba', 'Ile des Chenes, Manitoba', 'Niverville, Manitoba', 'Portage la Prairie, Manitoba', 'Saint Adolphe, Manitoba', 'Selkirk, Manitoba', 'Steinbach, Manitoba', 'West St. Paul, Manitoba', 'Winnipeg, Manitoba'], 'Quebec': ['Boisbriand, Quebec', 'Brossard, Quebec', 'Candiac, Quebec', 'Cote Saint-Luc, Quebec', 'Dorval, Quebec', 'Gatineau, Quebec', 'Hampstead, Quebec', 'Laval, Quebec', 'Longueuil, Quebec', 'Mascouche, Quebec', 'Montreal, Quebec', 'Pointe-Claire, Quebec', 'Quebec City, Quebec', 'Saguenay, Quebec', 'Saint-Hyacinthe, Quebec', 'Sherbrooke, Quebec', 'Vaudreuil-Dorion, Quebec', 'Westmount, Quebec'], 'New Brunswick': ['Dieppe, New Brunswick', 'Moncton, New Brunswick'], 'Newfoundland and Labrador': ["St. John's, Newfoundland and Labrador"]}

@app.route("/predict", methods=['POST'])
def predict():
    data = request.json
    try:
        org_data = {
            'city': [data['city']],
            'province': [data['province']],
            'lease_term': [data['lease_term']],
            'type': [data['type']],
            'beds': [data['beds']],
            'baths': [data['baths']],
            'sq_feet': [data['sq_feet']],
            'furnishing': [data['furnished']],
            'Pets': [data['pets']]
        }
        
        df = pd.DataFrame(org_data)
        predicted_price = model.predict(df)[0]
        
        if(float(data['beds']) + 1 <= 8):
            bedHigh = org_data.copy()
            bedHigh['beds'] = [float(data['beds']) + 1]
            bedHighDF = pd.DataFrame(bedHigh)
            bed_higher_prediction = model.predict(bedHighDF)[0]
        else:
            bed_higher_prediction = 0
        
        if(float(data['beds']) -1 >= 1):
            bedLow = org_data.copy()
            bedLow['beds'] = [float(data['beds']) - 1]
            bedLowDf = pd.DataFrame(bedLow)
            bed_lower_prediction = model.predict(bedLowDf)[0]
        else:
            bed_lower_prediction = 0
        
        if(float(data['baths']) + 0.5 <= 5):
            bathHigh = org_data.copy()
            bathHigh['baths'] = [float(data['baths']) + 0.5]
            bathHighDf = pd.DataFrame(bathHigh)
            bath_higher_prediction = model.predict(bathHighDf)[0]
        else:
            bath_higher_prediction = 0
        
        if(float(data['baths']) - 0.5 >= 1):
            bathLow = org_data.copy()
            bathLow['baths'] = [float(data['baths']) - 0.5]
            bathLowDef = pd.DataFrame(bathLow)
            bath_lower_prediction = model.predict(bathLowDef)[0]
        else:
            bath_lower_prediction = 0
        
        result = {
            'predicted_price': predicted_price,
            'bed_higher_prediction': bed_higher_prediction,
            'bed_lower_prediction': bed_lower_prediction,
            'bath_higher_prediction': bath_higher_prediction,
            'bath_lower_prediction': bath_lower_prediction,
            'city_prediction': []
        }
        
        closest_cities = get_2_closest_cities(data['city'], data['province'])
        for city in closest_cities:
            cityData = org_data.copy()
            cityData['city'] = [city]
            cityDataDef = pd.DataFrame(cityData)
            city_prediction = model.predict(cityDataDef)[0]
            result['city_prediction'].append((city[0], city_prediction))
            
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

def get_distance_between_cities(api_key, origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['rows'][0]['elements'][0]['status'] == 'OK':
            distance = data['rows'][0]['elements'][0]['distance']['value']
            return distance
        else:
            return float('inf')
    else:
        return float('inf')

def get_2_closest_cities(originCity, originProvince):
    listOfCities = cityProvDict["Ontario"]
    distances = []
    origin = originCity + ", " + originProvince
    for city in listOfCities:
        if city != origin:
            distance = get_distance_between_cities(API_KEY, origin, city)
            distances.append((city[:city.index(",")], distance))

    distances.sort(key=lambda x: x[1])
    closest_cities = distances[:2]
    return closest_cities

if __name__ == "__main__":
    app.run(debug=True)
