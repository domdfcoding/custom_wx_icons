=====================
custom_wx_icons
=====================

.. start short_desc

.. documentation-summary::
	:meta:

.. end short_desc
.. start shields

.. only:: html

	.. list-table::
		:stub-columns: 1
		:widths: 10 90

		* - Docs
		  - |docs| |docs_check|
		* - Tests
		  - |actions_linux| |actions_windows| |actions_macos|
		* - Activity
		  - |commits-latest| |commits-since| |maintained|
		* - QA
		  - |codefactor| |actions_flake8| |actions_mypy|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: custom-wx-icons
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/custom_wx_icons/badge.svg
		:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/custom_wx_icons/
		:alt: Requirements Status

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.0.1
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2023
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

.. sidebar-links::
	:caption: Links
	:github:
	:pypi: custom_wx_icons


.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <domdfcoding/custom_wx_icons>`

.. end links
