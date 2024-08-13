class OutputFile:
    def __init__(self, path, rendered_content, write_mode="w"):
        self.path = path
        self.rendered_content = rendered_content
        self.write_mode = write_mode
