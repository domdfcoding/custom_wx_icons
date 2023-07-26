****************
custom_wx_icons
****************

.. image:: https://travis-ci.com/domdfcoding/custom_wx_icons.svg?branch=master
    :target: https://travis-ci.com/domdfcoding/custom_wx_icons
    :alt: Build Status
.. image:: https://readthedocs.org/projects/custom_wx_icons/badge/?version=latest
    :target: https://custom_wx_icons.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

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
