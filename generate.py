"""
YAML Generator Prototype version 2

Reads Excel file and generates YAML file based on template.
"""

import pandas as pd
from jinja2 import Environment, FileSystemLoader

def debug_data(data):
    print("DEBUG: Data structure:")
    for key, value in data.items():
        print(f"{key}: {len(value)} entries") 

def debug_print(data):
    print("DEBUG: Data content:")
    for key, value in data.items():
        print(f"{key}:")
        for item in value:
            print(f"  - {item}")  

def calculate_l3_handoff(site_id):
    """
    Generates L3 handoff IP from site ID.
    Example:
    site_id = 40 → 10.40.40.1/30
    """
    return f"10.{site_id}.{site_id}.1/30"

# -----------------------------
# Step 1: Load Excel Data
# -----------------------------
def load_excel(file_path):
    """
    Reads Excel and returns structured data for all sheets.
    """

    def normalize(df):
        df.columns = df.columns.str.strip().str.lower()
        return df

    # VLAN sheet (already exists)
    vlans_df = normalize(pd.read_excel(file_path, sheet_name="vlans"))

    # New MAC Address sheet
    mac_df = normalize(pd.read_excel(file_path, sheet_name="mac_addresses"))
    #site_infor sheet 
    site_df = normalize(pd.read_excel(file_path, sheet_name="site_info"))
    return {
        "vlans": vlans_df.to_dict(orient="records"),
        "mac_addresses": mac_df.to_dict(orient="records"),
        "site_info": site_df.to_dict(orient="records")[0]  # Assuming only one row for site_info   
    }

# -----------------------------
# Step 2: Generate YAML
# -----------------------------
def generate_yaml(mdata, template_path, output_path):
    """
    Uses Jinja2 template to generate YAML.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_path)

    #debug_data(data)  # Debugging: Print data structure before rendering
    debug_print(mdata)  # Debugging: Print data content before rendering
    rendered_yaml = template.render(data=mdata)

    with open(output_path, "w") as f:
        f.write(rendered_yaml)


# -----------------------------
# Main Execution
# -----------------------------
def main():
    input_file = "input/site_data.xlsx"
    output_file = "output/generated.yml"

    print("Loading Excel...")
    data = load_excel(input_file)


    # Extract site_id
    site_id = int(data["site_info"]["site_id"])
    # Calculate L3 IP
    l3_ip = calculate_l3_handoff(site_id)
    # Add to data dictionary
    data["site_info"]["l3_handoff"] = l3_ip

    print (data)
    print(f"Loaded {len(data['vlans'])} VLAN entries")
    print(f"Loaded {len(data['mac_addresses'])} MAC entries")

    print("Generating YAML...")
    generate_yaml(data, "template.j2", output_file)

    print(f"✅ YAML generated: {output_file}")


if __name__ == "__main__":
    main()