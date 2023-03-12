# Trash-Muncher-Webapp

## File structure
.
├── github                  # Used to update backend host link 
├── design_documents        # Markdowns containing information about game and technical design choices
├── src                     # Source files 
├── trashmunchers           # Contains cache files 
├── .gitignore              # Prevents certain files from being pushed to the repository
├── Dockerfile              # Used to install the latest dependencies upon deployment 
├── Pipfile                 # Contains all project dependecies required for the application to be built 
├── Pipfile.lock            # Declares all project dependecies, their latest available versions and the hashes for those files
├── READMEFORDEVS.txt       # Information for development team on how to maintain program
├── docker-compose.yml      # Used to run the Django server through Docker 
├── readme.md               
├── requirements.txt        # List of dependencies used for deployment 
└── run-docker.sh           # Shell script to run the Docker server

### License

[MIT](https://choosealicense.com/licenses/mit/)

---

## API DOCUMENTATION

### ip:port/api/monsters/ - 
- get-tms [GET] -   
Gets all trashmunchers and associated data from db. Responds with serialized trashmunchers.

- get-tm [POST] -  
 Gets specific trashmuncher by id (`TM_ID`). Responds with serialized trashmuncher   
<b>Example request: `{"TM_ID":0}`</b>

- add-tm [POST] -  
 Adds trashmuncher to database. Id and Scores are auto-initialized. Responds with serialized trashmuncher that was just added.  
<b>Example request: `{"Longitude":12.3456, "Latitude":5.6789}`</b>

- calculate-distance [POST] -  
 Calculates the distance between trashmuncher specified and origin location. Responds with distance in meters.  
<b>Example request: `{"TM_ID":0, "o-lat": 12.3466, "o-long": 5.6789}`</b>

- calculate-distance [POST] -  
 Calculates the distance between trashmuncher specified and origin location and returns if it's within valid range. Responds with True or False.  
<b>Example request: `{"TM_ID":0, "o-lat": 12.3466, "o-long": 5.6789}`</b>

- change-score [POST] -  
Changes the scores for trashmuncher specified. If a score is not presented, it doesn"t change that score. Responds with the trashmuncher that was just edited.  
<b>Example request: `{"TM_ID":0, "T1Score":1, "T2Score":2, "T3Score":4}`</b>

- add-score [POST] -  
Adds scores for trashmunchers specified. If a score is not presented, it doesn"t increment that score. Responds with the trashmuncher that was just edited.  
<b>Example request: `{"TM_ID":0, "T1Score":1, "T2Score":1, "T3Score":0}`</b>

- remove-score [POST] -  
Removes scores for trashmunchers specified. If a score is not presented, it doesn"t decrease that score. Responds with the trashmuncher that was just edited.  
<b>Example request: `{"TM_ID":0, "T1Score":1, "T2Score":1, "T3Score":0}`</b>

- get-leader [POST] - 
Gets the team with the leading number of scores. Responds with team number.  
<b>Example request: `{"TM_ID":0}`</b>

---

### ip:port/api/images/ - 
- submit-image [POST] -   
Add an image to a database. IDs are auto-incremented. Responds with a serialized image containing the ID and a link to the image just added
<b>Example request: `{"id":5, "image":"http://localhost/media/images/example.jpg"}`</b>
- list-images [GET] -  
 Gets all images from the database. Responds with serialized list of images, containing their IDs and the links to them  
<b>Example request: `[{"id":5, "image":"http://localhost/media/images/example.jpg"}, {"id":6, "image":"http://localhost/media/images/example2.jpg"}]`</b>

- delete-images [POST] -  
Removes an image from the database with a specified ID. Responds with serialized message either stating the image has successfully been deleted (200), or the image couldn't be found (404).  
<b>Example request: `{"id":4}`</b>

---

### ip:port/api/users/ - 
- me [GET] -  
Gets the current user's information. Responds with their information serialized.
<b>Example request: `{"username":"tortoise_hugger", "first_name":"David", "last_name":"Smith", "Team":"Green"}`</b>

- player-register [POST] -  
Allows a person to register as a player. Responds with the information that they inputted serialized. Prevents input fields from being empty and requires a strong password. 
<b>Example request: `{"username":"OnionRings101", "first_name":"Souff", "last_name":"Lé", "Team":"Red"}`</b>

- gamekeeper-register [GET] -  
Allows a person to register as a gamekeeper. Responds with the information that they inputted serialized. Prevents input fields from being empty and requires a strong password. 
<b>Example request: `{"id":22, username":"GKeeper", "first_name":"Alban", "last_name":"Lafont"}`</b>

- login [POST] -  
Allows the user to login. Responds with the information that they inputted serialized. Prevents input fields from being empty. 

- logout [GET] -  
Allows a user to logout. Returns a HTTP response confirming to the user that they have been logged out