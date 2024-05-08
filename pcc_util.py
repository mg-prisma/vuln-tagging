import requests
import json
import sys
import datetime
import csv

# Returns string containing the short lived auth token
def get_token(url_base, access_key_id, access_key_secret):
    url_endpoint = url_base + '/login'
    payload = '{"username": "' + access_key_id + '", "password": "' + access_key_secret + '"}'
    headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json; charset=UTF-8'
    }

    response = requests.request("POST", url_endpoint, headers=headers, data=payload)
    # Parse the JSON string
    data = json.loads(response.text)
    token = ''
    # Check if 'token' key exists
    if 'token' in data:
        # Extract the token value
        token = data['token']
    else:
        # If 'token' key does not exist, exit with error code
        print("Error: 'token' key not found in JSON data.")
        sys.exit(1)
    return token


# Returns json array containing cloud accounts as described 
# in the output here: https://pan.dev/prisma-cloud/api/cspm/get-cloud-accounts/#responses
def get_accounts(url_base, token):
    url_endpoint = url_base + '/cloud'
    payload={}
    headers = {
    'Accept': 'application/json; charset=UTF-8',
    'x-redlock-auth': token
    }

    response = requests.request("GET", url_endpoint, headers=headers, data=payload)
    data = json.loads(response.text)
    return data


# Returns json array containing usage data as described
# here: https://pan.dev/prisma-cloud/api/cspm/license-usage-count-by-cloud-paginated-v-2/
# Note: the output of this function follows 'next_page' and appends everything to a 
# single json output array.
def get_usage_count_past_N_months(url_base, token, n_months=3):
    url_endpoint = url_base + '/license/api/v2/usage'
    payload = '{"accountIds":[],"cloudTypes":["aws","azure","oci","alibaba_cloud","gcp","others"],"accountGroupIds":[],"timeRange":{"type":"relative","value":{"amount":"' + str(n_months) + '","unit":"month"}},"limit":10}'
    headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json;charset=UTF-8',
    'x-redlock-auth': token
    }

    response = requests.request("POST", url_endpoint, headers=headers, data=payload)
    data = json.loads(response.text)
    account_stats = data['items']
    nextPageToken = data['nextPageToken']

    while nextPageToken != '' and nextPageToken is not None:
        payload = '{"accountIds":[],"cloudTypes":["aws","azure","oci","alibaba_cloud","gcp","others"],"accountGroupIds":[],"timeRange":{"type":"relative","value":{"amount":"3","unit":"month"}},"limit":10, "pageToken":"' + nextPageToken + '"}'
        response = requests.request("POST", url_endpoint, headers=headers, data=payload)
        data = json.loads(response.text)
        items = data['items']
        account_stats = account_stats + items
        nextPageToken = data['nextPageToken']

    return account_stats



            
def write_output_file(credits_with_accounts, outfile):
    fieldnames = ['accountName', 'accountId', 'groupName', 'groupId', 'cloudType',
                  'total', 'container', 'iam', 'container_caas', 'data_store',
                  'agentless_host', 'host', 'serverless', 'iaas',
                  'waas', 'agentless_container']
    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for c in credits_with_accounts:
            writer.writerow(c)


