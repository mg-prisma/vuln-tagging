import pcc_util
import requests
import datetime

def main():
    tenant_url_base = 'https://api[STACK-NUMBER].prismacloud.io' #e.g., api.prismacloud.io, api2.prismacloud.io
    compute_url_base = 'https://us-east1.cloud.twistlock.com/[COMPUTE ENDPOINT]'
    access_key_id = ''
    access_key_secret = ''
    token = pcc_util.get_token(tenant_url_base, access_key_id, access_key_secret)
    
    latest_image_scan_results = download_image_scans(compute_url_base, token)

    # Write the output to a CSV file
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H%M%S")
    outfile = 'image_scans_' + formatted_time + '.csv'
    with open(outfile, 'w', newline='') as csvfile:
        csvfile.write(latest_image_scan_results)
    print("Wrote credit data to %s" % (outfile))


def download_image_scans(url_base, token):
    # download image scan results
    # https://pan.dev/prisma-cloud/api/cwpp/get-images-download/
    url = url_base + "/api/v32.04/images/download"

    payload={}
    headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json;charset=UTF-8',
    'x-redlock-auth': token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    main()