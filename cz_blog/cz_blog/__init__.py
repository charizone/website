import logging
import os.path

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File
from mkdocs.structure.nav import _data_to_navigation

NAVTYPES = ("footernav",)


log = logging.getLogger("mkdocs")


def sort_articles(articles):
    """
    Sort articles by date.
    """
    return sorted(
        articles,
        key=lambda page: str(page.meta.get("date", page.file.name)),
    )[::-1]


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
            self.blog_files["articles"] = sorted(
                self.blog_files["articles"],
                key=lambda page: page.meta.get("date", page.file.name),
            )
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
        if "articles" in self.blog_files:
            featured_articles = sort_articles(
                [a for a in self.blog_files["articles"] if a.meta.get("featured")]
            )
            nonfeatured_articles = sort_articles(
                [a for a in self.blog_files["articles"] if not a.meta.get("featured")]
            )
            self.blog_files["articles"] = featured_articles + nonfeatured_articles
        env.globals.update(self.blog_files)
        return env
