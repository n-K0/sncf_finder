# Flask Travel Planner
This is a Flask application that helps in planning travels. It allows the user to select a starting point and a maximum travel time, and then suggests random destinations that can be reached within the specified time

## Prerequisites

This script requires the following pip modules :

- branca
- certifi
- charset-normalizer
- click
- colorama
- Flask
- folium
- geographiclib
- geopy
- idna
- importlib-metadata
- itsdangerous
- Jinja2
- MarkupSafe
- numpy
- python-dateutil
- requests
- six
- urllib3
- Werkzeug
- zipp


## Usage

To use the application, run the script using Python. This can be done by running the following command:
```
python app.py
```
This will start the Flask server, and the application can be accessed by opening a web browser and navigating to http://localhost:5000/.

The application consists of three pages:

* The index page, which allows the user to select a starting point and a maximum travel time.
* The result page, which displays a list of random destinations that can be reached within the specified time.
* The random page, which displays a randomly selected destination and its details.
The user can navigate between these pages using the buttons provided.

## Code Explanation
The main script app.py contains the Flask application, and consists of the following parts:

### Importing Libraries
The required libraries are imported at the beginning of the script.

### Defining Routes
Three routes are defined for the application:

* The index route (/) displays the index page, and handles the form submission.
* The result route (/result) displays the result page, and handles the form submission.
* The random route (/random) displays the random page, and handles the form submission.

Each of these routes has a corresponding function that handles the request.

### The Index Page
The index page displays a form that allows the user to select a starting point and a maximum travel time. If the form is submitted, the selected values are stored in the session, and the user is redirected to the result page or the random page based on their choice.

When the user submit the request, fonctions are used to make the api search and store the data in local db then, the map is generated.

### The Result Page
The result page displays a list of random destinations that can be reached within the specified travel time. The get_journey and gen_map libraries are used to generate the list of destinations and a map of France, respectively. If no destinations are found, a 404 error is displayed.

### The Random Page
The random page displays a randomly selected destination and its details. The dbmanager library is used to query the database for a random destination.


### Running the Application
The Flask application is run using the app.run() method. By default, the application runs in debug mode, which allows for easier debugging.

## Contributing / Reporting issues

* [Link to Issues](https://github.com/n-K0/sncf_finder/issues)
* [Link to project](https://github.com/n-K0/sncf_finder/projects)

## License

[Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/)

## THANKS / AUTHORS
 [@n-K0] (https://www.github.com/n-K0)
