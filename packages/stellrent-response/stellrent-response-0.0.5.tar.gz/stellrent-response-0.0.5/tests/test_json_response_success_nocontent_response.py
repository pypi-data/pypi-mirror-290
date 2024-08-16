from stellrent_response import json_response

def test_nocontent_response():
    no_content_resp = json_response.NoDataResponse()
    assert(no_content_resp.response_status == 204)
    assert(no_content_resp.response_data == {})
    assert(no_content_resp.response_message == None)
    assert(no_content_resp.response_details == None)
    body, status_code = no_content_resp.make_response()
    assert(body == {})
    assert(status_code == 204)
