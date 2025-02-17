from flask import Flask, jsonify
from cloud_providers.aws import AWS
from cloud_providers.azure import Azure
from cloud_providers.gcp import GCP
from cloud_providers.voltagepark import VoltagePark
from gpu_instances import GPUInstance

app = Flask(__name__)

# Initialize cloud provider instances
voltagepark = VoltagePark()


@app.route('/pricing/voltagepark', methods=['GET'])
def get_voltagepark_pricing():
    return jsonify(voltagepark.get_pricing())


if __name__ == '__main__':
    app.run(debug=True)
