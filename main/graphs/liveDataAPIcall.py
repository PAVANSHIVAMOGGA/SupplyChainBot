import requests

def liveDataApiGETCall(url):
    try:       
        response = requests.get(url=url, timeout=50)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as httpError:
        errorBody = response.json()
        errorDetails = errorBody.get("detail", "No error details found")

        return errorDetails

    except requests.exceptions.ConnectionError as error:
        return "The server isn't available at the moment, please try again later."

    except requests.exceptions.RequestException as error:
        return "An unexpected error occurred, please try again later"

import requests

def liveDataApiPOSTCall(url, payload):
    try:       
        response = requests.post(url=url, timeout=50, json=payload)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as httpError:
        errorBody = response.json()
        errorDetails = errorBody.get("detail", "No error details found")

        return errorDetails

    except requests.exceptions.ConnectionError as error:
        return "The server isn't available at the moment, please try again later."

    except requests.exceptions.RequestException as error:
        return "An unexpected error occurred, please try again later"
