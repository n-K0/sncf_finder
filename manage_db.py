import sqlite3
import random
import string
import datetime

db_path='gares.db'

def list_all_rows(conn):
    cursor = conn.cursor()
    # Sélection de toutes les lignes de la table
    cursor.execute("SELECT * FROM gare_destination")
    # Affichage des lignes
    rows = cursor.fetchall()
    return rows


def check_database_exists(conn):
    cursor = conn.cursor()
    result = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='gare_destination'
        """).fetchone()
    return result is not None

def check_table_structure(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(gare_destination)")
    column_info = cursor.fetchall()
    column_names = [column[1] for column in column_info]
    expected_columns = ['ID', 'Nom', 'ID_sncf', 'Lattitude', 'Longitude', 'Duration', 'date_depart']
    return column_names == expected_columns

def insert_example_rows(conn, num_rows=10):
    cursor = conn.cursor()
    for i in range(num_rows):
        # Génération aléatoire des données pour chaque ligne
        nom = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        id_sncf = ''.join(random.choices(string.digits, k=6))
        lattitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        duration = random.uniform(0, 24)
        date_depart = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insertion de la ligne dans la table
        cursor.execute("INSERT INTO gare_destination (Nom, ID_sncf, Lattitude, Longitude, Duration, date_depart) VALUES (?, ?, ?, ?, ?, ?)", (nom, id_sncf, lattitude, longitude, duration, date_depart))
    conn.commit()

def clear_table(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gare_destination")
    conn.commit()

def recreate_table(conn):
    cursor = conn.cursor()
    # Suppression de la table s'il existe
    cursor.execute("DROP TABLE IF EXISTS gare_destination")
    # Création de la table gare_destination
    cursor.execute("""CREATE TABLE gare_destination (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Nom TEXT NOT NULL,
                        ID_sncf TEXT NOT NULL,
                        Lattitude REAL NOT NULL,
                        Longitude REAL NOT NULL,
                        Duration REAL NOT NULL,
                        date_depart DATETIME NOT NULL)
                    """)
    conn.commit()

# Demande à l'utilisateur ce qu'il souhaite faire
def main():
    while True:
        print("Que souhaitez-vous faire ?")
        print("1 - Créer la base de données et la table")
        print("2 - Insérer des exemples dans la table")
        print("3 - Vider complètement la table")
        print("4 - Afficher les lignes de la Table")
        print("5 - Recréer la table")
        print("6 - Quit")
        choice = input("Entrez votre choix : ")
        if choice == '1':
            with sqlite3.connect(db_path) as conn:
                if not check_database_exists(conn):
                    cursor = conn.cursor()
                    # Création de la table gare_destination
                    cursor.execute("""CREATE TABLE gare_destination (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Nom TEXT,
                                        ID_sncf TEXT,
                                        Lattitude REAL,
                                        Longitude REAL,
                                        Duration REAL,
                                        date_depart DATE
                                        )""")

                    # Enregistrement des modifications
                    conn.commit()
                else:
                    if not check_table_structure(conn):
                        raise Exception("La structure de la table gare_destination n'est pas correcte")
            
            if choice == '2':
                with sqlite3.connect(db_path) as conn:
                    insert_example_rows(conn, num_rows=5)
            if choice == '3':
                with sqlite3.connect(db_path) as conn:
                    clear_table(conn)
            if choice == '4':
                with sqlite3.connect(db_path) as conn:
                    rows = list_all_rows(conn)
                    for row in rows:
                        print(row)
            if choice == '5':
                with sqlite3.connect(db_path) as conn:
                    recreate_table(conn)
            if choice == '6':
                exit()
                
if __name__ == '__main__':
    main()

