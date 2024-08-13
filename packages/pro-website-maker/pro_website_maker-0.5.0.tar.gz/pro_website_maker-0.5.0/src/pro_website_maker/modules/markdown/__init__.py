from pathlib import Path
from jinja2 import Template
from markdown import markdown
from pro_website_maker import Module
from pro_website_maker.output_file import OutputFile

class Markdown(Module):
    def get_output_files(self, globals, content):
        path = content["Output"]

        # Load up the template.
        template = self.load_template("markdown.html", autoescape=False)

        # Replace content markdown with rendered markdown content
        content["Markdown"] = markdown(content["Markdown"])

        # Render the content
        rendered_content = template.render({
            "content": content,
            "globals": globals,
        })

        return [
            OutputFile(Path(str(path)), rendered_content),
        ]
