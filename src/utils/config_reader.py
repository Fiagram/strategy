import argparse
import yaml

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fiagram Strategy gRPC Server")
    parser.add_argument(
        "--config",
        default="configs/local.yaml",
        help=f"Path to YAML config file (default: {"configs/local.yaml"})",
    )
    return parser.parse_args()

def load_yaml_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)