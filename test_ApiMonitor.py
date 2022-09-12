from unittest.mock import MagicMock, patch
from ApiMonitor import ApiMonitor

url = "dummy_url"

good_json = {'_links': {'self': {'href': '/health'}},
             'status': 'OK', 
             'message': 'Everything is hunky dory over here, how are you?'}

bad_json = {'_links': {'self': {'href': '/health'}},
            'status': 'NOT_OK', 
            'message': 'Sh*ts on fire, yo.'}

@patch('ApiMonitor.requests')
def test_monitorConsidersAnyResponseCodeOtherThan200ToBeAFailure(mock_requests):
    # Arrange
    monitor = ApiMonitor(url)
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
    monitor = ApiMonitor(url)
    mock_request_response = MagicMock()
    mock_request_response.status_code = 200
    mock_request_response.json.return_value = bad_json
    mock_requests.get.return_value = mock_request_response

    # Act 
    health = monitor.get()

    # Assert
    assert health == False

def test_monitorRunsContinuouslyUntilCtrlC():
    assert False

def test_allFailuresToInvokeApiAreLogged():
    assert False

def test_allApiRecoveriesAreLogged():
    assert False

def test_monitorIsNotTreatedAsADosAttack():
    assert False

def test_outageEmailIsTriggeredAppropriately():
    assert False

def test_recoveryEmailIsTriggeredAppropriately():
    assert False

def test_outageEmailIsUrgentAndSentToCorrectRecipient():
    assert False

def test_recoveryEmailIsSentToCorrectRecipient():
    assert False

def test_outageEmailIncludesCorrectUptimeDuration():
    assert False

def test_outageEmailIncludesCorrectAverageUptime():
    assert False

def test_recoveryEmailIncludesCorrectDowntimeDuration():
    assert False

def test_recoveryEmailIncludesCorrectAverageUptime():
    assert False