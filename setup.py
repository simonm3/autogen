"""
This file is automatically generated by the autosetup package.
Please edit the marked area only. Other areas will be
overwritten when autosetup is reruns.
"""

from setuptools import setup

params = dict(
    name='autogen',
    description='autogen',
    version='0.0.14',
    url='https://gitlab.com/simonm3/autogen.git',
    install_requires=['PyYAML', 'docopt', 'pipreqs',
                      "pywin32;platform_system=='Windows'"],
    packages=['autogen', 'templates'],
    data_files=[],
    py_modules=[],
    include_package_data=True,
    scripts=None)

########## EDIT BELOW THIS LINE ONLY ##########

# run in subprocess so not detected by pipreqs
params["install_requires"].extend(
    ["nbsphinx", "sphinx", "sphinx-rtd-theme"])

# enable command line
params.update(entry_points={
    'console_scripts': [
              "autogen = autogen.autogen:main",
              ]
})

########## EDIT ABOVE THIS LINE ONLY ##########

setup(**params)
