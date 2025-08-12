
# from smolagents import (
#    CodeAgent,
#    ToolCallingAgent,
# #    ManagedAgent,
#    DuckDuckGoSearchTool,
#    VisitWebpageTool,
# #    HfApiModel,
#    InferenceClientModel,
# )
# from smolagents import LiteLLMModel 
import os

# # model = LiteLLMModel(model_id="meta-llama/Llama-3.2-3B-Instruct")
# # # hfModel = InferenceClientModel(model_id="meta-llama/Llama-3.2-3B-Instruct", token=os.getenv("HF_API_KEY"))
# hfModel = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-7B-Instruct", token=os.getenv("HF_API_KEY"))

# # agent = ToolCallingAgent(
# #     tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
# #     model=hfModel,
# #     add_base_tools=True
# # )


# # result = agent.run("fetch the share price of google from 2020 to 2024, and create a line graph from it?")

# # print(result)


# agent = CodeAgent(
#     tools=[DuckDuckGoSearchTool()],
#     model=hfModel
# )

# # Execute a search query
# response = agent.run("best music for a party")
# print(response)

from typing import Optional
from smolagents import CodeAgent, InferenceClientModel, tool


from dotenv import load_dotenv
load_dotenv()

@tool
def get_travel_duration(start_location: str, destination_location: str, transportation_mode: Optional[str] = None) -> str:
    """Gets the travel time between two places.

    Args:
        start_location: the place from which you start your ride
        destination_location: the place of arrival
        transportation_mode: The transportation mode, in 'driving', 'walking', 'bicycling', or 'transit'. Defaults to 'driving'.
    """
    import os  
    import googlemaps
    from datetime import datetime

    gmaps = googlemaps.Client(os.getenv("GMAPS_API_KEY"))

    if transportation_mode is None:
        transportation_mode = "driving"
    try:
        directions_result = gmaps.directions(
            start_location,
            destination_location,
            mode=transportation_mode,
            departure_time=datetime(2025, 6, 6, 11, 0), # At 11, date far in the future
        )
        if len(directions_result) == 0:
            return "No way found between these places with the required transportation mode."
        return directions_result[0]["legs"][0]["duration"]["text"]
    except Exception as e:
        print(e)
        return e
    
hfModel = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-7B-Instruct", token=os.getenv("HF_API_KEY"))

agent = CodeAgent(tools=[get_travel_duration], model=hfModel, additional_authorized_imports=["datetime"])

agent.run("Can you give me a nice one-day trip around Paris with a few locations and the times? Could be in the city or outside, but should fit in one day. I'm travelling only with a rented bicycle.")
