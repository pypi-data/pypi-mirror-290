import os
import requests

def get_syncro_customers_managed():
    syncro_api_key = os.environ.get('SYNCRO_API_KEY_ALL')
    syncro_api_baseurl = os.environ.get('SYNCRO_API_BASEURL')

    if syncro_api_key is None or syncro_api_baseurl is None:
        return "Missing API Key or Base URL"

    syncro_api_url = syncro_api_baseurl + 'customers'
    headers = {
        'Authorization': 'Bearer ' + syncro_api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(syncro_api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        all_customers = response.json()
        managed_customers = []

        for customer in all_customers:
            # Check if 'properties' exist in customer and 'Managed Status' is correct
            if 'properties' in customer and customer['properties'].get("Managed Status") == 35984:
                managed_customers.append(customer)

        return managed_customers

    except requests.exceptions.RequestException as e:
        return f"Error fetching data from Syncro API: {e}"

    except Exception as ex:
        return f"Unexpected error: {ex}"