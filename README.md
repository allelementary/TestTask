#About The Project

##TestTask for Alar Studios

Python Flask application with authentication, allows to add, edit and delete users, 
give or denied access, collect data from three json-files with async requests, 
sort it by ids and display on page.

##Built With

* Python 3.9
* Flask
* Blueprint
* PostgreSQL
* SQLAlchemy
* Asyncio
* Aiohttp
* Bootstrap

##Installation

* Configure database settings in app_config.py and database.ini
* Create database
* Open terminal window
* Navigate to TestTask directory
* Activate virtualenv: *pipenv shell*
* Install requirements: *pip install -r requirements.txt*
* Navigate to data directory: *cd data*
* Run a local server with json files: *python3 -m http.server*
* Open new terminal window
* Navigate to root directory
* Run app: *gunicorn wsgi:app*

##Contact

Mikhail Antonov *allelementaryfor@gmail.com*
