from langgraph_swarm import create_swarm
from langgraph.checkpoint.memory import MemorySaver

from agent import flight_assistant, hotel_assistant, location_assistant




checkpointer = MemorySaver()
# Compile and run!
builder = create_swarm(
    [flight_assistant, hotel_assistant, location_assistant], default_active_agent="location_assistant"
)
app = builder.compile(checkpointer=checkpointer)