import yaml
from pathlib import Path

get_path = Path.absolute() / "data" / "config.yml"
dir_path = Path(get_path).parent
dir_path.mkdir(parents=True, exist_ok=True)

with open(get_path, "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    if data is None:
        yaml.dump({}, file)
        data = {}
        print("Generated config.yml file.")
    token = data.get("token")
