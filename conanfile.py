from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain
import os


class GLSL_OPTIMIZERConan(ConanFile):
    name = "glsl_optimizer"
    settings = "os", "compiler", "build_type", "arch"

    generators = "CMakeDeps"
    exports_sources = "CMakeLists.txt"

    def configure(self):
        self.settings.compiler.cppstd = "14"

    def requirements(self):
        self.requires(f"spirv_tools/{self.version}@")

    def generate(self):
        if self.settings.compiler == "gcc":
            self.conf.define("tools.build:cxxflags", ["-fno-strict-aliasing"])
            self.conf.define("tools.build:cflags", ["-fno-strict-aliasing"])
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        conan.tools.files.copy(self, "libglsl_optimizer.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        conan.tools.files.copy(self, "libmesa.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        conan.tools.files.copy(self, "libglcpp-library.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        conan.tools.files.copy(self, "glsl_optimizer.h",
                               os.path.join(self.folders.base_source, "src", "glsl"),
                               os.path.join(self.package_folder, "include"))

    def package_info(self):
        # link order matters
        self.cpp_info.libs = ["glsl_optimizer", "mesa", "glcpp-library"]
        self.buildenv_info.define("glsl_optimizer_DIR", self.package_folder)
