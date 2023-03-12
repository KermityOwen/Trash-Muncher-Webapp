# Trash-Muncher-Webapp - trashmonsters 

## File structure
./src/trashmonsters
├── migrations             # Used to create tables in the database from models.py  
├── __init__.py
├── admin.py               # Where models are registered on the admin site for use by the admin
├── apps.py                # Handles server startup to ensure that database isn't constantly recreated and overwritten
├── config.json            # Contains "monster eating" interval and maximum distance leeway   
├── jobs.py                # Handles the score decreasing methods using a scheduler    
├── models.py              # Definition of the database tables required by this app
├── serializer.py          # Outlines the JSON format that requests will be received/sent in  
├── tests.py               # Unit tests for this API
├── urls.py                # List of registered urls that lead to endpoints                
└── viewsets.py            # Outlines what happens when a user accesses a URL. For more info, visit https://www.django-rest-framework.org/api-guide/viewsets/