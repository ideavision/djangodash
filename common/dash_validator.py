import importlib
import tempfile
import os, sys
import re
from io import StringIO

class DashValidator():
    def __init__(self, dash_file):
        self.dash_file = dash_file
        self.dash_regex = re.compile(r"^app = dash.Dash\(.*\)$")
        self.dash_without_args_regex = re.compile(r"^app = dash.Dash\(\)$")

    def has_app_module(self):
        data = self.dash_file.read().decode("utf-8")
        for line in data.splitlines():
            if self.dash_regex.match(line):
                return True
        return False

    def load_module(self, path=None, module_name="app"):
        if path is None:
            path = self.dash_file.path
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module 
        spec.loader.exec_module(module)
        return module

    def is_executeable(self):
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                path = os.path.join(tmpdirname, "test-dash-file.py")
                with open(path, 'w') as f:
                    f.write(self.dash_file.read().decode("utf-8"))
                    self.load_module(path)
        except Exception:
            return False
        return True

    def validate_dash(self, new_name):
        with self.dash_file.open('r') as file:
            data = file.read()
        with open(self.dash_file.path, 'w', encoding='utf-8') as file:
            for line in data.splitlines():
                # Remove application script
                if "if__name__=='__main__':" in line.replace(' ', ''): break
                # Remove HTTP server class
                if "app.server" in line: continue
                if line.strip() != "":
                    # Rename dash app class to DjangoDash
                    result = ''
                    if self.dash_without_args_regex.match(line):
                        result = line.replace("app = dash.Dash()", f"app = DjangoDash('{new_name}')")
                    elif self.dash_regex.match(line):
                        result = line.replace("app = dash.Dash(", f"app = DjangoDash('{new_name}',")
                    
                    if line == "import dash":
                        result = "from django_plotly_dash import DjangoDash"

                    if result:
                        file.write(result + "\n")
                    else:
                        file.write(line + "\n")

