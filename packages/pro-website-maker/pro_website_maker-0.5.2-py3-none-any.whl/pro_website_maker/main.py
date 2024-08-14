from yaml import safe_load
from pathlib import Path
from shutil import rmtree
from .module_loader import ModuleLoader
import sys

sys.tracebacklimit = 0

module_loader = ModuleLoader()

class PWM:
    def load_globals(self):
        globals_path = Path("content/Globals.yaml")
        try:
            with globals_path.open("r") as f:
                self.globals = safe_load(f)
        except Exception as e:
            print("Error: Could not load Globals.yaml")
            print(e)
            exit(1)
        if "Domains" not in self.globals:
            print("Error: Globals.yaml must contain at least one domain.")
            exit(1)


    def print_processing(self, domain):
        print(f"[+] Processing {domain}")

    def initialize_variables(self, domain):
        self.globals["Domain"] = domain
        self.sitemap_paths = []

    def nuke_output_dir(self, domain):
        # Start fresh, keeping .git files
        print(f"    [*] Nuking ./{domain}/ subdirectory")
        for path in Path(domain).glob("*"):
            if not path.stem.startswith("."):
                if path.is_dir():
                    rmtree(path)
                else:
                    path.unlink()
    
    # Return content object
    def load_yaml_file(self, yaml_path):
        # Try to read the YAML file then print status to the terminal.
        try:
            with yaml_path.open("r") as f:
                raw_txt = f.read()
                for g in self.globals:
                    if isinstance(self.globals[g], str):
                        # Substitute in global variables, denoted by
                        # {{ VariableName }}
                        raw_txt = raw_txt.replace("{{ "+g+" }}", self.globals[g])
                content = safe_load(raw_txt)
        except Exception as e:
            print(f"Error: Could not load {yaml_path}")
            print(e)
            exit(1)

        print(f"    [+] Loaded {yaml_path}")

        return content

    def assert_module_in_yaml_spec(self, content):
        if "Module" not in content:
            print(f"Error: Could not find module spec in {yaml_path}")
            exit(1)
    
    def assert_module_exists(self, module_name):
        if not module_loader.exists(module_name):
            print(f"Error: Module does not exist: {module_name}")
            exit(1)

    def write_output_file_to_disk(self, output_file):
        output_path = Path(self.globals["Domain"]) / output_file.path
        output_path.parent.mkdir(exist_ok=True)
        with output_path.open(output_file.write_mode) as f:
            f.write(output_file.rendered_content)
        print(f"        [+] Generated {output_path}")

    def process_yaml_file(self, yaml_path):
        content = self.load_yaml_file(yaml_path)
        self.assert_module_in_yaml_spec(content)
        module_name = content["Module"]
        self.assert_module_exists(module_name)
        module = module_loader.load(module_name)
        output_files = module.get_output_files(self.globals, content)
        for output_file in output_files:
            self.write_output_file_to_disk(output_file)
            # Remember to update the sitemap!
            self.sitemap_paths.append(str(output_file.path))

    def finalize_sitemap(self):
        # Update the sitemap.
        content = {"paths": self.sitemap_paths}
        [output_file] = module_loader.load("Sitemap").get_output_files(self.globals, content)
        output_path = Path(self.globals["Domain"]) / output_file.path
        with output_path.open("w") as f:
            f.write(output_file.rendered_content)
        print(f"    [+] Generated {output_path}")

    def main(self):
        self.load_globals()

        # Main loop: For each domain
        for domain in self.globals["Domains"]:
            self.print_processing(domain)
            self.initialize_variables(domain)
            self.nuke_output_dir(domain)

            # Inner loop: For each YAML file in the current directory.
            for yaml_path in Path("content").glob("*.yaml"):
                # Special-case globals.yaml since we already handled that.
                if yaml_path.parts[-1] == "Globals.yaml":
                    continue
                self.process_yaml_file(yaml_path)

            self.finalize_sitemap()
        return 0

def main():
    pwm = PWM()
    return pwm.main()
