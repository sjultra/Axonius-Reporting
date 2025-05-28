# Axonius Infrastructure as Code Dashboard Exporter

A comprehensive Python tool that exports Axonius dashboards in the exact JSON format required for Infrastructure as Code (IaC) workflows. This tool enables you to version control, backup, and deploy dashboards programmatically across multiple Axonius environments.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Output Files](#output-files)
- [Import Process](#import-process)
- [IaC Workflow](#iac-workflow)
- [API Requirements](#api-requirements)
- [Troubleshooting](#troubleshooting)
- [Version Compatibility](#version-compatibility)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)

## Features

- **✅ Import-Ready Format**: Exports dashboards in Axonius's exact `import_spaces_schema` format
- **✅ Smart Filtering**: Automatically excludes system dashboards that cannot be exported
- **✅ Batch Export**: Export all dashboards or specific ones by name
- **✅ Comprehensive Documentation**: Generates inventory, instructions, and metadata
- **✅ IaC Ready**: Perfect for Git workflows and CI/CD pipelines
- **✅ Rate Limiting**: Built-in delays to respect API limits
- **✅ Error Handling**: Robust error handling with detailed feedback
- **✅ Cross-Platform**: Works on Windows, macOS, and Linux

## Prerequisites

- **Python 3.7+**
- **Active Axonius instance** with API access
- **Valid API credentials** (API Key and Secret)
- **Network access** to your Axonius instance
- **Required permissions** (see [API Requirements](#api-requirements))

## Installation

### 1. Install Required Python Packages

```bash
pip install requests
```

### 2. Download the Script

Save the script as `axonius_iac_exporter.py` or clone this repository:

```bash
# Direct download
curl -O https://github.com/sjultra/Axonius-Reporting/blob/main/axonius_iac_exporter.py

# Or clone repository
git clone https://github.com/sjultra/Axonius-Reporting.git
cd axonius-iac-tools
```

### 3. Make Executable (Optional)

```bash
chmod +x axonius_iac_exporter.py
```

## Quick Start

### 1. Get Your API Credentials

1. Log into Axonius with an account that has API access
2. Navigate to **User Settings** → **API Key** tab
3. Copy your **API Key** and **API Secret**

### 2. Run Your First Export

```bash
# See what dashboards are available
python axonius_iac_exporter.py \
  -a https://your-company.axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --inventory_only

# Export all dashboards
python axonius_iac_exporter.py \
  -a https://your-company.axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --export_all
```

## Usage Examples

### Basic Export Operations

```bash
# Export all available dashboards
python axonius_iac_exporter.py \
  -a https://company.axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --export_all

# Export specific dashboards by name
python axonius_iac_exporter.py \
  -a https://company.axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --dashboards "Security Overview" "Compliance Dashboard" "Asset Inventory"

# Export to custom directory
python axonius_iac_exporter.py \
  -a https://company.axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --export_all \
  -o ./production_dashboards

# Include system dashboards (usually not recommended)
python axonius_iac_exporter.py \
  -a https://company.axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --export_all \
  --include_system
```

### Inventory and Discovery

```bash
# Create inventory without exporting
python axonius_iac_exporter.py \
  -a https://company.axonius.com \
  -k your_api_key \
  -s your_api_secret \
  --inventory_only

# This creates dashboard_inventory.json with metadata about all dashboards
```

### Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `-a, --axonius_url` | ✅ | Axonius instance URL | `https://company.axonius.com` |
| `-k, --api_key` | ✅ | Axonius API Key | `your_api_key_here` |
| `-s, --api_secret` | ✅ | Axonius API Secret | `your_api_secret_here` |
| `--export_all` | ❌ | Export all available dashboards | |
| `--dashboards` | ❌ | Specific dashboard names | `"Dashboard 1" "Dashboard 2"` |
| `--include_system` | ❌ | Include system dashboards | |
| `-o, --output_dir` | ❌ | Output directory | `./my_dashboards` |
| `--inventory_only` | ❌ | Only create inventory | |

## Output Files

When you run the exporter, it creates several files in your output directory:

### 1. Individual Dashboard Files

**Format**: `{dashboard_name}_{timestamp}.json`

```json
{
  "meta": null,
  "data": {
    "type": "import_spaces_schema",
    "attributes": {
      "replace": true,
      "data": {
        // Complete dashboard configuration
        // Ready for import via API or UI
      }
    }
  }
}
```

### 2. Dashboard Inventory

**File**: `dashboard_inventory.json`

```json
{
  "export_metadata": {
    "exported_at": "2025-01-28T10:30:00",
    "axonius_url": "https://company.axonius.com",
    "total_dashboards": 15
  },
  "dashboards": [
    {
      "id": "dashboard_id_123",
      "name": "Security Overview",
      "description": "Main security dashboard",
      "type": "custom",
      "is_system": false,
      "can_export": true,
      "created_date": "2024-12-01T09:00:00",
      "modified_date": "2025-01-15T14:30:00"
    }
  ]
}
```

### 3. Import Instructions

Detailed step-by-step instructions for importing the exported dashboards via UI and API.

## Import Process

### Via Axonius UI

1. **Log into Axonius**
2. **Navigate to Dashboards** page
3. **Click "Add Dashboard"** → **"Import Dashboard"**
4. **Upload JSON file** for the dashboard you want to import
5. **Set dashboard name** and access permissions
6. **Choose import behavior**:
   - **"Overwrite"**: Replace existing dashboards with same name
   - **"Create a Copy"**: Create new dashboards with duplicate names
7. **Click "Save"**

### Via API

```bash
curl -X POST \
  https://your-company.axonius.com/api/dashboard/import \
  -H "Content-Type: application/vnd.api+json" \
  -H "api-key: your_api_key" \
  -H "api-secret: your_api_secret" \
  -d @Security_Overview_20250128_103000.json
```

### Successful Import Response

```json
{
  "inserted_charts": 5,
  "inserted_queries": 3,
  "inserted_spaces": 1,
  "replaced_charts": 0,
  "replaced_queries": 0,
  "replaced_spaces": 0
}
```

## IaC Workflow

### Git-Based Workflow

```bash
# 1. Export dashboards from production
python axonius_iac_exporter.py \
  -a https://prod.axonius.com \
  -k $PROD_API_KEY \
  -s $PROD_API_SECRET \
  --export_all \
  -o ./dashboards/production

# 2. Commit to version control
git add dashboards/
git commit -m "Export production dashboards - $(date)"
git push origin main

# 3. Deploy to other environments
# (Use import automation or manual process)
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
name: Export Axonius Dashboards
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday 2 AM
  workflow_dispatch:

jobs:
  export-dashboards:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install requests
      
      - name: Export dashboards
        run: |
          python axonius_iac_exporter.py \
            -a ${{ secrets.AXONIUS_URL }} \
            -k ${{ secrets.AXONIUS_API_KEY }} \
            -s ${{ secrets.AXONIUS_API_SECRET }} \
            --export_all \
            -o ./dashboards
      
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add dashboards/
          git commit -m "Automated dashboard export - $(date)" || exit 0
          git push
```

### Environment Management

```bash
# Directory structure for multiple environments
dashboards/
├── production/
│   ├── dashboard_inventory.json
│   ├── Security_Overview_20250128.json
│   └── Compliance_Dashboard_20250128.json
├── staging/
│   └── ... 
└── development/
    └── ...
```

## API Requirements

### Required Permissions

Your Axonius user account needs:

- **✅ API Access Enabled** permission
- **✅ View Dashboard** permission  
- **✅ Export Dashboard** permission
- **✅ Unrestricted role** (for export functionality)

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v2/dashboards` | GET | List available dashboards |
| `/api/dashboard/export` | POST | Export dashboard configurations |

### Rate Limiting

The script includes built-in rate limiting:
- **0.5 second delay** between dashboard exports
- **Configurable timeout** (30 seconds default)
- **Graceful error handling** for API limits

## Troubleshooting

### Common Issues

**❌ "You do not have all permissions required for this request"**
```
Solution: Ensure your user has API access and export permissions
Check: User Settings → Roles & Permissions
```

**❌ "Could not find matching spaces"**
```
Solution: Verify dashboard names are exact matches (case-sensitive)
Check: Use --inventory_only to see available dashboard names
```

**❌ "Could not export Default/Personal dashboards"**
```
Solution: This is expected - system dashboards cannot be exported
Action: Use --export_all without --include_system (default behavior)
```

**❌ Connection timeout or network errors**
```
Solution: Check network connectivity to Axonius instance
Check: Verify URL is correct and accessible
```

**❌ JSONDecodeError**
```
Solution: Usually indicates API authentication issues
Check: Verify API key and secret are correct
```

### Debug Mode

Add print statements or use verbose logging:

```python
# Add at the top of the script for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verify API Access

Test your credentials manually:

```bash
curl -X GET \
  "https://your-company.axonius.com/api/v2/dashboards" \
  -H "api-key: your_api_key" \
  -H "api-secret: your_api_secret" \
  -H "Content-Type: application/vnd.api+json"
```

## Version Compatibility

### Axonius Versions

- **✅ Tested**: Axonius 6.0.x and higher
- **⚠️ Note**: Dashboards can only be imported to same major version or higher
- **❌ Limitation**: Dashboard exported from 6.1.x cannot be imported to 6.0.x

### Python Versions

- **✅ Supported**: Python 3.7, 3.8, 3.9, 3.10, 3.11
- **❌ Not Supported**: Python 2.x, Python 3.6 and below

### Cross-Environment Compatibility

| Export From | Import To | Status |
|-------------|-----------|--------|
| Axonius 6.0.x | Axonius 6.0.x | ✅ Supported |
| Axonius 6.0.x | Axonius 6.1.x | ✅ Supported |
| Axonius 6.1.x | Axonius 6.0.x | ❌ Not Supported |

## Security Considerations

### API Credentials

- **🔒 Never commit API credentials** to version control
- **🔒 Use environment variables** or secure credential stores
- **🔒 Rotate API keys regularly**
- **🔒 Use service accounts** for automation (recommended)

### Environment Variables

```bash
# Set environment variables
export AXONIUS_URL="https://company.axonius.com"
export AXONIUS_API_KEY="your_api_key"
export AXONIUS_API_SECRET="your_api_secret"

# Use in script
python axonius_iac_exporter.py \
  -a $AXONIUS_URL \
  -k $AXONIUS_API_KEY \
  -s $AXONIUS_API_SECRET \
  --export_all
```

### Access Control

- **Dashboard access permissions are NOT exported**
- **Set appropriate permissions during import**
- **Review imported dashboards before sharing**
- **Use least-privilege principle for API accounts**

### Network Security

- **Use HTTPS URLs only**
- **Verify SSL certificates**
- **Consider network restrictions** (VPN, firewall rules)

## Advanced Usage

### Custom Output Processing

```python
# Example: Process exported data before saving
import json

def custom_process_dashboard(dashboard_data):
    # Add custom metadata
    dashboard_data['custom_metadata'] = {
        'exported_by': 'automated_script',
        'environment': 'production',
        'compliance_checked': True
    }
    return dashboard_data
```

### Integration with Other Tools

```bash
# Example: Combine with other IaC tools
terraform init
terraform plan -var-file="dashboards.tfvars"

# Example: Integration with Ansible
ansible-playbook deploy-dashboards.yml --extra-vars "dashboard_dir=./dashboards"
```

### Large-Scale Operations

```bash
# For large numbers of dashboards, use parallel processing
# or implement batching in the script

# Export in chunks
python axonius_iac_exporter.py --dashboards "Dashboard 1" "Dashboard 2"
python axonius_iac_exporter.py --dashboards "Dashboard 3" "Dashboard 4"
```

## Contributing

### Development Setup

```bash
git clone https://github.com/your-org/axonius-iac-tools.git
cd axonius-iac-tools
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Testing

```bash
# Test against development environment
python axonius_iac_exporter.py \
  -a https://dev.axonius.com \
  -k $DEV_API_KEY \
  -s $DEV_API_SECRET \
  --inventory_only
```

### Feature Requests

We welcome contributions! Please:

1. **Fork the repository**
2. **Create a feature branch**
3. **Add tests for new functionality**
4. **Submit a pull request**

### Roadmap

- **🚧 Import automation tool**
- **🚧 Template management system**
- **🚧 Diff tool for configuration changes**
- **🚧 Terraform provider integration**
- **🚧 Multi-environment deployment workflows**

## Support

### Documentation

- **Axonius API Documentation**: Contact Axonius support for API v2 access
- **Dashboard Management**: [Axonius Documentation](https://docs.axonius.com/docs/importing-and-exporting-dashboards)

### Issues

For issues related to:

- **Script functionality**: Check troubleshooting section above
- **Axonius API**: Contact Axonius support
- **Feature requests**: Open GitHub issue or contribute

### Example Support Request

```
Subject: Dashboard Export Issue

Environment:
- Axonius Version: 6.1.2
- Python Version: 3.9.7
- Script Version: 1.0
- OS: Ubuntu 20.04

Issue:
Getting "Could not find matching spaces" error when trying to export "Security Overview" dashboard.

Steps to reproduce:
1. Run: python axonius_iac_exporter.py --dashboards "Security Overview"
2. See error in output

Expected: Dashboard should export successfully
Actual: Error message about matching spaces

Additional context:
- API credentials work for inventory_only mode
- Dashboard exists and is visible in UI
- User has export permissions
```
## Changelog

### v1.0.0 
- Initial release
- Dashboard export functionality
- Inventory creation
- Import instructions generation
- Rate limiting and error handling

---