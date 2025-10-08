"""
Tutorial 05: Parallel Processing - Travel Planning System

This tutorial demonstrates how to use ParallelAgent for concurrent execution
and the fan-out/gather pattern. The travel planner searches for flights, hotels,
and activities in parallel, then merges the results into a complete itinerary.
"""

from __future__ import annotations

from google.adk.agents import Agent, ParallelAgent, SequentialAgent

# ============================================================================
# PARALLEL SEARCH AGENTS
# ============================================================================

# ===== Parallel Branch 1: Flight Finder =====
flight_finder = Agent(
    name="flight_finder",
    model="gemini-2.0-flash",
    description="Searches for available flights",
    instruction=(
        "You are a flight search specialist. Based on the user's travel request, "
        "search for available flights.\n"
        "\n"
        "Provide 2-3 flight options with:\n"
        "- Airline name\n"
        "- Departure and arrival times\n"
        "- Price range\n"
        "- Flight duration\n"
        "\n"
        "Format as a bulleted list. Be specific and realistic."
    ),
    output_key="flight_options"  # Saves to state
)

# ===== Parallel Branch 2: Hotel Finder =====
hotel_finder = Agent(
    name="hotel_finder",
    model="gemini-2.0-flash",
    description="Searches for available hotels",
    instruction=(
        "You are a hotel search specialist. Based on the user's travel request, "
        "find suitable hotels.\n"
        "\n"
        "Provide 2-3 hotel options with:\n"
        "- Hotel name and rating\n"
        "- Location (district/area)\n"
        "- Price per night\n"
        "- Key amenities\n"
        "\n"
        "Format as a bulleted list. Be specific and realistic."
    ),
    output_key="hotel_options"  # Saves to state
)

# ===== Parallel Branch 3: Activity Finder =====
activity_finder = Agent(
    name="activity_finder",
    model="gemini-2.0-flash",
    description="Finds activities and attractions",
    instruction=(
        "You are a local activities expert. Based on the user's travel request, "
        "recommend activities and attractions.\n"
        "\n"
        "Provide 4-5 activity suggestions with:\n"
        "- Activity name\n"
        "- Description (1 sentence)\n"
        "- Estimated duration\n"
        "- Estimated cost\n"
        "\n"
        "Format as a bulleted list. Include mix of paid/free activities."
    ),
    output_key="activity_options"  # Saves to state
)

# ============================================================================
# FAN-OUT: PARALLEL DATA GATHERING
# ============================================================================

# Create the ParallelAgent for concurrent search
parallel_search = ParallelAgent(
    name="ParallelSearch",
    sub_agents=[
        flight_finder,
        hotel_finder,
        activity_finder
    ],  # All run AT THE SAME TIME!
    description="Searches flights, hotels, and activities concurrently"
)

# ============================================================================
# GATHER: SEQUENTIAL RESULT MERGING
# ============================================================================

# ===== Gather: Merge Results into Itinerary =====
itinerary_builder = Agent(
    name="itinerary_builder",
    model="gemini-2.0-flash",
    description="Combines all search results into a complete travel itinerary",
    instruction=(
        "You are a travel planner. Create a complete, well-organized itinerary "
        "by combining the search results below.\n"
        "\n"
        "**Available Flights:**\n"
        "{flight_options}\n"  # Reads from state!
        "\n"
        "**Available Hotels:**\n"
        "{hotel_options}\n"  # Reads from state!
        "\n"
        "**Recommended Activities:**\n"
        "{activity_options}\n"  # Reads from state!
        "\n"
        "Create a formatted itinerary that:\n"
        "1. Recommends the BEST option from each category (flights, hotel)\n"
        "2. Organizes activities into a day-by-day plan\n"
        "3. Includes estimated total cost\n"
        "4. Adds helpful travel tips\n"
        "\n"
        "Format beautifully with clear sections and markdown."
    ),
    output_key="final_itinerary"
)

# ============================================================================
# COMPLETE FAN-OUT/GATHER PIPELINE
# ============================================================================

# Combine parallel search with sequential merge
travel_planning_system = SequentialAgent(
    name="TravelPlanningSystem",
    sub_agents=[
        parallel_search,     # Step 1: Gather data in parallel (FAST!)
        itinerary_builder    # Step 2: Merge results (synthesis)
    ],
    description="Complete travel planning system with parallel search and itinerary building"
)

# MUST be named root_agent for ADK discovery
root_agent = travel_planning_system