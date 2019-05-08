import psycopg2
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/pets')
def getStudent():
   try:
       connection = psycopg2.connect(user="walterbenson",
                                        host="localhost",
                                        port="5432",
                                        database="python_hotel")
       cursor = connection.cursor()
       sql_select_query = """ SELECT * FROM "pets" """
       cursor.execute(sql_select_query)
       record = cursor.fetchall()
       print(record)
       return jsonify(record)
   except (Exception, psycopg2.Error) as error :
       if(connection):
           print("Failed to GET from db", error)
   finally:
       #closing database connection.
       if(connection):
           cursor.close()
           connection.close()
           print("PostgreSQL connection is closed")