import python_weather  # Import the python_weather library to fetch weather information
import asyncio  # For handling asynchronous tasks
import os  # For working with system paths (not used directly in this code)

async def fetch_weather(location: str):
    """Fetch weather information asynchronously."""
    # Create an asynchronous weather client instance using the python_weather library
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        
        # Fetch the weather forecast for the given location
        forecast = await client.get(location)  # Ensure that the API call is awaited for the result

        # Get the daily forecast for today (index 0 for today's forecast)
        today = forecast.daily_forecasts[0]  
        
        # Initialize an empty list to store the weather information
        result = []

        # Add general weather details (location, country, temperature, and sunlight)
        result.append(f"Today's Weather in {forecast.location}, {forecast.country}:")
        result.append(f"- The date is {today.date}.")
        result.append(f"- The highest temperature today will be {today.highest_temperature}°C.")
        result.append(f"- The lowest temperature today will be {today.lowest_temperature}°C.")
        result.append(f"- Average temperature: {today.temperature}°C.")
        result.append(f"- Hours of sunlight: {today.sunlight:.2f} hours.")

        # Predict rain chances and the hour with the highest likelihood of rain
        rain_forecast = False
        highest_chance_of_rain = 0
        estimated_rain_hour = None

        # Loop through hourly forecasts to determine if there's a rain forecast
        for hourly in today.hourly_forecasts:
            if hourly.chances_of_rain > highest_chance_of_rain:
                highest_chance_of_rain = hourly.chances_of_rain  # Update the highest chance of rain
                estimated_rain_hour = hourly.time  # Update the estimated time of rain
                rain_forecast = True  # Mark that rain is expected

        # If rain is forecasted, add the details to the result
        if rain_forecast:
            result.append(f"Rain is most likely around {estimated_rain_hour}, with a {highest_chance_of_rain}% chance of rain.")
        else:
            result.append("No significant rain expected in the upcoming hours.")

        # Join the list of weather details into a single string with line breaks and return it
        return "\n".join(result)

async def get_weather(location: str):
    """Run the asynchronous fetch_weather function synchronously."""
    # Use asyncio.run to run the async fetch_weather function in a synchronous context
    return asyncio.run(fetch_weather(location))
