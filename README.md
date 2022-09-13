# GarminBoulderDevOpsInterview

This repository is my submission for this coding challenge: https://github.com/fitpay/eng-test/blob/master/README_DEVOPS.md

I have broken the requirements down into the following list of acceptance criterias:

(_) Send an outage email when API health changes from up to down (at least 2 failures in a row are considered an outage)

(_) Send a recovery email when API health changes from down to up (at least 2 successful calls in a row are considered a recovery)

(_) The outage email must be marked as urgent and sent to Garmin support staff.

(_) The recovery email must be sent to Garmin support staff.

(_) The outage threshold and recovery threshold should be configurable.

(_) The outage email must include metrics: uptime duration, average uptime between outages.

(_) The recovery email must include metrics: downtime duration, average uptime between outages.

(_) Both emails can be either plaintext or HTML.

(_) All failure to invoke the API must be logged.

(_) All API recoveries must be logged.

(_) The monitor must have a configurable, reasonable delay between attempts, to prevent the firewall from treating the monitor as a DoS attack.

(_) The monitor must run continuously until Ctrl-C’ed.

(_) The API must be configurable and set by default to GET https://api.qa.fitpay.ninja/health

(_) If the HTTP response code is not 200, the monitor considers it a failure to invoke the API.

(_) If the HTTP return status is not “OK”, the monitor considers it a failure to invoke the API.

(_) Unit tests are required.

(_) All assumptions must be documented.

(_) Extra credit: Determine which geographic regions the API is expected to function in. Create a list of proxy servers (configurable), to hit the API from so that all of the expected geographic regions are exercised by the monitor. Incorporate the design decison that answers the question: Are Garmin support email addresses region-specific?