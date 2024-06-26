from flask import Flask, request, jsonify
import sqlite3
import json
import uuid

app = Flask(__name__)

def fetch_flight_data(destination=None, airlines=None):
    conn = sqlite3.connect('flight_delays.db')
    cursor = conn.cursor()

    sql_query = """
    SELECT
        fs.FlightNumber AS flight_number,
        fs.AirlineID AS airline,
        fs.DepartureAirport AS origin,
        fs.ArrivalAirport AS destination,
        fs.ScheduledDepartureTimeUTC AS scheduled_departure_at,
        fs.ActualDepartureTimeUTC AS actual_departure_at,
        JSON_ARRAY(
            JSON_OBJECT(
                'code', fd.DepartureDelayCode1,
                'time_minutes', fd.DepartureDelayTime1,
                'description', fd.DepartureDelayDescription1
            ),
            JSON_OBJECT(
                'code', fd.DepartureDelayCode2,
                'time_minutes', fd.DepartureDelayTime2,
                'description', fd.DepartureDelayDescription2
            ),
            JSON_OBJECT(
                'code', fd.DepartureDelayCode3,
                'time_minutes', fd.DepartureDelayTime3,
                'description', fd.DepartureDelayDescription3
            )
        ) AS delays
    FROM
        flight_schedules fs
    LEFT JOIN
        flight_delays fd ON fs.FlightNumber = fd.FlightNumber
    """

    filters = []
    params = []

    if destination:
        filters.append("fs.ArrivalAirport = ?")
        params.append(destination)

    if airlines:
        placeholders = ','.join('?' for _ in airlines)
        filters.append(f"fs.AirlineID IN ({placeholders})")
        params.extend(airlines)

    if filters:
        sql_query += " WHERE " + " AND ".join(filters)

    sql_query += " GROUP BY fs.FlightNumber"

    cursor.execute(sql_query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    flight_data = []
    for row in rows:
        flight = {
            "id": str(uuid.uuid4()),
            "flight_number": row[0],
            "airline": row[1],
            "origin": row[2],
            "destination": row[3],
            "scheduled_departure_at": row[4],
            "actual_departure_at": row[5],
            "delays": json.loads(row[6]) if row[6] else []
        }
        flight_data.append(flight)

    return flight_data

@app.route('/api/flights', methods=['GET'])
def get_flights():
    destination = request.args.get('destination')
    airlines = request.args.getlist('airlines')
    flight_data = fetch_flight_data(destination, airlines)
    return jsonify(flight_data)

if __name__ == '__main__':
    app.run(debug=True)
