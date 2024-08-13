import json


async def test_get_example(jp_fetch):
    # When
    response = await jp_fetch("jupS3", "get-example")

    # Then
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {
        "data": "This is /jupS3/get-example endpoint!"
    }