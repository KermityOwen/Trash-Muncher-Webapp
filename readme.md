# API DOCUMENTATION

## ip:port/api/monsters/ - 
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
