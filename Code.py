# Import the necessary modules
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
def recommend_club(distance, wind_speed, wind_direction, slope_degrees, flag_color):
    # Validate inputs
    if distance < 0 or wind_speed < 0 or slope_degrees < -90 or slope_degrees > 90:
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
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

# Configure the app for mobile use
st.beta_set_page_config(
    page_title="Golf Club Recommender",
    layout="centered",
    initial_sidebar_state="auto"
)

# Add a title and description
st.title("Golf Club Recommender")
st.markdown("Enter the distance, wind speed, wind direction, slope, and flag color to get a recommendation for which golf club to use.")

# Add input fields for distance, wind speed, wind direction, slope, and flag color
col1, col2 = st.beta_columns(2)
with col1:
    distance = st.number_input("Distance (yards)", min_value=0)
    wind_speed = st.number_input("Wind Speed (mph)", min_value=0)
    wind_direction = st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
with col2:
    slope_degrees = st.slider("Slope (degrees)", min_value=-90, max_value=90)
    flag_color = st.selectbox("Flag Color", ["Red", "Blue", "Yellow", "White"])

# Add a button to trigger the recommendation function
st.button("Recommend Club", key="recommend_button")

# Call the recommend_club function with the input values and display the recommended club and flag explanation
club, explanation = recommend_club(distance, wind_speed, wind_direction, slope_degrees, flag_color)
if "Invalid input values" in club:
    st.error(club)
else:
    st.success(f"Recommended club: {club}")
    st.info(explanation)
