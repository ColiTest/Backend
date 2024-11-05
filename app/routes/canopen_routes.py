# canopen_routes.py
from flask import Blueprint, jsonify
import canopen
import os
from app.canopen_utils import eds_to_json, list_object_dictionary_entries

canopen_bp = Blueprint('canopen', __name__)

eds_file_path = os.path.join(os.path.dirname(__file__), '../../GenericCANopenSetup_line0.eds')

network = canopen.Network()
network.connect(interface='virtual')
node = network.add_node(1, eds_file_path)

@canopen_bp.route('/canopen/indexes', methods=['GET'])
def get_indexes():
    data = eds_to_json(node, eds_file_path)
    return jsonify(data)

@canopen_bp.route('/canopen/object-dictionary', methods=['GET'])
def get_object_dictionary():
    entries = list_object_dictionary_entries(node)
    return jsonify(entries)