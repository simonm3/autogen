"""
This file is automatically generated by the autogen package.
Please edit the marked area only. Other areas will be
overwritten when autogen is rerun.
"""

from setuptools import setup

params = dict(
    name='autogen',
    description='Automate development tasks',
    version='1.0.3',
    url='https://gitlab.com/simonm3/autogen.git',
    install_requires=['PyYAML', 'autopep8', 'docopt',
                      'pipreqs', "pywin32;platform_system=='Windows'"],
    packages=['autogen', 'templates'],
    package_data={'templates': [
        '.gitlab-ci.yml', 'example_image.jpg', 'example_page.rst', 'index.rst', 'Makefile']},
    include_package_data=True,
    py_modules=[],
    scripts=None)

########## EDIT BELOW THIS LINE ONLY ##########

# enable command line
params.update(entry_points={"console_scripts": [
              "autogen = autogen.autogen:main"]})

########## EDIT ABOVE THIS LINE ONLY ##########

setup(**params)
