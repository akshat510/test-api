import http.client
import urllib.parse
import json

def get_access_token():
    print("Starting authentication...")
    try:
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

        print(f"Request parameters: {params}")

        conn.request("POST", "/services/oauth2/token", params, headers)
        response = conn.getresponse()

        print(f"HTTP Response Status: {response.status}")
        print(f"HTTP Response Reason: {response.reason}")

        data = response.read()
        print(f"Response Data: {data.decode('utf-8')}")

        auth_response = json.loads(data.decode('utf-8'))

        if 'access_token' in auth_response:
            print("Authentication successful.")
            return auth_response['access_token']
        else:
            print("Authentication response:", auth_response)
            raise Exception(f"Failed to retrieve token: {auth_response}")
    except Exception as e:
        print(f"Error during authentication: {e}")

def main():
    try:
        access_token = get_access_token()
        if access_token:
            print(f"Access Token: {access_token}")
            # Proceed to fetch event log if necessary
        else:
            print("No access token retrieved.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
