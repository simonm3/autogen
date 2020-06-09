import ast
import logging
import os
import shutil
import site
from glob import glob
from importlib.util import find_spec
from pathlib import Path

import autopep8
import pkg_resources
from setuptools import find_packages

from . import utils
from .utils import subprocess_run

log = logging.getLogger()


class Project:
    """ a project for which we want to take actions such as generate a setup.py; docs; or release """

    def __init__(self, path=None):
        # change to project root to run git commands
        root = self.root(path)
        if not root:
            raise Exception("must be run inside a git repo")
        os.chdir(root)

        # exclude files not in git
        self.gitfiles = subprocess_run("git ls-files").splitlines()

    def create_docs(self):
        """ initialise everything needed for generating docs and publishing on gitlab pages automatically """

        # create srcdst pairs of Path dirs
        templates = Path(__file__).parent.parent.resolve() / "templates"
        srcdst = [(templates / "docs", Path("docs")), (templates, Path(""))]

        # can be test folders in more than one package
        for d in Path(self.root()).glob("*/test"):
            if d.is_dir():
                srcdst.append((templates / "test", d))

        # copy files
        for src, dst in srcdst:
            dst.mkdir(exist_ok=True)
            for f in src.glob("*"):
                if f.is_file() and not (dst / f.name).exists():
                    log.info(f"creating {dst/f.name}")
                    shutil.copy(f, dst)

    def create_setup(self):
        """ generate setup.py file """
        out = []

        # start
        out.append(
            '"""\n'
            "This file is automatically generated by the autogen package.\n"
            "Please edit the marked area only. Other areas will be\n"
            "overwritten when autogen is rerun.\n"
            '"""\n'
            "\n"
            "from setuptools import setup\n"
            "\n"
        )

        # params
        out.append("params = dict(\n")
        params = []
        for k, v in self.setup_defaults().items():
            if isinstance(v, str):
                v = "'%s'" % v
            params.append("   %s=%s" % (k, v))
        out.append(",\n".join(params))
        out.append(")\n")
        out.append("\n")

        # create requirements.txt with versions
        reqs = []
        for p in self.install_requires():
            try:
                version = pkg_resources.get_distribution(p).version
            except:
                version = ""
            if version:
                p = f"{p}=={version}"
            reqs.append(p)
        with open("requirements.txt", "w") as f:
            f.write("\n".join(reqs))

        # bespoke
        out.append("########## EDIT BELOW THIS LINE ONLY ##########\n")
        bespoke = "\n\n"
        try:
            with open("setup.py") as f:
                lines = f.readlines()
                search = "EDIT BELOW THIS LINE ONLY"
                start = [i for i, s in enumerate(lines) if search in s][0]
                search = "EDIT ABOVE THIS LINE ONLY"
                end = [i for i, s in enumerate(lines) if search in s][0]
                bespoke = lines[start + 1 : end]
        except FileNotFoundError:
            pass
        except IndexError:
            raise Exception(
                "Markers are missing from edit section. Replace\n"
                "markers manually or delete setup.py before running\n"
                "autogen"
            )

        out.extend(bespoke)
        out.append("########## EDIT ABOVE THIS LINE ONLY ##########\n")
        out.append("\n")

        # finish
        out.append("setup(**params)")
        out = autopep8.fix_code("".join(out))

        # write to file
        with open("setup.py", "w") as f:
            f.writelines(out)
        log.info("created new setup.py")

    def release(self):
        """ publish new release to pypi and github """
        version = self.version()

        # release to git
        subprocess_run("git commit -a -m 'version update'")
        subprocess_run(f"git tag {version}")
        subprocess_run("git push")
        subprocess_run("git push --tags origin master")

        # release to pypi
        subprocess_run("python setup.py clean --all bdist_wheel")
        subprocess_run(f"twine upload dist/*{version}*")

    def create_conda(self):
        """ todo release to conda """
        raise NotImplementedError

        # NOT TESTED, TAKES TIME TO RUN, NEEDS TO INCLUDE EACH PLATFORM SEPARATELY
        # with open("version") as f:
        #     version = f.read()
        # os.remove("condapack")
        # subprocess_run(f"conda skeleton pypi --output-dir condapack --version {version}")
        # subprocess_run("conda build condapack --output-folder condapack")
        # subprocess_run("anaconda upload condapack/win-64/*.tar.bz2")

    def update_version(self, level):
        """increment the level passed by one. version is in format level0.level1,level2

        :param level: 0, 1 or 2 for major, minor, patch update
        """
        version = self.version()

        # increment
        versions = [int(v) for v in version.split(".")]
        versions[level] += 1
        for i in range(level + 1, len(versions)):
            versions[i] = 0
        version = ".".join([str(v) for v in versions])

        # update
        with open("version", "w") as f:
            f.write(version)

    # metadata ##############################################################

    def setup_defaults(self):
        """ default params for setup """
        return dict(
            name=self.name(),
            description=self.description(),
            version=self.version(),
            url=self.url(),
            install_requires=self.install_requires(),
            packages=self.packages(),
            package_data=self.package_data(),
            include_package_data=True,
            py_modules=self.py_modules(),
            scripts=self.scripts(),
        )

    def root(self, path=None):
        """ return folder where .git is located; or False if not in a git repo """
        if not path:
            path = os.getcwd()
        while True:
            if ".git" in os.listdir(path):
                return path
            if path == os.path.dirname(path):
                return False
            path = os.path.dirname(path)

    def name(self):
        """ name is folder name """
        return os.path.basename(os.getcwd())

    def description(self):
        """ first line of readme """
        try:
            readme = [
                f for f in os.listdir(os.getcwd()) if f.lower().startswith("readme")
            ][0]
            with open(readme, "r") as f:
                return f.readline().strip(" #\n")
        except:
            log.warning("no readme provided. setting description=name")
            return self.name()

    def version(self):
        try:
            with open("version") as f:
                version = f.read()
        except FileNotFoundError:
            version = "0.0.0"
        return version

    def url(self):
        """ url is github page for project """
        try:
            url = subprocess_run("git remote get-url origin").rstrip("\n")
            url = url.replace("ssh://git@", "https://")
            url = url.replace("git@", "http://")
            url = url.replace("github.com:", "github.com/")
        except:
            return ""
        return url

    def packages(self):
        """ packages in git """
        return find_packages(exclude=["_*"])

    def install_requires(self):
        """ return pypi names of imports """
        user, _, missing = self.imports()
        return set(utils.import2pypi(sorted(user + missing)))

    def imports(self):
        """ get imports split into categories
        :return: user, system, missing
        """
        # get source files
        folders = [find_spec(p).submodule_search_locations[0] for p in self.packages()]
        files = []
        for folder in folders:
            files.extend(glob(f"{folder}/*.py"))

        # get imports
        imports = []
        for f in files:
            src = open(f).read()
            for node in ast.walk(ast.parse(src)):
                if isinstance(node, ast.ImportFrom) and node.level == 0:
                    imports.append(node.module)
                elif isinstance(node, ast.Import):
                    imports.extend([n.name for n in node.names])
        imports = set([m.split(".")[0] for m in imports])

        # exclude built ins
        system = []
        user = []
        missing = []
        for i in imports:
            spec = find_spec(i)
            if not spec:
                missing.append(i)
                continue
            if spec.origin is None or "site-packages" not in spec.origin:
                system.append(i)
                continue
            user.append(i)
        return user, system, missing

    def py_modules(self):
        """ all git controlled in root ending .py """
        files = [
            f
            for f in os.listdir(os.getcwd())
            if os.path.isfile(f)
            and f in self.gitfiles
            and f.endswith(".py")
            and f not in ["setup.py"]
        ]
        modules = [f[:-3] for f in files]
        return sorted(modules)

    def package_data(self):
        """ all files in packages; git controlled; not ending .py """
        package_data = dict()
        folders = [p.replace(".", "/") for p in self.packages()]
        for folder in folders:
            package_files = [f"{folder}/{f}" for f in os.listdir(folder)]
            package_files = [
                f
                for f in package_files
                if os.path.isfile(f) and not f.endswith(".py") and f in self.gitfiles
            ]
            if package_files:
                package_data[folder] = [f[len(folder) + 1 :] for f in package_files]
        return package_data

    def scripts(self):
        """ files from scripts folder managed by git """
        folder = "scripts"
        if not os.path.isdir(folder):
            return
        files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        ]
        files = [utils.normpath(f) for f in files]
        files = set(files) & set(self.gitfiles)
        return sorted(list(files))
