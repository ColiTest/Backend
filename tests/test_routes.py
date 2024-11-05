def test_get_indexes(client):
    response = client.get('/canopen/indexes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert '0x1000' in data
    assert '0x1018' in data

def test_get_object_dictionary(client):
    response = client.get('/canopen/object-dictionary')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert '0x1000' in data
    assert '0x1018' in data

def test_invalid_endpoint(client):
    response = client.get('/invalid-endpoint')
    assert response.status_code == 404

def test_post_not_allowed(client):
    response = client.post('/canopen/indexes')
    assert response.status_code == 405

def test_get_indexes_content(client):
    response = client.get('/canopen/indexes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    for index, entry in data.items():
        assert isinstance(index, str)
        assert isinstance(entry, dict)
        assert 'ParameterName' in entry
        assert 'ObjectType' in entry
        assert 'DataType' in entry
        assert 'AccessType' in entry
        assert 'DefaultValue' in entry
        assert 'PDOMapping' in entry
        assert 'SubIndexes' in entry
        assert isinstance(entry['SubIndexes'], dict)

def test_get_object_dictionary_content(client):
    response = client.get('/canopen/object-dictionary')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    for index, name in data.items():
        assert isinstance(index, str)
        assert isinstance(name, str)