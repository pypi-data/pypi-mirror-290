from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import os

class Module:
    def get_this_file_directory_path(self):
        return Path(os.path.os.path.realpath(__file__)).parent

    def get_output_files(self, globals, content):
        raise Exception("Classes must override Module.get_output_files.")

    def load_template(self, filename, autoescape=True):
        template_path = self.get_this_file_directory_path() / "templates"
        env = Environment(loader=FileSystemLoader(["templates", template_path]), autoescape=autoescape)
        template = env.get_template(filename)
        print(f"        [+] Loaded {filename} template")
        return template
