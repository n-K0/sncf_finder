from flask import Flask, render_template, request, session, redirect, url_for
import get_journey
import sqlite3
import gen_map
import os
from dbmanager import DBManager
from manage_db import clear_table
from dateutil import parser
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secret key'
db_path='gares.db'


@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
      session['field1'] = request.form['field1']
      session['field2'] = request.form['field2']
      if request.form['button-role'] == 'Random':
         #return 'c du random'
         return redirect(url_for('random'))
      elif request.form['button-role'] == 'Trajets':
         return redirect(url_for('result'))
      else:
         return 'pas de choix'
   else:
      DBManager().deleteFromTable('gare_destination')
      DBManager().setDbstructure()
      try:
         os.remove('templates/france_map.html')
      except:
         pass
      return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
   if request.method == 'POST':
      if request.form['button-role'] == 'Random':
         return redirect(url_for('random'))
      if request.form['button-role'] == 'Home':
         return redirect(url_for('index'))
   else:
      field1 = session.get('field1', '')
      field2 = session.get('field2', '')
      time_distance_h, time_distance_m= field2.split(':')
      time_distance_s = (int(time_distance_m)*60) + (int(time_distance_h)*3600)
      time_distance_m = round(int(time_distance_m))
      time_distance_h = round(int(time_distance_h))
      return_var = get_journey.main(field1, time_distance_s)
      if return_var == 404:
         return render_template('404.html'), 404
      #print(return_var)
      map_fr = gen_map.main()
      
      return render_template('result.html', field1=field1, field2=time_distance_s, time_distance=field2)

@app.route('/random', methods=['GET', 'POST'])
def random():
   if request.method == 'POST':
      if request.form['button-role'] == 'Home':
         return redirect(url_for('index'))
   else:
      field1 = session.get('field1', '')
      field2 = session.get('field2', '')
      time_distance_h, time_distance_m= field2.split(':')
      time_distance_s = (int(time_distance_m)*60) + (int(time_distance_h)*3600)
      time_distance_m = round(int(time_distance_m))
      time_distance_h = round(int(time_distance_h))
      return_var = get_journey.main(field1, time_distance_s)
      if return_var == 404:
         return render_template('404.html'), 404
      selected_gare=DBManager().getRandomRows('gare_destination')

      return render_template('random.html', selected_gare=selected_gare, time_distance=field2, date_depart=parser.parse(selected_gare[0][6]), duree_voyage=timedelta(seconds=selected_gare[0][5]))

@app.route('/waiting')
def waiting():
   return render_template('waiting.html')

if __name__ == '__main__':
   app.run(debug=True)
