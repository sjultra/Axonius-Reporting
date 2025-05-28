#!/usr/bin/env python3
"""
Axonius Infrastructure as Code Dashboard Exporter
Exports dashboards in the exact JSON format that Axonius can import
"""

import json
import os
import requests
import argparse
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class AxoniusIaCExporter:
    def __init__(self, axonius_url: str, api_key: str, api_secret: str):
        self.axonius_url = axonius_url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json', 
            'api-key': api_key,
            'api-secret': api_secret
        })
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> Optional[dict]:
        """Make authenticated request to Axonius API"""
        url = f"{self.axonius_url}/api/{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed for {endpoint}: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def get_dashboard_list(self) -> List[Dict[str, Any]]:
        """Get list of all available dashboards"""
        print("Fetching dashboard list...")
        
        # This might need to be adjusted based on actual API endpoint
        # Using the v2 API structure from the search results
        data = self._make_request('v2/dashboards')
        
        if data and 'data' in data:
            dashboards = data['data']
            print(f"Found {len(dashboards)} dashboards")
            return dashboards
        
        print("No dashboards found or error occurred")
        return []
    
    def export_dashboard(self, dashboard_names: List[str]) -> Optional[Dict[str, Any]]:
        """Export specific dashboards using Axonius API"""
        print(f"Exporting dashboards: {dashboard_names}")
        
        # Using the exact format from the documentation
        export_request = {
            "meta": None,
            "data": {
                "type": "export_spaces_schema",
                "attributes": {
                    "spaces": dashboard_names
                }
            }
        }
        
        response = self._make_request('dashboard/export', method='POST', data=export_request)
        
        if response:
            print(f"Successfully exported {len(dashboard_names)} dashboard(s)")
            return response
        else:
            print("Failed to export dashboards")
            return None
    
    def save_dashboard_config(self, dashboard_data: Dict[str, Any], output_dir: str, 
                            dashboard_name: str) -> str:
        """Save dashboard data as importable JSON file"""
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Sanitize filename
        safe_name = dashboard_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Save in the exact format Axonius expects for import
        import_ready_data = {
            "meta": None,
            "data": {
                "type": "import_spaces_schema", 
                "attributes": {
                    "replace": True,  # Set to False if you don't want to overwrite
                    "data": dashboard_data
                }
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(import_ready_data, f, indent=2, default=str)
        
        print(f"Dashboard saved to: {filepath}")
        return filepath
    
    def export_all_dashboards(self, output_dir: str = "./axonius_dashboards", 
                            exclude_system: bool = True) -> List[str]:
        """Export all dashboards as individual JSON files"""
        
        dashboards = self.get_dashboard_list()
        if not dashboards:
            print("No dashboards found to export")
            return []
        
        exported_files = []
        
        for dashboard in dashboards:
            dashboard_name = dashboard.get('name', dashboard.get('id', 'unknown'))
            
            # Skip system dashboards if requested
            if exclude_system:
                if dashboard_name in ['My Dashboard', 'Axonius Dashboard']:
                    print(f"Skipping system dashboard: {dashboard_name}")
                    continue
                
                # Check if it's a system dashboard by other indicators
                if dashboard.get('type') == 'system' or dashboard.get('is_system', False):
                    print(f"Skipping system dashboard: {dashboard_name}")
                    continue
            
            print(f"Exporting dashboard: {dashboard_name}")
            
            # Export single dashboard
            export_data = self.export_dashboard([dashboard_name])
            
            if export_data:
                # Save as importable file
                filepath = self.save_dashboard_config(
                    export_data, 
                    output_dir, 
                    dashboard_name
                )
                exported_files.append(filepath)
                
                # Add delay to avoid rate limiting
                time.sleep(0.5)
            else:
                print(f"Failed to export dashboard: {dashboard_name}")
        
        return exported_files
    
    def export_dashboard_by_names(self, dashboard_names: List[str], 
                                output_dir: str = "./axonius_dashboards") -> List[str]:
        """Export specific dashboards by name"""
        
        exported_files = []
        
        for dashboard_name in dashboard_names:
            print(f"Exporting dashboard: {dashboard_name}")
            
            export_data = self.export_dashboard([dashboard_name])
            
            if export_data:
                filepath = self.save_dashboard_config(
                    export_data, 
                    output_dir, 
                    dashboard_name
                )
                exported_files.append(filepath)
            else:
                print(f"Failed to export dashboard: {dashboard_name}")
            
            time.sleep(0.5)  # Rate limiting
        
        return exported_files
    
    def create_dashboard_inventory(self, output_dir: str = "./axonius_dashboards") -> str:
        """Create an inventory file listing all available dashboards"""
        
        dashboards = self.get_dashboard_list()
        
        inventory = {
            "export_metadata": {
                "exported_at": datetime.now().isoformat(),
                "axonius_url": self.axonius_url,
                "total_dashboards": len(dashboards)
            },
            "dashboards": []
        }
        
        for dashboard in dashboards:
            dashboard_info = {
                "id": dashboard.get('id'),
                "name": dashboard.get('name'),
                "description": dashboard.get('description', ''),
                "type": dashboard.get('type', 'custom'),
                "is_system": dashboard.get('is_system', False),
                "created_date": dashboard.get('created_date'),
                "modified_date": dashboard.get('modified_date'),
                "can_export": not dashboard.get('is_system', False) and 
                            dashboard.get('name') not in ['My Dashboard', 'Axonius Dashboard']
            }
            inventory["dashboards"].append(dashboard_info)
        
        # Save inventory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        inventory_file = os.path.join(output_dir, 'dashboard_inventory.json')
        
        with open(inventory_file, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=2, default=str)
        
        print(f"Dashboard inventory saved to: {inventory_file}")
        return inventory_file
    
    def create_import_instructions(self, exported_files: List[str], output_dir: str) -> str:
        """Create instructions for importing the exported dashboards"""
        
        instructions = f"""# Axonius Dashboard Import Instructions

## Exported Files
{len(exported_files)} dashboard(s) exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## How to Import via UI

1. Log into your Axonius instance
2. Navigate to Dashboards page
3. Click "Add Dashboard" → "Import Dashboard"
4. Upload the JSON file for the dashboard you want to import
5. Set dashboard name and access permissions
6. Choose import behavior:
   - "Overwrite" to replace existing dashboards with same name
   - "Create a Copy" to create new dashboards with duplicate names

## How to Import via API

Use the following curl command template:

```bash
curl -X POST \\
  {self.axonius_url}/api/dashboard/import \\
  -H "Content-Type: application/vnd.api+json" \\
  -H "api-key: YOUR_API_KEY" \\
  -H "api-secret: YOUR_API_SECRET" \\
  -d @dashboard_file.json
```

## Files Exported:

"""
        
        for i, filepath in enumerate(exported_files, 1):
            filename = os.path.basename(filepath)
            instructions += f"{i}. {filename}\n"
        
        instructions += f"""
## Important Notes

- Access permissions are NOT included in exports and must be set during import
- Dashboards can only be imported to same major version or higher
- System dashboards (My Dashboard, etc.) cannot be exported
- Consider testing imports in a development environment first

## Version Compatibility

Exported from: {self.axonius_url}
Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

These dashboards should be importable to Axonius instances running the same version or higher.
"""
        
        instructions_file = os.path.join(output_dir, 'IMPORT_INSTRUCTIONS.md')
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"Import instructions saved to: {instructions_file}")
        return instructions_file

def parse_arguments():
    parser = argparse.ArgumentParser(description='Export Axonius dashboards for Infrastructure as Code')
    parser.add_argument('-a', '--axonius_url', help='Axonius API URL', required=True)
    parser.add_argument('-k', '--api_key', help='Axonius API Key', required=True)
    parser.add_argument('-s', '--api_secret', help='Axonius API Secret', required=True)
    
    # Export options
    parser.add_argument('--export_all', action='store_true', 
                       help='Export all available dashboards')
    parser.add_argument('--dashboards', nargs='+', 
                       help='Specific dashboard names to export')
    parser.add_argument('--include_system', action='store_true',
                       help='Include system dashboards in export (usually not recommended)')
    
    # Output options
    parser.add_argument('-o', '--output_dir', default='./axonius_dashboards',
                       help='Output directory for exported files')
    parser.add_argument('--inventory_only', action='store_true',
                       help='Only create dashboard inventory, don\'t export dashboards')
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Initialize exporter
    exporter = AxoniusIaCExporter(
        axonius_url=args.axonius_url,
        api_key=args.api_key,
        api_secret=args.api_secret
    )
    
    try:
        # Create dashboard inventory
        print("Creating dashboard inventory...")
        exporter.create_dashboard_inventory(args.output_dir)
        
        if args.inventory_only:
            print("Inventory only mode - done!")
            return
        
        exported_files = []
        
        if args.export_all:
            print("Exporting all dashboards...")
            exported_files = exporter.export_all_dashboards(
                output_dir=args.output_dir,
                exclude_system=not args.include_system
            )
        
        elif args.dashboards:
            print(f"Exporting specific dashboards: {args.dashboards}")
            exported_files = exporter.export_dashboard_by_names(
                dashboard_names=args.dashboards,
                output_dir=args.output_dir
            )
        
        else:
            print("Please specify --export_all or --dashboards <names>")
            return
        
        if exported_files:
            print(f"\nSuccessfully exported {len(exported_files)} dashboard(s)")
            
            # Create import instructions
            exporter.create_import_instructions(exported_files, args.output_dir)
            
            print(f"\nAll files saved to: {args.output_dir}")
            print("\nNext steps:")
            print("1. Review the dashboard_inventory.json file")
            print("2. Check the exported JSON files")
            print("3. Read IMPORT_INSTRUCTIONS.md for import guidance")
            print("4. Test imports in a development environment first")
        else:
            print("No dashboards were exported")
    
    except Exception as e:
        print(f"Export failed: {e}")

if __name__ == "__main__":
    main()