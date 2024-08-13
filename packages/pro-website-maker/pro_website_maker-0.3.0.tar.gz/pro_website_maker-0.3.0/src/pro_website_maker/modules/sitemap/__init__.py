from pathlib import Path
from jinja2 import Template
from pro_website_maker import Module, get_file_directory_path
from pro_website_maker.output_file import OutputFile

MODULE_PATH = get_file_directory_path(__file__)

class Sitemap(Module):
    def get_output_files(self, globals, config):
        # Load up the template.
        template_path = MODULE_PATH / "template.xml"
        with template_path.open("r") as f:
            template = Template(f.read(), autoescape=True)

        print(f"    [+] Loaded sitemap template")

        # Render the configuration
        rendered_content = template.render({
            "paths": config["paths"],
            "globals": globals,
        })

        return [
            OutputFile(Path("sitemap.xml"), rendered_content),
        ]
