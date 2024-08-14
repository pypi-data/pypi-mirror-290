import typer
from rockai.server.http import start_server
from rockai.server.utils import is_valid_name
from pathlib import Path
from rockai.parser.config_util import parse_config_file
from typing_extensions import Annotated
from rockai.docker.docker_util import build_final_image
import os
import shutil
import requests
import subprocess
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

app = typer.Typer()

APP_NAME = "rockai"


@app.callback()
def callback():
    """
    Callback for the CLI app before any command
    """
    typer.echo("Callback excuted")


@app.command()
def init():
    file = open("rock.yaml", "w")
    file.close()
    file = open("predict.py", "w")
    file.close()


@app.command(name="build")
def build():
    """
    Build the image
    """
    if not os.path.exists(Path.cwd() / "temp"):
        os.makedirs(Path.cwd() / "temp")
        print(f"Folder '{Path.cwd() / 'temp'}' created.")
    else:
        print(f"Folder '{Path.cwd() / 'temp'}' already exists.")

    config_path: Path = Path.cwd() / "rock.yaml"
    if not config_path.is_file():
        raise Exception("rock.yaml config file doesn't exist in the current directory")
    else:
        print("rock.yaml config file exist")

    config_map = parse_config_file(config_path)
    logger.debug(config_map)
    if not is_valid_name(config_map["image"].split("/")[-1]):
        print("Invalid model name, please rename your model accordingly to the following rules")
        print("1. contain no more than 253 characters\n2. contain only lowercase alphanumeric characters,and '-'\n3. start with an alphanumeric character\n4. end with an alphanumeric character")
        raise Exception(
            "Invalid model name: {}".format(config_map["image"].split("/")[-1])
        )
    try:
        # Copy the content of file_1 to file_2
        if "python_requirements" in config_map["build"]:
            shutil.copyfile(
                Path.cwd() / config_map["build"]["python_requirements"],
                Path.cwd() / "temp" / "requirements.txt",
            )
            config_map["build"]["python_requirements"] = "temp/requirements.txt"

    except FileNotFoundError as e:
        raise FileNotFoundError("Source file not found") from e
    except Exception as e:
        raise Exception(f"An error occurred: {e}") from e

    build_final_image(config_map=config_map, port=8000)


@app.command()
def start():
    """
    start local development server
    """
    start_server(8000)


@app.command("push")
def push_model():
    """
    Push the model to the RockAI platform
    """
    build()
    config_path: Path = Path.cwd() / "rock.yaml"
    if not config_path.is_file():
        raise Exception("rock.yaml config file doesn't exist in the current directory")
    else:
        print("rock.yaml config file exist")

    config_map = parse_config_file(config_path)
    subprocess.run(["docker", "image", "push", "{}".format(config_map["image"])])


@app.command(name="login")
def login_to_docker(api_token: Annotated[str, typer.Argument(help="Your API token")]):
    url = "https://api.rockai.online/v1/user/docker_token"
    headers = {"Authorization": "Bearer {}".format(api_token)}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    subprocess.run(
        [
            "docker",
            "login",
            "r.18h.online",
            "-u",
            response.json()["data"]["docker_robot_account"],
            "-p",
            response.json()["data"]["docker_token"],
        ]
    )
