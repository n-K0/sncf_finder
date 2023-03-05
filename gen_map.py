import folium
import sqlite3
import logging
import time
import threading

logging.basicConfig(filename='logs/sncf_finder.log', level=logging.DEBUG, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("geopy").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
start_time = time.time()


def main():
    while True:
        try:
            # Ouvrez une connexion à la base de données
            conn = sqlite3.connect('gares.db')
            logging.debug('Connexion DB Reussi')
            # Si la connexion a réussi, sortez de la boucle
            break
        except sqlite3.Error:
            # Si la connexion a échoué, attendez 30 secondes avant de réessayer
            time.sleep(30)

    cursor = conn.cursor()
    query = "SELECT Lattitude, Longitude, Nom FROM gare_destination"
    cursor.execute(query)
    data = cursor.fetchall()
    data = [{'Lattitude': lat, 'Longitude': lon, 'name': name } for lat, lon, name in data]
    conn.close()

    # Création de la carte de France
    start_time = time.time()
    france_map = folium.Map(location=[46.2276, 2.2137], zoom_start=6)
    count_carte = 0
    for row in data:
        count_carte += 1
        lattitude = row['Lattitude']
        longitude = row['Longitude']
        Name = row['name']
        PutMarker(lattitude, longitude, Name, france_map)
        logging.debug('Mise en place du marker n°{1} pour : {0}'.format(Name,count_carte))

    france_map.save('templates/france_map.html')
    logging.debug('Sauvegarde de la carte dans les templates.')
    logging.debug('--- Script gen_map.py executed in {0} seconds ---'.format((time.time() - start_time)))
    logging.debug('############################ END ################################### \n\n')

def PutMarker(lattitude_def,longitude_def, Name, france_map):
    folium.Marker(location=[lattitude_def, longitude_def],popup=Name).add_to(france_map)
    return True

if __name__ == '__main__':
    main()