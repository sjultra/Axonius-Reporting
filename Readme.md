# Axonius Reporting Tools

A collection of Python tools for automating Axonius cybersecurity asset management workflows, including Infrastructure as Code (IaC) dashboard management and device operations.

## Repository Structure

```
axonius-reporting/
├── Dashboard-Export/           # IaC Dashboard Management
│   ├── axonius_iac_exporter.py    # Dashboard export tool
│   ├── Readme.md                  # Dashboard export documentation
│   └── requirements.txt           # Python dependencies
├── Device-Lookup/              # Device Operations
│   ├── script.py                  # Device lookup and URL generation
│   └── Readme.md                  # Device lookup documentation
└── Readme.md                   # This file - repository overview
```

## Tools Overview

### 🔧 Dashboard-Export
**Infrastructure as Code for Axonius Dashboards**

- **Purpose**: Export dashboards as JSON for version control and automated deployment
- **Use Case**: Dashboard backup, migration between environments, IaC workflows
- **Main Script**: `axonius_iac_exporter.py`
- **Key Features**:
  - Export dashboards in Axonius-compatible JSON format
  - Batch export capabilities
  - Dashboard inventory generation
  - Import instructions and automation-ready outputs

### 🔍 Device-Lookup
**Device Discovery and URL Generation**

- **Purpose**: Look up devices in Axonius and generate direct access URLs
- **Use Case**: Asset investigation, reporting, device management workflows
- **Main Script**: `script.py`
- **Key Features**:
  - CSV-based device input processing
  - Hostname-based device lookup via API
  - Direct URL generation for Axonius device pages
  - Bulk processing with error handling

## Quick Start

### Prerequisites
- Python 3.7+
- Axonius instance with API access
- Valid API credentials (API Key and Secret)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd axonius-reporting

# Choose your tool and install dependencies
cd Dashboard-Export/  # or Device-Lookup/
pip install -r requirements.txt
```

### Usage Examples

**Dashboard Export:**
```bash
cd Dashboard-Export/
python axonius_iac_exporter.py \
  -a https://your-axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --export_all
```

**Device Lookup:**
```bash
cd Device-Lookup/
python script.py \
  -f devices.csv \
  -a https://your-axonius.com \
  -k your_api_key \
  -s your_api_secret
```

## Getting API Credentials

1. Log into Axonius with an account that has API access
2. Navigate to **User Settings** → **API Key** tab
3. Copy your **API Key** and **API Secret**

## Documentation

Each tool includes comprehensive documentation:

- **Dashboard-Export/Readme.md**: Complete IaC workflow guide, API requirements, troubleshooting
- **Device-Lookup/Readme.md**: Device lookup operations, CSV format requirements, use cases

## Common Use Cases

### Dashboard Management (IaC)
- **Backup and Recovery**: Export production dashboards for backup
- **Environment Promotion**: Deploy dashboards from dev → staging → production
- **Version Control**: Track dashboard changes in Git
- **Template Management**: Create reusable dashboard patterns
- **Compliance**: Audit and document dashboard configurations

### Device Operations
- **Incident Response**: Quickly generate URLs for suspected devices
- **Asset Auditing**: Process lists of devices for compliance checking
- **Reporting**: Create reports with direct links to device details
- **Integration**: Connect Axonius data with external tools and workflows

## Security Considerations

- **Never commit API credentials** to version control
- **Use environment variables** for sensitive data
- **Follow least-privilege principle** for API accounts
- **Rotate API keys regularly**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add appropriate documentation
4. Test with your Axonius environment
5. Submit a pull request

## Support

For issues:
- Check the tool-specific README files for troubleshooting
- Verify API credentials and permissions
- Contact Axonius support for API-related questions

---

