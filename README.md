# GarminBoulderDevOpsInterview

This repository is my submission for this coding challenge: https://github.com/fitpay/eng-test/blob/master/README_DEVOPS.md

I have broken the requirements down into the following list of acceptance criterias:

- Send an outage email when API health changes from up to down (at least 2 failures in a row are considered an outage)
- Send a recovery email when API health changes from down to up (at least 2 successful calls in a row are considered a recovery)
- All failures to invoke the API must be logged.
- All API recoveries must be logged.
- The monitor must have a configurable, reasonable delay between attempts, to prevent the firewall from treating the monitor as a DoS attack.
- The monitor must run continuously until Ctrl-C’ed.
- If the HTTP response code is not 200, the monitor considers it a failure to invoke the API.
- If the HTTP return status is not “OK”, the monitor considers it a failure to invoke the API.
- Unit tests are required.
- All assumptions must be documented.

# Run Unit Tests
```bash
pytest *.py
```

# Builds and Run Locally
```bash
docker-compose up -d
```

# Connect to database
```bash
docker exec -it <container id> bash
mysql -u root -p # leave password empty
use garmin_api_state_db;
select * from state;
```