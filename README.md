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

# Description of my solution
- This app will monitor the API by continuously checking it every 5 seconds.
- In order to keep track of uptime and downtime, I've created a database with columns (Id, timestamp, healthy)
- Each time API changes from healthy to unhealthy, or vice versa, an email is sent and a row is added to the database.
- Before the email is sent, the database is queried to determine the latest outage/uptime length.
- More metrics could easily be built from the database, such as average uptime over the past 7 days.
- Some of the optional parts of the challenge were left out on purpose.

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
mysql -u root -p # enter 'password' when prompted.
use garmin_api_state_db;
select * from state;
```

# Run fake API to test monitor
```bash
uvicorn fake_api:app --reload
# to simulate an outage, change the status from OK
# to something else in fake_api.py
```
Update the docker-compose file to use the fake-api:
`- API_URL=http://host.docker.internal:8000`

# Continuous Integration
- This repository has a git CI pipeline here: https://github.com/mdreisinger/GarminBoulderDevOpsInterview/actions/workflows/ci.yml
- The pipeline runs pylint, runs unit tests, build images, and pushes them to AWS ECR.
- ApiMonitor image location: https://us-west-2.console.aws.amazon.com/ecr/repositories/public/126493000772/api_monitor?region=us-west-2
- Database image location: https://us-west-2.console.aws.amazon.com/ecr/repositories/public/126493000772/garmin_api_state_db?region=us-west-2
