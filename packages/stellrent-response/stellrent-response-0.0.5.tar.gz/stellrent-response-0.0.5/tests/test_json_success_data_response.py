from stellrent_response import json_response

def test_response():

    content_response_data = {
        "param1": "value1",
        "param2": "value2",
        "param3": "value3",
        "param4": "value4"
    }
    success_content_resp = json_response.DataResponse(data=content_response_data)
    assert(success_content_resp.response_status == 200)
    assert(success_content_resp.response_data is not None)
    assert(success_content_resp.response_message == None)
    assert(success_content_resp.response_details == None)
    body, status_code = success_content_resp.make_response()
    assert(len(body) == len(content_response_data))
    assert(status_code == 200)
    assert(content_response_data == body)