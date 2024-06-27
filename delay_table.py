import requests
import sqlite3

# Fetch the JSON data from the URL
json_url_dataset2 = "https://challenge.usecosmos.cloud/flight_delays.json"
response = requests.get(json_url_dataset2)
data = response.json()
flights_delay_info = []

#list of all the data in the json file fetch it as required
if isinstance(data, list):
    for flight in data:
        flight_info = {
            'FlightCode': flight['Flight']['OperatingFlight']['flightCode'],
            'Airline': flight['Flight']['OperatingFlight']['Airline'],
            'FlightNumber': flight['Flight']['OperatingFlight']['Number'],
            'FlightIdDate': flight['Flight']['OperatingFlight']['FlightIdDate'],
            'ArrivalStationIATA': flight['FlightLegs'][0]['Arrival']['Station']['IATA'],
            'ArrivalStationICAO': flight['FlightLegs'][0]['Arrival']['Station']['ICAO'],
            'ActualArrivalTime': flight['FlightLegs'][0].get('ActualArrivalTime', None),
            'ScheduledArrivalTime': flight['FlightLegs'][0].get('ScheduledArrivalTime', None),
            'DepartureStationIATA': flight['FlightLegs'][0]['Departure']['Station']['IATA'],
            'DepartureStationICAO': flight['FlightLegs'][0]['Departure']['Station']['ICAO'],
            'ActualDepartureTime': flight['FlightLegs'][0].get('ActualDepartureTime', None),
            'ScheduledDepartureTime': flight['FlightLegs'][0].get('ScheduledDepartureTime', None),
            'DepartureDelayCode1': flight['FlightLegs'][0]['Departure']['Delay']['Code1']['Code'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code1') else None,
            'DepartureDelayTime1': flight['FlightLegs'][0]['Departure']['Delay']['Code1']['DelayTime'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code1') else None,
            'DepartureDelayDescription1': flight['FlightLegs'][0]['Departure']['Delay']['Code1']['Description'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code1') else None,
            'DepartureDelayCode2': flight['FlightLegs'][0]['Departure']['Delay']['Code2']['Code'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code2') else None,
            'DepartureDelayTime2': flight['FlightLegs'][0]['Departure']['Delay']['Code2']['DelayTime'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code2') else None,
            'DepartureDelayDescription2': flight['FlightLegs'][0]['Departure']['Delay']['Code2']['Description'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code2') else None,
            'DepartureDelayCode3': flight['FlightLegs'][0]['Departure']['Delay']['Code3']['Code'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code3') else None,
            'DepartureDelayTime3': flight['FlightLegs'][0]['Departure']['Delay']['Code3']['DelayTime'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code3') else None,
            'DepartureDelayDescription3': flight['FlightLegs'][0]['Departure']['Delay']['Code3']['Description'] if flight['FlightLegs'][0]['Departure']['Delay'].get('Code3') else None,
            'OriginalArrivalStationIATA': flight['FlightLegs'][0]['Diversion']['OriginalArrivalStation']['IATA'] if flight['FlightLegs'][0].get('Diversion') else None,
            'OriginalArrivalStationICAO': flight['FlightLegs'][0]['Diversion']['OriginalArrivalStation']['ICAO'] if flight['FlightLegs'][0].get('Diversion') else None,
        }
        flights_delay_info.append(flight_info)

else:
    print("Unexpected data structure. Expected a list of flights.")



# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('flight_delays.db')
cursor = conn.cursor()

# Creating a flight_delays table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS flight_delays (
    FlightCode VARCHAR(10),
    Airline VARCHAR(10),
    FlightNumber VARCHAR(10),
    FlightIdDate DATE,
    ArrivalStationIATA VARCHAR(10),
    ArrivalStationICAO VARCHAR(10),
    ActualArrivalTime DATETIME,
    ScheduledArrivalTime DATETIME,
    DepartureStationIATA VARCHAR(10),
    DepartureStationICAO VARCHAR(10),
    ActualDepartureTime DATETIME,
    ScheduledDepartureTime DATETIME,
    DepartureDelayCode1 VARCHAR(10),
    DepartureDelayTime1 INT,
    DepartureDelayDescription1 VARCHAR(100),
    DepartureDelayCode2 VARCHAR(10),
    DepartureDelayTime2 INT,
    DepartureDelayDescription2 VARCHAR(100),
    DepartureDelayCode3 VARCHAR(10),
    DepartureDelayTime3 INT,
    DepartureDelayDescription3 VARCHAR(100),
    OriginalArrivalStationIATA VARCHAR(10),
    OriginalArrivalStationICAO VARCHAR(10)
);
"""
cursor.execute(create_table_query)
# Inserting data into the table
for flight in flights_delay_info:
    insert_query = """
    INSERT INTO flight_delays (
        FlightCode, Airline, FlightNumber, FlightIdDate,
        ArrivalStationIATA, ArrivalStationICAO,
        ActualArrivalTime, ScheduledArrivalTime,
        DepartureStationIATA, DepartureStationICAO,
        ActualDepartureTime, ScheduledDepartureTime,
        DepartureDelayCode1, DepartureDelayTime1, DepartureDelayDescription1,
        DepartureDelayCode2, DepartureDelayTime2, DepartureDelayDescription2,
        DepartureDelayCode3, DepartureDelayTime3, DepartureDelayDescription3,
        OriginalArrivalStationIATA, OriginalArrivalStationICAO
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    values = (
        flight['FlightCode'], flight['Airline'], flight['FlightNumber'], flight['FlightIdDate'],
        flight['ArrivalStationIATA'], flight['ArrivalStationICAO'],
        flight['ActualArrivalTime'], flight['ScheduledArrivalTime'],
        flight['DepartureStationIATA'], flight['DepartureStationICAO'],
        flight['ActualDepartureTime'], flight['ScheduledDepartureTime'],
        flight['DepartureDelayCode1'], flight['DepartureDelayTime1'], flight['DepartureDelayDescription1'],
        flight['DepartureDelayCode2'], flight['DepartureDelayTime2'], flight['DepartureDelayDescription2'],
        flight['DepartureDelayCode3'], flight['DepartureDelayTime3'], flight['DepartureDelayDescription3'],
        flight['OriginalArrivalStationIATA'], flight['OriginalArrivalStationICAO']
    )
    cursor.execute(insert_query, values)

# Commiting changes and closing connection
conn.commit()
conn.close()

print("Table 'Flightdelays' created successfully and data inserted.")

