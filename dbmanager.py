import sqlite3
import random
import string
import datetime
import os
import copy
import logging


db_path='./'

logging.basicConfig(filename='logs/sncf_finder.log', level=logging.DEBUG, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("geopy").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

class DBManager(object):
    """
    Data manager base class.
    """
    def __init__(self, db_name='gares', path2db=db_path, charset='utf8mb4'):
        """
        Initializes a DataManager object
        Args:
            db_name      :Name of the DB
            path2db      :Path to the project folder (sqlite only)
            charset      :Codificación a utilizar por defecto en la conexión
        """

        # Store paths to the main project folders and files
        self._path2db = copy.copy(path2db)
        self.dbname = db_name

        # Other class variables
        self.dbON = False    # Will switch to True when the db is connected.
        # Connector to database
        self._conn = None
        # Cursor of the database
        self._c = None

        # Try connection
        try:
            # sqlite3
            # sqlite file will be in the root of the project, we read the
            # name from the config file and establish the connection
            db_fname = os.path.join(self._path2db,
                                    self.dbname + '.db')
            logging.debug("---- Connecting to {}".format(db_fname))
            self._conn = sqlite3.connect(db_fname)
            self._c = self._conn.cursor()
            self.dbON = True
        except:
            logging.debug("---- Error connecting to the database")

        return


    def __del__(self):
        """
        When destroying the object, it is necessary to commit changes
        in the database and close the connection
        """
        try:
            self._conn.commit()
            self._conn.close()
        except:
            logging.debug("---- Error closing database")
        return


    def deleteDBtables(self, tables=None):
        """
        Delete tables from database
        Args:
            tables: If string, name of the table to reset.
                    If list, list of tables to reset
                    If None (default), all tables are deleted
        """
        # If tables is None, all tables are deleted and re-generated
        if tables is None:
            # Delete all existing tables
            self._c.execute('SET FOREIGN_KEY_CHECKS = 0')
            for table in self.getTableNames():
                self._c.execute("DROP TABLE " + table)
            self._c.execute('SET FOREIGN_KEY_CHECKS = 1')
        else:
            # It tables is not a list, make the appropriate list
            if type(tables) is str:
                tables = [tables]

            # Remove all selected tables (if exist in the database).
            for table in set(tables) & set(self.getTableNames()):
                self._c.execute("DROP TABLE " + table)
        self._conn.commit()
        return

    def getTableNames(self):
        """
        Returns a list with the names of all tables in the database
        """
        sqlcmd = "SELECT name FROM sqlite_master WHERE type='table'"
        self._c.execute(sqlcmd)
        tbnames = [el[0] for el in self._c.fetchall()]
        return tbnames

    def execute(self, sqlcmd):
        """
        Execute SQL command received as parameter
        Args:
            :
        """
        self._c.execute(sqlcmd)
        return

    def randomrows(self, num_rows=10):
        for i in range(num_rows):
            nom = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
            id_sncf = ''.join(random.choices(string.digits, k=6))
            lattitude = random.uniform(-90, 90)
            longitude = random.uniform(-180, 180)
            duration = random.uniform(0, 24)
            date_depart = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._c.execute("INSERT INTO gare_destination (Nom, ID_sncf, Lattitude, Longitude, Duration, date_depart) VALUES (?, ?, ?, ?, ?, ?)", (nom, id_sncf, lattitude, longitude, duration, date_depart))

    def deleteFromTable(self, tablename):
        """
        Delete rows from table
        Args:
            tablename:  Name of table from which data will be removed
        """
        # Make sure the tablename is valid
        if tablename in self.getTableNames():
            sqlcmd = 'DELETE FROM ' + tablename 
            self._c.execute(sqlcmd)
                # Commit changes
            self._conn.commit()
        else:
            logging.debug('Error deleting data from table: The table does not exist')
        return

    def getRandomRows(self, tablename):
        """
        Delete rows from table
        Args:
            tablename:  Name of table from which data will be removed
        """
        # Make sure the tablename is valid
        if tablename in self.getTableNames():
            sqlcmd = 'SELECT * FROM '+ tablename +' ORDER BY RANDOM() LIMIT 1'
            self._c.execute(sqlcmd)
            data_request = self._c.fetchall()
            return data_request
                # Commit changes
        else:
            logging.debug('Error deleting data from table: The table does not exist')
        return
    
    def setDbstructure(self):
        self._c.execute("DROP TABLE IF EXISTS gare_destination")
        self._c.execute("""CREATE TABLE gare_destination (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Nom TEXT NOT NULL,
                            ID_sncf TEXT NOT NULL,
                            Lattitude REAL NOT NULL,
                            Longitude REAL NOT NULL,
                            Duration REAL NOT NULL,
                            date_depart DATETIME NOT NULL)
                        """)