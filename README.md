# Weather_Tracker

A Python web application that fetches real time weather date of cites in a database.
## features
- Fetches weather data from Open-Metro API
- Stores the data in PostgresSQL database
- Displays all

## Installation
- PostgreSQL
- PGAdmin
- Git
#### Required software
- python **3.13.7**
- Postgres

#### Python packages
- requests
- pyscogp

### Steps
``` bash
1. Clone This repository:https://github.com/bcordero06/Final_project_weather
```

2. Open File Folder 
``` bash
CD Final_project_weather
```

3. Install Dependencies:
``` bash
pip install -r requirment.txt
```

4. Run route.py:
```
python3 route.py
```

5. See the weather for the 10 cities that are around the world

## Project Structure
```
Final_project_weather/
├──tempelates/
|   ├──index.html #HTML file showing the page    
├── .env #credentials
├── Db_manager.py #all database functions
├── Db.py #fetches weather from API
├── main.py #main runner file
├──routes.py #routes with flask and api endpoints


