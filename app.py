import sqlite3
import uuid
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

#to connect to database
def get_db_connection():
    conn = sqlite3.connect('flight_delays.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/flights', methods=['GET'])
def get_flights():
    airline = request.args.get('airline')
    destination = request.args.get('destination')

    query = """
    SELECT DISTINCT
        fs.AirlineID || fs.FlightNumber AS flight_code,
        fs.AirlineID AS airline,
        fs.DepartureAirport AS origin,
        fs.ArrivalAirport AS destination,
        fs.ScheduledDepartureTimeUTC AS scheduled_departure_at,
        fs.ActualDepartureTimeUTC AS actual_departure_at,
        fs.FlightNumber AS flight_number,
        fd.DepartureStationIATA AS departureairport,
        fd.DepartureDelayCode1 AS delay_code1,
        fd.DepartureDelayTime1 AS delay_time1,
        fd.DepartureDelayDescription1 AS delay_description1,
        fd.DepartureDelayCode2 AS delay_code2,
        fd.DepartureDelayTime2 AS delay_time2,
        fd.DepartureDelayDescription2 AS delay_description2,
        fd.DepartureDelayCode3 AS delay_code3,
        fd.DepartureDelayTime3 AS delay_time3,
        fd.DepartureDelayDescription3 AS delay_description3
    FROM 
        flight_schedules fs
    LEFT JOIN 
        flight_delays fd
    ON 
        fs.FlightNumber = fd.FlightNumber
        AND fs.DepartureAirport = fd.DepartureStationIATA
        AND fs.AirlineID = fd.Airline
       
    WHERE 1=1
    """

    params = []
    if airline:
        query += " AND fs.AirlineID = ?"
        params.append(airline)
    if destination:
        query += " AND fs.ArrivalAirport = ?"
        params.append(destination)

    conn = get_db_connection()
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    flights = []
    flight_ids = set() 

    #To fetch and display the output data
    for row in rows:
        flight_identifier = (row["flight_number"], row["airline"], row["origin"], row["destination"], row["scheduled_departure_at"], row["actual_departure_at"])
        if flight_identifier in flight_ids:
            continue
        flight_ids.add(flight_identifier)
        
        flight = {
            "id": str(uuid.uuid4()),  # Generating unique UUID
            "flight_number": row["flight_number"],
            "airline": row["airline"],
            "origin": row["origin"],
            "destination": row["destination"],
            "scheduled_departure_at": row["scheduled_departure_at"],
            "actual_departure_at": row["actual_departure_at"],
            "delays": []
        }
        
        # Add delay information if present
        if row["delay_code1"]:
            flight["delays"].append({
                "code": row["delay_code1"],
                "time_minutes": row["delay_time1"],
                "description": row["delay_description1"]
            })
        if row["delay_code2"]:
            flight["delays"].append({
                "code": row["delay_code2"],
                "time_minutes": row["delay_time2"],
                "description": row["delay_description2"]
            })
        if row["delay_code3"]:
            flight["delays"].append({
                "code": row["delay_code3"],
            })
        
        flights.append(flight)

    return jsonify(flights)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
