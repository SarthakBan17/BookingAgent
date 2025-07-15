import datetime
from collections import defaultdict
from typing import Callable

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import search_flights, book_flight, search_hotels, book_hotel, transfer_to_hotel_assistant, transfer_to_flight_assistant, create_prompt_flight, create_prompt_hotel
from tools import search_locations, book_locations, transfer_to_location_assistant, create_prompt_location

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20")

location_assistant = create_react_agent(
    model,
    [search_locations, book_locations, transfer_to_hotel_assistant, transfer_to_flight_assistant],
    prompt=create_prompt_location,
    name="location_assistant",
)

flight_assistant = create_react_agent(
    model,
    [search_flights, book_flight, transfer_to_hotel_assistant, transfer_to_location_assistant],
    prompt=create_prompt_flight,
    name="flight_assistant",
)

hotel_assistant = create_react_agent(
    model,
    [search_hotels, book_hotel, transfer_to_flight_assistant, transfer_to_location_assistant],
    prompt=create_prompt_hotel,
    name="hotel_assistant",
)