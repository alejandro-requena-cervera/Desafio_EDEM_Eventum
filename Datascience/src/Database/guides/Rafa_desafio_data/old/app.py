from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime as dt
from decouple import config



def create_db_connection(host_name, port, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            port=port,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")



app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


@app.route('/eventData', methods=['POST'])
def get_event_data():
    
    peticion = request.get_json()
    event = int(peticion["event"])
    
    name = config('RENDER_DB_USER')
    password = config('RENDER_DB_PASS')
    host = config('RENDER_DB_HOST')
    port = config('RENDER_DB_PORT')
    db = config('RENDER_DB_DB')
    
    connection = create_db_connection(host, port, name, password, db)

    q_title = f"SELECT title FROM Events WHERE id = {event};"
    result_title = read_query(connection, q_title)
    
    q_description = "SELECT description FROM Events WHERE id = 4;"
    result_description = read_query(connection, q_description)
    
    q_speaker = "SELECT speacker FROM Events WHERE id = 4;"
    result_speaker = read_query(connection, q_speaker)
    
    q_date = """SELECT 
        DAY(datetime) AS DiaNumero,
        CASE MONTH(datetime)
            WHEN 1 THEN 'Enero'
            WHEN 2 THEN 'Febrero'
            WHEN 3 THEN 'Marzo'
            WHEN 4 THEN 'Abril'
            WHEN 5 THEN 'Mayo'
            WHEN 6 THEN 'Junio'
            WHEN 7 THEN 'Julio'
            WHEN 8 THEN 'Agosto'
            WHEN 9 THEN 'Septiembre'
            WHEN 10 THEN 'Octubre'
            WHEN 11 THEN 'Noviembre'
            WHEN 12 THEN 'Diciembre'
        END AS MesPalabra
    FROM Events
    WHERE id = 4;"""
    result_date = read_query(connection, q_date)

    q_registered = """SELECT U.confirmed, SUM(U.confirmed) as totalconfirmados 
    FROM Users U
    INNER JOIN EventUsers Eu ON U.id = Eu.user_id
    WHERE U.id = 4;"""
    result_registered = read_query(connection, q_registered)

    q_present = """ SELECT CAST(SUM(
    CASE 
        WHEN event_id = 4 AND arriveTime != 0 THEN 1
        ELSE 0
    END
    ) AS SIGNED) AS suma_n_registros
    FROM EventUsers
    WHERE event_id = 4;"""
    result_present = read_query(connection, q_present)

    # q_arrives = """SELECT DATE_FORMAT(arriveTime, '%H:%i') AS HoraMinuto,
    #     COUNT(user_id) AS CantidadUsuarios
    # FROM EventUsers
    # WHERE event_id = 4
    # GROUP BY HoraMinuto
    # ORDER BY HoraMinuto;"""
    # result_arrives = read_query(connection, q_arrives)

    # q_exits = """SELECT DATE_FORMAT(leaveTime, '%H:%i') AS HoraMinuto,
    #     COUNT(user_id) AS CantidadUsuarios
    # FROM EventUsers
    # WHERE event_id = 4
    # GROUP BY HoraMinuto
    # ORDER BY HoraMinuto;"""
    # result_exits = read_query(connection, q_exits)

    # q_nationality = """ SELECT COALESCE(U.Country, 'Desconocido') AS Pais, COUNT(*) AS CantidadPersonas
    # FROM EventUsers EU
    # INNER JOIN Users U ON EU.User_id = U.ID
    # WHERE EU.event_id = 4 
    # GROUP BY Pais;"""
    # result_nationality = read_query(connection, q_nationality)

    # q_count = """SELECT
    # O.id AS id,
    # T.name AS typeName,
    # COUNT(EU.User_id) AS typeCount
    # FROM EventUsers EU
    # INNER JOIN Users U ON EU.User_id = U.id
    # INNER JOIN Organizations O ON U.organization_id = O.id
    # INNER JOIN Types T ON O.Type_id = T.id
    # WHERE EU.event_id = 4
    # GROUP BY O.id, T.name;"""
    # result_count = read_query(connection, q_count)


    return {"title": result_title[0][0],
            "description": result_description[0][0],
            "speacker": result_speaker[0][0],
            "day": result_date[0][0],
            "month": result_date[0][1],
            "attendees": {
            "registered": result_registered,
            "confirmed": result_registered,
            "present": result_present}}
            # "capacity": ,
            # "entry_exit": [
            # {"id": "Entradas",
            # "data": [ ]},
            # {"id": "Salidas",
            # "data": [ ]}],
            # "nationality": [
            # {"country": "País 4",
            # "userCount": 1}],
            # "type": [
            # {"id": 4,
            # "typeName": "Sector X",
            # "typeCount": 1}]
            


if __name__ == "__main___":
    app.run(debug = True)


