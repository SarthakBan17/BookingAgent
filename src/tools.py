import datetime
from collections import defaultdict
from typing import Callable

from langchain_core.runnables import RunnableConfig
from langgraph_swarm import create_handoff_tool

from prompts import location_assistant_prompt, flight_assistant_prompt, hotel_assistant_prompt

# Mock data for tools
RESERVATIONS = defaultdict(lambda: {"location_info": {},"flight_info": {}, "hotel_info": {}})
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
LOCATIONS = [
    {
        "name": "New York",
        "country": "United States",
        "popularity": 9,
        "id": "1",
    },
    {
        "name": "Los Angeles",
        "country": "United States",
        "popularity": 6,
        "id": "2",
    }
]
FLIGHTS = [
    {
        "departure_airport": "BOS",
        "arrival_airport": "JFK",
        "airline": "Jet Blue",
        "date": TOMORROW,
        "id": "1",
    }
]
HOTELS = [
    {
        "location": "New York",
        "name": "McKittrick Hotel",
        "neighborhood": "Chelsea",
        "id": "1",
    }
]

def search_locations(
    name: str
) -> list[dict]:
    """Search locations.

    Args:
        name: offical, legal city name (proper noun)
        country: country name (proper noun)
        popularity: 1-10 scale of popularity, where 10 is the most popular
    """
    # return all locations for simplicity
    return LOCATIONS

def book_locations(
    location_id: str,
    config: RunnableConfig,
) -> str:
    """Book a flight."""
    user_id = config["configurable"].get("user_id")
    location = [location for location in LOCATIONS if location["id"] == location_id][0]
    RESERVATIONS[user_id]["location_info"] = location
    return "Successfully booked location"


# Flight tools
def search_flights(
    departure_airport: str,
    arrival_airport: str,
    date: str,
) -> list[dict]:
    """Search flights.

    Args:
        departure_airport: 3-letter airport code for the departure airport. If unsure, use the biggest airport in the area
        arrival_airport: 3-letter airport code for the arrival airport. If unsure, use the biggest airport in the area
        date: YYYY-MM-DD date
    """
    # return all flights for simplicity
    return FLIGHTS


def book_flight(
    flight_id: str,
    config: RunnableConfig,
) -> str:
    """Book a flight."""
    user_id = config["configurable"].get("user_id")
    flight = [flight for flight in FLIGHTS if flight["id"] == flight_id][0]
    RESERVATIONS[user_id]["flight_info"] = flight
    return "Successfully booked flight"


# Hotel tools
def search_hotels(location: str) -> list[dict]:
    """Search hotels.

    Args:
        location: offical, legal city name (proper noun)
    """
    # return all hotels for simplicity
    return HOTELS


def book_hotel(
    hotel_id: str,
    config: RunnableConfig,
) -> str:
    """Book a hotel"""
    user_id = config["configurable"].get("user_id")
    hotel = [hotel for hotel in HOTELS if hotel["id"] == hotel_id][0]
    RESERVATIONS[user_id]["hotel_info"] = hotel
    return "Successfully booked hotel"

# Define handoff tools
transfer_to_hotel_assistant = create_handoff_tool(
    agent_name="hotel_assistant",
    description="Transfer user to the hotel-booking assistant that can search for and book hotels.",
)
transfer_to_flight_assistant = create_handoff_tool(
    agent_name="flight_assistant",
    description="Transfer user to the flight-booking assistant that can search for and book flights.",
)
transfer_to_location_assistant = create_handoff_tool(
    agent_name="location_assistant",
    description="Transfer user to the location-searching assistant that can search for and book locations.",
)

def create_prompt_location(state: dict, config: RunnableConfig):
    return [
        {
            "role": "system", 
            "content": location_assistant_prompt.format(
                current_reservation=RESERVATIONS[config["configurable"].get("user_id")], 
                datetime=datetime.datetime.now()
            )
        }
    ] + state['messages']

def create_prompt_flight(state: dict, config: RunnableConfig):
    return [
        {
            "role": "system", 
            "content": flight_assistant_prompt.format(
                current_reservation=RESERVATIONS[config["configurable"].get("user_id")], 
                datetime=datetime.datetime.now()
            )
        }
    ] + state['messages']


def create_prompt_hotel(state: dict, config: RunnableConfig):
    return [
        {
            "role": "system", 
            "content": hotel_assistant_prompt.format(
                current_reservation=RESERVATIONS[config["configurable"].get("user_id")], 
                datetime=datetime.datetime.now()
            )
        }
    ] + state['messages']