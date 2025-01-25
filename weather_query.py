import python_weather
import asyncio
import os

async def fetch_weather(location: str):
  """Fetch weather information asynchronously."""
  async with python_weather.Client(unit=python_weather.METRIC) as client:
      forecast = await client.get(location)  # Ensure this is awaited
      today = forecast.daily_forecasts[0]  # Access daily forecasts
      result = []

      result.append(f"Today's Weather in {forecast.location}, {forecast.country}:")
      result.append(f"- The date is {today.date}.")
      result.append(f"- The highest temperature today will be {today.highest_temperature}°C.")
      result.append(f"- The lowest temperature today will be {today.lowest_temperature}°C.")
      result.append(f"- Average temperature: {today.temperature}°C.")
      result.append(f"- Hours of sunlight: {today.sunlight:.2f} hours.")

      # Predict rain chances
      rain_forecast = False
      highest_chance_of_rain = 0
      estimated_rain_hour = None

      for hourly in today.hourly_forecasts:
        if hourly.chances_of_rain > highest_chance_of_rain:
          highest_chance_of_rain = hourly.chances_of_rain
          estimated_rain_hour = hourly.time
          rain_forecast = True

      if rain_forecast:
        result.append(f"Rain is most likely around {estimated_rain_hour}, with a {highest_chance_of_rain}% chance of rain.")
      else:
        result.append("No significant rain expected in the upcoming hours.")

      return "\n".join(result)

async def get_weather(location:str):
  """Run the asynchronous fetch_weather function synchronously."""
  return asyncio.run(fetch_weather(location))