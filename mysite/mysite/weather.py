import requests
from django.http import JsonResponse
from django.views import View
import os
from dotenv import load_dotenv

load_dotenv()



class WeatherDataView(View):
    def get(self, request, *args, **kwargs):
        user_ip = self.get_client_ip(request)
        location = self.get_location_from_ip(user_ip)
        weather_data = self.get_weather_data(location['lat'], location['lon'])
        return JsonResponse(weather_data)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(f'if{ip}')
        else:
            ip = request.META.get('REMOTE_ADDR')
            print(f'else{ip}')
        return ip

    @staticmethod
    def get_location_from_ip(ip):
        try:
            response = requests.get(f'https://ipinfo.io/{ip}/json')
            data = response.json()
            print(data)
            # The location data is in "loc" key and the value is in 'latitude,longitude' format
            location_data = data.get('loc', '0,0').split(',')
            location = {"lat": location_data[0], "lon": location_data[1]}
        except Exception as e:
            # If the request fails, set a default location
            location = {"lat": "0", "lon": "0"}

        return location


    @staticmethod
    def get_weather_data(lat, lon):
        api_key = os.environ.get('WEATHER_API_KEY')
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        )
        return weather_response.json()
