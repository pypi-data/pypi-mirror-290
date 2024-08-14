# List of all modules and their names

from pro_website_maker.modules.resume import Resume
from pro_website_maker.modules.contact import Contact
from pro_website_maker.modules.sitemap import Sitemap
from pro_website_maker.modules.markdown import Markdown
from pro_website_maker.modules.static import Static
from pro_website_maker.modules.github_pages import GitHub_Pages

class ModuleLoader:
    def __init__(self):
        self.MODULES = {
            "Resume": Resume(),
            "Contact": Contact(),
            "Sitemap": Sitemap(),
            "Markdown": Markdown(),
            "GitHub_Pages": GitHub_Pages(),
            "Static": Static(),
        }
    def exists(self, module_name):
        return module_name in self.MODULES
    def load(self, module_name):
        return self.MODULES[module_name]
