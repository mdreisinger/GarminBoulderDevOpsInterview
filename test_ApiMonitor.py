from threading import Thread
import time
from unittest.mock import MagicMock, patch
from unittest import mock

from ApiMonitor import ApiMonitor


url = "dummy_url"

good_json = {'_links': {'self': {'href': '/health'}},
             'status': 'OK', 
             'message': 'Everything is hunky dory over here, how are you?'}

good_resp = MagicMock()
good_resp.status_code = 200
good_resp.json.return_value = good_json

bad_json = {'_links': {'self': {'href': '/health'}},
            'status': 'NOT_OK', 
            'message': 'NOT hunky dory!!.'}

bad_resp = MagicMock()
bad_resp.status_code = 666
bad_resp.json.return_value = bad_json


@patch('ApiMonitor.requests')
def test_monitorConsidersAnyResponseCodeOtherThan200ToBeAFailure(mock_requests):
    # Arrange
    db = MagicMock()
    monitor = ApiMonitor(url, db)
    mock_request_response = MagicMock()
    mock_request_response.status_code = 666
    mock_request_response.json.return_value = good_json
    mock_requests.get.return_value = mock_request_response

    # Act 
    health = monitor.get()

    # Assert
    assert health == False

@patch('ApiMonitor.requests')
def test_monitorConsidersAnyReturnStatusOtherThanOkToBeAFailure(mock_requests):
    # Arrange
    db = MagicMock()
    monitor = ApiMonitor(url, db)
    mock_request_response = MagicMock()
    mock_request_response.status_code = 200
    mock_request_response.json.return_value = bad_json
    mock_requests.get.return_value = mock_request_response

    # Act 
    health = monitor.get()

    # Assert
    assert health == False

@patch('ApiMonitor.requests.get', 
        side_effect=[good_resp, good_resp, good_resp]+[bad_resp for _ in range(100)])
def test_outageEmailIsTriggeredAppropriately(mock_requests):
    # Arrange
    db = MagicMock()
    monitor = ApiMonitor(url, db, sleep_time=0.1)
    email_service = MagicMock()
    monitor.email_service = email_service

    # Act
    thread = Thread(target=monitor.start_monitoring)
    thread.start()
    time.sleep(1)
    monitor.monitor = False
    thread.join()
    
    # Assert
    email_service.assert_called_once_with(monitor.recipient, monitor.fail_subject, monitor.build_outage_body())

@patch('ApiMonitor.requests.get', 
        side_effect=[bad_resp, bad_resp, bad_resp]+[good_resp for _ in range(100)])
def test_recoveryEmailIsTriggeredAppropriately(mock_requests):
    # Arrange
    db = MagicMock()
    monitor = ApiMonitor(url, db, sleep_time=0.1)
    email_service = MagicMock()
    monitor.email_service = email_service

    # Act
    thread = Thread(target=monitor.start_monitoring)
    thread.start()
    time.sleep(1)
    monitor.monitor = False
    thread.join()
    
    # Assert
    email_service.assert_has_calls(
        [mock.call(monitor.recipient, monitor.fail_subject, monitor.build_outage_body()), 
         mock.call(monitor.recipient, monitor.recovery_subject, monitor.build_recovery_body())])


# TODO more tests: test the database insertion / metrics stuff