from smhi.smhi import SmhiParser, calculate_high_low_temperature
import pytest
from unittest.mock import patch, MagicMock


def test_check_connection():
    parser = SmhiParser()
    assert 200 == parser.make_request().status_code
    assert 200 == parser.make_request(path="/parameter/2").status_code


@pytest.mark.parametrize("station_response, temperature_responses, expected",
    [
        # Test case 1: four active stations with positive temperature values
        (
            {
                "status_code": 200,
                "json": {
                    "station": [
                        {"key": "station1", "active": True},
                        {"key": "station2", "active": True},
                        {"key": "station3", "active": True},
                        {"key": "station4", "active": True},
                    ]
                }
            },
            [
                {"status_code": 200, "json": {"value": [{"value": "15.0"}], "station": {"name": "Station 1"}}},
                {"status_code": 200, "json": {"value": [{"value": "20.0"}], "station": {"name": "Station 2"}}},
                {"status_code": 200, "json": {"value": [{"value": "5.3"}], "station": {"name": "Station 3"}}},
                {"status_code": 200, "json": {"value": [{"value": "2.0"}], "station": {"name": "Station 4"}}},
            ],
            ("Station 2", 20.0, "Station 4", 2.0)
        ),
        # Test case 2: two active stations and one inactive station
        (
            {
                "status_code": 200,
                "json": {
                    "station": [
                        {"key": "station1", "active": True},
                        {"key": "station2", "active": False},
                        {"key": "station3", "active": True},
                    ]
                }
            },
            [
                {"status_code": 200, "json": {"value": [{"value": "15.0"}], "station": {"name": "Station 1"}}},
                {"status_code": 200, "json": {"value": [{"value": "18.0"}], "station": {"name": "Station 3"}}},
            ],
            ("Station 3", 18.0, "Station 1", 15.0)
        ),
        # Test case 3: two active stations and they have same temperatures
        (
            {
                "status_code": 200,
                "json": {
                    "station": [
                        {"key": "station1", "active": True},
                        {"key": "station2", "active": True},
                    ]
                }
            },
            [
                {"status_code": 200, "json": {"value": [{"value": "15.0"}], "station": {"name": "Station 1"}}},
                {"status_code": 200, "json": {"value": [{"value": "15.0"}], "station": {"name": "Station 2"}}},
            ],
            ("Station 1", 15.0, "Station 1", 15.0)
        ),
        # Test case 4: four active stations with negative temperature values
        (
            {
                "status_code": 200,
                "json": {
                    "station": [
                        {"key": "station1", "active": True},
                        {"key": "station2", "active": True},
                        {"key": "station3", "active": True},
                        {"key": "station4", "active": True},
                    ]
                }
            },
            [
                {"status_code": 200, "json": {"value": [{"value": "-15.0"}], "station": {"name": "Station 1"}}},
                {"status_code": 200, "json": {"value": [{"value": "-20.0"}], "station": {"name": "Station 2"}}},
                {"status_code": 200, "json": {"value": [{"value": "-5.3"}], "station": {"name": "Station 3"}}},
                {"status_code": 200, "json": {"value": [{"value": "-2.0"}], "station": {"name": "Station 4"}}},
            ],
            ("Station 4", -2.0, "Station 2", -20.0)
        ),
        # Test case 5: four active stations with positive and negative temperature values
        (
            {
                "status_code": 200,
                "json": {
                    "station": [
                        {"key": "station1", "active": True},
                        {"key": "station2", "active": True},
                        {"key": "station3", "active": True},
                        {"key": "station4", "active": True},
                    ]
                }
            },
            [
                {"status_code": 200, "json": {"value": [{"value": "-15.0"}], "station": {"name": "Station 1"}}},
                {"status_code": 200, "json": {"value": [{"value": "-20.0"}], "station": {"name": "Station 2"}}},
                {"status_code": 200, "json": {"value": [{"value": "5.3"}], "station": {"name": "Station 3"}}},
                {"status_code": 200, "json": {"value": [{"value": "2.0"}], "station": {"name": "Station 4"}}},
            ],
            ("Station 3", 5.3, "Station 2", -20.0)
        )
    ]
)
@patch("smhi.smhi.SmhiParser.make_request")
def test_calculate_high_low_temperature(mock_make_request, station_response, temperature_responses, expected):
    # Mock the response_station
    mock_response_station = MagicMock()
    mock_response_station.status_code = station_response["status_code"]
    mock_response_station.json.return_value = station_response["json"]

    # Mock the response_temp for each stations' data
    mock_temperature_responses = []
    for r in temperature_responses:
        mock_temperature_response = MagicMock()
        mock_temperature_response.status_code = r["status_code"]
        mock_temperature_response.json.return_value = r["json"]
        mock_temperature_responses.append(mock_temperature_response)

    mock_make_request.side_effect = [mock_response_station] + mock_temperature_responses

    smhi_parser = SmhiParser()
    smhi_parser.make_request = mock_make_request

    # Call the function to test
    highest_place, highest_temp, lowest_place, lowest_temp = calculate_high_low_temperature(smhi_parser)

    assert (highest_place, highest_temp, lowest_place, lowest_temp) == expected



