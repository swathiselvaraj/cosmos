import requests
import json
import sqlite3

json_url_dataset1 = "https://challenge.usecosmos.cloud/flight_schedules.json"
response = requests.get(json_url_dataset1)
data = response.json()

# Extracting information
flights_details = data['FlightStatusResource']['Flights']['Flight']

# List to store dictionaries for each flight
flights_list = []

# Iterate over each flight and extract relevant information
for flight in flights_details:
    flight_dict = {
        'DepartureAirport': flight['Departure']['AirportCode'],
        'ScheduledDepartureTimeLocal': flight['Departure']['ScheduledTimeLocal']['DateTime'],
        'ScheduledDepartureTimeUTC': flight['Departure'].get('ScheduledTimeUTC', {}).get('DateTime', None),
        'ActualDepartureTimeLocal': flight['Departure'].get('ActualTimeLocal', {}).get('DateTime', None),
        'ActualDepartureTimeUTC': flight['Departure'].get('ActualTimeUTC', {}).get('DateTime', None),
        'DepartureTerminal': flight['Departure'].get('Terminal', {}).get('Name', None),
        'DepartureGate': flight['Departure'].get('Terminal', {}).get('Gate', None),
        'ArrivalAirport': flight['Arrival']['AirportCode'],
        'ScheduledArrivalTimeLocal': flight['Arrival']['ScheduledTimeLocal']['DateTime'],
        'ScheduledArrivalTimeUTC': flight['Arrival'].get('ScheduledTimeUTC', {}).get('DateTime', None),
        'ActualArrivalTimeLocal': flight['Arrival'].get('ActualTimeLocal', {}).get('DateTime', None),
        'ActualArrivalTimeUTC': flight['Arrival'].get('ActualTimeUTC', {}).get('DateTime', None),
        'ArrivalTerminal': flight['Arrival'].get('Terminal', {}).get('Name', None),
        'ArrivalGate': flight['Arrival'].get('Terminal', {}).get('Gate', None),
        'AirlineID': flight['MarketingCarrier']['AirlineID'],
        'FlightNumber': flight['MarketingCarrier']['FlightNumber'],
        'AircraftCode': flight['Equipment']['AircraftCode'],
        'AircraftRegistration': flight['Equipment']['AircraftRegistration'],
        'FlightStatus': flight['FlightStatus']['Definition'],
        'ServiceType': flight['ServiceType']
    }
    flights_list.append(flight_dict)

conn = sqlite3.connect('flight_delays.db')
cursor = conn.cursor()

# Create table flight_schedules if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flight_schedules (
    DepartureAirport VARCHAR(10),
    ScheduledDepartureTimeUTC DATETIME,
    ActualDepartureTimeUTC TEXT,
    DepartureTerminal TEXT,
    DepartureGate TEXT,
    ArrivalAirport TEXT,
    ScheduledArrivalTimeUTC TEXT,
    ActualArrivalTimeUTC TEXT,
    ArrivalTerminal TEXT,
    ArrivalGate TEXT,
    AirlineID VARCHAR(10),
    FlightNumber VARCHAR(10),
    AircraftCode TEXT,
    AircraftRegistration TEXT,
    FlightStatus TEXT,
    ServiceType TEXT
    )
''')

# Insert data into the table
for flight in flights_list:
    cursor.execute('''
        INSERT INTO flight_schedules (
            DepartureAirport, ScheduledDepartureTimeUTC,
            ActualDepartureTimeUTC, DepartureTerminal, DepartureGate, ArrivalAirport, 
            ScheduledArrivalTimeUTC, ActualArrivalTimeUTC, ArrivalTerminal, ArrivalGate,
            AirlineID, FlightNumber, AircraftCode, AircraftRegistration, FlightStatus, ServiceType
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        flight['DepartureAirport'], flight['ScheduledDepartureTimeUTC'],
        flight['ActualDepartureTimeLocal'], flight['DepartureTerminal'],
        flight['DepartureGate'], flight['ArrivalAirport'],
        flight['ScheduledArrivalTimeUTC'], flight['ActualArrivalTimeUTC'],
        flight['ArrivalTerminal'], flight['ArrivalGate'], flight['AirlineID'], flight['FlightNumber'],
        flight['AircraftCode'], flight['AircraftRegistration'], flight['FlightStatus'], flight['ServiceType']
    ))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Data successfully imported into SQLite database.")