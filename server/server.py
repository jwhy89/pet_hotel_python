import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

mainConnection = psycopg2.connect(user="walterbenson",
                                       host="localhost",
                                       port="5432",
                                       database="python_hotel")
@app.route('/pets', methods=['GET'])
def getPet():
   try:
       connection = mainConnection
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

@app.route('/pets/add', methods=['POST'])
def postPet():
   print(request.json)
   try:
       connection = mainConnection
       cursor = connection.cursor()
       postgres_insert_query="""INSERT INTO "pets" ("owner_id", "pet_name", "breed", "color", "status") VALUES (%s,%s,%s,%s,%s) """
       record_to_insert = (request.json['owner_id'], request.json['pet_name'], request.json['breed'], request.json['color'], request.json['status'])
       cursor.execute(postgres_insert_query, record_to_insert)
       connection.commit()
       return 'HTTP_201_Created'
   except (Exception, psycopg2.Error) as error :
       if(connection):
          print("Failed to POST to db", error)
          return 'failed'
   finally:
       #closing database connection.
       if(connection):
          cursor.close()
          connection.close()
          print("PostgreSQL connection is closed")
          return 'finally'

# ---- OWNER ROUTES -----
@app.route('/owners')
def getOwner():
   try:
       connection = mainConnection
       cursor = connection.cursor()
       sql_select_query = """ SELECT * FROM "owners" """
       cursor.execute(sql_select_query)
       record = cursor.fetchall()
       print(record)
       return jsonify(record)
   except (Exception, psycopg2.Error) as error:
       if(connection):
           print("Failed to GET from db", error)
   finally:
       # closing database connection.
       if(connection):
           cursor.close()
           connection.close()
           print("PostgreSQL connection is closed")

@app.route('/owners/add', methods=['POST'])
def addOwner():
   print(request.json)

   try:
       connection = mainConnection
       cursor = connection.cursor()
       postgres_insert_query = """ INSERT INTO "owners" ("first_name") VALUES (%s) """
       record_to_insert = (request.json['first_name'])
       cursor.execute(postgres_insert_query, [record_to_insert])
       connection.commit()
       return 'HTTP_201_Created'
   except (Exception, psycopg2.Error) as error :
       if(connection):
          print("Failed to POST to db", error)
          return 'failed'
   finally:
       #closing database connection.
       if(connection):
          cursor.close()
          connection.close()
          print("PostgreSQL connection is closed")
          return 'finally'