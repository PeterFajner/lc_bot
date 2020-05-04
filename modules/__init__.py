from os.path import dirname, basename, isfile, join
import glob, importlib
# make all files in this folder importable
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
#for module in __all__:
#    importlib.import_module('.' + module, '.')
