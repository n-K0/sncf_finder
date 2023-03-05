import requests, sys, time
import logging
import numpy as np
from dateutil import parser
import datetime
from geopy.geocoders import Nominatim
import sqlite3

logging.basicConfig(filename='logs/sncf_finder.log', level=logging.DEBUG, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("geopy").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


def main(adresse, duree_max_minutes):
    jour=datetime.datetime.now()
    # Connexion à la base de données
    conn = sqlite3.connect("gares.db")
    cursor = conn.cursor()
    logging.debug('Connexion à la base de données')
    # Convertissez l'adresse de l'utilisateur en latitude et longitude
    geolocator = Nominatim(user_agent="mon_application")
    start_time = time.time()
    location = geolocator.geocode(adresse)
    latitude = location.latitude
    longitude = location.longitude
    logging.debug('Localisation : {0}'.format(location))
    logging.debug('lat,long : {0}{1}'.format(latitude,longitude))
    # Récupérez la gare la plus proche de l'adresse de l'utilisateur
    headers = {'Authorization': 'ff8b5745-359b-4917-b1d3-e6c990bf17e1'}
    params = {"distance": '4000'}
    response = requests.get('https://api.sncf.com/v1/coverage/sncf/coords/{long};{lat}/places_nearby'.format(lat=latitude, long=longitude), headers=headers, params=params)
    data = response.json()
    gare_depart = data['places_nearby'][0]['stop_area']['administrative_regions'][0]['id']
    gare_depart_name = data['places_nearby'][1]['name']
    for site in data['places_nearby']:
        logging.debug('Les gares les plus proches sont : {0}'.format(site['name']))
    # Récupérez la durée maximum souhaitée
    #duree_max_minutes = 11880
    date_depart= jour.strftime("%Y%m%dT%H%M%S")
    
    # Faites une requête à l'API Sncf pour trouver les destinations possibles à partir de la gare de départ
    params = {'from': gare_depart, 'max_duration': duree_max_minutes}
    response = requests.get('https://api.sncf.com/v1/coverage/sncf/journeys', headers=headers, params=params)
    data = response.json()

    # Parcourez les trajets disponibles et affichez les informations sur les trajets qui ont une durée inférieure à la durée maximum
    count=0
    list_gare_arrivee=[]
    try:
        logging.debug('Il y a {0} destinations possibles.'.format(len(data['journeys'])))
    except KeyError:
        logging.debug("Il n'y a pas de destination possible ! ------")
        code_page = 404
        return code_page

    for trajet in data['journeys']:
        duree_trajet_minutes = trajet['duration']
        depart = trajet['departure_date_time']
        arrivee = trajet['arrival_date_time']
        gare_arrivee = trajet['to']['name']
        gare_arrivee_id = trajet['to']['id']
        coord_arrivee = trajet['to']['stop_point']['coord']
        list_gare_arrivee.append(gare_arrivee)
        lattitude = coord_arrivee['lat']
        longitude = coord_arrivee['lon']
        count+=1
        cursor.execute("INSERT INTO gare_destination (Nom, ID_sncf, Lattitude, Longitude, Duration, date_depart) VALUES (?, ?, ?, ?, ?, ?)", (gare_arrivee, gare_arrivee_id, lattitude, longitude, duree_trajet_minutes, date_depart))
        conn.commit()

    list_gare_arrivee=np.unique(list_gare_arrivee)
    conn.close()
    respon_builded={
        'request_url_place_nearby': response,
        'adresse': location,
        'data': data
    }
    logging.debug('--- Script Get_journey.py executed in {0} seconds ---'.format((time.time() - start_time)))
    logging.debug('------------------------------------')
    return respon_builded

if __name__ == '__main__':
    main()
    
    # adresse = "19 Rue Jean GIONO, 31130 Balma"
    # duree_max_minutes = 11880
    # main(adresse, duree_max_minutes)
