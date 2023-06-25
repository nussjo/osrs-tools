from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv

class Package(ConanFile):
    name = "osrs_tools"
    version = "0.0"
    package_type = "library"

    license = "GPL-3.0"
    author = "Jonas Nußdorfer"
    url = "https://github.com/nussjo/osrs-tools.git"
    description = "Collection of utility tools for Old-School Runescape (OSRS) for personal account statistics."

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "clang_tidy": [True, False],
        "default_warning_levels": [True, False],
        "default_optimization_levels": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "clang_tidy": False,
        "default_warning_levels": True,
        "default_optimization_levels": True,
    }

    no_copy_source = True
    revision_mode = "scm"

    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto"
    }

    def build_requirements(self):
        self.test_requires("gtest/[^1.12.1]@")
        self.tool_requires("protobuf/3.21.9@")
        self.tool_requires("grpc/1.50.1@")

    def requirements(self):
        # transitive_headers = True -> dependency used in public header
        # transitive_headers = False -> independent public header
        self.requires("boost/[^1.81.0]@", transitive_headers=True)
        self.requires("fmt/[^8.1.1]@", transitive_headers=False)
        self.requires("grpc/1.50.1@", transitive_headers=False)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        toolchain = CMakeToolchain(self, "Ninja Multi-Config")
        toolchain.cache_variables["osrs_ENABLE_DEFAULT_WARNING_LEVELS"] = self.options.default_warning_levels
        toolchain.cache_variables["osrs_ENABLE_DEFAULT_OPTIMIZATION_LEVELS"] = self.options.default_optimization_levels
        toolchain.generate()
        vbe = VirtualBuildEnv(self)
        vbe.generate()
        vre = VirtualRunEnv(self)
        vre.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build(target="all_verify_interface_header_sets")
        cmake.build()
        if not can_run(self):
            return
        cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def layout(self):
        # experimental:
        # rename build folder and generated cmake user presets only for this package
        # does nothing if already specified via profile
        # conf_key = 'tools.cmake.cmake_layout:build_folder_vars'
        # conf_value = ['settings.os.distro']
        # self.conf[conf_key] = self.conf.get(conf_key, conf_value)
        pass

        self.folders.root = "."
        cmake_layout(self, "Ninja Multi-Config")
        # locate export headers in editable mode
        self.cpp.build.includedirs = [""]
        self.cpp.build.libs = [""]
        self.cpp.package.libs = [""]
