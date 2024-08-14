
def recursive_chomp(data):
    if isinstance(data, str) and data.endswith("\n"):
        data = data[:-1]
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = recursive_chomp(data[i])
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = recursive_chomp(value)
    return data

#    @staticmethod
#    def load_yaml(path):
#        from ruamel.yaml import YAML
#        data = recursive_chomp(YAML(typ='safe').load(yaml))

