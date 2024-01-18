"""Multithreading fetch of City weather data"""

import concurrent.futures
from HW1.cities import cities


def fetch():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(lambda city: city.fetch_weather(), cities)
        for result in results:
            print(result)
