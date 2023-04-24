# Import the necessary modules
import math
import streamlit as st
import csv
import time
import os.path

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
def recommend_club(distance, wind_speed, wind_direction, slope_degrees):
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
    
    # Return the recommended club as a string
    return closest_club

# Set up the Streamlit app
st.title("Golf Club Recommender")
st.markdown("Enter the distance, wind speed, wind direction, and slope to get a recommendation for which golf club to use.")

# Add input fields for distance, wind speed, wind direction, and slope
distance = st.number_input("Distance (yards)", min_value=0)
wind_speed = st.number_input("Wind Speed (mph)", min_value=0)
wind_direction = st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
slope_degrees = st.slider("Slope (degrees)", min_value=-90, max_value=90)

# Add a button to trigger the recommendation function
if st.button("Recommend Club"):
    # Call the recommend_club function with the input values and display the recommended club
    club = recommend_club(distance, wind_speed, wind_direction, slope_degrees)
    if "Invalid input values" in club:
        st.error(club)
    else:
        st.success(f"Recommended club: {club}")

# Define the path and filename for the log file
log_path = "logs/"
log_filename = "golf_club_recommender_logs.csv"

# Create the logs directory if it doesn't exist
if not os.path.exists(log_path):
    os.makedirs(log_path)

# Define the header for the log file
header = ["timestamp", "ip_address", "distance", "wind_speed", "wind_direction", "slope_degrees"]

# Create the log file if it doesn't exist
if not os.path.isfile(log_path + log_filename):
    with open(log_path + log_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

# Get the user's IP address
user_ip = st.request_headers["X-Forwarded-For"]

# Get the current timestamp in ISO format
timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

# Write the user's input values to the log file
with open(log_path + log_filename, "a+", newline="") as f:
    writer = csv.writer(f)
    
    # Check if the file is empty, and write the header row if necessary
    f.seek(0)
    first_char = f.read(1)
    if not first_char:
        writer.writerow(header)
        
    writer.writerow([timestamp, user_ip, distance, wind_speed, wind_direction, slope_degrees])

