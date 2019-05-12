
# psycopg2: handles queries between Flask server and postgresql
import psycopg2
# add on for psycopg2 to format postgres response as dictionary
import psycopg2.extras
# Flask is our run-time for server
from flask import Flask, request, jsonify
# runs flask on Python3
app = Flask(__name__)

# configures connection to database
mainConnection = psycopg2.connect(user="youruser",
                                       host="localhost",
                                       port="5432",
                                       database="python_hotel")

# GETS all pets
@app.route('/pets', methods=['GET'])
def getPet():
    try:
        connection = mainConnection

        # cursor: allows Python code to execute postgresql commands in database session created by connection.cursor
        # cursor is configured to provide rows stored as dictionary
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql_select_query = """ SELECT "owners"."id" AS "owner_id", "owners"."first_name", "pets"."id" as "pet_id", "pets"."breed", "pets"."color", "pets"."pet_name", "pets"."status"
        FROM "owners" JOIN "pets" ON "owners"."id" = "pets"."owner_id" ORDER BY "pets"."status" ASC; """
        # sends query using session
        cursor.execute(sql_select_query)
        # cursor method determines response rows
        # .fetchall gets all rows satisfiying query
        record = cursor.fetchall()
        print(record)
        # jsonify the returned rows
        return jsonify(record)

    except (Exception, psycopg2.Error) as error :
        # handles errors
        if(connection):
            print("Failed to GET from db", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            # connection.close()
            print("PostgreSQL cursor is closed")



@app.route("/pets/add", methods=["POST"])
def postPet():
   print(request.json)
   try:
       connection = mainConnection
       cursor = connection.cursor()
        # replace template %s with record_to_insert 
       postgres_insert_query="""INSERT INTO "pets" ("owner_id", "pet_name", "breed", "color", "status") VALUES (%s,%s,%s,%s,%s) """
       # record_to_insert must be interable
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
        #   connection.close()
          print("PostgreSQL cursor is closed")
          return 'finally'

#  <int:pet_id> creates a variable (like params) and passes to the connected function def putPet
@app.route('/pets/update/status/<int:pet_id>', methods=['PUT'])
def putPet(pet_id):
    try:
        print(pet_id, request.json['date'])
        connection = mainConnection
        cursor = connection.cursor()
        postgres_insert_query=""" UPDATE "pets" SET "status"=%s WHERE "id"=%s """
        record_to_insert = (request.json['date'],pet_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        return 'recieved PUT'
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to PUT to db", error)
            return 'failed'
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            # connection.close()
            print("PostgreSQL cursor is closed")
            return 'finally'

@app.route('/pets/delete/<int:pet_id>', methods=['DELETE'])
def deletePet(pet_id):
    try:
        print(pet_id)
        connection = mainConnection
        cursor = connection.cursor()
        postgres_insert_query=""" DELETE FROM "pets" WHERE "id" = %s """
        record_to_insert = [pet_id]
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        return 'recieved PUT'
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to DELETE in db: ", error)
            return 'failed'
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            # connection.close()
            print("PostgreSQL cursor is closed")
            return 'finally'

# ---- OWNER ROUTES -----
@app.route("/owners", methods=["GET"])
def getOwners():
    try:
        connection = mainConnection
        cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql_select_query = """ SELECT "owners"."id", "owners"."first_name", count("pets"."owner_id") FROM "owners"
        LEFT JOIN "pets" ON "pets"."owner_id" = "owners"."id" GROUP BY "owners"."id"; """
        cursor.execute(sql_select_query)
        record = cursor.fetchall()
        print(record)
        return jsonify(record)
    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to GET from db", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            # connection.close()
            print("PostgreSQL connection is closed")


@app.route("/owners/add", methods=["POST"])
def addOwner():
    print(request.json)

    try:
        connection = mainConnection
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO "owners" ("first_name") VALUES (%s) """
        record_to_insert = request.json["first_name"]
        cursor.execute(postgres_insert_query, [record_to_insert])
        connection.commit()
        return "HTTP_201_Created"
    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to POST to db", error)
            return "failed"
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            # connection.close()
            print("PostgreSQL connection is closed")
            return "finally"


@app.route("/owners/delete/<int:owner_id>", methods=["DELETE"])
def deleteOwner(owner_id):
    try:
        print(owner_id)
        connection = mainConnection
        cursor = connection.cursor()
        # Update single record now
        sql_delete_query = """ DELETE FROM "owners" WHERE "id" = %s """
        record_to_insert = [owner_id]
        cursor.execute(sql_delete_query, record_to_insert)
        connection.commit()
        return "recieved DELETE"
    except (Exception, psycopg2.Error) as error:
        print("Error in Delete OWNER operation", error)
        return "failed"
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            print("PostgreSQL connection is closed")
            return "Connection Closed"
