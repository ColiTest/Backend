import configparser

def parse_eds_file(eds_file_path):
    config = configparser.ConfigParser()
    config.read(eds_file_path)
    return config

def eds_to_json(node, eds_file_path):
    eds_config = parse_eds_file(eds_file_path)
    
    data = {}
    for index, entry in node.object_dictionary.items():
        section_name = f"{index:04X}"
        
        fallback_data = eds_config[section_name] if section_name in eds_config else {}

        entry_data = {
            'ParameterName': getattr(entry, 'name', None) or fallback_data.get('ParameterName'),
            'ObjectType': getattr(entry, 'object_type', None) or fallback_data.get('ObjectType'),
            'DataType': getattr(entry, 'data_type', None) or fallback_data.get('DataType'),
            'AccessType': getattr(entry, 'access_type', None) or fallback_data.get('AccessType'),
            'DefaultValue': getattr(entry, 'default_value', None) or fallback_data.get('DefaultValue'),
            'PDOMapping': getattr(entry, 'pdo_mapping', None) or fallback_data.get('PDOMapping'),
            'SubIndexes': {}
        }
        
        if hasattr(entry, 'subindices'):
            for subindex, subentry in entry.subindices.items():
                entry_data['SubIndexes'][subindex] = {
                    'ParameterName': getattr(subentry, 'name', None),
                    'DataType': getattr(subentry, 'data_type', None),
                    'AccessType': getattr(subentry, 'access_type', None),
                    'DefaultValue': getattr(subentry, 'default_value', None),
                    'PDOMapping': getattr(subentry, 'pdo_mapping', None)
                }
        
        data[hex(index)] = entry_data
    return data


def list_object_dictionary_entries(node):
    entries = {hex(entry.index): entry.name for entry in node.object_dictionary.values()}
    return entries