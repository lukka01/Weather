# Weather Data Service

A simple REST API that fetches real-time weather data, saves it to a database, and returns it as JSON.

## Stack
- Flask — web framework
- Flask-SQLAlchemy — database ORM
- SQLite — local database (no setup required)
- Open-Meteo — free weather API (no API key needed)

#Setup

```bash
pip install -r requirements.txt
python app.py
```
## Endpoints

### `GET /fetch-data`
Fetches current weather and saves it to the database.

```
/fetch-data                    
/fetch-data?lat=48.85&lon=2.35  (any location)
```
### `GET /records`
Returns saved records from the database.

```
/records
/records?limit=10
```

## Notes
- Database file `weather.db` is created automatically on first run
- All errors are handled and returned as JSON — the server never crashes
