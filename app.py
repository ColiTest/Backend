from flask import Flask, jsonify
import canopen
import os

app = Flask(__name__)

eds_file_path = os.path.join(os.path.dirname(__file__), 'GenericCANopenSetup_line0.eds')

def eds_to_json(node):
    data = {}
    for index, entry in node.object_dictionary.items():
        entry_data = {
            'name': entry.name,
            'index': hex(entry.index),
            'data_type': entry.data_type if hasattr(entry, 'data_type') else None,
            'subindex': {}
        }
        if hasattr(entry, 'subindices'):
            for subindex, subentry in entry.subindices.items():
                entry_data['subindex'][subindex] = {
                    'name': subentry.name,
                    'data_type': subentry.data_type if hasattr(subentry, 'data_type') else None,
                    'value': subentry.default if hasattr(subentry, 'default') else None
                }
        data[hex(index)] = entry_data
    return data

network = canopen.Network()
network.connect(bustype='virtual')

node = network.add_node(1, eds_file_path)

@app.route('/canopen/indexes', methods=['GET'])
def get_indexes():
    data = eds_to_json(node)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
