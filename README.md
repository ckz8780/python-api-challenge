# Python API Challenge

This is a simple python API using the Django Rest Framework. The goal was to first load the initial DB data, then query the local API and paginate through the results to generate a filtered CSV file.

### Methodology: 

For this challenge there were several potential ways to do it. To stick to the challenge specs, I opted to first load the data into the DB by writing an empty migration and reading the JSON file using the 'json' module. A more standard way to load the initial data would be to place the file in a fixtures folder within the app, and then run `python manage.py loaddata [appname]`. This could cause migration failures if the schema changed down the road though, since the default serializer used by loaddata would deserialize the current models into a format the fixture didn't match. To avoid that, the best solution would likely be to write a custom serializer, as detailed [here](https://stackoverflow.com/questions/25960850/loading-initial-data-with-django-1-7-and-data-migrations/39743581#39743581). All that aside, assuming the schema matches the json file the current method should work correctly in most cases.

To write out the CSV I simply used the requests module to make a request to the API root with a new function-based view: `get_csv`. I used the requests module's `json()` method to parse the response from the API root into JSON, then extracted the `next` and `results` parameters. I used a while loop to make repeated requests to the API until the `next` parameter was null, which means it's the last page, appending the `results` parameter to the results list with each request. After the final request, the results list is filtered using a simple list comprehension and then written to `departures.csv` in the project root using python's built in `csv` module, and the user is redirected to the API root. While I believe there are better ways to do this, the challenge required iteration over API results pages. With that in mind, if this were a real world project I would likely use the `limit` parameter in the API request to increase the number of results it could send back, overriding the default pagination and **limiting the number of requests made to the API**. This would both speed up the execution of the program as well as reduce load on the API which is always nice if you're an API owner :) 

### Usage: 

I added the requests module and its dependencies in order to write the `get_csv` view. I've updated requirements.txt accordingly using `pip freeze > requirements.txt`. That said, you should be able to simply clone this project, navigate to the project root, then: 

    ```
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```

Once the server is running, simply navigate to http://localhost:8000/csv/ to generate the CSV file (if you cloned the repo you may want to delete the CSV that's in there currently, to verify that the code does in fact generate one).