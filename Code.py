import math
import streamlit as st

# Define the distances for each golf club in yards
clubDistances = {
    "Driver": 230,
    "3-wood": 210,
    "5-wood": 180,
    "3-iron": 170,
    "4-iron": 160,
    "5-iron": 150,
    "6-iron": 140,
    "7-iron": 130,
    "8-iron": 120,
    "9-iron": 110,
    "Pitching wedge": 100,
    "Sand wedge": 80,
    "Lob wedge": 60
}

def get_wind_degrees(wind_direction):
    if wind_direction == "N":
        return 0
    elif wind_direction == "S":
        return 180
    elif wind_direction == "E":
        return 90
    elif wind_direction == "W":
        return 270

def recommend_club(distance, wind_speed, wind_direction, slope):
    # Calculate actual distance taking into account wind and slope
    wind_degrees = get_wind_degrees(wind_direction)
    wind_effect = wind_speed * math.sin(math.radians(wind_degrees))
    slope_effect = slope / 4 # estimate of distance change per degree of slope
    actual_distance = distance + wind_effect + slope_effect

    # Find the club with the closest distance to the actual distance
    closest_distance = float("inf")
    closest_club = ""
    for club, club_distance in clubDistances.items():
        distance_diff = abs(club_distance - actual_distance)
        if distance_diff < closest_distance:
            closest_distance = distance_diff
            closest_club = club

    # Return the recommended club as a string
    return closest_club

# Set up the Streamlit app
st.title("Golf Club Recommender")
st.markdown("Enter the distance, wind speed, wind direction, and slope to get a recommendation for which golf club to use.")

distance = st.number_input("Distance (yards)")
wind_speed = st.number_input("Wind Speed (mph)")
wind_direction = st.selectbox("Wind Direction", ["N", "S", "E", "W"])
slope = st.number_input("Slope (degrees)")

if st.button("Recommend Club"):
    club = recommend_club(distance, wind_speed, wind_direction, slope)
    st.success(f"Recommended club: {club}")
