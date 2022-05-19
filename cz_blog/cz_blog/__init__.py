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

    def on_files(self, files, config):

        for navtype in NAVTYPES:
            pages = {}

            for page_entry in config.get(navtype, []):
                page_title = None
                if isinstance(page_entry, dict):
                    page_title, page_name = list(page_entry.items())[0]
                else:
                    page_name = page_entry
                for f in files:
                    if f.src_path != page_name:
                        continue
                    if not page_title:
                        page_title = page_name
                    pages[page_title] = f

            config[navtype] = pages

        if config.get("privacy"):
            for f in files:
                if f.src_path != config["privacy"]:
                    continue
                config["privacy"] = f

    def on_env(self, env, config, files):
        for navtype in NAVTYPES:
            env.globals[navtype] = {
                title: f.page for title, f in config.get(navtype, {}).items()
            }
            print(env.globals[navtype])
        if isinstance(config.get("privacy"), File):
            env.globals["privacy"] = config["privacy"].page
        return env
