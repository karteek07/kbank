import yaml

with open("./static/yaml/paths.yaml", "r") as file:
    data = yaml.safe_load(file)

files = data['files']
routes = data['routes']

# print(routes)