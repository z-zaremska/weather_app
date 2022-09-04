from django.shortcuts import render

def home(request):
    import json
    import requests

    category_settings = {
        '1': ["#0C0", "Current Air Quality is the most recent air quality in your area. It's updated hourly. Check your current air quality to see if now is a good time for outdoor activities."],
        '2': ['#FFFF00', "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."],
        '3': ['#FF9900', "Members of sensitive groups may experience health effects. The general public is less likely to be affected."],
        '4': ['#FF0000', "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."],
        '5': ['#990066', "Health alert: The risk of health effects is increased for everyone."],
        '6': ['#660000', "Health warning of emergency conditions: everyone is more likely to be affected."],
        }

    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')  
        url = f'https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zipcode}&distance=5&API_KEY=9332FC10-36D2-47FB-A794-D0D655706A0A'
        api_request = requests.get(url)
        
        try:
            api = json.loads(api_request.content)
            category_number = str(api[0]['Category']['Number'])
            if category_number in category_settings.keys():
                status_color = category_settings[category_number][0]
                status_description = category_settings[category_number][1]
            return render(request, 'home_air_quality.html', {
            'api': api,
            'zipcode': zipcode,
            'status_color': status_color,
            'status_description': status_description,})

        except Exception as e:
            api = "Error"
            return render(request, 'home_air_quality.html', {'api': api, 'zipcode': zipcode})



        