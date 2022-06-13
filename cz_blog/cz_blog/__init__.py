import logging
import os.path

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File
from mkdocs.structure.nav import _data_to_navigation

NAVTYPES = ("footernav",)


log = logging.getLogger("mkdocs")


class CZBlog(BasePlugin):

    config_scheme = tuple(
        (navtype, config_options.Type(list, default=list())) for navtype in NAVTYPES
    ) + (
        ("privacy", config_options.Type(str, default=None)),
        ("articles_folder", config_options.Type(str, default="blog")),
    )

    def on_files(self, files, config):
        self.blog_files = {}

        if self.config.get("articles_folder"):
            self.blog_files["articles"] = []
            for file in files.documentation_pages():
                if os.path.normpath(file.src_path).startswith(
                    self.config["articles_folder"] + os.path.sep
                ):
                    self.blog_files["articles"].append(Page(None, file, config))
            self.blog_files["articles"] = self.blog_files["articles"][::-1]
            log.info("Found {:,.0f} articles".format(len(self.blog_files["articles"])))

        for navtype in NAVTYPES:
            if self.config.get(navtype):
                self.blog_files[navtype] = _data_to_navigation(
                    self.config[navtype], files, config
                )
                log.info(
                    "Found {:,.0f} items in {} navigation".format(
                        len(self.blog_files[navtype]), navtype
                    )
                )

        if isinstance(self.config.get("privacy"), str):
            self.blog_files["privacy"] = _data_to_navigation(
                self.config["privacy"], files, config
            )
            if self.blog_files["privacy"]:
                log.info(
                    "Found privacy page: {}".format(self.blog_files["privacy"].url)
                )

    def on_env(self, env, config, files):
        env.globals.update(self.blog_files)
        return env
