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

def test_get_index_value_without_subindex(client):
    response = client.get('/canopen/index/1000')
    assert response.status_code == 200
    data = response.get_json()
    assert 'index' in data
    assert 'message' in data
    assert data['message'] == 'This index does not have any subindices'

def test_get_index_value_with_subindex(client):
    response = client.get('/canopen/index/1018/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'index' in data
    assert 'subindex' in data
    assert 'details' in data
    details = data['details']
    assert 'ParameterName' in details
    assert 'ObjectType' in details
    assert 'DataType' in details
    assert 'AccessType' in details
    assert 'DefaultValue' in details
    assert 'PDOMapping' in details

def test_get_index_value_invalid_subindex(client):
    response = client.get('/canopen/index/1018/99')
    assert response.status_code == 400
    data = response.get_json()
    assert 'index' in data
    assert 'message' in data
    assert 'available_subindices' in data
    assert data['message'] == 'Invalid subindex'

def test_get_index_value_invalid_index(client):
    response = client.get('/canopen/index/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Index 0x9999 not found'