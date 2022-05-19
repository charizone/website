import os.path

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File

NAVTYPES = (
    "articles",
    "footernav",
)


class CZBlog(BasePlugin):

    config_scheme = (
        ("articles", config_options.Type(list, default=list())),
        ("footernav", config_options.Type(list, default=list())),
        ("privacy", config_options.Type(str, default=None)),
    )

    def _get_file(self, files, filename):
        for f in files:
            if f.src_path.replace("/", "\\") == filename.replace("/", "\\"):
                return f

    def on_files(self, files, config):

        for navtype in NAVTYPES:
            pages = {}

            for page_entry in config.get(navtype, []):
                page_title = None
                if isinstance(page_entry, dict):
                    page_title, page_name = list(page_entry.items())[0]
                else:
                    page_name = page_entry
                if not page_title:
                    page_title = page_name
                pages[page_title] = self._get_file(files, page_name)

            config[navtype] = pages

        if isinstance(config.get("privacy"), str):
            privacy_location = config["privacy"]
            config["privacy"] = self._get_file(files, config["privacy"])

    def on_env(self, env, config, files):
        for navtype in NAVTYPES:
            env.globals[navtype] = {
                title: f.page for title, f in config.get(navtype, {}).items()
            }
            print(env.globals[navtype])
        if isinstance(config.get("privacy"), File):
            env.globals["privacy"] = config["privacy"].page
        return env
