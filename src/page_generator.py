import os
from src.markdown_to_html_node import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split('\n')
    if markdown.strip() == "":
        raise Exception("Markdown content is empty.")
    if not lines[0].startswith('# '):
        raise Exception("Markdown content does not start with a title.")
    return lines[0][2:].strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    markdown_content = ""
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)
    
    template_content = ""
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    # Create any necessary directories for dest_path if they don't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                relative_path = os.path.relpath(root, dir_path_content)
                from_path = os.path.join(root, file)
                dest_subdir = os.path.join(dest_dir_path, relative_path)
                dest_path = os.path.join(dest_subdir, file[:-3] + '.html')  # Change .md to .html
                generate_page(from_path, template_path, dest_path)
