import importlib, os

def load_plugins():
    for file in os.listdir("plugins"):
        if file.endswith(".py") and not file.startswith("_"):
            importlib.import_module(f"plugins.{file[:-3]}")
