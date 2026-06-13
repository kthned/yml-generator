"""
YAML Generator Prototype version 2

Reads Excel file and generates YAML file based on template.
"""

import pandas as pd
from jinja2 import Environment, FileSystemLoader


# -----------------------------
# Step 1: Load Excel Data
# -----------------------------
def load_excel(file_path):
    """
    Reads Excel and returns structured data for all sheets.
    """

    # VLAN sheet (already exists)
    vlans_df = pd.read_excel(file_path, sheet_name="vlans")

    # New MAC Address sheet
    mac_df = pd.read_excel(file_path, sheet_name="mac_addresses")

    return {
        "vlans": vlans_df.to_dict(orient="records"),
        "mac_addresses": mac_df.to_dict(orient="records"),
    }

# -----------------------------
# Step 2: Generate YAML
# -----------------------------
def generate_yaml(data, template_path, output_path):
    """
    Uses Jinja2 template to generate YAML.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_path)

    rendered_yaml = template.render(data=data)

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
    print (data)
    print(f"Loaded {len(data['vlans'])} VLAN entries")
    print(f"Loaded {len(data['mac_addresses'])} MAC entries")

    print("Generating YAML...")
    generate_yaml(data, "template.j2", output_file)

    print(f"✅ YAML generated: {output_file}")


if __name__ == "__main__":
    main()