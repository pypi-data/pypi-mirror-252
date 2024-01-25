# NOTE: to use this script, you'll need a gitignored "bin" in the 
# project directory, it needs to contain ffmpeg.exe (win-x64)
# setuptools 60.10.0 may also be important, somehow
# build app directory or msi
# python .\setup_cx.py build
# python .\setup_cx.py bdist_msi
# W:\development\vs\vcpkg> .\vcpkg install tesseract:x64-windows-static
import os
from cx_Freeze import setup, Executable
from setup import version as get_positor_version

positor_version= get_positor_version()
platform_base = "Console"
path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))

# after build, check that no new cruft has been added. exclude if so.
# this snapshot was after reseting global site-packages to 0, then minimal install
# cx_Freeze picks up unnecessary things sometimes, so this is a necessary watchdog.
# required to maintain the binary distributable as lean as it can be.
minimal_packages = ('asyncio', 'caffe2', 'certifi', 'charset_normalizer', 'collections', 
    'colorama', 'concurrent', 'ctypes', 'curses', 'dbm', 'email', 'encodings', 'ffmpeg', 
    'filelock', 'future', 'google', 'html', 'http', 'huggingface_hub', 'idna', 'importlib', 
    'json', 'logging', 'lzstring', 'more_itertools', 'multiprocessing', 'numpy', 'packaging', 'past', 
    'PIL', 'pkg_resources', 'positor', 'pydoc_data', 'pytz', 'regex', 'requests', 'test', 
    'tokenizers', 'torch', 'tqdm', 'transformers', 'unittest', 'urllib', 'urllib3', 
    'whisper', 'xml', 'xmlrpc', 'yaml', 'piexif')



positor_exe = Executable(
    "positor/__main__.py",
    base=platform_base,
    icon="positor.ico",
    target_name="positor",
)

bdist_msi_options = {
    "add_to_path": True,
    "upgrade_code": "{bacceb2a-5ad4-4da9-bb0e-6ce84e68b4a1}",
    "initial_target_dir": r"[ProgramFilesFolder]\positor",
    "target_name": "positor",
    "directories": None,
    "environment_variables": None,
    "data": None,
    "product_code": None,
    "install_icon": "positor.ico",
}

build_exe_options = {
    "packages": ["whisper", "colorama", "torch", "numpy"],
    "includes": [],
    "include_files": [r".\bin\ffmpeg.exe", r".\bin\tesseract.exe", r".\bin\tessdata"],
    "include_msvcr": True,
    "excludes": ["tkinter", "tcltk", "sqlite3", "imageio", "lief", "setuptools"
                 "imageio_ffmpeg", "pygame", "lib2to3", "lxml", "Cython", 
                 "distutils", "importlib-metadata", "setuptools", "msilib", 
                 "_distutils_hack", "torchgen", "functorch", "exiv2"],
    "bin_excludes": [],
    "optimize": 1, # need the docstrings, or numpy throws
}

setup(
    name = "positor",
    version = positor_version,
    author="pragmar",
    description = "Utilities for digital archives.",
    options = {
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables = [positor_exe],
)

build_lib = os.path.join(path, "build", "exe.win-amd64-3.10", "lib")
build_lib_packages = [ os.path.basename(f.path) for f in os.scandir("build\exe.win-amd64-3.10\lib") if f.is_dir()]
difference = set(build_lib_packages) - set(minimal_packages)
if len(difference) > 0:
    print()
    print("Site-packages mismatch, found new and probably unnecessary folders:")
    print(difference)
    raise Exception("Bloat is not fully contained.")
