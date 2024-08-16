from stellrent_response import json_response

detailed_error_message = "A detailed error message"
custom_message = "A custom Bad Request message"
default_message = "Bad Request"

def test_response():
    bad_request_response = json_response.BadRequest()
    assert(bad_request_response.response_status == 400)
    assert(bad_request_response.response_data == None)
    assert(bad_request_response.response_message is not None)
    assert(bad_request_response.response_details == None)
    body, status_code = bad_request_response.make_response()
    assert(len(body) == 2)
    assert(status_code == 400)
    assert(body['message'] == json_response.default_messages[400])
    assert(body['status'] == 400)

def test_response_with_details():
    bad_request_response = json_response.BadRequest(details=detailed_error_message)
    assert(bad_request_response.response_status == 400)
    assert(bad_request_response.response_data == None)
    assert(bad_request_response.response_message is not None)
    assert(bad_request_response.response_details is not None)
    body, status_code = bad_request_response.make_response()
    assert(len(body) == 3)
    assert(status_code == 400)
    assert(body['details'] == detailed_error_message)
    assert(body['message'] == json_response.default_messages[400])
    assert(body['status'] == 400)

def test_response_with_custom_message():
    bad_request_response = json_response.BadRequest()
    bad_request_response.response_message = custom_message
    assert(bad_request_response.response_status == 400)
    assert(bad_request_response.response_data == None)
    assert(bad_request_response.response_message is not None)
    assert(bad_request_response.response_details == None)
    body, status_code = bad_request_response.make_response()
    assert(len(body) == 2)
    assert(status_code == 400)
    assert(body['message'] == custom_message)
    assert(body['status'] == 400)

def test_response_with_details_and_custom_message():
    bad_request_response = json_response.BadRequest(detailed_error_message)
    bad_request_response.response_message = custom_message
    assert(bad_request_response.response_status == 400)
    assert(bad_request_response.response_data == None)
    assert(bad_request_response.response_message is not None)
    assert(bad_request_response.response_details is not None)
    body, status_code = bad_request_response.make_response()
    assert(len(body) == 3)
    assert(status_code == 400)
    assert(body['message'] == custom_message)
    assert(body['details'] == detailed_error_message)
    assert(body['status'] == 400)

def test_response_not_found():
    bad_request_response = json_response.NotFound(detailed_error_message)
    bad_request_response.response_message = custom_message
    assert(bad_request_response.response_status == 404)
    assert(bad_request_response.response_message is not None)
    assert(bad_request_response.response_details is not None)
    body, status_code = bad_request_response.make_response()
    assert(len(body) == 3)
    assert(status_code == 404)
    assert(body['message'] == custom_message)
    assert(body['details'] == detailed_error_message)
    assert(body['status'] == 404)
