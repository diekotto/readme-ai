"""Configuration constants."""
from dataclasses import dataclass
from pathlib import Path
from typing import List

from file_factory import FileHandler
from logger import Logger

LOGGER = Logger("readme_ai_logger")


@dataclass
class OpenAI:
    """OpenAI API details."""

    api_key: str
    engine: str
    prompt_intro: str
    prompt_slogan: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float


@dataclass
class GitHub:
    """GitHub repository."""

    url: str
    owner: str = ""
    repo_name: str = ""

    def __post_init__(self):
        """Extract owner and repository name from GitHub URL."""
        if self.url.startswith("https://github.com/"):
            path = self.url[len("https://github.com/") :]
            parts = path.split("/")
            if len(parts) >= 2:
                self.owner = parts[0]
                self.repo_name = parts[1]
        else:
            raise ValueError(f"Invalid GitHub URL: {self.url}")


@dataclass
class Markdown:
    """Markdown template code."""

    close: str
    head: str
    intro: str
    dropdown: str
    modules: str
    setup: str
    toc: str
    tree: str


@dataclass
class Paths:
    """Project file paths."""

    badges: str
    docs: str
    md: str


@dataclass
class AppConf:
    """Configuration constants object."""

    api: OpenAI
    github: GitHub
    md: Markdown
    paths: Paths


@dataclass
class AppConfHelper:
    file_names: List[str]
    file_extensions: dict
    setup: dict


def load_conf_helper(conf_path_list: List[str]) -> AppConfHelper:
    handler = FileHandler()
    file_extensions = {}
    file_names = []
    setup = {}

    for path in conf_path_list:
        path = Path("conf/").joinpath(path).resolve()
        conf_dict = handler.read(path)

        if "file_names" in conf_dict:
            file_names.extend(conf_dict["file_names"].get("name", []))

        if "file_extensions" in conf_dict:
            file_extensions.update(conf_dict["file_extensions"])

        if "setup" in conf_dict:
            setup.update(conf_dict["setup"])

    return AppConfHelper(
        file_names=file_names, file_extensions=file_extensions, setup=setup
    )
