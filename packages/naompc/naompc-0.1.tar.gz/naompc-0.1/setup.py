import os
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

cfg = None
if "--cfg" in sys.argv:
    arg_index = sys.argv.index("--cfg")
    if arg_index + 1 < len(sys.argv):
        cfg = sys.argv[arg_index + 1]
        del sys.argv[arg_index : arg_index + 2]
print(f"Custom argument received: {cfg}")

# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())

class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        # Must be in this form due to bug in .resolve() only fixed in Python 3.10+
        ext_fullpath = Path.cwd() / self.get_ext_fullpath(ext.name)
        extdir = ext_fullpath.parent.resolve()

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}{os.sep}",
            f"-DCMAKE_BUILD_TYPE={cfg}"
        ]

        configure = subprocess.run( 
            ["cmake", "--preset", f"conan-{cfg.lower()}", *cmake_args]
        )
        
        build = subprocess.run(
            ["cmake", "--build", "--preset", f"conan-{cfg.lower()}"]
        )
        

# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    name="naompc",
    version="0.1",
    author="Davide Ceriola, Flavio Maiorana, Luca Murra",
    author_email="boh@gmail.com",
    description="Cose",
    long_description="Altre cose",
    ext_modules=[CMakeExtension("naompc")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    extras_require={"test": ["pytest>=6.0"]},
    python_requires=">=3.8",
    package_data={"pynaompc": ["pynaompc.pyi"]},
    package_dir={"": "."},
    packages=["pynaompc"],
)