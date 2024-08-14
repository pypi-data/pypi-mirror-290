from pathlib import Path
from jinja2 import Template
from pro_website_maker import Module
from pro_website_maker.output_file import OutputFile

class Sitemap(Module):
    def get_output_files(self, globals, config):
        template = self.load_template("sitemap.xml")

        # Render the configuration
        rendered_content = template.render({
            "paths": config["paths"],
            "globals": globals,
        })

        return [
            OutputFile(Path("sitemap.xml"), rendered_content),
        ]
