# canopen_routes.py
from flask import Blueprint, jsonify, abort, make_response
import canopen
import os
from app.canopen_utils import eds_to_json, list_object_dictionary_entries, parse_eds_file

canopen_bp = Blueprint('canopen', __name__)

eds_file_path = os.path.join(os.path.dirname(__file__), '../../GenericCANopenSetup_line0.eds')

network = canopen.Network()
network.connect(interface='virtual')
node = network.add_node(1, eds_file_path)

@canopen_bp.route('/indexes', methods=['GET'])
def get_indexes():
    data = eds_to_json(node, eds_file_path)
    return jsonify(data)

@canopen_bp.route('/object-dictionary', methods=['GET'])
def get_object_dictionary():
    entries = list_object_dictionary_entries(node)
    return jsonify(entries)

@canopen_bp.route('/index/<string:index>', methods=['GET'])
@canopen_bp.route('/index/<string:index>/', methods=['GET'])
@canopen_bp.route('/index/<string:index>/<subindex>', methods=['GET'])
def get_index_value(index, subindex=None):
    try:
        index_int = int(index, 16)
        entry = node.object_dictionary[index_int]
    except ValueError:
        response = jsonify({'message': f"Invalid hex index '{index}'. Please use a valid hex format like '1018'."})
        response.status_code = 400
        return response
    except KeyError:
        response = jsonify({'message': f"Index {hex(index_int)} not found"})
        response.status_code = 404
        return response

    if subindex is None:
        if hasattr(entry, 'subindices') and entry.subindices:
            response = jsonify({
                'index': hex(index_int),
                'message': 'Missing input. Please enter a subindex.',
                'available_subindices': list(entry.subindices.keys())
            })
            response.status_code = 400
            return response
        else:
            response = jsonify({
                'index': hex(index_int),
                'message': 'Invalid input. This index does not have any subindices.'
            })
            response.status_code = 400
            return response

    try:
        subindex_int = int(subindex)
    except ValueError:
        response = jsonify({'message': f"Invalid subindex '{subindex}'. Please use a valid integer format."})
        response.status_code = 400
        return response

    if hasattr(entry, 'subindices') and subindex_int in entry.subindices:
        subentry = entry.subindices[subindex_int]
        sub_section_name = f"{index_int:04X}sub{subindex_int}"
        eds_config = parse_eds_file(eds_file_path)
        sub_fallback_data = eds_config[sub_section_name] if sub_section_name in eds_config else {}

        subentry_data = {
            'ParameterName': getattr(subentry, 'name', None) or sub_fallback_data.get('ParameterName'),
            'ObjectType': getattr(subentry, 'object_type', None) or sub_fallback_data.get('ObjectType'),
            'DataType': getattr(subentry, 'data_type', None) or sub_fallback_data.get('DataType'),
            'AccessType': getattr(subentry, 'access_type', None) or sub_fallback_data.get('AccessType'),
            'DefaultValue': getattr(subentry, 'default_value', None) or sub_fallback_data.get('DefaultValue'),
            'PDOMapping': getattr(subentry, 'pdo_mapping', None) or sub_fallback_data.get('PDOMapping')
        }
        return jsonify({
            'index': hex(index_int),
            'subindex': subindex_int,
            'details': subentry_data
        })

    else:
        available_subindices = list(entry.subindices.keys()) if hasattr(entry, 'subindices') else []
        response = jsonify({
            'index': hex(index_int),
            'message': 'Invalid subindex. Please enter a valid subindex.',
            'available_subindices': available_subindices
        })
        response.status_code = 400
        return response