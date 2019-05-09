import psycopg2
import psycopg2.extras

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
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql_select_query = """ SELECT "owners"."id" AS "owner_id", "owners"."first_name", "pets"."id" as "pet_id", "pets"."breed", "pets"."color", "pets"."pet_name", "pets"."status"
        FROM "owners" JOIN "pets" ON "owners"."id" = "pets"."owner_id"; """
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
            # connection.close()
            print("PostgreSQL cursor is closed")



@app.route("/pets/add", methods=["POST"])
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
        #   connection.close()
          print("PostgreSQL cursor is closed")
          return 'finally'

@app.route('/pets/update/status/<int:pet_id>', methods=['PUT'])
def putPet(pet_id):
    try:
        print(pet_id)
        connection = mainConnection
        cursor = connection.cursor()
        postgres_insert_query=""" UPDATE "pets" SET "status"=null WHERE "id"=%s """
        record_to_insert = pet_id
        cursor.execute(postgres_insert_query, [record_to_insert])
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


# ---- OWNER ROUTES -----
@app.route("/owners", methods=["GET"])
def getOwners():
    try:
        connection = mainConnection
        cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql_select_query = """ SELECT * FROM "owners" """
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
            connection.close()
            print("PostgreSQL connection is closed")
            return "finally"


@app.route("/owners/delete/<int:ownerId>", methods=["DELETE"])
def deleteData(ownerId):
    try:
        connection = mainConnection
        cursor = connection.cursor()
        print("arguments: ", ownerId)
        # Update single record now
        sql_delete_query = """ Delete from "owners" where id = %s """
        cursor.execute(sql_delete_query, [ownerId])
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")
        return "HTTP_201_Deleted"
    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)
        return "failed"
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return "Connection Closed"
