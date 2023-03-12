# Trash-Muncher-Webapp - trashimages 

## File structure
./src/trashimages
├── migrations             # Used to create tables in the database from models.py  
├── __init__.py
├── admin.py               # File where models are registered on the admin site for use by the admin
├── apps.py                # Name of the application  
├── models.py              # Definition of the tables 
├── serializer.py          # Outlines the JSON format that requests will be received/sent in  
├── tests.py               # Unit tests for this API
├── urls.py                # List of registered urls that lead to endpoints                
└── viewsets.py            # Outlines what happens when a user accesses a URL. For more info, visit https://www.django-rest-framework.org/api-guide/viewsets/