from pro_website_maker import Module
from pro_website_maker.output_file import OutputFile
from pathlib import Path

class Static(Module):
    def get_output_files(self, globals, content):
        output_files = []
        for file in content["Files"]:
            source_path = Path("content") / file
            with open(source_path, "rb") as f:
                output_files.append(OutputFile(file, f.read(), "wb"))
        return output_files
