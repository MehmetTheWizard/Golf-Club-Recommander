import math
import streamlit as st

# Define the distances for each golf club in yards
clubDistances = {
    "Driver": 270,
    "3-hybrid": 240,
    "4-iron": 200,
    "5-iron": 190,
    "6-iron": 180,
    "7-iron": 170,
    "8-iron": 160,
    "9-iron": 150,
    "Pitching wedge": 140,
    "Approach wedge": 130,
    "Sand wedge": 120,
    "Lob wedge": 100
}

# Define a function to convert wind direction string to degrees
def get_wind_degrees(wind_direction):
    # Dictionary to map wind direction strings to degrees
    directions = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
    # Return the corresponding degree value for the input wind direction string
    return directions.get(wind_direction.upper())

# Define the main function that recommends a golf club based on input parameters
def recommend_club(distance, wind_speed, wind_direction, slope_degrees, flag_color):
    # Validate inputs
    if distance is None or distance < 0 or wind_speed < 0 or slope_degrees < -40 or slope_degrees > 40:
        return "Invalid input values. Please check your inputs."
    
    # Calculate the actual distance taking into account wind and slope
    wind_degrees = get_wind_degrees(wind_direction)
    wind_effect = wind_speed * math.sin(math.radians(wind_degrees))
    slope_effect = distance * math.tan(math.radians(slope_degrees))
    actual_distance = distance + wind_effect + slope_effect
    
    # Find the club with the closest distance to the actual distance
    closest_distance = float("inf")
    closest_club = ""
    for club, club_distance in clubDistances.items():
        distance_diff = abs(club_distance - actual_distance)
        if distance_diff < closest_distance:
            closest_distance = distance_diff
            closest_club = club
    
    # Return the recommended club and flag explanation as a string
    flag_explanation = ""
    if flag_color == "Red":
        flag_explanation = "A red flag indicates the hole is at the front of the green."
    elif flag_color == "Blue":
        flag_explanation = "A blue flag denotes the pin is at the back of the green."
    elif flag_color == "Yellow":
        flag_explanation = "A yellow flag shows the pin position is at the back of the green."
    elif flag_color == "White":
        flag_explanation = "A white flag signals the hole position is in the middle of the green."
    
    return closest_club, flag_explanation

# Set up the Streamlit app
st.title("Golf Club Recommender")
st.markdown("Enter the distance, wind speed, wind direction, slope, and flag color to get a recommendation for which golf club to use.")

# Add two columns for data input
col1, col2 = st.beta_columns(2)

# Add input fields for distance, wind speed, wind direction, and flag color in the first column
distance = col1.number_input("Distance (yards)", min_value=0)
wind_speed = col1.number_input("Wind Speed (km/h)", min_value=0)
wind_direction = col1.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
flag_color = col1.selectbox("Flag Color", ["Red", "Blue", "Yellow", "White"])

# Add a box for the slope input in the second column
slope_degrees = col2.number_input("Slope (degrees)", min_value=-40, max_value=40, value=0)

# Add a button to trigger the recommendation function
if st.button("Recommend Club"):
    # Call the recommend_club function with the input values and display the recommended club
    club, explanation = recommend_club(distance, wind_speed, wind_direction, slope_degrees, flag_color)
    if "Invalid input values" in club:
        st.error(club)
    else:
        st.success(f"Recommended club: {club}")
        st.info(explanation)
