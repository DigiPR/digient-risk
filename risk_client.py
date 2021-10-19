import os
import requests
import json
import httpimport
with httpimport.github_repo('DigiBP', 'digibp-camunda-external-python-task', 'cam'): import cam


class RiskClient:
    def __init__(self):
        self.camunda_rest_url = os.environ.get("CAMUNDA_REST_URL", "https://digibp.herokuapp.com/engine-rest")
        self.camunda_tenant_id = os.environ.get("CAMUNDA_TENANT_ID", "showcase")
        self.worker = cam.Client(self.camunda_rest_url)
        self.worker.subscribe("DetermineRisks", self.determine_risks_callback, self.camunda_tenant_id)
        self.worker.subscribe("CalculateRetention", self.calculate_retention_callback, self.camunda_tenant_id)
        self.worker.polling()

    def determine_risks_callback(self, taskid, body):
        age = body[0]['variables']['age']['value']
        kw = body[0]['variables']['kw']['value']
        license_revocation = body[0]['variables']['licenseRevocation']['value']

        request = {"variables": {
            "age": {"value": age, "type": "integer"},
            "kw": {"value": kw, "type": "integer"},
            "licenseRevocation": {"value": license_revocation, "type": "boolean"}
        }}

        endpoint = str(
            self.camunda_rest_url) + "/decision-definition/key/Decision_DetermineRisk/tenant-id/" + self.camunda_tenant_id + "/evaluate"

        response = requests.post(endpoint, json=request)
        response_body = json.loads(response.text)
        risk = response_body[0]['risk']['value']

        variables = {"risk": risk}
        self.worker.complete(taskid, **variables)

    def calculate_retention_callback(self, taskid, body):
        age = body[0]['variables']['age']['value']
        car_price = body[0]['variables']['carPrice']['value']

        request = {"variables": {
            "age": {"value": age, "type": "integer"},
            "carPrice": {"value": car_price, "type": "integer"}
        }}

        endpoint = str(
            self.camunda_rest_url) + "/decision-definition/key/Decision_CalculateRetention/tenant-id/" + self.camunda_tenant_id + "/evaluate"

        response = requests.post(endpoint, json=request)
        response_body = json.loads(response.text)
        retention = response_body[0]['retention']['value']

        variables = {"retention": retention}
        self.worker.complete(taskid, **variables)


if __name__ == '__main__':
    RiskClient()
