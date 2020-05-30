=====================
custom_wx_icons
=====================

.. start short_desc

**Framework for creating freedesktop-esque icon themes for wxPython.**

.. end short_desc
.. start shields 

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs|
	* - Tests
	  - |travis| |requires| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Other
	  - |license| |language| |commits-since| |commits-latest| |maintained| 

.. |docs| image:: https://readthedocs.org/projects/custom_wx_icons/badge/?version=latest
	:target: https://custom_wx_icons.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/custom_wx_icons/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/custom_wx_icons
	:alt: Travis Build Status

.. |requires| image:: https://requires.io/github/domdfcoding/custom_wx_icons/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/custom_wx_icons/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/custom_wx_icons
	:target: https://www.codefactor.io/repository/github/domdfcoding/custom_wx_icons
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/custom_wx_icons.svg
	:target: https://pypi.org/project/custom_wx_icons/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/custom_wx_icons.svg
	:target: https://pypi.org/project/custom_wx_icons/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/custom_wx_icons
	:target: https://pypi.org/project/custom_wx_icons/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/custom_wx_icons
	:target: https://pypi.org/project/custom_wx_icons/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/custom_wx_icons
	:alt: License
	:target: https://github.com/domdfcoding/custom_wx_icons/blob/master/LICENSE

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/custom_wx_icons
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/custom_wx_icons/v0.0.1
	:target: https://github.com/domdfcoding/custom_wx_icons/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/custom_wx_icons
	:target: https://github.com/domdfcoding/custom_wx_icons/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. end shields



This repository contains a framework for creating freedesktop-esque icon themes for wxPython.
Each theme provides a custom wx.ArtProvider class that allows the icons to be accessed using icon names from the `FreeDesktop Icon Theme Specification <https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html>`_.

Several themes have been created using this framework:

.. list-table::
	:stub-columns: 1
	:widths: 10 50 15

	* - `wx_icons_hicolor <https://github.com/domdfcoding/custom_wx_icons_hicolor>`_
	  - This is the base theme for all other themes. It is based on the `gnome-icon-theme <https://launchpad.net/gnome-icon-theme>`_.
	  - |hicolor_pypi| |hicolor_py_version| |hicolor_license|
	* - `wx_icons_adwaita <https://github.com/domdfcoding/custom_wx_icons_adwaita>`_
	  - This theme is based on the `Adwaita icon theme <https://github.com/GNOME/adwaita-icon-theme>`_ version 3.28.
	  - |adwaita_pypi| |adwaita_py_version| |adwaita_license|
	* - `wx_icons_humanity <https://github.com/domdfcoding/custom_wx_icons_humanity>`_
	  - This theme is based on the `Humanity icon theme <https://launchpad.net/ubuntu/+source/humanity-icon-theme>`_ version 0.6.15. It also includes the Humanity_Dark theme
	  - |humanity_pypi| |humanity_py_version| |humanity_license|
	* - `wx_icons_suru <https://github.com/domdfcoding/custom_wx_icons_suru>`_
	  - This theme is based on the `Suru icon theme <https://github.com/ubuntu/yaru/blob/master/icons>`_ version 20.04.4.
	  - |suru_pypi| |suru_py_version| |suru_license|
	* - `wx_icons_tango <https://github.com/domdfcoding/custom_wx_icons_tango>`_
	  - This theme is based on public domain icons from the Tango Desktop Project.
	  - |tango_pypi| |tango_py_version| |tango_license|


.. |hicolor_pypi| image:: https://img.shields.io/pypi/v/wx_icons_hicolor.svg
    :target: https://pypi.org/project/wx_icons_hicolor/
    :alt: PyPI

.. |hicolor_py_version| image:: https://img.shields.io/pypi/pyversions/wx_icons_hicolor.svg
    :target: https://pypi.org/project/wx_icons_hicolor/
    :alt: PyPI - Python Version

.. |hicolor_license| image:: https://img.shields.io/pypi/l/wx_icons_hicolor.svg
    :target: https://github.com/domdfcoding/custom_wx_icons_hicolor/LICENSE
    :alt: PyPI - License


.. |adwaita_pypi| image:: https://img.shields.io/pypi/v/wx_icons_adwaita.svg
    :target: https://pypi.org/project/wx_icons_adwaita/
    :alt: PyPI

.. |adwaita_py_version| image:: https://img.shields.io/pypi/pyversions/wx_icons_adwaita.svg
    :target: https://pypi.org/project/wx_icons_adwaita/
    :alt: PyPI - Python Version

.. |adwaita_license| image:: https://img.shields.io/pypi/l/wx_icons_adwaita.svg
    :target: https://github.com/domdfcoding/custom_wx_icons_adwaita/LICENSE
    :alt: PyPI - License


.. |humanity_pypi| image:: https://img.shields.io/pypi/v/wx_icons_humanity.svg
    :target: https://pypi.org/project/wx_icons_humanity/
    :alt: PyPI

.. |humanity_py_version| image:: https://img.shields.io/pypi/pyversions/wx_icons_humanity.svg
    :target: https://pypi.org/project/wx_icons_humanity/
    :alt: PyPI - Python Version

.. |humanity_license| image:: https://img.shields.io/pypi/l/wx_icons_humanity.svg
    :target: https://github.com/domdfcoding/custom_wx_icons_humanity/LICENSE
    :alt: PyPI - License


.. |suru_pypi| image:: https://img.shields.io/pypi/v/wx_icons_suru.svg
    :target: https://pypi.org/project/wx_icons_suru/
    :alt: PyPI

.. |suru_py_version| image:: https://img.shields.io/pypi/pyversions/wx_icons_suru.svg
    :target: https://pypi.org/project/wx_icons_suru/
    :alt: PyPI - Python Version

.. |suru_license| image:: https://img.shields.io/pypi/l/wx_icons_suru.svg
    :target: https://github.com/domdfcoding/custom_wx_icons_suru/LICENSE
    :alt: PyPI - License


.. |tango_pypi| image:: https://img.shields.io/pypi/v/wx_icons_tango.svg
    :target: https://pypi.org/project/wx_icons_tango/
    :alt: PyPI

.. |tango_py_version| image:: https://img.shields.io/pypi/pyversions/wx_icons_tango.svg
    :target: https://pypi.org/project/wx_icons_tango/
    :alt: PyPI - Python Version

.. |tango_license| image:: https://img.shields.io/pypi/l/wx_icons_tango.svg
    :target: https://github.com/domdfcoding/custom_wx_icons_tango/LICENSE
    :alt: PyPI - License


The individual themes contain instructions on how to use them in your program.

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	docs

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/custom_wx_icons>`__

.. end links
