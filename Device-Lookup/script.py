import csv
import requests
import argparse
import re
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Check hostnames in Axonius and get device URLs.')
    parser.add_argument('-f', '--file', help='CSV file with IP, DNS, TYPE.', required=True)
    parser.add_argument('-a', '--axonius_url', help='Axonius API URL.', required=True)
    parser.add_argument('-k', '--api_key', help='Axonius API Key.', required=True)
    parser.add_argument('-s', '--api_secret', help='Axonius API Secret.', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file with results.', default='results.csv')
    parser.add_argument('--delay', help='Delay between API calls in seconds.', type=float, default=0.1)
    return parser.parse_args()

def escape_regex_chars(hostname):
    """Escape special regex characters in hostname"""
    return re.escape(hostname)

def get_axonius_uuid(axonius_url, api_key, api_secret, hostname):
    url = f"{axonius_url}/api/v2/assets/devices"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'api-key': api_key,
        'api-secret': api_secret
    }
    
    # Escape special regex characters in hostname
    escaped_hostname = escape_regex_chars(hostname)
    
    payload = {
        "include_metadata": True,
        "page": { "limit": 1000 },
        "use_cache_entry": True,
        "include_details": True,
        "query": f"(\"specific_data.data.hostname\" == regex(\"{escaped_hostname}\", \"i\"))"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'assets' in data and len(data['assets']) > 0:
            return data['assets'][0]['internal_axon_id']
        return 'Not Found'
        
    except requests.exceptions.Timeout:
        print(f"Timeout error for hostname: {hostname}")
        return 'Timeout Error'
    except requests.exceptions.RequestException as e:
        print(f"API error for hostname {hostname}: {e}")
        return 'API Error'
    except KeyError as e:
        print(f"Unexpected API response format for hostname {hostname}: {e}")
        return 'Response Error'

def read_csv(file):
    devices = []
    try:
        with open(file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                devices.append(row)
        return devices
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def write_csv(file, devices):
    try:
        with open(file, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['IP', 'DNS', 'TYPE', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device in devices:
                writer.writerow(device)
        return True
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return False

def main():
    args = parse_arguments()
    
    axonius_url = args.axonius_url.rstrip('/')  # Remove trailing slash
    api_key = args.api_key
    api_secret = args.api_secret
    file = args.file
    output = args.output
    delay = args.delay
    
    devices = read_csv(file)
    if devices is None:
        return
    
    if not devices:
        print("No devices found in CSV file.")
        return
    
    print(f"Processing {len(devices)} devices...")
    
    for i, device in enumerate(devices, 1):
        if 'DNS' not in device:
            print(f"Warning: No 'DNS' column found for row {i}")
            device['URL'] = 'Missing DNS Column'
            continue
            
        hostname = device['DNS'].strip()
        if not hostname:
            print(f"Warning: Empty hostname for row {i}")
            device['URL'] = 'Empty Hostname'
            continue
            
        print(f"Processing {i}/{len(devices)}: {hostname}")
        
        uuid = get_axonius_uuid(axonius_url, api_key, api_secret, hostname)
        
        if uuid not in ['Not Found', 'Timeout Error', 'API Error', 'Response Error']:
            device_url = f"{axonius_url}/assets/devices/{uuid}"
            device['URL'] = device_url
        else:
            device['URL'] = uuid
            
        print(f"  Result: {device['URL']}")
        
        # Add delay between API calls to avoid rate limiting
        if i < len(devices):  # Don't delay after the last item
            time.sleep(delay)
    
    if write_csv(output, devices):
        print(f"\nResults written to {output}")
    else:
        print(f"\nError: Failed to write results to {output}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")