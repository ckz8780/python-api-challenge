from rest_framework import generics
from rest_framework import serializers
from django.shortcuts import redirect

# Extra imports 
from apichallenge.settings import BASE_DIR
from datetime import datetime
import requests, os, csv

from .models import Departure

class DepartureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departure
        fields = ('name', 'start_date', 'finish_date', 'category')

class DepartureView(generics.ListAPIView):
    queryset = Departure.objects.all()
    serializer_class = DepartureSerializer

def get_csv(request):
    """
    Builds a CSV w/ the specified filtering and then redirects to API root.
    A much faster way to do this would be to set a limit (eg 9999) as a parameter to the
    function to avoid repeated requests to the API...but that wasn't part
    of the challenge :)
    """

    # Set request URL, date limit and category.
    url = request.build_absolute_uri('/departures/')
    formatter = '%Y-%m-%d'
    limit = datetime.strptime('2018-06-01', formatter)
    category = 'Adventurous'

    # Get first page of results
    response = requests.get(url).json()
    results = response['results']
    next_url = response['next']

    # Repeat until 'next' is None (null).
    while not next_url == None:
        next_response = requests.get(next_url).json()
        next_url = next_response['next']
        results += next_response['results']

    # Now filter results w/ a list comprehension.
    # Convert string dates to datetime objects to make sure math is right. 
    filtered = [result for result in results if result['category'] == category and datetime.strptime(result['start_date'], formatter) > limit]

    # Write CSV.
    # We need to use a custom header row since
    # DictWriter.writeheader() uses literal field names.
    with open(os.path.join(BASE_DIR, 'departures.csv'), 'w', newline='') as f:
        fieldnames = ['name', 'start_date', 'finish_date', 'category']
        header = {'name': 'Name', 'start_date': 'Start Date', 'finish_date':'Finish Date', 'category':'Category'}
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writerow(header)
        for row in filtered:
            writer.writerow(row)

    # Redirect back to API root.
    return redirect('departures_home')