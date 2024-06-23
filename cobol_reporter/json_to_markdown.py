import json

def json_to_markdown(json_data):
    """Convert JSON data to Markdown format."""
    markdown_lines = []

    def parse_dict(data, indent=0):
        for key, value in data.items():
            prefix = " " * indent
            if isinstance(value, dict):
                # Print the key and recursively parse its dictionary value
                markdown_lines.append(f"{prefix}### {key.capitalize()}")
                parse_dict(value, indent + 4)
            elif isinstance(value, list):
                # Print the key and iterate its list value
                markdown_lines.append(f"{prefix}### {key.capitalize()}")
                for item in value:
                    if isinstance(item, dict):
                        parse_dict(item, indent + 4)
                    else:
                        markdown_lines.append(f"{prefix}- {item}")
            else:
                # Print the key-value pair
                markdown_lines.append(f"{prefix}- **{key.capitalize()}:** {value}")

    # Start parsing the root of the JSON data
    parse_dict(json_data)
    
    return "\n".join(markdown_lines)

def load_json_file(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

# Main script
if __name__ == "__main__":
    json_file_path = 'results.jsonlines'
    json_data = load_json_file(json_file_path)
    markdown_content = json_to_markdown(json_data)
    
    with open('output.md', 'w') as markdown_file:
        markdown_file.write(markdown_content)
    
    print("Markdown content generated and saved to output.md")