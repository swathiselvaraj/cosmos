import sqlite3
import json
import uuid

def fetch_flight_data(destination=None, airlines=None):
    # Connect to SQLite database
    conn = sqlite3.connect('flight_delays.db')
    cursor = conn.cursor()

    # Define the base SQL query
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

    # Add filters if necessary
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

    # Execute the query
    cursor.execute(sql_query, params)

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Convert rows to the desired JSON format
    flight_data = []
    for row in rows:
        flight = {
            "id": str(uuid.uuid4()),  # Generate a unique UUID for each flight
            "flight_number": row[0],
            "airline": row[1],
            "origin": row[2],
            "destination": row[3],
            "scheduled_departure_at": row[4],
            "actual_departure_at": row[5],
            "delays": json.loads(row[6]) if row[6] else []  # Convert delays JSON array string to Python list
        }
        flight_data.append(flight)

    # Return the flight_data in JSON format
    return json.dumps(flight_data, indent=2)

# Example usage:

airlines_list = []
destination_airport = 'SOF'
# Fetch flight data with the given filters
flight_data_json = fetch_flight_data(destination=destination_airport, airlines=airlines_list)
print(flight_data_json)
