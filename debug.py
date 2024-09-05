import http.client
import urllib.parse
import json

def get_access_token():
    print("Starting authentication...")
    conn = http.client.HTTPSConnection("test.salesforce.com")

    params = urllib.parse.urlencode({
        'grant_type': 'password',
        'client_id': '3MVG9S6qnsIUe5wCLCT_QegxuMnskGt17bI3VwTaCw4ize7rlX4CvEYxASZlMuJryRdZ36px1tdBHf8u9Elaq',
        'client_secret': '2D1AC3D4B05396FD55145D7E0ACC6D2AEA16014143CA2434C635EDE6BCD8459C',
        'username': 'corpsys.integration@barclays.com.ucrm.qa',
        'password': 'Integration@2024YourSecurityToken'
    })

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    conn.request("POST", "/services/oauth2/token", params, headers)

    response = conn.getresponse()
    data = response.read()

    auth_response = json.loads(data.decode('utf-8'))

    if 'access_token' in auth_response:
        print("Authentication successful.")
        return auth_response['access_token']
    else:
        raise Exception(f"Failed to retrieve token: {auth_response}")

def fetch_event_log(access_token):
    print("Fetching event log...")
    log_file_url = '/services/data/v62.0/sobjects/EventLogFile/0AT8C000004jlIUWAY/LogFile'

    conn = http.client.HTTPSConnection("barclays-ucrm--qa.sandbox.my.salesforce.com")

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    conn.request("GET", log_file_url, headers=headers)

    response = conn.getresponse()
    log_data = response.read()

    if response.status == 200:
        with open('event_log.csv', 'wb') as file:
            file.write(log_data)
        print("Event Log CSV Content Fetched and saved as event_log.csv")
    else:
        print(f"Failed to fetch event log: {response.status}, {response.reason}")

def main():
    try:
        access_token = get_access_token()
        print(f"Access Token: {access_token}")
        fetch_event_log(access_token)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
