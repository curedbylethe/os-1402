class City:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return self.name

    def __repr__(self):
        return "City('" + self.name + "', " + str(self.lat) + ", " + str(self.lon) + ")"

    def __getitem__(self, item):
        if item == 'name':
            return self.name
        elif item == 'lat':
            return self.lat
        elif item == 'lon':
            return self.lon
        else:
            raise KeyError("Invalid key: " + item)

    def fetch_weather(self) -> str:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key: str = os.environ['API_KEY']
        url: str = "https://api.openweathermap.org/data/2.5/weather?"
        import requests
        import json

        # get the weather data
        response = requests.get(
            url + f"lat={self['lat']}&lon={self['lon']}&appid={api_key}&units=metric")
        data = json.loads(response.text)

        # get the current weather
        weather = data['weather'][0]['main']
        current_weather = data['main']
        current_temp = current_weather['temp']
        current_min_temp = current_weather['temp_min']
        current_max_temp = current_weather['temp_max']
        current_feels_like = current_weather['feels_like']
        current_weather_description = data['weather'][0]['description']
        current_weather_icon = data['weather'][0]['icon']

        return (f"Current weather in {self['name']}: \n"
                f"Weather: {weather}\n"
                f"Temperature: {current_temp}°C "
                f"with min: {current_min_temp}°C and max: {current_max_temp}°C\n"
                f"Feels like: {current_feels_like}°C\n"
                f"Description: {current_weather_description}\n"
                f"Icon: {current_weather_icon}\n")
