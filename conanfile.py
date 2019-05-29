# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibnameConan(ConanFile):
    name = "ucl"
    version = "1.03"
    description = "UCL is a portable lossless data compression library written in ANSI C."
    topics = ("conan", "libname", "logging")
    url = "https://github.com/bincrafters/conan-ucl"
    homepage = "http://www.oberhumer.com/opensource/ucl/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GP"
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    no_copy_source = True
    _source_subfolder = "source_subfolder"

    def configure(self):
        if str(self.settings.compiler) in ("gcc", "clang", "apple-clang", ):
            del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == 'Windows' or self.options.shared:
            del self.options.fPIC

    def build_requirements(self):
        if tools.os_info.is_windows:
            self.build_requires("msys2_installer/20161025@bincrafters/stable")

    def source(self):
        source_url = "http://www.oberhumer.com/opensource/{0}/download/{0}-{1}.tar.gz".format(self.name, self.version)
        sha256 = "b865299ffd45d73412293369c9754b07637680e5c826915f097577cd27350348"
        tools.get(source_url, sha256=sha256)
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        configure_args = [
            "--with-pic" if self.options.get_safe("fPIC") in (True, None, ) else "--without-pic",
            "--enable-shared" if self.options.shared else "--disable-shared",
            "--disable-static" if self.options.shared else "--enable-static",
        ]
        autotools.flags.append("-std=c90")
        autotools.configure(configure_dir=os.path.join(self.source_folder, self._source_subfolder), args=configure_args)
        autotools.make()

    def package(self):
        autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        with tools.chdir(self.build_folder):
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
