from distutils.core import setup

setup(
    name="cz_blog",
    entry_points={
        "mkdocs.plugins": [
            "cz_blog = cz_blog:CZBlog",
        ]
    },
)
