# Axonius Device Lookup Tool

A Python script that integrates with the Axonius cybersecurity asset management platform to look up devices and generate direct URLs for viewing device details in the Axonius interface.

## Description

This tool takes a CSV file containing device information (IP addresses, hostnames, and device types) and queries the Axonius API to find corresponding devices. For each device found, it generates a direct URL to the device's detail page in Axonius, making it easy for IT administrators and security teams to quickly access device information.

## Prerequisites

- Python 3.6 or higher
- Active Axonius instance with API access
- Valid Axonius API credentials (API key and secret)
- Network access to your Axonius instance

## Required Python Packages

The script uses only standard Python libraries:
- `csv` (built-in)
- `requests` (may need installation)
- `argparse` (built-in)

Install requests if not already available:
```bash
pip install requests
```

## Installation

1. Download or clone the script to your local machine
2. Ensure Python 3.6+ is installed
3. Install the requests library if needed:
   ```bash
   pip install requests
   ```

## Usage

### Basic Command Structure

```bash
python axonius_lookup.py -f <input_csv> -a <axonius_url> -k <api_key> -s <api_secret> [-o <output_csv>]
```

### Required Arguments

- `-f, --file`: Path to input CSV file containing device information
- `-a, --axonius_url`: Your Axonius instance URL (e.g., `https://your-company.axonius.com`)
- `-k, --api_key`: Your Axonius API key
- `-s, --api_secret`: Your Axonius API secret

### Optional Arguments

- `-o, --output`: Output CSV filename (default: `results.csv`)

### Example Usage

```bash
python axonius_lookup.py \
  -f devices.csv \
  -a https://company.axonius.com \
  -k your_api_key_here \
  -s your_api_secret_here \
  -o device_results.csv
```

## Input CSV Format

The input CSV file must contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| IP | Device IP address | 192.168.1.100 |
| DNS | Device hostname | server01.company.com |
| TYPE | Device type | Server |

### Sample Input CSV

```csv
IP,DNS,TYPE
192.168.1.100,server01.company.com,Server
10.0.0.50,workstation-05.company.com,Workstation
172.16.1.200,printer-lobby.company.com,Printer
```

## Output CSV Format

The output CSV includes all original columns plus a new URL column:

| Column | Description | Example |
|--------|-------------|---------|
| IP | Original IP address | 192.168.1.100 |
| DNS | Original hostname | server01.company.com |
| TYPE | Original device type | Server |
| URL | Axonius device URL or "Not Found" | https://company.axonius.com/assets/devices/abc123 |

## API Authentication

This script uses Axonius API v2 with header-based authentication. You'll need:

1. **API Key**: Obtained from your Axonius admin panel
2. **API Secret**: Obtained from your Axonius admin panel

### Getting API Credentials

1. Log into your Axonius instance as an administrator
2. Navigate to System Settings → API Clients
3. Create a new API client or use existing credentials
4. Copy the API Key and API Secret

## How It Works

1. **CSV Parsing**: Reads the input CSV file and extracts device information
2. **API Query**: For each device, queries Axonius using the hostname with a case-insensitive regex search
3. **Device Matching**: Searches for devices where the hostname matches the DNS column value
4. **URL Generation**: If a device is found, constructs a direct URL using the device's internal UUID
5. **Result Output**: Creates output CSV with original data plus the device URLs

## Error Handling

The script includes comprehensive error handling:

- **File not found**: Clear error message if input CSV doesn't exist
- **API errors**: HTTP status code errors are caught and displayed
- **Network issues**: Connection problems are handled gracefully
- **Missing devices**: Devices not found in Axonius are marked as "Not Found"
- **General exceptions**: Unexpected errors are caught and displayed

## Troubleshooting

### Common Issues

**"Not Found" results**
- Verify hostnames in your CSV match exactly with Axonius records
- Check if devices are actually ingested into Axonius
- Ensure the hostname field in Axonius is populated

**API Authentication Errors**
- Verify API key and secret are correct
- Check that the API client has appropriate permissions
- Ensure your Axonius URL is correct and accessible

**Connection Issues**
- Verify network connectivity to Axonius instance
- Check firewall rules and proxy settings
- Ensure the Axonius URL includes the correct protocol (https://)

**CSV Format Errors**
- Ensure your CSV has the required columns: IP, DNS, TYPE
- Check for proper CSV formatting and encoding
- Verify there are no special characters causing parsing issues

### Debug Steps

1. Test API connectivity manually using curl or Postman
2. Verify CSV format by opening in a text editor
3. Run script with a single-row CSV to isolate issues
4. Check Axonius logs for API query details

## Limitations

- Maximum 1000 devices returned per API query (Axonius API limit)
- Searches only by hostname field in Axonius
- Requires exact hostname matches (with case-insensitive regex)
- Network connectivity required during execution

## Security Considerations

- Store API credentials securely
- Consider using environment variables for sensitive data
- Limit API client permissions to minimum required access
- Use HTTPS URLs for Axonius connections

## Sample Output

```
Hostname: server01.company.com, URL: https://company.axonius.com/assets/devices/abc123
Hostname: workstation-05.company.com, URL: Not Found
Hostname: printer-lobby.company.com, URL: https://company.axonius.com/assets/devices/def456
Results written to results.csv
```

## Version History

- v1.0: Initial release with basic device lookup functionality

## Support

For issues related to:
- **Script functionality**: Review this README and troubleshooting section
- **Axonius API**: Consult Axonius documentation or support
- **Python/technical issues**: Check Python documentation and error messages

## License

This script is provided as-is for educational and operational purposes. Please ensure compliance with your organization's security policies and Axonius terms of service.
