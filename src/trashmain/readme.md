# Trash-Muncher-Webapp - trashmain

## File structure
```
./src/trashimages
├── __init__.py  
├── asgi.py
├── auxillary.py           # Used to get a player's team 
├── permissions.py         # Used to check if a player is a gamekeeper or a player to restrict them from certain endpoints   
├── settings.py            # Contains settings used for configuration to ensure that the app runs as intended. Must include created APIs in ```INSTALLED_APPS```
├── urls.py                # List of registered urls that lead to endpoints. Defined for every application created               
└── wsgi.py                
```