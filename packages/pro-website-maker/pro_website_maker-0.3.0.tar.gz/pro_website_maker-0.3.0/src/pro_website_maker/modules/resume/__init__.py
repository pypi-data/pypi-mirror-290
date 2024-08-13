from pathlib import Path
from jinja2 import Template
from os import system
from pro_website_maker import Module, get_file_directory_path
from pro_website_maker.output_file import OutputFile

MODULE_PATH = get_file_directory_path(__file__)

class Resume(Module):
    def get_output_files(self, globals, content):
        # Load up the template.
        template_path = MODULE_PATH / "template.html"
        with template_path.open("r") as f:
            template = Template(f.read(), autoescape=True)

        print(f"        [+] Loaded resume template")

        # Render the content
        rendered_website_content = template.render({
            "content": content,
            "globals": globals,
            "pdf": False,
        })

        # Render the content intended for PDF
        rendered_pdf_content = template.render({
            "content": content,
            "globals": globals,
            "pdf": True,
        })

        # Render the PDF
        with open("/tmp/Resume_PDF.html", "w") as f:
            f.write(rendered_pdf_content)

        print(f"        [+] Wrote /tmp/Resume_PDF.html")

        resume_pdf_path = Path("/tmp/Resume.pdf")

        if resume_pdf_path.exists():
            resume_pdf_path.unlink()

        system("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless /tmp/Resume_PDF.html --print-to-pdf-no-header --print-to-pdf=/tmp/Resume.pdf")

        print(f"        [+] Generated /tmp/Resume.pdf")

        with open("/tmp/Resume.pdf", "rb") as f:
            resume_blob = f.read()

        print(f"        [+] Read /tmp/Resume.pdf blob")

        return [
            OutputFile(Path("Resume.html"), rendered_website_content),
            OutputFile(Path(content['Name'].replace(' ', '-') + "-Resume.pdf"), resume_blob, "wb"),
        ]
