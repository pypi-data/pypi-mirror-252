import requests
import yaml
import re
import os

gitlab_api = 'https://gitlab.atopile.io/api/v4/'

# Typical link
# https://gitlab.atopile.io/packages/RP2040/-/raw/main/README.md
gitlab_packages = 'https://gitlab.atopile.io/packages/'

# Get the list of all projects on our gitlab instance
response = requests.get(f"{gitlab_api}/projects/")
projects = response.json()

# collect the packges that will be added to the docs
packages_to_add = {}
for project in projects:
    if project['namespace']['name'] != 'packages':
        continue
    project_id = project['id']
    project_name = project['name']

    readme_url = f"{gitlab_packages}{project_name}/-/raw/main/README.md"

    readme_response = requests.get(readme_url)
    readme_content = readme_response.text

    # Find the images in the readme
    img_regex = r'!\[.*?\]\((.*?\.(?:png|jpg|jpeg|gif|bmp))\)'
    image_paths = re.findall(img_regex, readme_content)

    if readme_response.status_code == 200:
        # Create a dicretory to store the project
        if not os.path.exists(f"docs/{project_name}"):
            os.makedirs(f"docs/{project_name}")
        with open(f"docs/readme_{project_name}.md", 'w') as file:
            pattern = r'(!\[.*?\]\()(docs/)'

            # Replace 'docs/' with an empty string in image paths
            readme_content = readme_content.replace('](docs/', f']({project_name}/')
            #readme_content = re.sub(pattern, r'\1', readme_content)
            file.write(readme_content)

        packages_to_add[project_name] = f"readme_{project_name}.md"
        # handle the images
        for img_path in image_paths:
            img_url = f"{gitlab_packages}{project_name}/-/raw/main/{img_path}"
            img_response = requests.get(img_url)

            if img_response.status_code == 200:
                file_name = os.path.basename(img_path)
                with open(f"docs/{project_name}/{file_name}", 'wb') as img_file:
                    img_file.write(img_response.content)
            else:
                print(f"Failed to fetch image: {img_path}")
    else:
        print(f"README not found for {project_name}")


def load_yaml_as_dict(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def export_dict_to_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# load the existing mkdocs.yaml
mkdocs_yaml_dict = load_yaml_as_dict('mkdocs.yml')
with open('mkdocs.yml', 'r') as file:
    # load the existing mkdocs.yaml
    mkdocs_yaml_dict = yaml.safe_load(file)
    package_list = []
    for package_name, package_file_path in packages_to_add.items():
        package_list.append({package_name : package_file_path})
    mkdocs_yaml_dict['nav'][1]['Packages'] = package_list

with open('mkdocs.yml', 'w') as file:
    yaml.dump(mkdocs_yaml_dict, file)
