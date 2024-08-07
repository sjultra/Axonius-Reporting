
import csv
import requests
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Check hostnames in Axonius and get device URLs.')
    parser.add_argument('-f', '--file', help='CSV file with IP, DNS, TYPE.', required=True)
    parser.add_argument('-a', '--axonius_url', help='Axonius API URL.', required=True)
    parser.add_argument('-k', '--api_key', help='Axonius API Key.', required=True)
    parser.add_argument('-s', '--api_secret', help='Axonius API Secret.', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file with results.', default='results.csv')
    return parser.parse_args()

def get_axonius_uuid(axonius_url, api_key, api_secret, hostname):
    url = f"{axonius_url}/api/v2/assets/devices"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'api-key': api_key,
        'api-secret': api_secret
    }
    payload = {
        "include_metadata": True,
        "page": { "limit": 1000 },
        "use_cache_entry": True,
        "include_details": True,
        "query": f"(\"specific_data.data.hostname\" == regex(\"{hostname}\", \"i\"))"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    if len(data['assets']) > 0:
        return data['assets'][0]['internal_axon_id']
    return 'Not Found'

def read_csv(file):
    devices = []
    with open(file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            devices.append(row)
    return devices

def write_csv(file, devices):
    with open(file, mode='w', newline='') as csvfile:
        fieldnames = ['IP', 'DNS', 'TYPE', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for device in devices:
            writer.writerow(device)
def main():
    args = parse_arguments()
    
    axonius_url=args.axonius_url
    api_key=args.api_key
    api_secret=args.api_secret
    file=args.file
    output=args.output

    devices = read_csv(file)
    for device in devices:
        hostname = device['DNS']
        uuid = get_axonius_uuid(axonius_url, api_key, api_secret, hostname)
        if uuid != 'Not Found':
            device_url = f"{axonius_url}/assets/devices/{uuid}"
            device['URL'] = device_url
        else:
            device['URL'] = 'Not Found'
        print(f"Hostname: {hostname}, URL: {device['URL']}")
    
    write_csv(output, devices)
    print(f"Results written to {output}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
