import pathlib
import os
import sys

sys.path.append(str(pathlib.Path("_extensions").resolve()))

os.environ["MPLCONFIGDIR"] = "./.matplotlib"

author = "Kayce Basques"
copyright = f"2025, {author}"
exclude_patterns = [
    ".github",
    ".gitignore",
    "_extensions",
    "BUILD.bazel",
    "MODULE.bazel",
    "MODULE.bazel.lock",
    "bazel-*",
    "bazelisk",
    "local.fish",
    "ml/reviews/*.rst",
    "out",
    "requirements.lock",
    "requirements.txt",
    "venv"
]
extensions = [
    "matplotlib.sphinxext.plot_directive",
    "sitemap",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
    "sphinx_embeddings",
    "sphinx_reredirects",
]
# TODO: Customize this depending on whether you're developing locally or
# publishing to production.
html_baseurl = "https://technicalwriting.dev"
html_file_suffix = ".html"
html_extra_path = [
    "rss.xml", 
]
html_permalinks_icon = "§"
html_static_path = ["_static"]
html_theme = 'basic'
project = "technicalwriting.dev"
pygments_style = "github-dark"
redirects = {
    "a11y/skip": "https://web.archive.org/web/20250225001215/https://technicalwriting.dev/a11y/skip.html",
    "ai/agents/index": "../agents/index.html",
    "ai/agents/colocate": "../agents/colocate.html",
    "data/embeddings": "../embeddings/underrated.html",
    "data/intertwingularity": "../links/intertwingularity.html",
    "embeddings/overview": "./embeddings/underrated.html",
    "embeddings/underrated": "https://web.archive.org/web/20251230174005/https://technicalwriting.dev/embeddings/underrated.html",
    "ml/embeddings/overview": "../embeddings/underrated.html",
    "ml/embeddings/tasks/index": "../embeddings/tasks/index.html",
    "ml/gn": "../automation/gn.html",
    "ml/plugins": "https://web.archive.org/web/20250222025828/https://technicalwriting.dev/ml/plugins.html",
    "seo/discovered-not-indexed": "https://web.archive.org/web/20250222024724/https://technicalwriting.dev/seo/discovered-not-indexed.html",
    "seo/sentry-overflow": "https://web.archive.org/web/20250221195536/https://technicalwriting.dev/seo/sentry-overflow.html",
    "src/link-text-automation": "../links/automation.html",
    "src/verbatim-wrangling": "https://web.archive.org/web/20240724083629/https://technicalwriting.dev/src/verbatim-wrangling.html",
    "ux/offline": "https://web.archive.org/web/20250221193209/https://technicalwriting.dev/ux/offline.html",
    "ux/pdf": "../links/pdf.html",
    "ux/methodology": "https://web.archive.org/web/20250225002414/https://technicalwriting.dev/ux/methodology.html",
    "ux/searchboxes": "https://web.archive.org/web/20250225002920/https://technicalwriting.dev/ux/searchboxes.html",
    "www/pdf": "../links/pdf.html",
}
release = "0.0.0"
templates_path = ["_templates"]
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html#configuration-options
plot_html_show_formats = False
copybutton_prompt_text = "$ "
