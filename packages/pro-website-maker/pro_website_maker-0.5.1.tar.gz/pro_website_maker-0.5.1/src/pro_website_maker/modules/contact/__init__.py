from pathlib import Path
from pro_website_maker import Module
from pro_website_maker.output_file import OutputFile

class Contact(Module):
    def get_output_files(self, globals, content):
        output_files = []
        for filename in ["Contact/Form.html", "Contact/Sent.html"]:
            rendered_website_content = self.load_template(filename).render({
                "content": content,
                "globals": globals,
            })
            output_files.append(
                OutputFile(
                    Path(filename),
                    rendered_website_content,
                ),
            )
        return output_files
