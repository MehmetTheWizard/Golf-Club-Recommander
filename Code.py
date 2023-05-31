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

# Define a function to convert wind direction string to degrees
def get_wind_degrees(wind_direction):
    # Dictionary to map wind direction strings to degrees
    directions = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
    # Return the corresponding degree value for the input wind direction string
    return directions.get(wind_direction.upper())

# Define the main function that recommends a golf club based on input parameters
def recommend_club(distance, wind_speed, wind_direction, flag_position, rough, sand):
    # Validate inputs
    if distance is None or distance < 0 or wind_speed < 0:
        return "Invalid input values. Please check your inputs."
    
    # Adjust distance based on wind and flag position
    wind_degrees = get_wind_degrees(wind_direction)
    wind_effect = wind_speed * math.sin(math.radians(wind_degrees))
    adjusted_distance = distance + wind_effect + flag_position
    
    # Adjust distance based on rough or sand
    if rough:
        adjusted_distance *= 0.9  # Reduce distance by 10% in rough
    if sand:
        adjusted_distance *= 0.8  # Reduce distance by 20% in sand
    
    # Find the club with the closest distance to the adjusted distance
    closest_distance = float("inf")
    closest_club = ""
    for club, club_distance in clubDistances.items():
        distance_diff = abs(club_distance - adjusted_distance)
        if distance_diff < closest_distance:
            closest_distance = distance_diff
            closest_club = club
    
    return closest_club

# Set up the Streamlit app
st.title("Golf Club Recommender")
st.markdown("Enter the distance, wind speed, wind direction, flag position, rough, and sand to get a recommendation for which golf club to use.")

# Add input fields for distance, wind speed, wind direction, flag position, rough, and sand
distance = st.number_input("Distance (yards)", min_value=0)
wind_speed = st.number_input("Wind Speed (mph)", min_value=0)
wind_direction = st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
flag_position = st.slider("Flag Position", min_value=-10, max_value=10, step=1)
rough = st.checkbox("Rough")
sand = st.checkbox("Sand")

# Add a button to trigger the recommendation function
if st.button("Recommend Club"):
    # Call the recommend_club function with the input values and display the recommended club
    club = recommend_club(distance, wind_speed, wind_direction, flag_position, rough, sand)
    if "Invalid input values" in club:
        st.error(club)
    else:
        st.success(f"Recommended club: {club}")
