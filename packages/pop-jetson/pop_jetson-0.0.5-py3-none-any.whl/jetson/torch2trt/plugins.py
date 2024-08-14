import sys
import os, subprocess


version_info = sys.version_info

def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, importlib.util
    path = os.path.dirname(__file__)
    lib = os.path.join(path, 'plugins.cpython-aarch64-linux-gnu.so')
    if not os.path.exists(lib):
        ori_path = os.getcwd()
        os.chdir(os.path.join(path, "lib"))
        subprocess.run(['python3', 'setup.py', 'build_ext'])
        os.chdir(ori_path)
    __file__ = pkg_resources.resource_filename(__name__, 'plugins.cpython-aarch64-linux-gnu.so')
    __loader__ = None; del __bootstrap__, __loader__
    spec = importlib.util.spec_from_file_location(__name__,__file__)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
__bootstrap__()
