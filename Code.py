import math
import streamlit as st

# Define the distances for each golf club in yards
clubDistances = {
    "Driver": 290,
    "3 hybrid": 210,
    "4": 200,
    "5": 190,
    "6": 180,
    "7": 170,
    "8": 160,
    "9": 150,
    "54": (135, "Sand wedge"),
    "56": (115, "Lob wedge"),
    "60": (100, "Lob wedge")
}

# Define a function to convert wind direction in km/h to degrees
def get_wind_degrees(wind_direction):
    # Dictionary to map wind direction strings to degrees
    directions = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
    # Return the corresponding degree value for the input wind direction string
    return directions.get(wind_direction.upper())

# Define the main function that recommends a golf club based on input parameters
def recommend_club(distance, wind_speed, wind_direction):
    # Validate inputs
    if distance < 0 or wind_speed < 0:
        return "Invalid input values. Please check your inputs."
    
    # Convert wind direction from km/h to degrees
    wind_degrees = get_wind_degrees(wind_direction)
    
    # Adjust distance based on wind speed and direction
    adjusted_distance = distance + (wind_speed * math.sin(math.radians(wind_degrees)))
    
    # Find the club with the closest distance to the adjusted distance
    closest_distance = float("inf")
    closest_club = ""
    for club, club_data in clubDistances.items():
        if isinstance(club_data, tuple):  # Check if it's a wedge
            club_distance, club_name = club_data
        else:
            club_distance = club_data
            club_name = club
        distance_diff = abs(club_distance - adjusted_distance)
        if distance_diff < closest_distance:
            closest_distance = distance_diff
            closest_club = f"{club_name} ({club_distance} yards)"
    
    return closest_club

# Set up the Streamlit app
st.title("Golf Club Recommender")
st.markdown("Enter the distance you want to hit from the start, wind speed in km/h, and wind direction to get a recommendation for the right golf club to use.")

# Add input fields for distance, wind speed, and wind direction
distance = st.number_input("Distance to Hit (yards)", min_value=0)
wind_speed = st.number_input("Wind Speed (km/h)", min_value=0)
wind_direction = st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])

# Add a button to trigger the recommendation function
if st.button("Recommend Club"):
    # Call the recommend_club function with the input values and display the recommended club
    club = recommend_club(distance, wind_speed, wind_direction)
    if "Invalid input values" in club:
        st.error(club)
    else:
        st.success(f"Recommended Club: {club}")
