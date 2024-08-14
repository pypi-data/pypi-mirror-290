import requests
import gzip
import json
from io import BytesIO


def fetch_data(simulation_id, file, api_key='', api_url="https://data.ptn.cobrabreiz.services/graphql"):
    payload = ("{\"query\":\" query {\\n    simulationGet(id: \\\"%s\\\") {\\n        id\\n        status\\n        "
               "startDate\\n        stopDate\\n        links\\n        error\\n        friendlyName\\n        "
               "metadata\\n        preview {\\n            data {\\n                id\\n                series {\\n  "
               "                  kind\\n                    rows\\n                }\\n            }\\n        }\\n  "
               "  }\\n}\",\"variables\":{}}") % simulation_id

    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", api_url, headers=headers, data=payload)

    result = response.json()

    time_resul_link = result['data']['simulationGet']['links'][file]

    try:
        response_file = requests.request("GET", time_resul_link)

        buffer_data = BytesIO(response_file.content)

        result_file = gzip.GzipFile(fileobj=buffer_data).read()

        return json.loads(result_file)
    except Exception as e:
        print(f"An exception occurred: {e}")
