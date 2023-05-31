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
    if distance is None or distance < 0 or wind_speed < 0 or slope_degrees < -30 or slope_degrees > 30:
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
    
    # Calculate the iron or wedge to use based on the flag color and distance
    club_type = calculate_club_type(distance, flag_color)
    if club_type == "Iron":
        iron_to_use = calculate_iron(distance)
        club_to_use = iron_to_use
    else:
        club_to_use = club_type
    
    # Return the recommended club, flag explanation, and club to use as a string
    flag_explanation = get_flag_explanation(flag_color)
    return closest_club, flag_explanation, club_to_use

# Define a function to calculate the iron or wedge to use based on the distance and flag color
def calculate_club_type(distance, flag_color):
    # Wedge distances for each flag color
    wedgeDistances = {
        "Red": (0, 100),
        "Blue": (100, 120),
        "Yellow": (120, 140),
        "White": (140, float("inf"))
    }
    
    # Check if the distance falls within the wedge distances
    for color, (min_distance, max_distance) in wedgeDistances.items():
        if min_distance <= distance < max_distance:
            return "Wedge"
    
    # Return "Iron" if distance doesn't fall within wedge distances
    return "Iron"

# Define a function to calculate the iron to use based on the distance
def calculate_iron(distance):
    # Find the iron that provides the best chance of reaching the green based on distance
    closest_distance = float("inf")
    closest_iron = ""
    for iron, iron_distance in clubDistances.items():
        if "iron" in iron.lower():
            distance_diff = abs(iron_distance - distance)
            if distance_diff < closest_distance:
                closest_distance = distance_diff
                closest_iron = iron
    
    return closest_iron

# Define a function to get the flag explanation based on the flag color
def get_flag_explanation(flag_color):
    # Dictionary to map flag colors to explanations
    flag_explanations = {
        "Red": "A red flag indicates the hole is at the front of the green.",
        "Blue": "A blue flag denotes the pin is at the back of the green.",
        "Yellow": "A yellow flag shows the pin position is at the back of the green.",
        "White": "A white flag signals the hole position is in the middle of the green."
    }
    
    # Return the flag explanation for the given flag color
    return flag_explanations.get(flag_color)

# Set up the Streamlit app
st.title("Golf Club Recommender")
st.markdown("Enter the distance, wind speed, wind direction, slope, and flag color to get a recommendation for which golf club to use.")

# Add input fields for distance, wind speed, wind direction, and slope
distance = st.number_input("Distance (yards)", min_value=0)
wind_speed = st.number_input("Wind Speed (mph)", min_value=0)
wind_direction = st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
slope_degrees = st.number_input("Slope (degrees)", min_value=-30, max_value=30, step=1, format="%d")

# Add input field for flag color
flag_color = st.selectbox("Flag Color", ["Red", "Blue", "Yellow", "White"])

# Add a button to trigger the recommendation function
if st.button("Recommend Club"):
    # Check if the distance field is empty
    if distance == 0:
        st.error("Please enter a valid distance.")
    else:
        # Call the recommend_club function with the input values and display the recommended club, flag explanation, and club to use
        club, explanation, club_to_use = recommend_club(distance, wind_speed, wind_direction, slope_degrees, flag_color)
        if "Invalid input values" in club:
            st.error(club)
        else:
            st.success(f"Recommended club: {club}")
            st.info(explanation)
            st.info(f"Club to use: {club_to_use}")
