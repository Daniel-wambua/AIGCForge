import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

def generate_html_report(results, outpath=None):
    """
    Write static, self-contained HTML report using Jinja2 template.
    """
    if outpath is None:
        outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "report.html")
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("report.html")
    html = template.render(results=results, tool="AIGCForge", version="1.0")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
