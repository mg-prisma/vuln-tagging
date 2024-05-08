import pcc_util
import requests
import datetime
import json

def main():
    tenant_url_base = 'https://api[STACK-NUMBER].prismacloud.io' #e.g., api.prismacloud.io, api2.prismacloud.io
    compute_url_base = 'https://us-east1.cloud.twistlock.com/[COMPUTE ENDPOINT]'
    access_key_id = ''
    access_key_secret = ''
    token = pcc_util.get_token(tenant_url_base, access_key_id, access_key_secret)
    
    response_code = set_tag_vuln(compute_url_base, token, "CVE-2021-33195")


def set_tag_vuln(url_base, token, cve_id):
    # first, create the tag with the current timestamp
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y_%m_%d_%H%M%S")
    first_seen_tag = "first_seen_" + formatted_time
    url = url_base + "/api/v32.04/tags"
    #payload = json.dumps({"name": first_seen_tag})
    payload = json.dumps({"name": first_seen_tag,
                          "vulns":[{"id":cve_id,
                         "packageName":"*",
                         "resourceType":"image", # "host", "function",
                         #"resources":["alpine:3.7"],
                         "resources":["*"],
                         "comment":""}]})
    headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json;charset=UTF-8',
    'x-redlock-auth': token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(response.status_code)

    return


if __name__ == '__main__':
    main()