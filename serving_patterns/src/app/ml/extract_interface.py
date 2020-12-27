import yaml
from typing import Dict, Any


def extract_interface_yaml(filepath: str) -> Dict[str, Any]:
    with open(filepath, "r") as f:
        interface = yaml.load(f, Loader=yaml.SafeLoader)
    model_name = list(interface.keys())[0]
    interface[model_name]["data_interface"]["input_shape"] = tuple(interface[model_name]["data_interface"]["input_shape"])
    interface[model_name]["data_interface"]["output_shape"] = tuple(interface[model_name]["data_interface"]["output_shape"])
    return interface
