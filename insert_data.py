import requests
import json
import uuid

# URLs of the JSON data
json_url_dataset1 = "https://challange.usecosmos.cloud/flight_schedules.json"
json_url_dataset2 = "https://challange.usecosmos.cloud/flight_delays.json"

def fetch_flight_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()

def extract_flight_details(data):
    flights = data.get('FlightStatusResource', {}).get('Flights', {}).get('Flight', [])
    flight_details = []

    for flight in flights:
        departure = flight.get('Departure', {})
        arrival = flight.get('Arrival', {})
        flight_status = flight.get('FlightStatus', {})

        detail = {
            "FlightCode": flight.get('OperatingFlight', {}).get('flightCode', 'N/A'),
            "FlightIdDate": flight.get('OperatingFlight', {}).get('FlightIdDate', 'N/A'),
            "Departure Airport Code": departure.get('AirportCode', 'N/A'),
            "Departure Scheduled Time (Local)": departure.get('ScheduledTimeLocal', {}).get('DateTime', 'N/A'),
            "Arrival Airport Code": arrival.get('AirportCode', 'N/A'),
            "Arrival Scheduled Time (Local)": arrival.get('ScheduledTimeLocal', {}).get('DateTime', 'N/A'),
            "Actual Departure Time": departure.get('ActualTimeLocal', {}).get('DateTime', 'N/A'),
            "Flight Status": {
                "Code": flight_status.get('Code', 'N/A'),
                "Definition": flight_status.get('Definition', 'N/A')
            }
        }
        flight_details.append(detail)

    return flight_details

def extract_delay_details(data):
    delay_details = []

    if isinstance(data, list):
        for item in data:
            flights = item.get('FlightDelaysResource', {}).get('Flights', {}).get('Flight', [])
            for flight in flights:
                departure = flight.get('Departure', {})
                delays = departure.get('Delay', [])
                delay_list = []

                for delay in delays:
                    delay_detail = {
                        "code": delay.get('Code', 'N/A'),
                        "time_minutes": delay.get('DelayTime', 'N/A'),
                        "description": delay.get('Description', 'N/A')
                    }
                    delay_list.append(delay_detail)

                detail = {
                    "FlightCode": flight.get('OperatingFlight', {}).get('flightCode', 'N/A'),
                    "FlightIdDate": flight.get('OperatingFlight', {}).get('FlightIdDate', 'N/A'),
                    "Delays": delay_list
                }
                delay_details.append(detail)
    else:
        flights = data.get('FlightDelaysResource', {}).get('Flights', {}).get('Flight', [])
        for flight in flights:
            departure = flight.get('Departure', {})
            delays = departure.get('Delay', [])
            delay_list = []

            for delay in delays:
                delay_detail = {
                    "code": delay.get('Code', 'N/A'),
                    "time_minutes": delay.get('DelayTime', 'N/A'),
                    "description": delay.get('Description', 'N/A')
                }
                delay_list.append(delay_detail)

            detail = {
                "FlightCode": flight.get('OperatingFlight', {}).get('flightCode', 'N/A'),
                "FlightIdDate": flight.get('OperatingFlight', {}).get('FlightIdDate', 'N/A'),
                "Delays": delay_list
            }
            delay_details.append(detail)

    return delay_details

def find_common_flights(schedule_details, delay_details):
    common_flights = []

    for schedule in schedule_details:
        for delay in delay_details:
            if schedule["FlightCode"] == delay["FlightCode"] and schedule["FlightIdDate"] == delay["FlightIdDate"]:
                common_flight = {
                    "id": str(uuid.uuid4()),
                    "flight_number": schedule["FlightCode"],
                    "airline": schedule["FlightCode"][:2],
                    "origin": schedule["Departure Airport Code"],
                    "destination": schedule["Arrival Airport Code"],
                    "scheduled_departure_at": schedule["Departure Scheduled Time (Local)"],
                    "actual_departure_at": schedule["Actual Departure Time"],
                    "delays": delay["Delays"]
                }
                common_flights.append(common_flight)

    return common_flights

def main():
    data1 = fetch_flight_data(json_url_dataset1)
    data2 = fetch_flight_data(json_url_dataset2)
    
    schedule_details = extract_flight_details(data1)
    delay_details = extract_delay_details(data2)

    common_flights = find_common_flights(schedule_details, delay_details)

    for flight in common_flights:
        print(json.dumps(flight, indent=4))
    
    try:
        data1 = fetch_flight_data(json_url_dataset1)
        print("Fetched data from json_url_dataset1 successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from json_url_dataset1: {e}")
        return
    
    
    try:
        data1 = fetch_flight_data(json_url_dataset1)
        print("Fetched data from json_url_dataset1 successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from json_url_dataset1: {e}")
        return
    
    try:
        data2 = fetch_flight_data(json_url_dataset2)
        print("Fetched data from json_url_dataset2 successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from json_url_dataset2: {e}")
        return
    
    schedule_details = extract_flight_details(data1)
    print(f"Extracted {len(schedule_details)} flight details from dataset1")
    
    delay_details = extract_delay_details(data2)
    print(f"Extracted {len(delay_details)} delay details from dataset2")
    
    common_flights = find_common_flights(schedule_details, delay_details)
    print(f"Found {len(common_flights)} common flights")
    
    for flight in common_flights:
        print(json.dumps(flight, indent=4))

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()














########shedule
# Connect to SQLite database (or create it if it doesn't exist)

