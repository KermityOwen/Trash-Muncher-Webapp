# Trash-Muncher-Webapp

## Contents

- [Overview](https://github.com/KermityOwen/Trash-Muncher-Webapp#overview)

- [Creating a developer user](https://github.com/KermityOwen/Trash-Muncher-Webapp#creating-a-developer-user)

- [File structure](https://github.com/KermityOwen/Trash-Muncher-Webapp#file-structure) 

- [Contributors](https://github.com/KermityOwen/Trash-Muncher-Webapp/blob/main/readme.md#contributors-computer)

- [Privacy policy](https://github.com/KermityOwen/Trash-Muncher-Webapp/blob/main/readme.md#privacy-policy-lock)

- [License](https://github.com/KermityOwen/Trash-Muncher-Webapp/blob/main/readme.md#license-page_with_curl)




---

## Overview

[Trashmunchers](https://www.trashmunchers.co.uk/) is a location based game developed to promote sustainability at the University of Exeter. The objective of the game is for players to feed Trashmonsters at different recycling points scattered across campus in order for their team to gain control of the Trashmonsters. Players can visit their nearest Trashmonster and take a picture of what they are recycling. By doing so, they are awarded a certain amount of points based on the size of what they recycled. [NEEDS TO BE ELABORATED]

---

## Creating a developer user

Prerequisites:
1. Have Python installed (Link to download: https://www.python.org/downloads/)
2. Have pipenv installed (Steps to installation: https://pypi.org/project/pipenv/#installation)
3. Have a local version of the repository (How to clone a repository: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

Steps:
1. Open a terminal (Windows - PowerShell or Command Prompt, UNIX - Terminal)
2. Open the src folder in a terminal 

![How to open src in terminal](https://cdn.discordapp.com/attachments/796358887396999198/1084816785104183346/image.png)

3. Run ```pipenv install``` to download all dependencies

![How to install dependencies](https://cdn.discordapp.com/attachments/796358887396999198/1084817425477927012/image.png)

4. Enter the pip environment shell ```pipenv shell```

![How to enter pip environment](https://cdn.discordapp.com/attachments/796358887396999198/1084817618604662784/image.png)

- You should be met with a message confirming that you have entered the pipenv shell

![pipenv shell confirmation](https://cdn.discordapp.com/attachments/796358887396999198/1084817674418270289/image.png)

5. Enter src folder ```cd src```

![How to enter src folder](https://cdn.discordapp.com/attachments/796358887396999198/1084817966815789056/image.png)

6. Create a developer user ```python manage.py createsuperuser```

![How to create a developer account](https://cdn.discordapp.com/attachments/796358887396999198/1084818356651163750/image.png)

7. Enter the details that you would like the account to have (username, email and password) 

![Entering user details](https://cdn.discordapp.com/attachments/796358887396999198/1084818641377316954/image.png)

8. If already deployed, go to host-ip/admin (for us: http://38.242.137.81:8000/admin/) and login
   - If it hasn't been deployed (being run locally), run ```python manage.py loaddata teams``` to initialise the teams
   - Then, run ```python manage.py runserver```
   - Go to localhost:8000/admin and login to see if it was successfully created

![Admin login page](https://cdn.discordapp.com/attachments/796358887396999198/1084569132894269570/image.png)

9. Now, you can manage all users, teams and trashmonsters in the database. (It is also possible to edit team names in src/trashusers/fixtures/teams.json)
---

## File structure
```
.
├── github                  # Used to update backend host link 
├── design_documents        # Markdowns containing information about game and technical design choices
	│ ├── .obsidian               # JSONs for styling markdowns  
    │ ├── GDD.md                  # Information about game design choices
    │ ├── TDD.md                  # Information about technical design choices (Needs to be completed)
    │ └── TrashImagesApp.md       # Instructions on how to run the TrashImages APIs locally to ensure that they can be used for deployment
├── src                     # Source files 
│ ├── assests                 # JSONs for styling markdowns  
│ ├── media/images            # Contains the images submitted by users
│ ├── trashimages             # Django app used for image handling
	│├── migrations             # Used to create tables in the database from models.py  
    │├── __init__.py
    │├── admin.py               # File where models are registered on the admin site for use by the admin
    │├── apps.py                # Name of the application  
    │├── models.py              # Definition of the tables 
    │├── serializer.py          # Outlines the JSON format that requests will be received/sent in  
    │├── tests.py               # Unit tests for this API
    │├── urls.py                # List of registered urls that lead to endpoints                
    │└── viewsets.py            # Outlines what happens when a user accesses a URL. For more info, visit https://www.django-rest-framework.org/api-guide/viewsets/
│ ├── trashmain               # Main Django app for configuration (Initial API endpoint)
	│├── __init__.py  
	│├── asgi.py
	│├── auxillary.py           # Used to get a player's team 
	│├── permissions.py         # Used to check if a player is a gamekeeper or a player to restrict them from certain endpoints   
	│├── settings.py            # Contains settings used for configuration to ensure that the app runs as intended. Must include created APIs in INSTALLED_APPS
	│├── urls.py                # List of registered urls that lead to endpoints. Defined for every application created               
	│└── wsgi.py    
│ ├── trashmonsters           # Django app for handling the game's monsters
	│├── migrations             # Used to create tables in the database from models.py  
    │├── __init__.py
    │├── admin.py               
    │├── apps.py                # Handles server startup to ensure that database isn't constantly recreated and overwritten
    │├── config.json            # Contains "monster eating" interval and maximum distance leeway   
    │├── jobs.py                # Handles the score decreasing methods using a scheduler    
    │├── models.py              
    │├── serializer.py 
    │├── tests.py               # Unit tests for this application
    │├── urls.py                                
    │└── viewsets.py 
│ ├── trashusers              # Django app for handling users
	│├── fixtures                
		│├── teams.json       # JSON file that is used to create three teams on startup 
	│├── migrations               
	│├── __init__.py
	│├── admin.py               
	│├── apps.py                 
	│├── models.py               
	│├── serializer.py            
	│├── tests.py               
	│├── urls.py                                
	│└── viewsets.py             
│ ├── db.sqlite3              # Database where information is stored 
│ ├── manage.py               # Autocreated by Django. Used for executing Django related tasks (e.g., running the server)
│ └── requirements.txt        # List of dependencies used for deployment
├── trashmunchers           # Contains cache files
	│├── trashmunchers/__pycache__        
    │└── trashsite/__pycache__         
 
├── .gitignore              # Prevents certain files from being pushed to the repository
├── Dockerfile              # Used to install the latest dependencies upon deployment 
├── Pipfile                 # Contains all project dependecies required for the application to be built 
├── Pipfile.lock            # Declares all project dependecies, their latest available versions and the hashes for those files
├── INFOFORGROUP.txt        # Information for development team on how to maintain program
├── docker-compose.yml      # Used to run the Django server through Docker 
├── readme.md               
├── requirements.txt        # List of dependencies used for deployment
├── run-docker.sh           # Shell script to run the Docker server 
├── LICENSE           # License used for this repository  
└── api_documentation.md    # Information about API endpoints
```

--- 

## Contributors :computer: 

<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/KermityOwen"><img src="https://avatars.githubusercontent.com/u/47197696?v=4" width="100px;" alt="Owen Lee"/><br /><sub><b>Owen Lee</b></sub></a></td>
	  <td align="center"><a href="https://github.com/whoisEllie"><img src="https://avatars.githubusercontent.com/u/37041249?v=4" width="100px;" alt="Ellie Kelemen"/><br /><sub><b>Ellie Kelemen</b></sub></a></td>
	  <td align="center"><a href="https://github.com/TerraTree"><img src="https://avatars.githubusercontent.com/u/22399437?v=4" width="100px;" alt="William Liversidge"/><br /><sub><b>William Liversidge</b></sub></a></td>
	  <td align="center"><a href="https://github.com/vigneshmohan2002"><img src="https://avatars.githubusercontent.com/u/85409344?v=4" width="100px;" alt="Vignesh Mohanarajan"/><br /><sub><b>Vignesh Mohanarajan</b></sub></a></td>
	  <td align="center"><a href="https://github.com/scarlettp1619"><img src="https://avatars.githubusercontent.com/u/95775118?v=4" width="100px;" alt="Scarlett Parker"/><br /><sub><b>Scarlett Parker</b></sub></a></td>
	  <td align="center"><a href="https://github.com/FBWWTeto"><img src="https://avatars.githubusercontent.com/u/93519490?v=4" width="100px;" alt="Malik Besta"/><br /><sub><b>Malik Besta</b></sub></a></td>
	  </tr>
  </tbody>
</table>
	  

---

## Privacy Policy :lock:

[Privacy policy](tm_privacy_policy.pdf)

---

## License :page_with_curl:

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
