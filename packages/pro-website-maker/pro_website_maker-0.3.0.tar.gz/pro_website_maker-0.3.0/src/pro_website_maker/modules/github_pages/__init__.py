from pro_website_maker import Module
from pro_website_maker.output_file import OutputFile

class GitHub_Pages(Module):
    def get_output_files(self, globals, content):
        print(globals)
        return [OutputFile(
            "CNAME",
            f"www.{globals['Domain']}",
        )]
