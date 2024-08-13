# Copyright 2024 Macéo Tuloup

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .common import SharedLinker


class SharedLinkerGNU(SharedLinker):
    type = "gnu"
    shared_lib_extension = ".so"

    def __init__(self, path: str = "cc"):
        super().__init__(path)

    @classmethod
    def format_args(self, shared_libs: list[str], flags: list[str]):
        return ["-l"+lib for lib in shared_libs] + flags

    def basic_link_command(self, outputfile: str, objectfiles: set[str], archives: list[str] = [], args: list[str] = []) -> list[str]:
        return [self.path, "-shared", "-o", outputfile, *objectfiles, *archives, *args]


class SharedLinkerGCC(SharedLinkerGNU):
    type = "gcc"

    def __init__(self, path: str = "gcc"):
        super().__init__(path)


class SharedLinkerGPlusPlus(SharedLinkerGNU):
    type = "g++"

    def __init__(self, path: str = "g++"):
        super().__init__(path)


class SharedLinkerClang(SharedLinkerGNU):
    type = "clang"

    def __init__(self, path: str = "clang"):
        super().__init__(path)


class SharedLinkerClangPlusPlus(SharedLinkerGNU):
    type = "clang++"

    def __init__(self, path: str = "clang++"):
        super().__init__(path)
