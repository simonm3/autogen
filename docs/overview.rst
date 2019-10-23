Automate development tasks
==========================

This automates development tasks:

* automatically creates html documentation and publishes on gitlab pages
* creates a setup.py with defaults which can be overridden.
* creates a release and pushes to gitlab and pypi

Installation
============

To install::

    pip install autogen

Usage
=====

Create Documentation
--------------------

To configure a project to automatically create and publish html documentation every commit::

    autogen -d

To create and publish html documentation on gitlab pages:

* Git commit changes to gitlab
* Your new html documentation will be automatically appear at https://{username}.gitlab.io{project}/index.html
* The initial docs include a home/index page, example contents page and docstrings from your source code

To create your own documentation pages:

* Create pages in rst format in the docs folder. See :doc:`example_page` for examples of rst.
* Add the pages to the contents list in index.rst
* When you git commit these pages will automatically be added to https://{username}.gitlab.io{project}/index.html

To manually create html pages locally (not necessary but may be useful if you are offline)::

    cd docs
    make

The configuration creates the following files. It does not overwrite existing files but does update gitlab-ci.yml if
it exists:

.. table::

    =================  ===================================================
    File               Description
    =================  ===================================================
    conf.py            generic settings that work for most projects
    confplus.py        in case you do want to change any settings!
    index.rst          a draft home page for you to edit
    example_page.rst   an example content page for you to edit
    example_image.jpg  an example image inserted on the example page
    makefile           to manually create html docs locally
    gitlab-ci.yml      to automatically publish html docs every git commit
    =================  ===================================================


Create Setup.py
---------------

To create setup.py::

    autogen -s

This will have the following defaults:

.. table::

    ================  ===================================================
    Section           Default
    ================  ===================================================
    name              project root name
    description       from readme
    version           from version.py
    url               remote origin
    install_requires  using pipreqs
    packages          all packages under git control
    package_data      all git controlled files in packages
    py_modules        .py files in root
    scripts           scripts folder
    ================  ===================================================

Once generated you can edit part of the file. When you regenerate it your edits will be retained.

Create a release
----------------

To create a release::

    git commit. it will raise an exception if there are outstanding commits.
    autogen -M|-m|-p

This updates the appropriate version (major.minor.patch); recreates setup.py; uploads to git and pypi