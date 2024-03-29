#!/usr/bin/env python
#
#  create_custom_theme.py
"""
Script to create the boilerplate for a custom theme
"""
#
#  Copyright 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import datetime
import os
import pathlib

# TODO: Make the CAPS variables argparse arguments. For now just fill in manually.

THEME_NAME = "Example"  # Typically this will have a capital letter at the beginning
# THEME_NAME is used in the following places:
# 	Package name: wx_icons_{THEME_NAME.lower()}
# 	Icons directory: THEME_NAME
# 	IconTheme class: {THEME_NAME}IconTheme
# 	wxIconTheme class: wx{THEME_NAME}IconTheme
# amongst others.

BUILD_SVG_FROM_SRC = True
SVG_FROM_SRC_DPIS = [1]

INHERITS_FROM = "hicolor"
INHERIT_LIST = [INHERITS_FROM]
# If this inherited from e.g. Adwaita, the list would have "hicolor" as a second entry

INITIAL_VERSION = "0.0.0"
UPSTREAM_VERSION = "12.34.56"

AUTHOR = "Dominic Davis-Foster"
AUTHOR_EMAIL = "dominic@davis-foster.co.uk"

###################################################################
# Script starts here. Don't change anything beyond this point
###################################################################

package_name = f"wx_icons_{THEME_NAME.lower()}"
package_root = pathlib.Path('.').resolve() / THEME_NAME.lower()

print(f"Creating theme in {package_root} .")


def maybe_make(directory):
	if not directory.is_dir():
		directory.mkdir()


# Create content root for package
maybe_make(package_root)

# Make python package directory and the __init__.py file
maybe_make(package_root / package_name)

license_placeholder = """#  This file is distributed under the same license terms as the program it came with.
#  There will probably be a file called LICEN[S/C]E in the same directory as this file.
#
#  In any case, this program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."""

author_copyright_string = f"Copyright (c) {datetime.datetime.now().year} {AUTHOR} <{AUTHOR_EMAIL}>"

shebang = "#!/usr/bin/python3"

(package_root / package_name / "__init__.py").write_text(
		f'''{shebang}
#
#  __init__.py
#
#  {author_copyright_string}
#
{license_placeholder}
#


# 3rd party
import importlib_resources

# this package
from {package_name} import {THEME_NAME}


from wx_icons_{INHERITS_FROM.lower()} import {INHERITS_FROM.capitalize()}IconTheme, wx{INHERITS_FROM.capitalize()}IconTheme


__version__ = "{INITIAL_VERSION}"


def version():
	return f"""{package_name}
Version {{__version__}}
{THEME_NAME} Icon Theme Version {UPSTREAM_VERSION}
"""
# TODO: Add the name of your theme and the theme version above


with importlib_resources.path({THEME_NAME}, "index.theme") as theme_index_path:
	theme_index_path = str(theme_index_path)


class {THEME_NAME}IconTheme({INHERITS_FROM.capitalize()}IconTheme):  # TODO: If you're not inheriting from {INHERITS_FROM.capitalize()}, change this as appropriate.
	"""
	This class shows how to construct an icon theme. Not much needs changing except some variable names.
	"""
	_{THEME_NAME.lower()}_theme = {INHERITS_FROM.capitalize()}IconTheme.create()

	@classmethod
	def create(cls):
		"""
		Create an instance of the {THEME_NAME} Icon Theme
		"""

		with importlib_resources.path({THEME_NAME}, "index.theme") as theme_index_path:
			theme_index_path = str(theme_index_path)

		return cls.from_configparser(theme_index_path)

	def find_icon(self, icon_name, size, scale, prefer_this_theme=True):
		"""

		:param icon_name:
		:type icon_name:
		:param size:
		:type size:
		:param scale:
		:type scale:
		:param prefer_this_theme: Return an icon from this theme even if it has to be resized,
			rather than a correctly sized icon from the parent theme.
		:type prefer_this_theme:
		:return:
		:rtype:
		"""

		icon = self._do_find_icon(icon_name, size, scale, prefer_this_theme)
		if icon:
			return icon
		else:
			# If we get here we didn't find the icon.
			return self._{THEME_NAME.lower()}_theme.find_icon(icon_name, size, scale)


class wx{THEME_NAME}IconTheme(wx{INHERITS_FROM.capitalize()}IconTheme):
	_{THEME_NAME.lower()}_theme = {THEME_NAME}IconTheme.create()

	def CreateBitmap(self, id, client, size):
		icon = self._{THEME_NAME.lower()}_theme.find_icon(id, size.x, None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size.x)
		else:
			print("Icon not found in {THEME_NAME} theme")
			return super().CreateBitmap(id, client, size)


if __name__ == '__main__':
	# theme = {THEME_NAME}IconTheme.from_configparser(theme_index_path)
	theme = {THEME_NAME}IconTheme.create()

	# for directory in theme.directories:
	# 	print(directory.icons)

	# test_random_icons(theme)
	test.test_icon_theme(theme)

'''
		)

# Create directory to store icons
maybe_make(package_root / package_name / THEME_NAME)

(package_root / package_name / THEME_NAME / "__init__.py").write_text('')

# Create .bumpversion.cfg
(package_root / ".bumpversion.cfg").write_text(
		f"""[bumpversion]
current_version = {INITIAL_VERSION}
commit = True
message = Bump {package_name} version: {{current_version}} → {{new_version}}
tag = False

[bumpversion:file:{package_name}/__init__.py]

[bumpversion:file:setup.py]

"""
		)

# Create __pkginfo__.py
if not (package_root / "__pkginfo__.py").exists():
	os.symlink("../__pkginfo__.py", package_root / "__pkginfo__.py")

if BUILD_SVG_FROM_SRC:

	# Create build_icons_from_src.py
	with open(package_root / "build_icons_from_src.py", 'w') as fp:
		fp.write(
				f'''{shebang}
#
"""
Script to chop up SVGs into individual sizes

This takes around 15 minutes to run so be patient.
"""
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
{license_placeholder}
#
#


# stdlib
import os
import sys

sys.path.append(".")
sys.path.append("..")
'''
				)
		for theme in INHERIT_LIST:
			fp.write(f'sys.path.append("../{theme.lower()}")\n')

		fp.write(
				f'''

# this package
from gnome_icon_builder import get_scalable_directories, main
from {package_name} import theme_index_path

scalable_directories = get_scalable_directories(theme_index_path)
output_dir = "./{package_name}/{THEME_NAME}"
dpis = {str(SVG_FROM_SRC_DPIS)}  # DPI multipliers to render at
main(os.path.join('.', 'svg_src'), dpis, output_dir, scalable_directories)
'''
				)

	if not (package_root / "svg_src").exists():
		(package_root / "svg_src").mkdir()

	# Create example svg
	(package_root / "svg_src" / "example-delete-me.svg").write_text(
			'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   height="300"
   id="svg11300"
   inkscape:export-filename="/home/jimmac/Desktop/wi-fi.png"
   inkscape:export-xdpi="90.000000"
   inkscape:export-ydpi="90.000000"
   inkscape:output_extension="org.inkscape.output.svg.inkscape"
   inkscape:version="0.48.4 r9939"
   sodipodi:docname="accessories-calculator.svg"
   sodipodi:version="0.32"
   style="display:inline;enable-background:new"
   version="1.0"
   width="400">
  <title
     id="title3615">Calculator</title>
  <metadata
     id="metadata154">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>Calculator</dc:title>
        <dc:creator>
          <cc:Agent>
            <dc:title>Jakub Steiner</dc:title>
          </cc:Agent>
        </dc:creator>
        <dc:contributor>
          <cc:Agent>
            <dc:title>Lapo Calamandrei</dc:title>
          </cc:Agent>
        </dc:contributor>
        <dc:source />
        <cc:license
           rdf:resource="" />
        <dc:subject>
          <rdf:Bag>
            <rdf:li>calc</rdf:li>
            <rdf:li>calculator</rdf:li>
            <rdf:li>compute</rdf:li>
          </rdf:Bag>
        </dc:subject>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <sodipodi:namedview
     bordercolor="#666666"
     borderopacity="0.25490196"
     fill="#f57900"
     gridtolerance="12"
     guidetolerance="13"
     height="300px"
     id="base"
     inkscape:current-layer="layer2"
     inkscape:cx="175.32776"
     inkscape:cy="170.37642"
     inkscape:document-units="px"
     inkscape:grid-bbox="true"
     inkscape:guide-bbox="true"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:showpageshadow="false"
     inkscape:snap-bbox="true"
     inkscape:snap-nodes="true"
     inkscape:window-height="1381"
     inkscape:window-width="2560"
     inkscape:window-x="2560"
     inkscape:window-y="27"
     inkscape:zoom="1"
     objecttolerance="7"
     pagecolor="#ffffff"
     showgrid="false"
     showguides="true"
     stroke="#ef2929"
     width="400px"
     inkscape:window-maximized="1">
    <inkscape:grid
       empspacing="4"
       enabled="true"
       id="grid5883"
       spacingx="1px"
       spacingy="1px"
       type="xygrid"
       visible="true" />
  </sodipodi:namedview>
  <defs
     id="defs3">
    <inkscape:perspective
       sodipodi:type="inkscape:persp3d"
       inkscape:vp_x="0 : 150 : 1"
       inkscape:vp_y="0 : 1000 : 0"
       inkscape:vp_z="400 : 150 : 1"
       inkscape:persp3d-origin="200 : 100 : 1"
       id="perspective809" />
    <linearGradient
       id="linearGradient3213">
      <stop
         id="stop3215"
         offset="0"
         style="stop-color:#2e3436;stop-opacity:1" />
      <stop
         id="stop3217"
         offset="1"
         style="stop-color:#555753;stop-opacity:1" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient4242">
      <stop
         style="stop-color:#888a85;stop-opacity:1;"
         offset="0"
         id="stop4244" />
      <stop
         style="stop-color:#babdb6;stop-opacity:1"
         offset="1"
         id="stop4246" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient4178">
      <stop
         style="stop-color:#eeeeec;stop-opacity:1;"
         offset="0"
         id="stop4180" />
      <stop
         style="stop-color:#eeeeec;stop-opacity:0;"
         offset="1"
         id="stop4182" />
    </linearGradient>
    <linearGradient
       id="linearGradient4010">
      <stop
         style="stop-color:#787a75;stop-opacity:1;"
         offset="0"
         id="stop4012" />
      <stop
         style="stop-color:#bbc1b5;stop-opacity:1;"
         offset="1"
         id="stop4014" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient3945">
      <stop
         style="stop-color:#2e3436;stop-opacity:1;"
         offset="0"
         id="stop3947" />
      <stop
         style="stop-color:#888a85;stop-opacity:1"
         offset="1"
         id="stop3949" />
    </linearGradient>
    <linearGradient
       id="linearGradient3169">
      <stop
         id="stop3171"
         offset="0"
         style="stop-color:#ffffff;stop-opacity:1" />
      <stop
         id="stop3173"
         offset="1"
         style="stop-color:#ffffff;stop-opacity:0" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient9199"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient9197"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,136,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient9195"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.1372797,0.02702703,-0.04032064,1.3003104,82.777548,-5.746112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient9193"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000021"
       cy="21.500011"
       fx="9.5000021"
       fy="21.500011"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9187"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9189"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient9167"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient9165"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,136,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient9163"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.1372797,0.02702703,-0.04032064,1.3003104,82.777548,-35.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       id="linearGradient9201"
       inkscape:collect="always">
      <stop
         id="stop9203"
         offset="0"
         style="stop-color:#71726f;stop-opacity:1" />
      <stop
         id="stop9205"
         offset="1"
         style="stop-color:#565854;stop-opacity:1" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9201"
       id="radialGradient9159"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.094947,-0.01232379,0.01228178,2.0949434,-10.679982,-24.66566)"
       cx="9.5000019"
       cy="22.633802"
       fx="9.5000019"
       fy="22.633802"
       r="2.0000012" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient9161"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000021"
       cy="21.500011"
       fx="9.5000021"
       fy="21.500011"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9155"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9157"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient9132"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-53.3755,99.5429)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient9128"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient9126"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient9124"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,67.425821,55.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient9118"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient9116"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.316067"
       fx="9.5000019"
       fy="20.316067"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient9122"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient9120"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9112"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9114"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient9090"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-89.3755,99.5429)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient9135"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(38,91)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient9086"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient9084"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient9082"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,31.425821,55.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient9076"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient9074"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.498825"
       fx="9.5000019"
       fy="20.498825"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient9080"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient9078"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9070"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient9072"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8938"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-125.3755,99.5429)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8936"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.5,92)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8934"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8932"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8930"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,-4.5741795,55.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8924"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8922"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.498825"
       fx="9.5000019"
       fy="20.498825"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8928"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8926"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8918"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8920"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8896"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-53.3755,68.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8894"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(71.5,61)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8892"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8890"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8888"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,67.425821,24.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8882"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8880"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.376987"
       fx="9.5000019"
       fy="20.376987"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8886"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8884"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8876"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8878"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8874"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-89.3755,68.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8872"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(35.5,61)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8870"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8868"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8866"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,31.425821,24.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8860"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017"
       gradientTransform="translate(0,-43.000022)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8858"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,-42.999987)"
       cx="9.5000019"
       cy="20.376987"
       fx="9.5000019"
       fy="20.376987"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8864"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8862"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8854"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8856"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8852"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-125.3755,68.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8850"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.5,61)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8848"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8846"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8844"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,-4.5741795,24.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8838"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017"
       gradientTransform="translate(0,-43.000022)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8836"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,-42.999987)"
       cx="9.5000019"
       cy="20.498825"
       fx="9.5000019"
       fy="20.498825"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8842"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8840"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8832"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8834"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8770"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-53.3755,38.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8768"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(71.5,31)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8766"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8764"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8762"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,67.425821,-5.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8756"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8754"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.255148"
       fx="9.5000019"
       fy="20.255148"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8760"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8758"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8750"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8752"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8748"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-89.3755,38.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8746"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(35.5,31)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8744"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8742"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8740"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,31.425821,-5.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8734"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8732"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.437906"
       fx="9.5000019"
       fy="20.437906"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8738"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8736"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8728"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8730"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8726"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-125.3755,38.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8724"
       gradientUnits="userSpaceOnUse"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634"
       gradientTransform="translate(-0.5,31)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8722"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8720"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8718"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,-4.5741795,-5.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8712"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8710"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.498825"
       fx="9.5000019"
       fy="20.498825"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8716"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8714"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8706"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8708"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8644"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-53.3755,8.5429038)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8642"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(71.5,1)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8640"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8638"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8636"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,67.425821,-35.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8630"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8628"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.437906"
       fx="9.5000019"
       fy="20.437906"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8634"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8632"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8624"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8602"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-89.3755,8.5429038)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8600"
       gradientUnits="userSpaceOnUse"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634"
       gradientTransform="translate(35.5,1)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8598"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8596"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8594"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,31.425821,-35.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8588"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017"
       gradientTransform="translate(0,-43.000022)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8586"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,-42.999987)"
       cx="9.5000019"
       cy="20.498825"
       fx="9.5000019"
       fy="20.498825"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8592"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8590"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8582"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8584"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient8554">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop8556" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop8558" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient8560"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12"
       gradientTransform="matrix(2.3541667,-0.1145833,0.05192057,1.0667318,-125.3755,8.5429038)"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient8544">
      <stop
         style="stop-color:#2e3436;stop-opacity:1;"
         offset="0"
         id="stop8546" />
      <stop
         style="stop-color:#2e3436;stop-opacity:0;"
         offset="1"
         id="stop8548" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient8550"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.5,1)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8466"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,30,32.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient8464"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.7342807,0.02702703,-0.0327179,1.3003104,-4.5741795,-35.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <filter
       inkscape:collect="always"
       id="filter8528">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.094969588"
         id="feGaussianBlur8530" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient8532">
      <stop
         style="stop-color:#555753;stop-opacity:1;"
         offset="0"
         id="stop8534" />
      <stop
         style="stop-color:#555753;stop-opacity:0;"
         offset="1"
         id="stop8536" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient8538"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017"
       gradientUnits="userSpaceOnUse" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient8478"
       cx="9.5000019"
       cy="22.387325"
       fx="9.5000019"
       fy="22.387325"
       r="2.0000012"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8456"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient8458"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <filter
       inkscape:collect="always"
       id="filter8372"
       x="-0.32675562"
       width="1.6535112"
       y="-0.3075347"
       height="1.6150694">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.38508518"
         id="feGaussianBlur8374" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient8272">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop8274" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop8276" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8272"
       id="radialGradient8278"
       cx="221.50121"
       cy="231.51643"
       fx="221.50121"
       fy="231.51643"
       r="1.4142135"
       gradientTransform="matrix(1,0,0,1.0625,0,-14.469773)"
       gradientUnits="userSpaceOnUse" />
    <filter
       inkscape:collect="always"
       id="filter8266">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.56039415"
         id="feGaussianBlur8268" />
    </filter>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8180"
       cx="37.434528"
       cy="228.36681"
       fx="37.434528"
       fy="228.36681"
       r="4.4194174"
       gradientTransform="matrix(4.2102648,0.07071068,-0.0599536,3.5697647,-106.12979,-586.50269)"
       gradientUnits="userSpaceOnUse" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8170"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.8051118,0,22.363614)"
       cx="56.375"
       cy="124.26783"
       fx="56.375"
       fy="124.26783"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient8168"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,142.25,124.21369)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8162"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8158"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8154"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625" />
    <filter
       inkscape:collect="always"
       id="filter8148"
       x="-0.2221075"
       width="1.444215"
       y="-0.5136236"
       height="2.0272472">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.85603933"
         id="feGaussianBlur8150" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient8012">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop8014" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop8016" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8012"
       id="radialGradient8018"
       cx="56.375"
       cy="121"
       fx="56.375"
       fy="121"
       r="4.625"
       gradientTransform="matrix(1,0,0,0.4324324,0,68.675676)"
       gradientUnits="userSpaceOnUse" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient7995"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,0,124.21369)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient7993"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.3648649,0.02702703,-0.02574872,1.3003104,-17.479924,56.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7989"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.094947,-0.01232379,0.01228178,2.0949434,-10.679982,-24.66566)"
       cx="9.5000019"
       cy="22.633802"
       fx="9.5000019"
       fy="22.633802"
       r="2.0000012" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7991"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000021"
       cy="21.500011"
       fx="9.5000021"
       fy="21.500011"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7985"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7987"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient7967"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,0,92.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient7965"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.3648649,0.02702703,-0.02574872,1.3003104,-17.479924,24.753888)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7961"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.094947,-0.01232379,0.01228178,2.0949434,-10.679982,-24.66566)"
       cx="9.5000019"
       cy="22.633802"
       fx="9.5000019"
       fy="22.633802"
       r="2.0000012" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7963"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000021"
       cy="21.500011"
       fx="9.5000021"
       fy="21.500011"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7957"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7959"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient7939"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.7426471,0,62.213693)"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient7937"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.3648649,0.02702703,-0.02574872,1.3003104,-17.479924,-5.246112)"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7933"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.094947,-0.01232379,0.01228178,2.0949434,-10.679982,-24.66566)"
       cx="9.5000019"
       cy="22.633802"
       fx="9.5000019"
       fy="22.633802"
       r="2.0000012" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7935"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000021"
       cy="21.500011"
       fx="9.5000021"
       fy="21.500011"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7929"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7931"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <filter
       inkscape:collect="always"
       id="filter7897">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.38483146"
         id="feGaussianBlur7899" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7861">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7863" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop7865" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7861"
       id="radialGradient7867"
       cx="133.5"
       cy="-6.6153889"
       fx="133.5"
       fy="-6.6153889"
       r="90.5"
       gradientTransform="matrix(1.7458564,-0.01104972,0.00555539,0.8777509,-99.535072,35.2818)"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3115"
       id="linearGradient6946"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(5.8093554,0,0,6.1456265,-9.924533,-21.20276)"
       x1="10.375"
       y1="11.0625"
       x2="10.25"
       y2="5.6206751" />
    <filter
       inkscape:collect="always"
       id="filter7763"
       x="-0.051701917"
       width="1.1034038"
       y="-0.54088159"
       height="2.0817632">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.36622191"
         id="feGaussianBlur7765" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7719">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7721" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop7723" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7719"
       id="radialGradient7725"
       cx="56"
       cy="124.6875"
       fx="56"
       fy="124.6875"
       r="8.5"
       gradientTransform="matrix(1,0,0,0.7426471,0,32.213693)"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7709">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7711" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop7713" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7709"
       id="radialGradient7715"
       cx="55.875"
       cy="112.89494"
       fx="55.875"
       fy="112.89494"
       r="9.25"
       gradientTransform="matrix(1.3648649,0.02702703,-0.02574872,1.3003104,-17.479924,-35.346112)"
       gradientUnits="userSpaceOnUse" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3115"
       id="radialGradient7368"
       cx="129.49998"
       cy="-5.3824277"
       fx="129.49998"
       fy="-5.3824277"
       r="92.949686"
       gradientTransform="matrix(1.0188274,0,-8.4344042e-8,0.1078672,-2.4381364,16.251584)"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7356">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7358" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop7360" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7356"
       id="radialGradient7362"
       cx="39"
       cy="77.25"
       fx="39"
       fy="77.25"
       r="1.5"
       gradientTransform="matrix(25.680624,-0.3804558,0.3333352,22.5,-988.29446,-1628.5372)"
       gradientUnits="userSpaceOnUse" />
    <filter
       inkscape:collect="always"
       id="filter7350">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.439375"
         id="feGaussianBlur7352" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7342">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7344" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop7346" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7342"
       id="linearGradient7348"
       x1="142"
       y1="231"
       x2="98"
       y2="127"
       gradientUnits="userSpaceOnUse" />
    <filter
       inkscape:collect="always"
       id="filter7555">
      <feBlend
         inkscape:collect="always"
         mode="screen"
         in2="BackgroundImage"
         id="feBlend7557" />
    </filter>
    <linearGradient
       id="linearGradient7541">
      <stop
         style="stop-color:#ffffff;stop-opacity:0"
         offset="0"
         id="stop7543" />
      <stop
         id="stop7549"
         offset="0.18079267"
         style="stop-color:#ffffff;stop-opacity:0.49803922;" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0.36875001"
         offset="0.53719509"
         id="stop7551" />
      <stop
         id="stop7553"
         offset="0.96285063"
         style="stop-color:#ffffff;stop-opacity:0" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0.60624999"
         offset="1"
         id="stop7545" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7541"
       id="linearGradient7547"
       x1="35.517193"
       y1="54.80405"
       x2="223.4828"
       y2="54.80405"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7172">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7174" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop7176" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7172"
       id="radialGradient7178"
       cx="197.9899"
       cy="179.83231"
       fx="197.9899"
       fy="179.83231"
       r="14.49569"
       gradientTransform="matrix(6.9252316,-0.02339605,0.00819456,2.425589,-1174.6019,-261.87109)"
       gradientUnits="userSpaceOnUse" />
    <filter
       inkscape:collect="always"
       id="filter9038">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.092082125"
         id="feGaussianBlur9040" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient9042">
      <stop
         style="stop-color:#ffffff;stop-opacity:0.43125001"
         offset="0"
         id="stop9044" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0"
         offset="1"
         id="stop9046" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9042"
       id="linearGradient9048"
       x1="13.779406"
       y1="29.598591"
       x2="13.775816"
       y2="24.5"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7104">
      <stop
         style="stop-color:#6b6e69;stop-opacity:1"
         offset="0"
         id="stop7106" />
      <stop
         style="stop-color:#555753;stop-opacity:1"
         offset="1"
         id="stop7108" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7104"
       id="radialGradient8961"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.7398762,-0.1394278,0.136854,2.6984926,-30.222535,-34.249554)"
       cx="15.489412"
       cy="23.992456"
       fx="15.489412"
       fy="23.992456"
       r="3" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient9219">
      <stop
         style="stop-color:#fcaf3e;stop-opacity:1;"
         offset="0"
         id="stop9221" />
      <stop
         style="stop-color:#fcaf3e;stop-opacity:0;"
         offset="1"
         id="stop9223" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9219"
       id="radialGradient9225"
       cx="185.38165"
       cy="33.250217"
       fx="185.38165"
       fy="33.250217"
       r="20.320606"
       gradientTransform="matrix(1.5167169,0.02460541,-0.01764404,1.0876066,-95.20316,-7.474331)"
       gradientUnits="userSpaceOnUse" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7705"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.094947,-0.01232379,0.01228178,2.0949434,-10.679982,-24.66566)"
       cx="9.5000019"
       cy="22.633802"
       fx="9.5000019"
       fy="22.633802"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7643">
      <stop
         style="stop-color:#555753;stop-opacity:1;"
         offset="0"
         id="stop7645" />
      <stop
         style="stop-color:#3c3e3b;stop-opacity:1"
         offset="1"
         id="stop7647" />
    </linearGradient>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7643"
       id="radialGradient7649"
       cx="9.5000021"
       cy="21.500011"
       fx="9.5000021"
       fy="21.500011"
       r="2.0000012"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7629"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <filter
       inkscape:collect="always"
       id="filter7615">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.0943149"
         id="feGaussianBlur7617" />
      <feBlend
         inkscape:collect="always"
         mode="screen"
         in2="BackgroundImage"
         id="feBlend7619" />
    </filter>
    <linearGradient
       id="linearGradient7621">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7623" />
      <stop
         style="stop-color:#ffffff;stop-opacity:0;"
         offset="1"
         id="stop7625" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient7627"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       id="linearGradient7767">
      <stop
         style="stop-color:#ffffff;stop-opacity:1;"
         offset="0"
         id="stop7769" />
      <stop
         style="stop-color:#c2e59f;stop-opacity:1"
         offset="1"
         id="stop7771" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7767"
       id="linearGradient7773"
       x1="129.49998"
       y1="78.893631"
       x2="129.49998"
       y2="34.714905"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       id="linearGradient7527">
      <stop
         style="stop-color:#8ae234;stop-opacity:1;"
         offset="0"
         id="stop7529" />
      <stop
         style="stop-color:#63af19;stop-opacity:1;"
         offset="1"
         id="stop7531" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7527"
       id="linearGradient7533"
       x1="139.21758"
       y1="93.714897"
       x2="138.5"
       y2="61.214905"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3093"
       id="linearGradient5449"
       gradientUnits="userSpaceOnUse"
       x1="8.125"
       y1="18.625"
       x2="8.125"
       y2="1.5623856"
       gradientTransform="matrix(5.0801517,0,0,5.0714903,7.5763599,7.892765)" />
    <filter
       inkscape:collect="always"
       id="filter7258">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="2.3907457"
         id="feGaussianBlur7260" />
    </filter>
    <clipPath
       clipPathUnits="userSpaceOnUse"
       id="clipPath7186">
      <rect
         style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         id="rect7188"
         width="187.96562"
         height="184.90331"
         x="35.517193"
         y="48.671291"
         rx="2.8749998"
         ry="2.875" />
    </clipPath>
    <linearGradient
       id="linearGradient6958">
      <stop
         id="stop6960"
         offset="0"
         style="stop-color:#a2a39f;stop-opacity:1" />
      <stop
         style="stop-color:#8d8f88;stop-opacity:1"
         offset="0.90325278"
         id="stop6962" />
      <stop
         id="stop6964"
         offset="1"
         style="stop-color:#babdb6;stop-opacity:1" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient6958"
       id="linearGradient5453"
       gradientUnits="userSpaceOnUse"
       x1="26.637926"
       y1="17.504595"
       x2="26.71343"
       y2="44.500103"
       gradientTransform="matrix(5.0801517,0,0,5.0714903,7.5763599,7.892765)" />
    <filter
       inkscape:collect="always"
       id="filter7801"
       x="-0.0404325"
       width="1.080865"
       y="-0.44700375"
       height="1.8940075">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="3.3525281"
         id="feGaussianBlur7803" />
    </filter>
    <filter
       inkscape:collect="always"
       id="filter7855"
       x="-0.10659477"
       width="1.2131895"
       y="-1.1784644"
       height="3.3569288">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="8.8384831"
         id="feGaussianBlur7857" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient9210">
      <stop
         style="stop-color:#eeeeec;stop-opacity:1;"
         offset="0"
         id="stop9212" />
      <stop
         style="stop-color:#eeeeec;stop-opacity:0;"
         offset="1"
         id="stop9214" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient9730">
      <stop
         style="stop-color:#babdb6;stop-opacity:1"
         offset="0"
         id="stop9732" />
      <stop
         style="stop-color:#888a85;stop-opacity:1"
         offset="1"
         id="stop9734" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient9724">
      <stop
         style="stop-color:#babdb6;stop-opacity:1"
         offset="0"
         id="stop9726" />
      <stop
         style="stop-color:#888a85;stop-opacity:1"
         offset="1"
         id="stop9728" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient9718">
      <stop
         style="stop-color:#babdb6;stop-opacity:1"
         offset="0"
         id="stop9720" />
      <stop
         style="stop-color:#888a85;stop-opacity:1"
         offset="1"
         id="stop9722" />
    </linearGradient>
    <linearGradient
       id="linearGradient9532"
       inkscape:collect="always">
      <stop
         id="stop9534"
         offset="0"
         style="stop-color:#eeeeec;stop-opacity:1" />
      <stop
         id="stop9536"
         offset="1"
         style="stop-color:#888a85;stop-opacity:1" />
    </linearGradient>
    <linearGradient
       id="linearGradient9526"
       inkscape:collect="always">
      <stop
         id="stop9528"
         offset="0"
         style="stop-color:#555753;stop-opacity:1" />
      <stop
         id="stop9530"
         offset="1"
         style="stop-color:#888a85;stop-opacity:1" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient9403">
      <stop
         style="stop-color:#888a85;stop-opacity:1"
         offset="0"
         id="stop9405" />
      <stop
         style="stop-color:#555753;stop-opacity:1"
         offset="1"
         id="stop9407" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       id="linearGradient8620">
      <stop
         style="stop-color:#2e3436;stop-opacity:1;"
         offset="0"
         id="stop8622" />
      <stop
         style="stop-color:#555753;stop-opacity:1"
         offset="1"
         id="stop8624" />
    </linearGradient>
    <linearGradient
       id="linearGradient10373">
      <stop
         style="stop-color:#ffffff;stop-opacity:0.37089202"
         offset="0"
         id="stop10375" />
      <stop
         style="stop-color:#a4a7a4;stop-opacity:0;"
         offset="1"
         id="stop10377" />
    </linearGradient>
    <linearGradient
       id="linearGradient3396"
       inkscape:collect="always">
      <stop
         id="stop3398"
         offset="0"
         style="stop-color:white;stop-opacity:1;" />
      <stop
         id="stop3400"
         offset="1"
         style="stop-color:white;stop-opacity:0;" />
    </linearGradient>
    <linearGradient
       id="linearGradient3245"
       inkscape:collect="always">
      <stop
         id="stop3247"
         offset="0"
         style="stop-color:#babdb6;stop-opacity:1" />
      <stop
         id="stop3249"
         offset="1"
         style="stop-color:#888a85;stop-opacity:1" />
    </linearGradient>
    <linearGradient
       id="linearGradient3221"
       inkscape:collect="always">
      <stop
         id="stop3223"
         offset="0"
         style="stop-color:white;stop-opacity:1;" />
      <stop
         id="stop3225"
         offset="1"
         style="stop-color:white;stop-opacity:0;" />
    </linearGradient>
    <linearGradient
       id="linearGradient3123"
       inkscape:collect="always">
      <stop
         id="stop3125"
         offset="0"
         style="stop-color:#888a85;stop-opacity:1;" />
      <stop
         id="stop3127"
         offset="1"
         style="stop-color:#babdb6;stop-opacity:1" />
    </linearGradient>
    <linearGradient
       id="linearGradient3115"
       inkscape:collect="always">
      <stop
         id="stop3117"
         offset="0"
         style="stop-color:white;stop-opacity:1;" />
      <stop
         id="stop3119"
         offset="1"
         style="stop-color:white;stop-opacity:0;" />
    </linearGradient>
    <linearGradient
       id="linearGradient3093">
      <stop
         id="stop3095"
         offset="0"
         style="stop-color:#2e3436;stop-opacity:1" />
      <stop
         id="stop3097"
         offset="1"
         style="stop-color:#555753;stop-opacity:1;" />
    </linearGradient>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3093"
       id="linearGradient9465"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.744539,0,0,0.7131556,301.22802,176.43027)"
       x1="8.125"
       y1="18.625"
       x2="8.125"
       y2="1.5623856" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient10373"
       id="linearGradient10379"
       x1="315.01389"
       y1="177.97581"
       x2="315.01389"
       y2="198.09837"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.2000005,0,0,1,-63.300185,2.2980232e-6)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3093"
       id="linearGradient10553"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.5408856,0,0,0.4165922,302.08476,218.87513)"
       x1="8.125"
       y1="18.625"
       x2="8.125"
       y2="1.5623856" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient10373"
       id="linearGradient10651"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7333333,0,0,0.7222223,80.733324,91.583327)"
       x1="315.01389"
       y1="177.97581"
       x2="315.01389"
       y2="198.09837" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3115"
       id="linearGradient8219"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.0425836,0,0,1,301.85024,125)"
       x1="10.375"
       y1="11.0625"
       x2="10.25"
       y2="5.6206751" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3396"
       id="linearGradient8224"
       gradientUnits="userSpaceOnUse"
       x1="7.625"
       y1="4.9375"
       x2="9.1875"
       y2="22.625"
       gradientTransform="matrix(1.134675,0,0,0.8516947,300.2593,125.37077)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3093"
       id="linearGradient8228"
       gradientUnits="userSpaceOnUse"
       x1="8.125"
       y1="18.625"
       x2="8.125"
       y2="1.5623856"
       gradientTransform="matrix(1.1219348,0,0,0.8773354,300.4902,125.184)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3123"
       id="linearGradient8232"
       gradientUnits="userSpaceOnUse"
       x1="11.579321"
       y1="21.053846"
       x2="35.079323"
       y2="52.56406"
       gradientTransform="matrix(1.1219348,0,0,1,300.4902,126)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3115"
       id="linearGradient8369"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(296,51)"
       x1="10.375"
       y1="11.0625"
       x2="10.25"
       y2="5.6206751" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3396"
       id="linearGradient8374"
       gradientUnits="userSpaceOnUse"
       x1="7.625"
       y1="4.9375"
       x2="9.1875"
       y2="22.625"
       gradientTransform="translate(296,50)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3093"
       id="linearGradient8378"
       gradientUnits="userSpaceOnUse"
       x1="8.125"
       y1="18.625"
       x2="8.125"
       y2="1.5623856"
       gradientTransform="translate(296,50)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3123"
       id="linearGradient8382"
       gradientUnits="userSpaceOnUse"
       x1="11.579321"
       y1="21.053846"
       x2="35.079323"
       y2="52.56406"
       gradientTransform="translate(296,50)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="linearGradient8388"
       gradientUnits="userSpaceOnUse"
       x1="14.49791"
       y1="20.819609"
       x2="15.223973"
       y2="22.249367" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="linearGradient8390"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.999989,4.291534e-6)"
       x1="14.49791"
       y1="20.819609"
       x2="17.692724"
       y2="24.905617" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="linearGradient8464"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.999989,4.291534e-6)"
       x1="14.49791"
       y1="20.819609"
       x2="14.911473"
       y2="22.593117" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="linearGradient8466"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-6,0)"
       x1="14.49791"
       y1="20.819609"
       x2="15.005223"
       y2="21.905617" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3245"
       id="radialGradient8468"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.959694,0,0,1.657851,-14.97639,-13.84084)"
       cx="15.902422"
       cy="21.731947"
       fx="15.902422"
       fy="21.731947"
       r="2.9999985" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="linearGradient8470"
       gradientUnits="userSpaceOnUse"
       x1="14.49791"
       y1="20.819609"
       x2="15.223973"
       y2="22.249367" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8620"
       id="linearGradient8626"
       x1="11.666673"
       y1="22.625292"
       x2="11.666673"
       y2="19.500015"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8620"
       id="linearGradient9401"
       gradientUnits="userSpaceOnUse"
       x1="11.666673"
       y1="22.625292"
       x2="10.833339"
       y2="19.750015"
       gradientTransform="matrix(0.7499994,0,0,0.7500009,301.87499,122.87497)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9403"
       id="radialGradient9409"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.5303692,2.9045263e-6,-1.3743314e-6,0.7241237,-165.08609,38.11425)" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9403"
       id="radialGradient9413"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.5303692,2.9045263e-6,-1.3743314e-6,0.7241237,-165.08609,42.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8620"
       id="linearGradient9415"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7499994,0,0,0.7500009,301.87499,126.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="10.833339"
       y2="19.750015" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9403"
       id="radialGradient9419"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.5303692,2.9045263e-6,-1.3743314e-6,0.7241237,-165.08609,46.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8620"
       id="linearGradient9421"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7499994,0,0,0.7500009,301.87499,130.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="10.833339"
       y2="19.750015" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9403"
       id="radialGradient9425"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.5303692,2.9045263e-6,-1.3743314e-6,0.7241237,-165.08609,50.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8620"
       id="linearGradient9427"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7499994,0,0,0.7500009,301.87499,134.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="10.833339"
       y2="19.750015" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9437"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-318.615,38.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9439"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,304.00001,122.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9540"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-318.615,42.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9542"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,304.00001,126.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9546"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-318.615,46.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9548"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,304.00001,130.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9552"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-318.615,50.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9554"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,304.00001,134.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9636"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-313.615,38.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9638"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,309.00001,122.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9640"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-313.615,42.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9642"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,309.00001,126.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9644"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-313.615,46.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9646"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,309.00001,130.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9648"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-313.615,50.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9650"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,309.00001,134.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9660"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-308.615,38.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9662"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,314.00001,122.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9664"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-308.615,42.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9666"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,314.00001,126.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9532"
       id="radialGradient9668"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-308.615,46.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9670"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,314.00001,130.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9730"
       id="radialGradient9706"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-303.615,38.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9708"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,319.00001,122.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9724"
       id="radialGradient9710"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-303.615,42.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9712"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,319.00001,126.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9718"
       id="radialGradient9714"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,6.7772265e-6,-1.8324426e-6,1.6896216,-303.615,-86.400038)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9716"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,1.7500017,319.00001,111.37493)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9730"
       id="radialGradient9738"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.0404929,2.9045263e-6,-1.8324426e-6,0.7241237,-308.615,50.11425)"
       cx="309.38129"
       cy="138.16031"
       fx="309.38129"
       fy="138.16031"
       r="2.0000006" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9526"
       id="linearGradient9740"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.9999995,0,0,0.7500009,314.00001,134.87497)"
       x1="11.666673"
       y1="22.625292"
       x2="9.5000038"
       y2="17.333351" />
    <filter
       inkscape:collect="always"
       id="filter9752"
       x="-0.048359518"
       width="1.096719"
       y="-0.36753233"
       height="1.7350647">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.76569236"
         id="feGaussianBlur9754" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9210"
       id="linearGradient9324"
       gradientUnits="userSpaceOnUse"
       x1="307.27084"
       y1="225.84029"
       x2="307.27084"
       y2="227.00362" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3221"
       id="radialGradient12456"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.9999983,0,3.5881993e-5)"
       cx="9.5000019"
       cy="20.498825"
       fx="9.5000019"
       fy="20.498825"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8532"
       id="linearGradient12458"
       gradientUnits="userSpaceOnUse"
       x1="9.9188643"
       y1="20.316927"
       x2="9.5000019"
       y2="24.507017" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3245"
       id="radialGradient12460"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.959694,0,0,1.657851,-14.97639,-13.84084)"
       cx="15.902422"
       cy="21.731947"
       fx="15.902422"
       fy="21.731947"
       r="2.9999985" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9201"
       id="radialGradient12462"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.094947,-0.01232379,0.01228178,2.0949434,-10.679982,-24.66566)"
       cx="9.5000019"
       cy="22.633802"
       fx="9.5000019"
       fy="22.633802"
       r="2.0000012" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3169"
       id="linearGradient3167"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7333333,0,0,0.7222223,80.733324,91.583327)"
       x1="315.01389"
       y1="177.97581"
       x2="315.01389"
       y2="181.75279" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3945"
       id="linearGradient3951"
       x1="304.625"
       y1="222.34544"
       x2="304.625"
       y2="217.86449"
       gradientUnits="userSpaceOnUse" />
    <filter
       inkscape:collect="always"
       id="filter4174"
       x="-0.063"
       width="1.126"
       y="-1.26"
       height="3.52">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.525"
         id="feGaussianBlur4176" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient4242"
       id="linearGradient4248"
       x1="320.30493"
       y1="194.08774"
       x2="318.73602"
       y2="187.84944"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-1,1)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient4242"
       id="linearGradient4256"
       x1="316.67725"
       y1="194.44554"
       x2="316.06232"
       y2="192.43666"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(0,1)" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient3646"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7825836,0,0,0.7825836,85.805879,116.78592)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient3648"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7825836,0,0,0.7825836,85.805879,116.78592)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient3650"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7825836,0,0,0.7825836,85.805879,116.78592)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient3652"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.7825836,0,0,0.7825836,85.805879,116.78592)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient4010"
       id="linearGradient3191"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.6666667,0,0,1,102.66667,0)"
       x1="309.875"
       y1="185.82629"
       x2="309.875"
       y2="184.39676" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient4178"
       id="linearGradient3193"
       gradientUnits="userSpaceOnUse"
       x1="309.40625"
       y1="184.5"
       x2="309.40625"
       y2="186.00293" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3213"
       id="linearGradient3209"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.6666667,0,0,1,102.66667,0)"
       x1="309.875"
       y1="185.82629"
       x2="309.875"
       y2="184.39676" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient4178"
       id="linearGradient3211"
       gradientUnits="userSpaceOnUse"
       x1="309.40625"
       y1="184.5"
       x2="309.40625"
       y2="186.00293" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient3115"
       id="linearGradient3182"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.8126761,0,0,0.6154869,300.05774,176.94417)"
       x1="10.375"
       y1="11.0625"
       x2="10.25"
       y2="5.6206751" />
    <clipPath
       clipPathUnits="userSpaceOnUse"
       id="clipPath4393">
      <rect
         y="53.536179"
         x="73.618324"
         height="22.85745"
         width="111.76333"
         id="rect4395"
         style="fill:none;stroke:#000000;stroke-width:1;stroke-opacity:1;marker:none;visibility:visible;display:inline;overflow:visible" />
    </clipPath>
    <filter
       inkscape:collect="always"
       id="filter4401"
       x="-0.028981541"
       width="1.0579631"
       y="-0.12773656"
       height="1.2554731">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="1.349614"
         id="feGaussianBlur4403" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9042"
       id="linearGradient4414"
       gradientUnits="userSpaceOnUse"
       x1="13.779406"
       y1="29.598591"
       x2="13.775816"
       y2="24.5" />
    <filter
       inkscape:collect="always"
       id="filter4447">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.096338348"
         id="feGaussianBlur4449" />
    </filter>
    <filter
       inkscape:collect="always"
       id="filter4451">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.049221138"
         id="feGaussianBlur4453" />
    </filter>
    <filter
       inkscape:collect="always"
       id="filter4455">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.049221138"
         id="feGaussianBlur4457" />
    </filter>
    <filter
       inkscape:collect="always"
       id="filter4459">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.12128867"
         id="feGaussianBlur4461" />
    </filter>
    <filter
       inkscape:collect="always"
       id="filter4463">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.12128867"
         id="feGaussianBlur4465" />
    </filter>
    <filter
       inkscape:collect="always"
       id="filter4467">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.12128867"
         id="feGaussianBlur4469" />
    </filter>
    <filter
       inkscape:collect="always"
       id="filter4471">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.048000006"
         id="feGaussianBlur4473" />
    </filter>
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient4477"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.8024089,-0.1145833,0.03975169,1.0667318,-108.03163,8.4429038)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient4481"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.8024089,-0.1145833,0.03975169,1.0667318,-108.03163,38.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient4485"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.8024089,-0.1145833,0.03975169,1.0667318,-108.03163,68.542904)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient4489"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.8024089,-0.1145833,0.03975169,1.0667318,-108.03163,100.5429)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient4493"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.8156893,-0.1145833,0.06209934,1.0667318,-58.306764,38.0429)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient4499"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.8156893,-0.1145833,0.06209934,1.0667318,-58.306764,8.7929)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <radialGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8554"
       id="radialGradient4503"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(2.7465278,-0.25893192,0.060574,2.4105686,-51.667246,-56.195297)"
       cx="88.625"
       cy="103.28233"
       fx="88.625"
       fy="103.28233"
       r="12" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient9042"
       id="linearGradient4507"
       gradientUnits="userSpaceOnUse"
       x1="13.779406"
       y1="29.598591"
       x2="13.775816"
       y2="24.5" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4513"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4515"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4521"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4523"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4529"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4531"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4537"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4539"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4549"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4551"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4557"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient7621"
       id="linearGradient4559"
       gradientUnits="userSpaceOnUse"
       x1="9.5000019"
       y1="23.077457"
       x2="9.5000019"
       y2="20.90847" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65166"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.5,1)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65168"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(35.5,1)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65170"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(71.5,1)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65172"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.5,31)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65174"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(35.5,31)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65176"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(71.5,31)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65178"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.5,61)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65180"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(35.5,61)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65182"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(71.5,61)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient8544"
       id="linearGradient65184"
       gradientUnits="userSpaceOnUse"
       gradientTransform="translate(-0.5,92)"
       x1="86.084511"
       y1="113.12634"
       x2="86.084511"
       y2="129.12634" />
  </defs>
  <g
     id="layer6"
     inkscape:groupmode="layer"
     inkscape:label="baseplate"
     style="display:none">
    <rect
       height="48"
       id="rect6284"
       inkscape:label="48x48"
       style="fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
       width="48"
       x="296"
       y="50" />
    <rect
       height="32"
       id="rect6592"
       inkscape:label="32x32"
       style="fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
       width="32"
       x="303"
       y="126" />
    <rect
       height="24"
       id="rect8628"
       inkscape:label="24x24"
       style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
       width="24"
       x="302"
       y="176" />
    <rect
       height="22"
       id="rect6749"
       inkscape:label="22x22"
       style="fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
       width="22"
       x="303"
       y="177" />
    <rect
       height="16"
       id="rect6833"
       inkscape:label="16x16"
       style="fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
       width="16"
       x="303"
       y="219" />
    <text
       id="context"
       inkscape:label="context"
       style="font-size:18.30070686px;font-style:normal;font-weight:normal;fill:#000000;fill-opacity:1;stroke:none;display:inline;enable-background:new;font-family:Bitstream Vera Sans"
       x="20.970737"
       xml:space="preserve"
       y="21.513618"><tspan
         id="tspan2716"
         sodipodi:role="line"
         x="20.970737"
         y="21.513618">apps</tspan></text>
    <text
       id="icon-name"
       inkscape:label="icon-name"
       sodipodi:linespacing="125%"
       style="font-size:18.30070686px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;fill:#000000;fill-opacity:1;stroke:none;display:inline;enable-background:new;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
       x="161.97073"
       xml:space="preserve"
       y="21.513618"><tspan
         id="tspan3023"
         sodipodi:role="line"
         x="161.97073"
         y="21.513618">accessories-calculator</tspan></text>
    <rect
       inkscape:label="256x256"
       y="36"
       x="24"
       height="256"
       width="256"
       id="rect6282"
       style="fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />
    <path
       style="opacity:0.29455285;fill:#729fcf;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
       d="m 24.0625,36 0,238 0,18 237.9375,0 18,0 0.0625,0 0,-18 -0.0625,0 0,-238 -18,0 0,238 -219.9375,0 0,-238 -18,0 z"
       id="rect3068-1"
       inkscape:connector-curvature="0" />
  </g>
  <g
     id="layer2"
     inkscape:groupmode="layer"
     inkscape:label="small sizes"
     style="display:inline">
    <rect
       style="opacity:0.3;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;filter:url(#filter9752);enable-background:new"
       id="rect9742"
       width="38"
       height="5"
       x="301"
       y="91"
       transform="matrix(1.0460526,0,0,0.8585786,-14.736842,13.57645)"
       ry="2.5"
       rx="2.5" />
    <rect
       y="58.040737"
       x="301.5"
       width="37"
       style="fill:url(#linearGradient8382);fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000024;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       ry="2.875"
       rx="2.875"
       id="rect2157"
       height="36.459362" />
    <rect
       y="52.5"
       x="302.5"
       width="35.000004"
       style="opacity:0.3;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#ffffff;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       ry="1.9236857"
       rx="1.9236857"
       id="rect3052"
       height="41.000008" />
    <path
       style="fill:url(#linearGradient8378);fill-opacity:1;fill-rule:nonzero;stroke:#2e3436;stroke-width:1.00000024;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       sodipodi:nodetypes="cccccc"
       id="rect3047"
       d="M 338.5,67 L 338.5,54.375 C 338.5,52.78225 337.21775,51.5 335.625,51.5 L 304.375,51.5 C 302.78225,51.5 301.5,52.78225 301.5,54.375 L 301.5,67" />
    <rect
       y="57"
       x="304"
       width="32"
       style="fill:#8ae234;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       ry="1.1762378"
       rx="1.1762378"
       id="rect3045"
       height="9" />
    <path
       style="opacity:0.2;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8374);stroke-width:1.00000036;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       sodipodi:nodetypes="cccccc"
       id="path3072"
       d="M 337.5,66.510137 L 337.5,54.347874 C 337.5,53.298322 336.70204,52.500001 335.65296,52.500001 L 304.34705,52.500001 C 303.29797,52.500001 302.5,53.298323 302.5,54.347874 L 302.5,66.510137" />
    <rect
       y="59"
       x="309"
       width="22"
       style="opacity:0.6;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       id="rect3075"
       height="5" />
    <path
       style="opacity:0.3;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       id="rect3555"
       d="M 309,59 L 309,59.5 L 309,64 L 309.5,64 L 309.5,59.5 L 331,59.5 L 331,59 L 309.5,59 L 309,59 z" />
    <path
       style="opacity:0.4;fill:url(#linearGradient8369);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       sodipodi:nodetypes="ccccccc"
       id="rect3109"
       d="M 305.1875,57 C 304.53586,57 304,57.535864 304,58.1875 L 304,63.21875 C 315.70221,58.558037 328.20602,60.991812 336,64.53125 L 336,58.1875 C 336,57.535864 335.46414,57 334.8125,57 L 305.1875,57 z" />
    <g
       transform="translate(296,50.000004)"
       id="g3253">
      <rect
         y="19.5"
         x="13.499995"
         width="4.9999967"
         style="opacity:1;fill:url(#radialGradient8468);fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000024;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="1.046875"
         rx="1.046875"
         id="rect3133"
         height="3.9999957" />
      <rect
         y="20.499979"
         x="14.499989"
         width="3.0000131"
         style="opacity:0.4;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8470);stroke-width:1;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="0"
         rx="0"
         id="rect3211"
         height="2.0000167" />
    </g>
    <g
       id="g3279"
       transform="translate(296,50)">
      <rect
         y="19.500013"
         x="7.500001"
         width="4.0000024"
         style="opacity:1;fill:#555753;fill-opacity:1;fill-rule:nonzero;stroke:#2e3436;stroke-width:1.0000006;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="1.016466"
         rx="1.016466"
         id="rect3131"
         height="3.9999957" />
      <rect
         y="20.499979"
         x="8.4999886"
         width="2.0000114"
         style="opacity:0.3;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8466);stroke-width:1;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="0"
         rx="0"
         id="rect3229"
         height="2.000021" />
    </g>
    <use
       y="0"
       xlink:href="#g3279"
       x="0"
       width="48"
       transform="translate(0,6)"
       id="use3283"
       height="48" />
    <use
       y="0"
       xlink:href="#use3283"
       x="0"
       width="48"
       transform="translate(0,6)"
       id="use3285"
       height="48" />
    <use
       y="0"
       xlink:href="#use3285"
       x="0"
       width="48"
       transform="translate(0,6)"
       id="use3287"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(-4.887581e-6,5.999996)"
       id="use3331"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(-4.887581e-6,12)"
       id="use3333"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(6.999995,-4e-6)"
       id="use3335"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(6.999995,5.999996)"
       id="use3337"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(6.999995,12)"
       id="use3339"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(6.999995,18)"
       id="use3341"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(14,-4e-6)"
       id="use3343"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(14,12)"
       id="use3345"
       height="48" />
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(14,5.999996)"
       id="use3347"
       height="48" />
    <g
       transform="translate(318,50)"
       id="g3349">
      <rect
         y="19.5"
         x="12.5"
         width="5.9999919"
         style="opacity:1;fill:#888a85;fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000024;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="1.046875"
         rx="1.046875"
         id="rect3351"
         height="3.9999957" />
      <rect
         y="20.499983"
         x="13.5"
         width="4"
         style="opacity:0.4;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8464);stroke-width:1;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="0"
         rx="0"
         id="rect3353"
         height="2.0000172" />
    </g>
    <use
       y="0"
       xlink:href="#g3349"
       x="0"
       width="48"
       transform="translate(0,6)"
       id="use3359"
       height="48" />
    <g
       transform="translate(318,62)"
       id="use3363">
      <rect
         y="19.5"
         x="12.5"
         width="6"
         style="opacity:1;fill:#888a85;fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000024;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="1.046875"
         rx="1.046875"
         id="rect3367"
         height="10" />
      <rect
         y="20.499983"
         x="13.5"
         width="4"
         style="opacity:0.4;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8390);stroke-width:1;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="0"
         rx="0"
         id="rect3369"
         height="8.0000172" />
    </g>
    <use
       y="0"
       xlink:href="#g3253"
       x="0"
       width="48"
       transform="translate(-4.887581e-6,18)"
       id="use3375"
       height="48" />
    <g
       transform="translate(310,68)"
       id="use3377">
      <rect
         y="19.5"
         x="13.499995"
         width="4.9999967"
         style="opacity:1;fill:#888a85;fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000024;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="1.046875"
         rx="1.046875"
         id="rect3381"
         height="3.9999957" />
      <rect
         y="20.499979"
         x="14.499989"
         width="3.0000131"
         style="opacity:0.4;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8388);stroke-width:1;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
         ry="0"
         rx="0"
         id="rect3383"
         height="2.0000167" />
    </g>
    <path
       style="font-size:3.17188883px;font-style:normal;font-weight:bold;fill:#eeeeec;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;font-family:Bitstream Vera Sans"
       id="text3390"
       d="M 307.39492,54.105439 L 307.39492,54.602037 C 307.32628,54.545349 307.25716,54.5034 307.18758,54.476187 C 307.11894,54.448978 307.04748,54.435372 306.9732,54.435371 C 306.83215,54.435372 306.72214,54.485259 306.64316,54.585031 C 306.56511,54.683671 306.52609,54.821993 306.52609,54.999996 C 306.52609,55.178002 306.56511,55.31689 306.64316,55.416663 C 306.72214,55.515303 306.83215,55.564622 306.9732,55.564622 C 307.05218,55.564622 307.12693,55.55045 307.19746,55.522105 C 307.26892,55.493761 307.33474,55.451811 307.39492,55.396255 L 307.39492,55.894554 C 307.31593,55.929701 307.23554,55.955778 307.15373,55.972785 C 307.07287,55.990925 306.99153,55.999996 306.90973,55.999996 C 306.62482,55.999996 306.40197,55.912127 306.24118,55.73639 C 306.08039,55.55952 306,55.314056 306,54.999996 C 306,54.685939 306.08039,54.441041 306.24118,54.265303 C 306.40197,54.088434 306.62482,53.999999 306.90973,53.999997 C 306.99247,53.999999 307.07381,54.009069 307.15373,54.027208 C 307.2346,54.044217 307.31499,54.070294 307.39492,54.105439 M 308.58533,54.435371 C 308.47343,54.435372 308.38786,54.484125 308.32863,54.581629 C 308.27033,54.678002 308.24118,54.817458 308.24118,54.999996 C 308.24118,55.182537 308.27033,55.322559 308.32863,55.420064 C 308.38786,55.516436 308.47343,55.564622 308.58533,55.564622 C 308.69534,55.564622 308.77949,55.516436 308.83779,55.420064 C 308.89609,55.322559 308.92524,55.182537 308.92524,54.999996 C 308.92524,54.817458 308.89609,54.678002 308.83779,54.581629 C 308.77949,54.484125 308.69534,54.435372 308.58533,54.435371 M 308.58533,53.999997 C 308.85707,53.999999 309.0691,54.088434 309.22143,54.265303 C 309.3747,54.442175 309.45133,54.687073 309.45133,54.999996 C 309.45133,55.312922 309.3747,55.557819 309.22143,55.73469 C 309.0691,55.91156 308.85707,55.999996 308.58533,55.999996 C 308.31264,55.999996 308.0992,55.91156 307.94499,55.73469 C 307.79172,55.557819 307.71509,55.312922 307.71509,54.999996 C 307.71509,54.687073 307.79172,54.442175 307.94499,54.265303 C 308.0992,54.088434 308.31264,53.999999 308.58533,53.999997 M 311.0959,54.105439 L 311.0959,54.602037 C 311.02726,54.545349 310.95815,54.5034 310.88857,54.476187 C 310.81993,54.448978 310.74846,54.435372 310.67418,54.435371 C 310.53314,54.435372 310.42312,54.485259 310.34414,54.585031 C 310.26609,54.683671 310.22707,54.821993 310.22707,54.999996 C 310.22707,55.178002 310.26609,55.31689 310.34414,55.416663 C 310.42312,55.515303 310.53314,55.564622 310.67418,55.564622 C 310.75316,55.564622 310.82792,55.55045 310.89844,55.522105 C 310.9699,55.493761 311.03572,55.451811 311.0959,55.396255 L 311.0959,55.894554 C 311.01692,55.929701 310.93652,55.955778 310.85472,55.972785 C 310.77385,55.990925 310.69252,55.999996 310.61071,55.999996 C 310.3258,55.999996 310.10295,55.912127 309.94216,55.73639 C 309.78138,55.55952 309.70098,55.314056 309.70098,54.999996 C 309.70098,54.685939 309.78138,54.441041 309.94216,54.265303 C 310.10295,54.088434 310.3258,53.999999 310.61071,53.999997 C 310.69346,53.999999 310.77479,54.009069 310.85472,54.027208 C 310.93558,54.044217 311.01598,54.070294 311.0959,54.105439 M 312.28631,54.435371 C 312.17441,54.435372 312.08885,54.484125 312.02961,54.581629 C 311.97131,54.678002 311.94216,54.817458 311.94216,54.999996 C 311.94216,55.182537 311.97131,55.322559 312.02961,55.420064 C 312.08885,55.516436 312.17441,55.564622 312.28631,55.564622 C 312.39632,55.564622 312.48048,55.516436 312.53878,55.420064 C 312.59707,55.322559 312.62622,55.182537 312.62622,54.999996 C 312.62622,54.817458 312.59707,54.678002 312.53878,54.581629 C 312.48048,54.484125 312.39632,54.435372 312.28631,54.435371 M 312.28631,53.999997 C 312.55805,53.999999 312.77009,54.088434 312.92242,54.265303 C 313.07568,54.442175 313.15232,54.687073 313.15232,54.999996 C 313.15232,55.312922 313.07568,55.557819 312.92242,55.73469 C 312.77009,55.91156 312.55805,55.999996 312.28631,55.999996 C 312.01362,55.999996 311.80018,55.91156 311.64597,55.73469 C 311.4927,55.557819 311.41607,55.312922 311.41607,54.999996 C 311.41607,54.687073 311.4927,54.442175 311.64597,54.265303 C 311.80018,54.088434 312.01362,53.999999 312.28631,53.999997 M 314.22848,55.093534 C 314.12317,55.093535 314.04371,55.115077 313.99012,55.15816 C 313.93746,55.201244 313.91113,55.264736 313.91113,55.348636 C 313.91113,55.425734 313.93229,55.486391 313.9746,55.530608 C 314.01785,55.573692 314.07756,55.595234 314.15373,55.595234 C 314.24869,55.595234 314.32862,55.554418 314.3935,55.472785 C 314.45838,55.390019 314.49082,55.286845 314.49082,55.163262 L 314.49082,55.093534 L 314.22848,55.093534 M 314.99999,54.863942 L 314.99999,55.950676 L 314.49082,55.950676 L 314.49082,55.668363 C 314.42312,55.78401 314.34696,55.868477 314.26233,55.921764 C 314.1777,55.973919 314.07474,55.999996 313.95344,55.999996 C 313.78983,55.999996 313.65678,55.942739 313.55429,55.828227 C 313.45274,55.712581 313.40196,55.562922 313.40196,55.379248 C 313.40196,55.155893 313.46543,54.992061 313.59237,54.887752 C 313.72025,54.783444 313.92053,54.73129 314.19322,54.731289 L 314.49082,54.731289 L 314.49082,54.68367 C 314.49082,54.5873 314.45932,54.517005 314.39632,54.472786 C 314.33332,54.427436 314.23506,54.40476 314.10154,54.404759 C 313.99341,54.40476 313.8928,54.417799 313.79971,54.443874 C 313.70662,54.469953 313.62011,54.509068 313.54019,54.561221 L 313.54019,54.096936 C 313.64832,54.065192 313.75692,54.041382 313.866,54.025507 C 313.97507,54.008502 314.08414,53.999999 314.19322,53.999997 C 314.47813,53.999999 314.68358,54.068026 314.80958,54.204079 C 314.93652,54.339001 314.99999,54.558955 314.99999,54.863942" />
    <rect
       y="54"
       x="327"
       width="8"
       style="opacity:0.3;fill:#fcaf3e;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       id="rect3394"
       height="2" />
    <g
       id="g3522"
       transform="translate(296,50)">
      <path
         style="font-size:2.1034534px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3443"
         d="m 16.500046,34.000104 -0.436339,0 0,-0.719423 c -0.159423,0.06522 -0.347312,0.11345 -0.56367,0.1447 l 0,-0.173233 c 0.113872,-0.0163 0.23758,-0.0471 0.371122,-0.09239 0.133541,-0.04574 0.225156,-0.09896 0.274846,-0.159645 l 0.354041,0 0,0.999991"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10345578px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3447"
         d="m 23.764759,33.822846 0,0.177308 -1.529518,0 c 0.01656,-0.06703 0.06625,-0.130433 0.149069,-0.190215 0.08282,-0.06024 0.246379,-0.139945 0.490688,-0.239129 0.196689,-0.08016 0.317289,-0.13451 0.361805,-0.163042 0.06004,-0.0394 0.09006,-0.07835 0.09006,-0.116847 -2e-6,-0.04257 -0.0264,-0.07518 -0.07919,-0.09783 -0.05176,-0.0231 -0.123709,-0.03465 -0.215841,-0.03465 -0.0911,10e-7 -0.163563,0.012 -0.217393,0.03601 -0.05383,0.024 -0.08489,0.06386 -0.09317,0.119565 l -0.434788,-0.01902 c 0.02588,-0.105071 0.107145,-0.180478 0.243793,-0.226221 0.136646,-0.04574 0.307456,-0.06861 0.512426,-0.06861 0.22464,0 0.401142,0.02649 0.529509,0.07948 0.128364,0.05299 0.192548,0.118885 0.192549,0.197688 -1e-6,0.04484 -0.01864,0.08764 -0.0559,0.128396 -0.03623,0.04031 -0.09421,0.08265 -0.173915,0.127037 -0.0528,0.02944 -0.148037,0.07178 -0.285717,0.127037 -0.137685,0.05525 -0.225159,0.09194 -0.262425,0.110053 -0.03623,0.01812 -0.06574,0.03578 -0.08851,0.05299 l 0.866469,0"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10345769px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3451"
         d="m 29.275646,33.73593 0.422364,-0.02242 c 0.01346,0.0471 0.04969,0.08311 0.108698,0.108016 0.059,0.02491 0.130435,0.03736 0.214288,0.03736 0.09006,0 0.165631,-0.01494 0.22671,-0.04484 0.06211,-0.02989 0.09317,-0.0702 0.09317,-0.120923 -2e-6,-0.04801 -0.0295,-0.08605 -0.08851,-0.11413 -0.05901,-0.02808 -0.130955,-0.04212 -0.215841,-0.04212 -0.0559,0 -0.122673,0.0048 -0.200314,0.01427 l 0.04814,-0.15557 c 0.118013,0.0014 0.208076,-0.0097 0.27019,-0.03329 0.06211,-0.024 0.09317,-0.0557 0.09317,-0.09511 0,-0.03351 -0.02277,-0.06023 -0.06832,-0.08016 -0.04555,-0.01993 -0.106111,-0.02989 -0.181679,-0.02989 -0.07454,1e-6 -0.138202,0.01132 -0.190996,0.03397 -0.0528,0.02265 -0.08489,0.05571 -0.09628,0.09918 l -0.402177,-0.02989 c 0.02795,-0.06023 0.06987,-0.108241 0.125777,-0.14402 0.05693,-0.03623 0.135612,-0.06454 0.236027,-0.08492 0.10145,-0.02083 0.214805,-0.03125 0.340066,-0.03125 0.214286,10e-7 0.386132,0.02989 0.515533,0.08967 0.106626,0.04891 0.159939,0.104167 0.159941,0.16576 -2e-6,0.08741 -0.109216,0.157155 -0.327644,0.209237 0.130435,0.01223 0.234473,0.03963 0.312115,0.0822 0.07867,0.04257 0.118012,0.09398 0.118014,0.154211 -2e-6,0.08741 -0.07298,0.16191 -0.218946,0.223504 -0.145967,0.06159 -0.327646,0.09239 -0.545038,0.09239 -0.206007,0 -0.376816,-0.02582 -0.512428,-0.07745 -0.135611,-0.05208 -0.214288,-0.120017 -0.236027,-0.203803"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10346055px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3455"
         d="m 30.769506,27.248206 -0.422366,0.02038 c -0.01035,-0.03804 -0.03727,-0.06612 -0.08075,-0.08424 -0.04348,-0.01812 -0.0999,-0.02717 -0.169257,-0.02717 -0.09213,1e-6 -0.170293,0.01812 -0.234475,0.05435 -0.06315,0.03623 -0.103004,0.11164 -0.119566,0.226222 0.108696,-0.05616 0.243791,-0.08424 0.405283,-0.08424 0.182195,10e-7 0.337995,0.03035 0.467398,0.09103 0.130434,0.06069 0.195653,0.13904 0.195654,0.235053 -10e-7,0.101902 -0.06833,0.183649 -0.204972,0.245243 -0.136649,0.06159 -0.312117,0.09239 -0.526403,0.09239 -0.229817,0 -0.418744,-0.03895 -0.566777,-0.116847 -0.148036,-0.07835 -0.222053,-0.20652 -0.222053,-0.384508 0,-0.182517 0.07712,-0.314083 0.231369,-0.394699 0.154246,-0.08061 0.354558,-0.120923 0.600939,-0.120923 0.17288,0 0.315738,0.02129 0.428576,0.06386 0.113873,0.04212 0.186337,0.103487 0.217396,0.184102 m -0.989144,0.416437 c 0,0.06205 0.03261,0.110055 0.09783,0.144021 0.06522,0.03352 0.139753,0.05027 0.223606,0.05027 0.08075,0 0.148033,-0.01381 0.201867,-0.04144 0.05383,-0.02763 0.08074,-0.07292 0.08075,-0.135869 -2e-6,-0.06476 -0.02899,-0.112091 -0.08696,-0.141982 -0.05797,-0.03034 -0.130437,-0.04552 -0.217393,-0.04552 -0.08385,10e-7 -0.154765,0.01449 -0.212736,0.04348 -0.05797,0.02853 -0.08696,0.07088 -0.08696,0.127037"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10346389px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3459"
         d="m 22.297487,27.744179 0.434789,-0.0197 c 0.01242,0.04303 0.04917,0.07722 0.11025,0.10258 0.06108,0.02491 0.131471,0.03737 0.211183,0.03737 0.0911,0 0.16822,-0.01608 0.231369,-0.04823 0.06315,-0.03261 0.09472,-0.08152 0.09472,-0.146739 -1e-6,-0.06114 -0.03158,-0.106882 -0.09472,-0.137227 -0.06211,-0.0308 -0.143376,-0.0462 -0.243792,-0.0462 -0.125262,1e-6 -0.237582,0.02423 -0.336961,0.07269 l -0.354042,-0.02242 0.223606,-0.51834 1.153742,0 0,0.178667 -0.822992,0 -0.06832,0.169158 c 0.09731,-0.02129 0.19669,-0.03193 0.298141,-0.03193 0.193583,1e-6 0.357664,0.0308 0.492243,0.09239 0.134576,0.0616 0.201865,0.141531 0.201867,0.239809 -2e-6,0.08197 -0.05435,0.155117 -0.163047,0.219428 -0.148036,0.08786 -0.353525,0.131793 -0.616467,0.131793 -0.210149,0 -0.381477,-0.02468 -0.513984,-0.07405 -0.132506,-0.04937 -0.211699,-0.115715 -0.23758,-0.199048"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10346723px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3467"
         d="m 16.146912,28.000345 0,-0.200406 -0.931691,0 0,-0.16712 0.987593,-0.632471 0.366464,0 0,0.631792 0.282614,0 0,0.167799 -0.282614,0 0,0.200406 -0.422366,0 m 0,-0.368205 0,-0.340352 -0.523299,0.340352 0.523299,0"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10347009px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3473"
         d="m 15.291336,21.19536 0,-0.17731 1.492262,0 0,0.138587 c -0.123193,0.05299 -0.248454,0.129076 -0.375783,0.22826 -0.127333,0.09919 -0.224643,0.20471 -0.291931,0.316576 -0.06626,0.111413 -0.09886,0.21105 -0.09783,0.298912 l -0.420814,0 c 0.0072,-0.13768 0.07195,-0.278078 0.194101,-0.421194 0.123191,-0.143116 0.287271,-0.271059 0.492245,-0.383831 l -0.992253,0"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10347342px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3477"
         d="m 22.665601,21.463056 c -0.112839,-0.02083 -0.195139,-0.04937 -0.246899,-0.0856 -0.05073,-0.03668 -0.07609,-0.07677 -0.07609,-0.120244 0,-0.07428 0.05901,-0.135642 0.177022,-0.184104 0.119049,-0.04846 0.287789,-0.07269 0.50622,-0.07269 0.216359,2e-6 0.384064,0.02423 0.503115,0.07269 0.120083,0.04846 0.180126,0.109829 0.180127,0.184104 -10e-7,0.0462 -0.02743,0.08741 -0.0823,0.123642 -0.05487,0.03578 -0.131991,0.06318 -0.23137,0.0822 0.126295,0.02219 0.222052,0.05457 0.287273,0.09715 0.06625,0.04257 0.09938,0.09171 0.09938,0.147418 -2e-6,0.09194 -0.06729,0.166667 -0.201867,0.224186 -0.133544,0.05752 -0.311601,0.08628 -0.534172,0.08628 -0.207043,0 -0.379407,-0.02378 -0.51709,-0.07133 -0.162529,-0.05616 -0.243792,-0.133152 -0.243792,-0.230978 0,-0.0539 0.03054,-0.10326 0.09162,-0.148098 0.06108,-0.04529 0.157353,-0.08016 0.288825,-0.10462 m 0.09006,-0.192255 c -2e-6,0.03804 0.02433,0.06771 0.07298,0.089 0.04969,0.02129 0.115426,0.03193 0.197209,0.03193 0.08282,1e-6 0.14907,-0.01064 0.198761,-0.03193 0.04969,-0.02174 0.07453,-0.05163 0.07454,-0.08967 -1e-6,-0.03578 -0.02485,-0.06431 -0.07454,-0.0856 -0.04866,-0.02174 -0.113357,-0.03261 -0.194103,-0.03261 -0.08385,1e-6 -0.150625,0.01087 -0.200314,0.03261 -0.04969,0.02174 -0.07454,0.0505 -0.07454,0.08628 m -0.04037,0.42663 c -2e-6,0.05254 0.03054,0.09352 0.09162,0.122963 0.06211,0.02944 0.139236,0.04416 0.231371,0.04416 0.09006,1e-6 0.164597,-0.01404 0.223606,-0.04212 0.05901,-0.02853 0.08851,-0.06952 0.08851,-0.122963 -2e-6,-0.04665 -0.03002,-0.08401 -0.09006,-0.112092 -0.06004,-0.02853 -0.136132,-0.0428 -0.228265,-0.0428 -0.106628,0 -0.18634,0.01608 -0.239135,0.04823 -0.05176,0.03216 -0.07764,0.06703 -0.07764,0.104619"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10347676px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3481"
         d="m 29.300734,21.770157 0.422369,-0.02038 c 0.01035,0.03759 0.03727,0.06544 0.08075,0.08356 0.04348,0.01812 0.100933,0.02717 0.172364,0.02717 0.09006,0 0.166669,-0.01812 0.229818,-0.05435 0.06315,-0.03623 0.10352,-0.111413 0.121121,-0.225543 -0.109735,0.05571 -0.246901,0.08356 -0.4115,0.08356 -0.179093,1e-6 -0.333857,-0.03012 -0.464294,-0.09035 -0.129403,-0.06069 -0.194103,-0.139493 -0.194103,-0.236414 0,-0.100996 0.06832,-0.182291 0.204972,-0.243886 0.137684,-0.06205 0.312635,-0.09307 0.524855,-0.09307 0.230852,10e-7 0.420297,0.03918 0.568335,0.117527 0.148034,0.0779 0.222052,0.206297 0.222054,0.385191 -2e-6,0.182067 -0.07713,0.313407 -0.231371,0.394023 -0.154249,0.08062 -0.355082,0.120924 -0.602496,0.120924 -0.178058,0 -0.321953,-0.02061 -0.431687,-0.06182 -0.109733,-0.04167 -0.180127,-0.103714 -0.211184,-0.186141 m 0.987597,-0.417121 c 0,-0.06159 -0.03261,-0.109374 -0.09783,-0.143343 -0.06419,-0.03397 -0.13872,-0.05095 -0.223607,-0.05095 -0.08075,0 -0.148037,0.01404 -0.201867,0.04212 -0.0528,0.02763 -0.07919,0.07314 -0.07919,0.136549 0,0.06431 0.02899,0.111641 0.08696,0.141984 0.05797,0.02989 0.130437,0.04484 0.217395,0.04484 0.08385,1e-6 0.154248,-0.01449 0.211185,-0.04348 0.05797,-0.02899 0.08696,-0.07156 0.08696,-0.127718"
         inkscape:connector-curvature="0" />
      <path
         style="font-size:2.10345864px;font-style:normal;font-weight:bold;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Arial"
         id="text3485"
         d="m 23.028762,39.000222 c 0.220499,10e-7 0.392861,0.03442 0.517087,0.10326 0.148034,0.08152 0.22205,0.216711 0.222052,0.405568 -2e-6,0.188405 -0.07454,0.32382 -0.223605,0.406247 -0.123191,0.06793 -0.295035,0.101902 -0.515534,0.101902 -0.221535,0 -0.400108,-0.03714 -0.53572,-0.111412 -0.135613,-0.07473 -0.203419,-0.207653 -0.203419,-0.398775 0,-0.187498 0.07454,-0.322461 0.223606,-0.404888 0.123188,-0.06793 0.295034,-0.101901 0.515533,-0.101902 m 0,0.158287 c -0.0528,10e-7 -0.0999,0.0075 -0.141306,0.02242 -0.04141,0.01449 -0.0735,0.04076 -0.09627,0.0788 -0.03002,0.04937 -0.04503,0.132473 -0.04503,0.249319 -2e-6,0.116848 0.01346,0.197236 0.04037,0.241167 0.02691,0.04348 0.06056,0.07246 0.100932,0.08696 0.04141,0.01449 0.08851,0.02174 0.141306,0.02174 0.05279,0 0.0999,-0.0072 0.141307,-0.02174 0.04141,-0.01495 0.0735,-0.04144 0.09627,-0.07948 0.03002,-0.04891 0.04503,-0.131792 0.04503,-0.24864 -1e-6,-0.116846 -0.01346,-0.197008 -0.04037,-0.240488 -0.02692,-0.04393 -0.06108,-0.07314 -0.102486,-0.08764 -0.04037,-0.01494 -0.08696,-0.02242 -0.139753,-0.02242"
         inkscape:connector-curvature="0" />
    </g>
    <rect
       style="opacity:0.3;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;filter:url(#filter9752);enable-background:new"
       id="rect9756"
       width="38"
       height="5"
       x="301"
       y="91"
       transform="matrix(0.7861845,0,0,0.6249991,67.483469,96.62508)"
       rx="2.5"
       ry="2.5" />
    <rect
       y="132.26346"
       x="305.5"
       width="26.965326"
       style="fill:url(#linearGradient8232);fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000119;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       ry="1.8323157"
       rx="2.0952787"
       id="rect137"
       height="23.236544" />
    <rect
       y="128.5"
       x="306.5"
       width="24.962812"
       style="opacity:0.3;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#ffffff;stroke-width:1.00000072;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       ry="0.95473367"
       rx="1.0833105"
       id="rect139"
       height="26.000013" />
    <path
       style="fill:url(#linearGradient8228);fill-opacity:1;fill-rule:nonzero;stroke:#2e3436;stroke-width:1.00000072;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       sodipodi:nodetypes="cccccc"
       id="path141"
       d="M 332.46535,135.88895 L 332.46535,128.21875 C 332.46535,127.26657 331.53086,126.5 330.37007,126.5 L 307.5953,126.5 C 306.43452,126.5 305.50001,127.26657 305.50001,128.21875 L 305.50001,135.88895" />
    <rect
       y="129.9649"
       x="308"
       width="21.999998"
       style="fill:#8ae234;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       ry="0.65805256"
       rx="0.77190608"
       id="rect143"
       height="5.0350981" />
    <path
       style="opacity:0.2;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8224);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       sodipodi:nodetypes="cccccc"
       id="path145"
       d="M 331.46286,135.37377 L 331.46286,128.53851 C 331.46286,127.94866 330.89373,127.5 330.14551,127.5 L 307.81737,127.5 C 307.06914,127.5 306.50001,127.94866 306.50001,128.53851 L 306.50001,135.37377" />
    <rect
       y="131"
       x="311"
       width="16"
       style="opacity:0.6;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       id="rect147"
       height="3" />
    <path
       style="opacity:0.3;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       id="path149"
       d="M 311,131 L 311,131.3 L 311,134 L 311.34091,134 L 311.34091,131.3 L 327,131.3 L 327,131 L 311.34091,131 L 311,131 z"
       sodipodi:nodetypes="ccccccccc" />
    <path
       style="opacity:0.4;fill:url(#linearGradient8219);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       sodipodi:nodetypes="ccccccc"
       id="path151"
       d="M 309,129.9649 C 308.55588,129.9649 308.19067,130.31171 308.19067,130.73345 L 308.19067,133.98964 C 316.16621,130.97326 324.68808,132.54838 330,134.83909 L 330,130.73345 C 330,130.31171 329.63478,129.9649 329.19067,129.9649 L 309,129.9649 z" />
    <rect
       y="127.64832"
       x="323.94974"
       width="5.1715727"
       style="opacity:0.3;fill:#fcaf3e;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       id="rect171"
       height="1.2943897" />
    <rect
       y="128"
       x="309"
       width="5.9930873"
       style="fill:#c5cbd2;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1.00000036;stroke-linecap:round;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       ry="0.97080517"
       rx="0.97080517"
       id="rect4669"
       height="1.1299423" />
    <rect
       style="opacity:0.7;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.5;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:1.5;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;filter:url(#filter4174);enable-background:new"
       id="rect4168"
       width="20"
       height="1"
       x="304"
       y="198"
       transform="matrix(1.05,0,0,1,-16.2,0)" />
    <path
       style="fill:#7e7f7b;fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000119;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 305.46669,180.92874 L 321.53329,180.92874 C 322.62285,180.92874 323.49999,181.79526 323.49999,182.87162 L 323.49999,196.29194 C 323.49999,197.36831 322.62285,198.50001 321.53329,198.50001 L 305.46669,198.50001 C 304.37714,198.50001 303.49999,197.36831 303.49999,196.29194 L 303.49999,182.87162 C 303.49999,181.79526 304.37714,180.92874 305.46669,180.92874 z"
       id="rect9467"
       sodipodi:nodetypes="ccccccccc" />
    <rect
       style="opacity:0.8;fill:#555753;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.5;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:1.5;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect3984"
       width="17"
       height="13"
       x="305"
       y="184"
       rx="0.74374998"
       ry="0.50555557" />
    <path
       style="fill:url(#linearGradient9465);fill-opacity:1;fill-rule:nonzero;stroke:#2e3436;stroke-width:1.00000048;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       sodipodi:nodetypes="cccccc"
       id="path9463"
       d="M 323.50002,185.03225 L 323.50002,179.33461 C 323.50002,178.56061 322.69238,177.5 321.92204,177.5 L 305.20299,177.5 C 304.43266,177.5 303.5,178.56061 303.5,179.33461 L 303.5,185.03225" />
    <rect
       y="180"
       x="305"
       width="17"
       style="fill:#8ae234;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       ry="0.75916445"
       rx="0.92184258"
       id="rect9593"
       height="4" />
    <rect
       y="181"
       x="307"
       width="13"
       style="opacity:0.6;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect9595"
       height="2" />
    <rect
       y="178.5"
       x="304.5"
       width="18.000008"
       style="opacity:0.3;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient10379);stroke-width:1.0000006;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       ry="0.45473349"
       rx="0.54568046"
       id="rect10371"
       height="17.999998" />
    <rect
       y="219.5"
       x="304.5"
       width="13"
       style="fill:#7e7f7b;fill-opacity:1;fill-rule:nonzero;stroke:#555753;stroke-width:1.00000119;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       ry="1.7439274"
       rx="1.7439274"
       id="rect10549"
       height="15.000006" />
    <path
       style="fill:url(#linearGradient10553);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient3951);stroke-width:1.00000048;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       sodipodi:nodetypes="cccccc"
       id="path10551"
       d="M 317.5,224 L 317.5,220.65989 C 317.5,220.20776 316.76823,219.50001 316.20861,219.50001 L 305.66638,219.50001 C 305.10676,219.50001 304.5,220.20776 304.5,220.65989 L 304.5,224" />
    <rect
       y="221"
       x="306"
       width="10"
       style="fill:#8ae234;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       ry="0"
       rx="0"
       id="rect10555"
       height="2" />
    <rect
       y="220.5"
       x="305.5"
       width="11"
       style="opacity:0.3;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient10651);stroke-width:1.0000006;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       ry="0.45473349"
       rx="0.50020683"
       id="rect10649"
       height="13" />
    <rect
       y="222"
       x="306.59375"
       width="8.8125"
       style="opacity:0.6;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect10653"
       height="1" />
    <rect
       height="3.0000005"
       id="rect8480"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9409);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9401);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible"
       width="2.999999"
       x="307.5"
       y="137.5" />
    <rect
       height="3.0000005"
       id="rect9411"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9413);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9415);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="2.999999"
       x="307.5"
       y="141.5" />
    <rect
       height="3.0000005"
       id="rect9417"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9419);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9421);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="2.999999"
       x="307.5"
       y="145.5" />
    <rect
       height="3.0000005"
       id="rect9423"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9425);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9427);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="2.999999"
       x="307.5"
       y="149.5" />
    <rect
       height="3.0000005"
       id="rect9429"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9437);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9439);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="311.5"
       y="137.5" />
    <rect
       height="3.0000005"
       id="rect9538"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9540);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9542);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="311.5"
       y="141.5" />
    <rect
       height="3.0000005"
       id="rect9544"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9546);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9548);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="311.5"
       y="145.5" />
    <rect
       height="3.0000005"
       id="rect9550"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9552);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9554);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="311.5"
       y="149.5" />
    <rect
       height="3.0000005"
       id="rect9628"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9636);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9638);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="316.5"
       y="137.5" />
    <rect
       height="3.0000005"
       id="rect9630"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9640);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9642);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="316.5"
       y="141.5" />
    <rect
       height="3.0000005"
       id="rect9632"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9644);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9646);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="316.5"
       y="145.5" />
    <rect
       height="3.0000005"
       id="rect9634"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9648);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9650);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="316.5"
       y="149.5" />
    <rect
       height="3.0000005"
       id="rect9652"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9660);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9662);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="321.5"
       y="137.5" />
    <rect
       height="3.0000005"
       id="rect9654"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9664);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9666);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="321.5"
       y="141.5" />
    <rect
       height="3.0000005"
       id="rect9656"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9668);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9670);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="321.5"
       y="145.5" />
    <rect
       height="3.0000005"
       id="rect9700"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9706);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9708);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="326.5"
       y="137.5" />
    <rect
       height="3.0000005"
       id="rect9702"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9710);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9712);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="326.5"
       y="141.5" />
    <rect
       height="6.9999995"
       id="rect9704"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9714);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9716);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="326.5"
       y="145.5" />
    <rect
       height="3.0000005"
       id="rect9736"
       rx="0.69999999"
       ry="0.69999999"
       style="fill:url(#radialGradient9738);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9740);stroke-width:1.00000072;stroke-linecap:square;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       width="4"
       x="321.5"
       y="149.5" />
    <rect
       style="opacity:1;fill:url(#linearGradient4256);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect10142"
       width="2"
       height="2"
       x="315"
       y="194"
       rx="0.69999999"
       ry="0.46666667" />
    <path
       style="fill:#888a85;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 318.46667,185 L 320.53333,185 C 320.79187,185 321,185.20813 321,185.46667 L 321,186.53333 C 321,186.79187 320.79187,187 320.53333,187 L 318.46667,187 C 318.20813,187 318,186.79187 318,186.53333 L 318,185.46667 C 318,185.20813 318.20813,185 318.46667,185 z"
       id="rect10144"
       sodipodi:nodetypes="ccccccccc" />
    <path
       style="fill:#888a85;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 318.46667,188 L 320.53333,188 C 320.79187,188 321,188.20813 321,188.46667 L 321,189.53333 C 321,189.79187 320.79187,190 320.53333,190 L 318.46667,190 C 318.20813,190 318,189.79187 318,189.53333 L 318,188.46667 C 318,188.20813 318.20813,188 318.46667,188 z"
       id="rect10146"
       sodipodi:nodetypes="ccccccccc" />
    <path
       style="fill:url(#linearGradient4248);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 318.5,191 L 320.5,191 C 320.777,191 321,191.223 321,191.5 L 321,195.5 C 321,195.777 320.777,196 320.5,196 L 318.5,196 C 318.223,196 318,195.777 318,195.5 L 318,191.5 C 318,191.223 318.223,191 318.5,191 z"
       id="rect10150"
       sodipodi:nodetypes="ccccccccc" />
    <path
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 315.46875,194 C 315.21022,194 315,194.21022 315,194.46875 L 315,195.53125 C 315,195.78978 315.21021,196 315.46875,196 L 316,196 L 316,195 L 317,195 L 317,194.46875 C 317,194.21022 316.78979,194 316.53125,194 L 315.46875,194 z"
       id="path10185"
       sodipodi:nodetypes="cccccccccc" />
    <path
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 318.46875,185 C 318.21022,185 318,185.21022 318,185.46875 L 318,186.53125 C 318,186.78978 318.21021,187 318.46875,187 L 319,187 L 319,186 L 321,186 L 321,185.46875 C 321,185.21022 320.78979,185 320.53125,185 L 318.46875,185 z"
       id="path10187"
       sodipodi:nodetypes="cccccccccc" />
    <path
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 318.46875,188 C 318.21022,188 318,188.21022 318,188.46875 L 318,189.53125 C 318,189.78978 318.21021,190 318.46875,190 L 319,190 L 319,189 L 321,189 L 321,188.46875 C 321,188.21022 320.78979,188 320.53125,188 L 318.46875,188 z"
       id="path10189"
       sodipodi:nodetypes="cccccccccc" />
    <path
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       d="M 318.46875,191 C 318.21022,191 318,191.21022 318,191.46875 L 318,195.53125 C 318,195.78978 318.21021,196 318.46875,196 L 319,196 L 319,192 L 321,192 L 321,191.46875 C 321,191.21022 320.78979,191 320.53125,191 L 318.46875,191 z"
       id="path10191"
       sodipodi:nodetypes="cccccccccc" />
    <rect
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect10231"
       width="1"
       height="1"
       x="318"
       y="185"
       rx="0.46666667"
       ry="0.46666667" />
    <rect
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect10233"
       width="1"
       height="1"
       x="318"
       y="188"
       rx="0.46666667"
       ry="0.46666667" />
    <rect
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect10235"
       width="1"
       height="1"
       x="318"
       y="191"
       rx="0.46666667"
       ry="0.46666667" />
    <rect
       style="opacity:0.2;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect10237"
       width="1"
       height="1"
       x="315"
       y="194"
       rx="0.46666667"
       ry="0.46666667" />
    <g
       id="use8226"
       transform="translate(2,0)">
      <rect
         style="opacity:0.5;fill:#a7aba2;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
         id="rect8236"
         width="2"
         height="2"
         x="306"
         y="225"
         rx="0.46666667"
         ry="0.46666667" />
      <path
         style="opacity:0.2;fill:url(#linearGradient9324);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
         d="M 306.46875,225 C 306.21022,225 306,225.21022 306,225.46875 L 306,226.53125 C 306,226.78978 306.21021,227 306.46875,227 L 307,227 L 307,226 L 308,226 L 308,225.46875 C 308,225.21022 307.78979,225 307.53125,225 L 306.46875,225 z"
         id="path8238" />
      <rect
         style="opacity:1;fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
         id="rect8240"
         width="1"
         height="1"
         x="306"
         y="225"
         rx="0.46666667"
         ry="0.46666667" />
    </g>
    <g
       id="g9199">
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="225"
         x="306"
         height="2"
         width="2"
         id="rect8330"
         style="opacity:0.7;fill:#2e3436;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <path
         id="path8332"
         d="M 306.46875,225 C 306.21022,225 306,225.21022 306,225.46875 L 306,226.53125 C 306,226.78978 306.21021,227 306.46875,227 L 307,227 L 307,226 L 308,226 L 308,225.46875 C 308,225.21022 307.78979,225 307.53125,225 L 306.46875,225 z"
         style="opacity:0.5;fill:#555753;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="225"
         x="306"
         height="1"
         width="1"
         id="rect8334"
         style="opacity:0.3;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
    </g>
    <g
       style="display:inline;enable-background:new"
       id="g8360"
       transform="translate(0,1)">
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="230"
         x="312"
         height="2"
         width="2"
         id="rect8354"
         style="opacity:0.8;fill:#50524e;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <path
         id="path8356"
         d="M 312.46875,230 C 312.21022,230 312,230.21022 312,230.46875 L 312,231.53125 C 312,231.78978 312.21021,232 312.46875,232 L 313,232 L 313,231 L 314,231 L 314,230.46875 C 314,230.21022 313.78979,230 313.53125,230 L 312.46875,230 z"
         style="opacity:0.5;fill:#888a85;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="230"
         x="312"
         height="1"
         width="1"
         id="rect8358"
         style="opacity:0.5;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
    </g>
    <use
       x="0"
       y="0"
       xlink:href="#g8360"
       id="use8393"
       transform="translate(2,-6)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g8360"
       id="use8395"
       transform="translate(2,-4)"
       width="400"
       height="300" />
    <g
       style="display:inline;enable-background:new"
       id="g8399"
       transform="translate(2,1)">
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="228"
         x="312"
         height="4.0000062"
         width="2"
         id="rect8401"
         style="opacity:0.8;fill:#50524e;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <path
         id="path8403"
         d="M 312.46875,228 C 312.21022,228 312,228.21022 312,228.46875 L 312,231.53125 C 312,231.78978 312.21021,232 312.46875,232 L 313,232 L 313,229 L 314,229 L 314,228.46875 C 314,228.21022 313.78979,228 313.53125,228 L 312.46875,228 z"
         style="opacity:0.5;fill:#888a85;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
         sodipodi:nodetypes="cccccccccc" />
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="228"
         x="312"
         height="1"
         width="1"
         id="rect8405"
         style="opacity:0.5;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
    </g>
    <use
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9177"
       transform="translate(2,0)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9179"
       transform="translate(4,0)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9181"
       transform="translate(4,2)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9183"
       transform="translate(2,2)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9185"
       transform="translate(0,2)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9187"
       transform="translate(0,4)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9189"
       transform="translate(2,4)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9191"
       transform="translate(4,4)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9193"
       transform="translate(2,6)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#use8226"
       id="use9195"
       transform="translate(0,6)"
       width="400"
       height="300" />
    <use
       x="0"
       y="0"
       xlink:href="#g9199"
       id="use9204"
       transform="translate(0,2)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g9199"
       id="use9206"
       transform="translate(0,4)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g9199"
       id="use9208"
       transform="translate(0,6)"
       width="400"
       height="300" />
    <rect
       y="220.5"
       x="305.5"
       width="11"
       style="opacity:0.4;fill:none;fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient3167);stroke-width:1.0000006;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       ry="0.45473349"
       rx="0.50020683"
       id="rect3165"
       height="13" />
    <g
       id="g4034"
       transform="translate(1,1)">
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="184"
         x="308"
         height="2"
         width="2"
         id="rect3986"
         style="opacity:1;fill:url(#linearGradient3191);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <path
         sodipodi:nodetypes="cccccccccc"
         id="path3992"
         d="M 308.46875,184 C 308.21022,184 308,184.21022 308,184.46875 L 308,185.53125 C 308,185.78978 308.21021,186 308.46875,186 L 309,186 L 309,185 L 310,185 L 310,184.46875 C 310,184.21022 309.78979,184 309.53125,184 L 308.46875,184 z"
         style="opacity:0.2;fill:url(#linearGradient3193);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="184"
         x="308"
         height="1"
         width="1"
         id="rect3998"
         style="opacity:0.7;fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
    </g>
    <use
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4146"
       width="400"
       height="300"
       transform="translate(3,0)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4148"
       width="400"
       height="300"
       transform="translate(6,0)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4150"
       width="400"
       height="300"
       transform="translate(6,3)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4152"
       width="400"
       height="300"
       transform="translate(3,3)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4154"
       width="400"
       height="300"
       transform="translate(0,3)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4156"
       width="400"
       height="300"
       transform="translate(0,6)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4158"
       width="400"
       height="300"
       transform="translate(3,6)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4160"
       width="400"
       height="300"
       transform="translate(6,6)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4162"
       width="400"
       height="300"
       transform="translate(3,9)" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g4034"
       id="use4164"
       width="400"
       height="300"
       transform="translate(0,9)" />
    <rect
       style="opacity:0.42672412;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.5;stroke-linecap:square;stroke-linejoin:round;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:1.5;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       id="rect4166"
       width="6"
       height="1"
       x="307"
       y="178"
       rx="0.46666667"
       ry="0.46666667" />
    <g
       style="display:inline;enable-background:new"
       id="g3195"
       transform="translate(-2,1)">
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="184"
         x="308"
         height="2"
         width="2"
         id="rect3197"
         style="opacity:1;fill:url(#linearGradient3209);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <path
         sodipodi:nodetypes="cccccccccc"
         id="path3199"
         d="M 308.46875,184 C 308.21022,184 308,184.21022 308,184.46875 L 308,185.53125 C 308,185.78978 308.21021,186 308.46875,186 L 309,186 L 309,185 L 310,185 L 310,184.46875 C 310,184.21022 309.78979,184 309.53125,184 L 308.46875,184 z"
         style="opacity:0.2;fill:url(#linearGradient3211);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
      <rect
         ry="0.46666667"
         rx="0.46666667"
         y="184"
         x="308"
         height="1"
         width="1"
         id="rect3201"
         style="opacity:0.7;fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new" />
    </g>
    <use
       x="0"
       y="0"
       xlink:href="#g3195"
       id="use3219"
       transform="translate(0,3)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g3195"
       id="use3221"
       transform="translate(0,6)"
       width="400"
       height="300" />
    <use
       style="display:inline;enable-background:new"
       x="0"
       y="0"
       xlink:href="#g3195"
       id="use3223"
       transform="translate(0,9)"
       width="400"
       height="300" />
    <path
       style="opacity:0.4;fill:url(#linearGradient3182);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;stroke-linecap:round;stroke-linejoin:miter;marker:none;marker-start:none;marker-mid:none;marker-end:none;stroke-miterlimit:6;stroke-dasharray:none;stroke-dashoffset:1.4;stroke-opacity:1;visibility:visible;display:inline;overflow:visible;enable-background:new"
       sodipodi:nodetypes="ccccccc"
       id="path3180"
       d="M 305.63086,180 C 305.28467,180 305,180.21346 305,180.47303 L 305,182.47717 C 311.2168,180.62063 317.85945,181.5901 322,183 L 322,180.47303 C 322,180.21346 321.71532,180 321.36914,180 L 305.63086,180 z" />
    <g
       id="g4418"
       style="font-size:40px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;opacity:0.85199998;fill:#000000;fill-opacity:1;stroke:none;display:inline;enable-background:new;font-family:Digital2;-inkscape-font-specification:Digital2"
       transform="matrix(0.12531293,0,0.0156056,0.12531293,307.31987,54.615058)">
      <path
         id="path4420"
         d="m 119.16872,44.56 c 0.23998,2.7e-5 0.53332,-0.159972 0.88,-0.48 l 3.84,-3.44 c 0.13331,-0.106635 0.17331,-0.226635 0.12,-0.36 -0.0533,-0.133301 -0.18669,-0.199968 -0.4,-0.2 l -15.12,0 c -0.24,3.2e-5 -0.38667,0.05336 -0.44,0.16 -0.0533,0.08003 -0.08,0.146698 -0.08,0.2 0,0.05336 0.0267,0.106698 0.08,0.16 0.37333,0.426698 1.41333,1.586696 3.12,3.48 0.29333,0.320028 0.54666,0.480027 0.76,0.48 l 7.24,0 m 0.08,10.32 c -0.0267,0.160017 -2e-5,0.266684 0.08,0.32 0.10665,0.05335 0.22665,0.04002 0.36,-0.04 l 3.64,-1.96 c 0.45331,-0.239981 0.70665,-0.546647 0.76,-0.92 l 1.16,-10.28 c 0.0266,-0.213303 -0.0134,-0.346636 -0.12,-0.4 -0.08,-0.0533 -0.13335,-0.07997 -0.16,-0.08 -0.08,3e-5 -0.14669,0.0267 -0.2,0.08 -0.0267,0.0267 -1.34669,1.200029 -3.96,3.52 -0.34668,0.29336 -0.53335,0.57336 -0.56,0.84 l -1,8.92 m -8.24,0.56 3.04,-1.64 c 0.34666,-0.186648 0.65332,-0.186648 0.92,0 0.90665,0.586684 1.81332,1.146684 2.72,1.68 0.42665,0.240016 0.62665,0.440016 0.6,0.6 -0.0267,0.213349 -0.29335,0.453349 -0.8,0.72 -1.78668,0.933348 -2.81334,1.480014 -3.08,1.64 -0.32001,0.18668 -0.62668,0.18668 -0.92,0 -0.61334,-0.399986 -1.52001,-0.973319 -2.72,-1.72 -0.34667,-0.213318 -0.50667,-0.439984 -0.48,-0.68 0.0267,-0.159984 0.26666,-0.359984 0.72,-0.6 m 7.24,-3.36 c 0.0266,-0.213313 -0.04,-0.333313 -0.2,-0.36 -0.08,2e-5 -0.56001,0.213353 -1.44,0.64 -0.45335,0.240019 -0.50668,0.466686 -0.16,0.68 0.23999,0.133352 0.62665,0.360019 1.16,0.68 0.26665,0.160018 0.45332,-0.02665 0.56,-0.56 0.0267,-0.346647 0.0533,-0.706647 0.08,-1.08 m -1.72,15.48 c 0.23999,4e-6 0.50665,0.160004 0.8,0.48 l 3.04,3.44 c 0.10665,0.133334 0.11998,0.266667 0.04,0.4 -0.08,0.106667 -0.24002,0.16 -0.48,0.16 l -15.08,0 c -0.24,0 -0.38667,-0.05333 -0.44,-0.16 -0.08,-0.186666 0.50667,-0.826666 1.76,-1.92 0.77333,-0.639997 1.53333,-1.279997 2.28,-1.92 0.37333,-0.319996 0.66666,-0.479996 0.88,-0.48 l 7.2,0 m 2.44,-10.32 c 0.0533,-0.373318 0.22665,-0.466651 0.52,-0.28 l 3.2,1.96 c 0.39998,0.240013 0.57331,0.560013 0.52,0.96 l -1.16,10.24 c -0.0267,0.320002 -0.16002,0.480001 -0.4,0.48 -0.08,1e-6 -0.13335,-0.02666 -0.16,-0.08 -0.29335,-0.319998 -1.34668,-1.49333 -3.16,-3.52 -0.26668,-0.293328 -0.38668,-0.573328 -0.36,-0.84 l 1,-8.92 m -8.8,2.8 c -0.0267,0.213345 0.04,0.333345 0.2,0.36 0.13333,1.2e-5 0.62666,-0.213322 1.48,-0.64 0.26666,-0.133321 0.39999,-0.266654 0.4,-0.4 -1e-5,-0.106654 -0.08,-0.199987 -0.24,-0.28 -0.29334,-0.159987 -0.69334,-0.386653 -1.2,-0.68 -0.24001,-0.13332 -0.41334,0.06668 -0.52,0.6 -0.0267,0.346679 -0.0667,0.693346 -0.12,1.04"
         inkscape:connector-curvature="0" />
      <path
         id="path4422"
         d="m 125.95372,68.28 c 0.18667,-0.159996 0.34667,-0.159996 0.48,0 l 1.36,1.36 c 0.18667,0.186669 0.28,0.346669 0.28,0.48 -0.0267,0.160002 -0.17333,0.346668 -0.44,0.56 l -1.64,1.32 c -0.16,0.133333 -0.30666,0.133333 -0.44,0 -0.45333,-0.48 -0.90666,-0.933332 -1.36,-1.36 -0.16,-0.159998 -0.22666,-0.346665 -0.2,-0.56 1e-5,-0.106665 0.65334,-0.706664 1.96,-1.8"
         inkscape:connector-curvature="0" />
      <path
         id="path4424"
         d="m 147.51372,56.08 c -2e-5,0.160016 0.42665,0.480015 1.28,0.96 0.23998,0.186681 0.37331,0.106682 0.4,-0.24 l 0.16,-1.64 c 0.0266,-0.07998 -0.0134,-0.133316 -0.12,-0.16 -0.10669,1.7e-5 -0.20002,0.02668 -0.28,0.08 -0.45335,0.21335 -0.93335,0.546683 -1.44,1 m -2.64,-1.2 c -0.0267,0.160017 -2e-5,0.266684 0.08,0.32 0.10665,0.05335 0.22665,0.04002 0.36,-0.04 l 3.64,-1.96 c 0.45331,-0.239981 0.70665,-0.546647 0.76,-0.92 l 1.16,-10.28 c 0.0266,-0.213303 -0.0134,-0.346636 -0.12,-0.4 -0.08,-0.0533 -0.13335,-0.07997 -0.16,-0.08 -0.08,3e-5 -0.14669,0.0267 -0.2,0.08 -0.0267,0.0267 -1.34669,1.200029 -3.96,3.52 -0.34668,0.29336 -0.53335,0.57336 -0.56,0.84 l -1,8.92 m -0.28,2.36 c 0.0533,-0.373318 0.22665,-0.466651 0.52,-0.28 l 3.2,1.96 c 0.39998,0.240013 0.57331,0.560013 0.52,0.96 l -1.16,10.24 c -0.0267,0.320002 -0.16002,0.480001 -0.4,0.48 -0.08,1e-6 -0.13335,-0.02666 -0.16,-0.08 -0.29335,-0.319998 -1.34668,-1.49333 -3.16,-3.52 -0.26668,-0.293328 -0.38668,-0.573328 -0.36,-0.84 l 1,-8.92"
         inkscape:connector-curvature="0" />
      <path
         id="path4426"
         d="m 173.13872,56.08 c -2e-5,0.160016 0.42665,0.480015 1.28,0.96 0.23998,0.186681 0.37331,0.106682 0.4,-0.24 l 0.16,-1.64 c 0.0266,-0.07998 -0.0134,-0.133316 -0.12,-0.16 -0.10669,1.7e-5 -0.20002,0.02668 -0.28,0.08 -0.45335,0.21335 -0.93335,0.546683 -1.44,1 m -2.64,-1.2 c -0.0267,0.160017 -2e-5,0.266684 0.08,0.32 0.10665,0.05335 0.22665,0.04002 0.36,-0.04 l 3.64,-1.96 c 0.45331,-0.239981 0.70665,-0.546647 0.76,-0.92 l 1.16,-10.28 c 0.0266,-0.213303 -0.0134,-0.346636 -0.12,-0.4 -0.08,-0.0533 -0.13335,-0.07997 -0.16,-0.08 -0.08,3e-5 -0.14669,0.0267 -0.2,0.08 -0.0267,0.0267 -1.34669,1.200029 -3.96,3.52 -0.34668,0.29336 -0.53335,0.57336 -0.56,0.84 l -1,8.92 m -8.24,0.56 3.04,-1.64 c 0.34666,-0.186648 0.65332,-0.186648 0.92,0 0.90665,0.586684 1.81332,1.146684 2.72,1.68 0.42665,0.240016 0.62665,0.440016 0.6,0.6 -0.0267,0.213349 -0.29335,0.453349 -0.8,0.72 -1.78668,0.933348 -2.81334,1.480014 -3.08,1.64 -0.32001,0.18668 -0.62668,0.18668 -0.92,0 -0.61334,-0.399986 -1.52001,-0.973319 -2.72,-1.72 -0.34667,-0.213318 -0.50667,-0.439984 -0.48,-0.68 0.0267,-0.159984 0.26666,-0.359984 0.72,-0.6 m 7.96,1.8 c 0.0533,-0.373318 0.22665,-0.466651 0.52,-0.28 l 3.2,1.96 c 0.39998,0.240013 0.57331,0.560013 0.52,0.96 l -1.16,10.24 c -0.0267,0.320002 -0.16002,0.480001 -0.4,0.48 -0.08,1e-6 -0.13335,-0.02666 -0.16,-0.08 -0.29335,-0.319998 -1.34668,-1.49333 -3.16,-3.52 -0.26668,-0.293328 -0.38668,-0.573328 -0.36,-0.84 l 1,-8.92 m -1.48,1.64 c -0.0267,0.213346 -0.08,0.600013 -0.16,1.16 -0.0533,0.426678 -0.26668,0.506678 -0.64,0.24 -0.21335,-0.106655 -0.52001,-0.279988 -0.92,-0.52 -0.21335,-0.133321 -0.32001,-0.253321 -0.32,-0.36 -1e-5,-0.106654 0.0933,-0.213321 0.28,-0.32 0.42665,-0.186654 0.87999,-0.41332 1.36,-0.68 0.26665,-0.159986 0.39999,1.4e-5 0.4,0.48 m -8.04,-4 c -0.0533,0.346683 -0.21334,0.440017 -0.48,0.28 l -3.2,-1.96 c -0.42667,-0.266648 -0.61334,-0.573314 -0.56,-0.92 l 1.16,-10.28 c 0.0267,-0.213303 0.10666,-0.35997 0.24,-0.44 0.18666,-0.106636 0.77333,0.40003 1.76,1.52 0.58666,0.693362 1.15999,1.373361 1.72,2.04 0.29333,0.320027 0.42666,0.600026 0.4,0.84 l -1.04,8.92 m 1.52,-1.64 c 0.0267,-0.213314 0.0667,-0.599981 0.12,-1.16 0.0533,-0.426646 0.27999,-0.506646 0.68,-0.24 0.29332,0.186687 0.59999,0.36002 0.92,0.52 0.37332,0.266686 0.37332,0.493352 0,0.68 -0.26668,0.133352 -0.72001,0.360019 -1.36,0.68 -0.16001,0.08002 -0.26667,0.06668 -0.32,-0.04 -0.0533,-0.133315 -0.0667,-0.279981 -0.04,-0.44"
         inkscape:connector-curvature="0" />
    </g>
  </g>
  <g
     id="layer4"
     inkscape:groupmode="layer"
     inkscape:label="hires"
     style="display:inline">
    <g
       id="g11761"
       transform="matrix(1.064329,0,0,1.064329,14.30689,23.274638)">
      <rect
         transform="matrix(1.1206032,0,0,1.1206032,-15.738693,-27.738693)"
         style="opacity:0.37356322;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7855);enable-background:accumulate"
         id="rect7805"
         width="199"
         height="18"
         x="31"
         y="221"
         rx="8.0313902"
         ry="8.0313902" />
      <rect
         transform="matrix(0.9698491,0,0,0.9698491,2.9346734,5.9346734)"
         ry="9.2797928"
         rx="9.2797928"
         y="221"
         x="31"
         height="18"
         width="199"
         id="rect7775"
         style="opacity:0.61494254;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7801);enable-background:accumulate" />
      <rect
         ry="2.875"
         rx="2.8749998"
         y="48.671291"
         x="35.517193"
         height="184.90331"
         width="187.96562"
         id="rect12250"
         style="fill:url(#linearGradient5453);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1.00000036;marker:none;visibility:visible;display:inline;overflow:visible" />
      <rect
         ry="0.39200974"
         rx="0.40360424"
         y="19.5"
         x="12.5"
         height="10"
         width="6"
         id="rect4406"
         style="fill:none;stroke:url(#linearGradient4414);stroke-width:0.19416213;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter9038)"
         transform="matrix(5.0801515,0,0,5.2214902,119.33969,64.6792)" />
      <rect
         transform="translate(0.5,0)"
         clip-path="url(#clipPath7186)"
         style="fill:none;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7258)"
         id="rect7182"
         width="187.96562"
         height="184.90331"
         x="35.517193"
         y="48.671291"
         rx="2.8749998"
         ry="2.875" />
      <path
         sodipodi:nodetypes="ccccccccc"
         id="path12253"
         d="m 35.517194,94.1081 c 0,0 0.732807,-2.5 8.982807,-2.5 l 169.500009,0 c 6.875,0.125 9.4828,2.5 9.4828,2.5 l 0,-64.027565 C 223.48281,22.002919 216.96878,15.5 208.87737,15.5 l -158.754739,0 c -8.091412,0 -14.605437,6.50292 -14.605437,14.580535 l 0,64.027565 z"
         style="fill:url(#linearGradient5449);fill-opacity:1;fill-rule:nonzero;stroke:#2e3436;stroke-width:1.00000036;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
         inkscape:connector-curvature="0" />
      <rect
         ry="1.1762378"
         rx="1.1762378"
         y="43.393196"
         x="48.217571"
         height="45.64341"
         width="162.56485"
         id="rect12255"
         style="fill:url(#linearGradient7533);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;marker:none;visibility:visible;display:inline;overflow:visible" />
      <rect
         y="53.536179"
         x="73.618324"
         height="25.35745"
         width="111.76333"
         id="rect12257"
         style="opacity:0.6;fill:url(#linearGradient7773);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible" />
      <g
         id="g7559"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,7.9927912)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient7627);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.20008577"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect7561"
           style="fill:none;stroke:url(#linearGradient7629);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient7649);fill-opacity:1;stroke:none;filter:url(#filter4471)"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,7.892765)"
         id="g12263">
        <rect
           style="fill:url(#radialGradient7705);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.19701266;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect12265"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.20008577"
           ry="0.20042747" />
      </g>
      <rect
         y="28.178726"
         x="165.06105"
         height="10.142981"
         width="40.641212"
         id="rect12267"
         style="opacity:0.3;fill:url(#radialGradient9225);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible" />
      <rect
         style="fill:url(#radialGradient8961);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.19416213;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter4447)"
         id="rect7102"
         width="6"
         height="10"
         x="12.5"
         y="19.5"
         rx="0.40360424"
         ry="0.39200974"
         transform="matrix(5.0801515,0,0,5.2214902,119.33969,64.6792)" />
      <path
         sodipodi:nodetypes="ccccccccc"
         id="path7170"
         d="m 184.09273,213.78439 0.0848,-45.65698 c 0.13118,-0.7043 0.44086,-0.74703 0.77159,-0.7267 l 26.19621,0.14048 c 0.66471,0.0486 1.12775,0.31561 1.11678,1.09619 l -0.35972,45.8253 -1.52615,-44.76673 -24.24865,0 -2.03484,44.08844 z"
         style="opacity:0.15060239;fill:url(#radialGradient7178);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <path
         style="opacity:0.71839085;fill:url(#linearGradient7547);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1.00000036;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7555)"
         d="m 35.517194,94.1081 c 0,0 1.107807,-2.375 8.982807,-2 l 171.000009,0 c 6.25,-0.25 7.9828,2 7.9828,2 l 0,-64.027565 C 223.48281,22.002919 216.96878,15.5 208.87737,15.5 l -158.754739,0 c -8.091412,0 -14.605437,6.50292 -14.605437,14.580535 l 0,64.027565 z"
         id="path7539"
         sodipodi:nodetypes="ccccccccc"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.0110803,0,0,1.0110803,-1.4432133,-2.6673084)"
         ry="2.8434932"
         rx="2.843493"
         y="60"
         x="40.5"
         height="170"
         width="179.5"
         id="rect7292"
         style="opacity:0.515625;fill:none;stroke:url(#linearGradient7348);stroke-width:0.98904109;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7350);enable-background:accumulate" />
      <rect
         ry="2.875"
         rx="2.8749998"
         y="47"
         x="37.5"
         height="95.5"
         width="3"
         id="rect7354"
         style="opacity:0.515625;fill:url(#radialGradient7362);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />
      <path
         style="opacity:0.85632181;fill:url(#radialGradient7368);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;marker:none;visibility:visible;display:inline;overflow:visible"
         d="m 55.448919,15.670999 c -8.47388,0.745726 -10.44803,3.851462 -13.89861,6.421116 0,0 175.399371,0 175.399371,0 -2.8923,-2.870685 -11.66339,-6.198405 -15.39861,-6.421116 l -146.102151,0 z"
         id="path7364"
         sodipodi:nodetypes="ccccc"
         inkscape:connector-curvature="0" />
      <g
         transform="scale(0.98599796,1.0142009)"
         style="font-size:29.95739174px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;opacity:0.515625;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text7535">
        <path
           d="m 193.91693,187.32085 0,-3.17419 13.92551,0 0,3.17419 -13.92551,0 m 0,5.69015 0,-3.20345 13.92551,0 0,3.20345 -13.92551,0"
           style="marker:none"
           id="path3633"
           inkscape:connector-curvature="0" />
      </g>
      <path
         id="path7707"
         d="m 46.625,124.9 0,-16.25 0.75,-1.125 17.25,0 0.5,0.75 0,16.875 -0.875,-16.5 -16.625,0 -1,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient7715);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.8125"
         y="124"
         x="47.5"
         height="1.625"
         width="17"
         id="rect7717"
         style="opacity:0.25862068;fill:url(#radialGradient7725);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate" />
      <path
         sodipodi:nodetypes="cccsscccc"
         id="path12279"
         d="m 43.448919,15.670999 c -3.785585,0 -6.89861,3.29322 -6.89861,7.297933 l 0,40.64757 c 0,0 0.30742,-4.560029 4.455339,-5.102206 64.174232,-8.388257 129.609792,-13.964852 177.840902,-6.746677 4.31904,0.64638 3.60313,6.915019 3.60313,6.915019 l 0,-35.713706 c 0,-4.004712 -3.11302,-7.297933 -6.89861,-7.297933 l -172.102151,0 z"
         style="opacity:0.072;fill:url(#linearGradient6946);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.99999994;marker:none;visibility:visible;display:inline;overflow:visible"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.0111111,0,0,1,-1.4388889,-1)"
         ry="12.999999"
         rx="12.857141"
         y="18"
         x="39.5"
         height="90"
         width="180"
         id="rect7859"
         style="opacity:0.37356322;fill:none;stroke:url(#radialGradient7867);stroke-width:1.98898065;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7897);enable-background:accumulate" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text7905">
        <path
           d="m 54.70024,117.85181 -2.787396,0 0,-1.66333 2.787396,0 0,-2.80258 1.663324,0 0,2.80258 2.779801,0 0,1.66333 -2.779801,0 0,2.76461 -1.663324,0 0,-2.76461"
           style="marker:none"
           id="path3644"
           inkscape:connector-curvature="0" />
      </g>
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient7931);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,37.992791)"
         id="g7913">
        <rect
           style="fill:none;stroke:url(#linearGradient7929);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect7915"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.20008577"
           ry="0.20042747" />
      </g>
      <g
         id="g7917"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,37.892765)"
         style="fill:url(#radialGradient7935);fill-opacity:1;stroke:none;filter:url(#filter4459)">
        <rect
           ry="0.20042747"
           rx="0.20008577"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect7919"
           style="fill:url(#radialGradient7933);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.19701266;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient7937);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 46.625,155 0,-16.25 0.75,-1.125 17.25,0 0.5,0.75 0,16.875 -0.875,-16.5 -16.625,0 -1,16.25 z"
         id="path7921"
         inkscape:connector-curvature="0" />
      <rect
         style="opacity:0.25862068;fill:url(#radialGradient7939);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect7923"
         width="17"
         height="1.625"
         x="47.5"
         y="154"
         rx="0.8125"
         ry="0.8125" />
      <path
         sodipodi:nodetypes="ccccc"
         id="text7925"
         d="m 51.46743,146.31552 0,1.59228 8.880458,0 0,-1.59228 -8.880458,0"
         style="font-size:15.76510906px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Myriad"
         inkscape:connector-curvature="0" />
      <g
         id="g7941"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,67.992791)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient7959);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.20008577"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect7943"
           style="fill:none;stroke:url(#linearGradient7957);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient7963);fill-opacity:1;stroke:none;filter:url(#filter4463)"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,67.892765)"
         id="g7945">
        <rect
           style="fill:url(#radialGradient7961);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.19701266;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect7947"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.20008577"
           ry="0.20042747" />
      </g>
      <path
         id="path7949"
         d="m 46.625,185 0,-16.25 0.75,-1.125 17.25,0 0.5,0.75 0,16.875 -0.875,-16.5 -16.625,0 -1,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient7965);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.8125"
         y="184"
         x="47.5"
         height="1.625"
         width="17"
         id="rect7951"
         style="opacity:0.25862068;fill:url(#radialGradient7967);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate" />
      <path
         id="text7953"
         d="m 58.111512,173.79498 -2.430185,2.43018 -2.329851,-2.32985 -1.036724,1.03673 2.329851,2.32985 -2.463624,2.46362 1.092466,1.09247 2.463624,-2.46362 2.329852,2.32985 1.036725,-1.03673 -2.329852,-2.32985 2.430184,-2.43018 -1.092466,-1.09247"
         style="font-size:15.76510906px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Myriad"
         inkscape:connector-curvature="0" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient7987);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,99.992791)"
         id="g7969">
        <rect
           style="fill:none;stroke:url(#linearGradient7985);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect7971"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.20008577"
           ry="0.20042747" />
      </g>
      <g
         id="g7973"
         transform="matrix(5.0801515,0,0,5.0714902,7.5763597,99.89276)"
         style="fill:url(#radialGradient7991);fill-opacity:1;stroke:none;filter:url(#filter4467)">
        <rect
           ry="0.20042747"
           rx="0.20008577"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect7975"
           style="fill:url(#radialGradient7989);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.19701266;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient7993);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 46.625,217 0,-16.25 0.75,-1.125 17.25,0 0.5,0.75 0,16.875 -0.875,-16.5 -16.625,0 -1,16.25 z"
         id="path7977"
         inkscape:connector-curvature="0" />
      <rect
         style="opacity:0.25862068;fill:url(#radialGradient7995);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect7979"
         width="17"
         height="1.625"
         x="47.5"
         y="216"
         rx="0.8125"
         ry="0.8125" />
      <g
         id="g8005"
         transform="translate(-0.25,0.75)">
        <path
           sodipodi:nodetypes="ccccc"
           id="path7999"
           d="m 51.71743,207.56552 0,1.59228 8.880458,0 0,-1.59228 -8.880458,0"
           style="font-size:15.76510906px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Myriad"
           inkscape:connector-curvature="0" />
        <rect
           style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
           id="rect8001"
           width="1.875"
           height="1.875"
           x="55.25"
           y="203.75" />
        <rect
           y="211.375"
           x="55.25"
           height="1.875"
           width="1.875"
           id="rect8003"
           style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />
      </g>
      <path
         transform="matrix(1.2162162,0,0,1.2162162,-12.689189,-26.912162)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8010"
         style="opacity:0.3103448;fill:url(#radialGradient8018);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient8154);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path8152"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.2162162,0,0,1.2162162,-12.689189,3.087838)" />
      <path
         transform="matrix(1.2162162,0,0,1.2162162,-12.689189,33.087838)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8156"
         style="opacity:0.3103448;fill:url(#radialGradient8158);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient8162);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path8160"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.2162162,0,0,1.2162162,-12.689189,65.087838)" />
      <rect
         transform="matrix(1.5882353,0,0,1,-116.61765,-0.75)"
         ry="0.8125"
         rx="0.51157409"
         y="216"
         x="189.75"
         height="1.625"
         width="17"
         id="rect8164"
         style="opacity:0.25862068;fill:url(#radialGradient8168);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate" />
      <path
         transform="matrix(2.3100159,0,0,4.8412162,68.574323,-379.78716)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8166"
         style="opacity:0.17241378;fill:url(#radialGradient8170);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <path
         sodipodi:nodetypes="ccccccc"
         id="path8172"
         d="m 36.681164,215.51814 0,14.58407 c 0.118287,1.02367 0.504157,1.947 1.944544,2.47488 l 17.269291,0 -16.915738,-0.97227 c -1.000631,-0.34011 -1.67592,-1.05979 -1.679379,-2.56327 l -0.618718,-13.52341 z"
         style="opacity:0.48850576;fill:url(#radialGradient8180);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8266);enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <path
         transform="matrix(1.2352941,0,0,1.2352941,-52.471486,-55.35834)"
         d="m 222.91542,231.51643 c 0,0.82987 -0.63317,1.50261 -1.41421,1.50261 -0.78105,0 -1.41422,-0.67274 -1.41422,-1.50261 0,-0.82986 0.63317,-1.5026 1.41422,-1.5026 0.78104,0 1.41421,0.67274 1.41421,1.5026 z"
         sodipodi:ry="1.5026019"
         sodipodi:rx="1.4142135"
         sodipodi:cy="231.51643"
         sodipodi:cx="221.50121"
         id="path8270"
         style="opacity:0.66666667;fill:url(#radialGradient8278);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8372);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8458);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(6.4551507,0,0,5.0714902,27.263865,8.7927912)"
         id="g8438">
        <rect
           style="fill:none;stroke:url(#linearGradient8456);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8440"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <g
         id="g8442"
         transform="matrix(6.4551507,0,0,-5.0714902,27.263865,225.96696)"
         style="fill:url(#radialGradient8478);fill-opacity:1;stroke:url(#linearGradient8538);stroke-opacity:1;filter:url(#filter8528)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8444"
           style="fill:url(#radialGradient12456);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient12458);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient8464);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 76.881451,125 0,-16.25 0.952996,-1.125 21.918903,0 0.63533,0.75 0,16.875 -1.111828,-16.5 -21.12474,0 -1.270661,16.25 z"
         id="path8446"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.2706611,0,0,1,-20.482953,0)"
         style="opacity:0.25862068;fill:url(#radialGradient8466);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect8448"
         width="17"
         height="1.625"
         x="77.5"
         y="124"
         rx="0.63943094"
         ry="0.8125" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient12460);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path8454"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.5453986,0,0,1.2162162,1.5132209,-26.912162)" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8550);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8540">
        <path
           d="m 85.816659,123 3.949445,-9.1141 -5.103898,0 0,-1.97472 7.655846,0 0,1.47344 -4.04818,9.61538 -2.453213,0"
           style="line-height:125%;fill:url(#linearGradient65166);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3602"
           inkscape:connector-curvature="0" />
      </g>
      <path
         id="path8552"
         d="m 76.625,117 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         style="opacity:0.66666667;fill:url(#radialGradient8560);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <g
         id="g8562"
         transform="matrix(6.4551507,0,0,5.0714902,63.263865,8.7927912)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8584);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8564"
           style="fill:none;stroke:url(#linearGradient8582);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient8590);fill-opacity:1;stroke:url(#linearGradient8592);stroke-opacity:1;filter:url(#filter8528)"
         transform="matrix(6.4551507,0,0,5.0714902,63.263865,7.892765)"
         id="g8566">
        <rect
           style="fill:url(#radialGradient8586);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8588);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8568"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="-23.50001"
           rx="0.15746589"
           ry="0.20042747"
           transform="scale(1,-1)" />
      </g>
      <path
         id="path8570"
         d="m 112.88145,125 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient8594);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.63943094"
         y="124"
         x="77.5"
         height="1.625"
         width="17"
         id="rect8572"
         style="opacity:0.25862068;fill:url(#radialGradient8596);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         transform="matrix(1.2706611,0,0,1,15.517047,0)" />
      <path
         transform="matrix(1.5453986,0,0,1.2162162,37.513221,-26.912162)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8574"
         style="opacity:0.3103448;fill:url(#radialGradient8598);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8600);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8576">
        <path
           d="m 124.5357,111.75168 c 0.46076,1e-5 0.89621,0.0557 1.30635,0.16709 0.41013,0.11141 0.76963,0.2785 1.07851,0.50128 0.30886,0.2228 0.55443,0.50128 0.73672,0.83546 0.18227,0.33419 0.27342,0.7266 0.27342,1.17723 0,0.3342 -0.0506,0.638 -0.1519,0.91141 -0.10127,0.26837 -0.24052,0.51395 -0.41773,0.73673 -0.17722,0.21773 -0.38735,0.41267 -0.63039,0.58482 -0.24305,0.17216 -0.50635,0.32913 -0.78989,0.47089 0.29367,0.15697 0.57975,0.33166 0.85825,0.52406 0.28354,0.19242 0.53418,0.41014 0.75191,0.65318 0.21772,0.23799 0.3924,0.50635 0.52406,0.80508 0.13164,0.29874 0.19746,0.63293 0.19747,1.00255 -1e-5,0.46077 -0.0911,0.8785 -0.27342,1.25319 -0.18229,0.37469 -0.43799,0.69369 -0.7671,0.95698 -0.32913,0.2633 -0.72408,0.46583 -1.18484,0.60761 -0.45571,0.14177 -0.95952,0.21266 -1.51142,0.21266 -0.59748,0 -1.12914,-0.0683 -1.59497,-0.20507 -0.46583,-0.13671 -0.85824,-0.33165 -1.17724,-0.58482 -0.31899,-0.25317 -0.56203,-0.56456 -0.72912,-0.93419 -0.16203,-0.36963 -0.24305,-0.78483 -0.24305,-1.2456 0,-0.37975 0.0557,-0.72153 0.16709,-1.02533 0.1114,-0.3038 0.2633,-0.57723 0.45571,-0.82027 0.19241,-0.24304 0.41773,-0.45823 0.67596,-0.64558 0.25823,-0.18734 0.53419,-0.3519 0.82787,-0.49369 -0.24811,-0.15695 -0.48103,-0.32658 -0.69875,-0.50887 -0.21773,-0.18734 -0.40761,-0.3924 -0.56963,-0.6152 -0.15697,-0.22784 -0.28355,-0.47848 -0.37976,-0.75191 -0.0911,-0.27342 -0.13671,-0.57469 -0.13671,-0.90382 0,-0.4405 0.0911,-0.82532 0.27342,-1.15445 0.18735,-0.33417 0.43799,-0.61266 0.75192,-0.83546 0.31393,-0.22784 0.67596,-0.39746 1.0861,-0.50887 0.41013,-0.11138 0.84051,-0.16708 1.29116,-0.16709 m -1.57218,8.29383 c -1e-5,0.20254 0.0329,0.38989 0.0987,0.56204 0.0658,0.16709 0.16203,0.3114 0.28862,0.43292 0.13164,0.12152 0.29367,0.21773 0.48608,0.28861 0.19241,0.0658 0.4152,0.0987 0.66837,0.0987 0.53165,0 0.92913,-0.12405 1.19243,-0.37216 0.26329,-0.25317 0.39494,-0.58482 0.39494,-0.99496 0,-0.21266 -0.0456,-0.40253 -0.13671,-0.56963 -0.0861,-0.17215 -0.20001,-0.32912 -0.34178,-0.47089 -0.13671,-0.14684 -0.29368,-0.28102 -0.47089,-0.40254 -0.17723,-0.12152 -0.35445,-0.23798 -0.53166,-0.34938 l -0.16709,-0.10633 c -0.22279,0.1114 -0.42533,0.23292 -0.60761,0.36456 -0.18228,0.12659 -0.33925,0.26837 -0.47089,0.42533 -0.12659,0.15191 -0.22533,0.319 -0.29621,0.50128 -0.0709,0.18228 -0.10634,0.37975 -0.10633,0.59241 m 1.55699,-6.57734 c -0.1671,1e-5 -0.32406,0.0253 -0.4709,0.076 -0.14177,0.0506 -0.26583,0.12406 -0.37216,0.22026 -0.10127,0.0962 -0.18228,0.2152 -0.24304,0.35697 -0.0608,0.14178 -0.0911,0.30128 -0.0911,0.47849 0,0.21267 0.0304,0.39748 0.0911,0.55444 0.0658,0.15191 0.1519,0.28862 0.25824,0.41013 0.11139,0.11647 0.23797,0.2228 0.37975,0.31899 0.14683,0.0911 0.30127,0.18229 0.4633,0.27343 0.15696,-0.081 0.30633,-0.16962 0.44811,-0.26583 0.14177,-0.0962 0.26582,-0.20506 0.37216,-0.32659 0.11139,-0.12658 0.2,-0.26835 0.26583,-0.42532 0.0658,-0.15696 0.0987,-0.33671 0.0987,-0.53925 0,-0.17721 -0.0304,-0.33671 -0.0911,-0.47849 -0.0608,-0.14177 -0.14431,-0.26076 -0.25064,-0.35697 -0.10633,-0.0962 -0.23292,-0.16962 -0.37975,-0.22026 -0.14684,-0.0506 -0.30634,-0.0759 -0.47849,-0.076"
           style="line-height:125%;fill:url(#linearGradient65168);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3605"
           inkscape:connector-curvature="0" />
      </g>
      <path
         style="opacity:0.66666667;fill:url(#radialGradient8602);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 112.625,117 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         id="path8580"
         inkscape:connector-curvature="0" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8626);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(6.4551507,0,0,5.0714902,99.26386,8.7927912)"
         id="g8604">
        <rect
           style="fill:none;stroke:url(#linearGradient8624);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8606"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <g
         id="g8608"
         transform="matrix(6.4551507,0,0,-5.0714902,99.26386,225.96696)"
         style="fill:url(#radialGradient8632);fill-opacity:1;stroke:url(#linearGradient8634);stroke-opacity:1;filter:url(#filter8528)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8610"
           style="fill:url(#radialGradient8628);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8630);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient8636);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 148.88145,125 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         id="path8612"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.2706611,0,0,1,51.517047,0)"
         style="opacity:0.25862068;fill:url(#radialGradient8638);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect8614"
         width="17"
         height="1.625"
         x="77.5"
         y="124"
         rx="0.63943094"
         ry="0.8125" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient8640);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path8616"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.5453986,0,0,1.2162162,73.513221,-26.912162)" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8642);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8618">
        <path
           d="m 164.25729,116.63532 c -1e-5,0.53166 -0.0304,1.06332 -0.0911,1.59497 -0.0557,0.52659 -0.1595,1.0304 -0.3114,1.51142 -0.14684,0.48102 -0.34938,0.93166 -0.6076,1.35192 -0.25318,0.4152 -0.57724,0.7747 -0.97218,1.07851 -0.38988,0.3038 -0.86078,0.54431 -1.41268,0.72153 -0.54685,0.17215 -1.1899,0.25823 -1.92915,0.25823 -0.10634,0 -0.2228,-0.003 -0.34938,-0.008 -0.12658,-0.005 -0.2557,-0.0127 -0.38735,-0.0228 -0.12658,-0.005 -0.25064,-0.0152 -0.37216,-0.0304 -0.12152,-0.0101 -0.22785,-0.0253 -0.31899,-0.0456 l 0,-1.88358 c 0.18734,0.0506 0.38735,0.0911 0.60001,0.12152 0.21773,0.0253 0.43798,0.038 0.66077,0.038 0.68356,0 1.24559,-0.0836 1.68611,-0.25064 0.44051,-0.17215 0.78989,-0.41013 1.04813,-0.71394 0.25822,-0.30886 0.4405,-0.67596 0.54684,-1.10129 0.11139,-0.42532 0.17975,-0.89368 0.20507,-1.40509 l -0.0987,0 c -0.10127,0.18229 -0.22279,0.35191 -0.36456,0.50887 -0.14178,0.15697 -0.30887,0.29368 -0.50128,0.41014 -0.19241,0.11646 -0.41014,0.2076 -0.65317,0.27342 -0.24305,0.0658 -0.51394,0.0987 -0.81268,0.0987 -0.48102,0 -0.91394,-0.0785 -1.29876,-0.23545 -0.38482,-0.15696 -0.71141,-0.38481 -0.97976,-0.68356 -0.2633,-0.29873 -0.46584,-0.66583 -0.60761,-1.10129 -0.14178,-0.43544 -0.21266,-0.93418 -0.21266,-1.49623 0,-0.60253 0.0835,-1.14178 0.25063,-1.61775 0.17216,-0.47595 0.4152,-0.87849 0.72913,-1.20762 0.31393,-0.33417 0.69369,-0.58987 1.13927,-0.7671 0.45063,-0.17721 0.95444,-0.26582 1.51142,-0.26583 0.54684,1e-5 1.05824,0.0988 1.5342,0.29621 0.47596,0.19242 0.88862,0.48862 1.238,0.88862 0.34937,0.40002 0.62533,0.90636 0.82787,1.51902 0.20253,0.61268 0.30379,1.33421 0.3038,2.1646 m -3.8583,-2.98487 c -0.2076,1e-5 -0.39748,0.038 -0.56963,0.11393 -0.17216,0.076 -0.32153,0.19495 -0.44811,0.35697 -0.12153,0.15697 -0.21773,0.3595 -0.28862,0.6076 -0.0658,0.24305 -0.0987,0.53167 -0.0987,0.86584 -1e-5,0.53673 0.11392,0.96205 0.34178,1.27598 0.22785,0.31393 0.57216,0.4709 1.03293,0.47089 0.23291,10e-6 0.44557,-0.0456 0.63798,-0.13671 0.19241,-0.0911 0.35697,-0.21012 0.49369,-0.35697 0.1367,-0.14683 0.2405,-0.31139 0.31139,-0.49368 0.076,-0.18228 0.11392,-0.36709 0.11393,-0.55444 -1e-5,-0.25823 -0.0329,-0.51393 -0.0987,-0.7671 -0.0608,-0.25823 -0.15697,-0.48861 -0.28861,-0.69116 -0.12659,-0.20759 -0.28609,-0.37468 -0.47849,-0.50127 -0.18735,-0.12658 -0.40761,-0.18987 -0.66077,-0.18988"
           style="line-height:125%;fill:url(#linearGradient65170);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3620"
           inkscape:connector-curvature="0" />
      </g>
      <path
         id="path8622"
         d="m 148.625,117 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         style="opacity:0.66666667;fill:url(#radialGradient8644);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <g
         id="g8646"
         transform="matrix(6.4551507,0,0,5.0714902,27.263865,38.792791)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8708);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8648"
           style="fill:none;stroke:url(#linearGradient8706);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient8714);fill-opacity:1;stroke:url(#linearGradient8716);stroke-opacity:1;filter:url(#filter8528)"
         transform="matrix(6.4551507,0,0,-5.0714902,27.263865,255.96696)"
         id="g8650">
        <rect
           style="fill:url(#radialGradient8710);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8712);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8652"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <path
         id="path8654"
         d="m 76.881451,155 0,-16.25 0.952996,-1.125 21.918903,0 0.63533,0.75 0,16.875 -1.111828,-16.5 -21.12474,0 -1.270661,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient8718);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.63943094"
         y="124"
         x="77.5"
         height="1.625"
         width="17"
         id="rect8656"
         style="opacity:0.25862068;fill:url(#radialGradient8720);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         transform="matrix(1.2706611,0,0,1,-20.482953,30)" />
      <path
         transform="matrix(1.5453986,0,0,1.2162162,1.5132209,3.087838)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8658"
         style="opacity:0.3103448;fill:url(#radialGradient8722);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8724);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8660">
        <path
           d="m 92.485144,150.69869 -1.336735,0 0,2.30131 -2.286121,0 0,-2.30131 -4.587431,0 0,-1.63294 4.716548,-7.16977 2.157004,0 0,6.97989 1.336735,0 0,1.82282 m -3.622856,-1.82282 0,-1.88358 c -4e-6,-0.0658 -4e-6,-0.15949 0,-0.28102 0.0051,-0.12658 0.01012,-0.26835 0.01519,-0.42533 0.0051,-0.15695 0.01012,-0.31898 0.01519,-0.48608 0.01012,-0.16709 0.01772,-0.32658 0.02278,-0.47849 0.01012,-0.1519 0.01772,-0.28354 0.02278,-0.39495 0.01012,-0.11645 0.01772,-0.19999 0.02278,-0.25063 l -0.06835,0 c -0.09115,0.21267 -0.194945,0.43799 -0.311399,0.67596 -0.111399,0.23799 -0.240515,0.47596 -0.387349,0.71394 l -1.853201,2.81018 2.521568,0"
           style="line-height:125%;fill:url(#linearGradient65172);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3599"
           inkscape:connector-curvature="0" />
      </g>
      <path
         style="opacity:0.66666667;fill:url(#radialGradient8726);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 76.625,147 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         id="path8664"
         inkscape:connector-curvature="0" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8730);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(6.4551507,0,0,5.0714902,63.263865,38.792791)"
         id="g8666">
        <rect
           style="fill:none;stroke:url(#linearGradient8728);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8668"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <g
         id="g8670"
         transform="matrix(6.4551507,0,0,-5.0714902,63.263865,255.96696)"
         style="fill:url(#radialGradient8736);fill-opacity:1;stroke:url(#linearGradient8738);stroke-opacity:1;filter:url(#filter8528)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8672"
           style="fill:url(#radialGradient8732);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8734);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient8740);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 112.88145,155 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         id="path8674"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.2706611,0,0,1,15.517047,30)"
         style="opacity:0.25862068;fill:url(#radialGradient8742);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect8676"
         width="17"
         height="1.625"
         x="77.5"
         y="124"
         rx="0.63943094"
         ry="0.8125" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient8744);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path8678"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.5453986,0,0,1.2162162,37.513221,3.087838)" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8746);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8680">
        <path
           d="m 124.78634,145.90619 c 0.47595,1e-5 0.919,0.0734 1.32914,0.22026 0.41013,0.14684 0.76709,0.36204 1.0709,0.64558 0.3038,0.28356 0.54178,0.63799 0.71394,1.06331 0.17215,0.42027 0.25823,0.90382 0.25824,1.45066 -1e-5,0.60255 -0.0937,1.14433 -0.28102,1.62535 -0.18736,0.47596 -0.46331,0.88103 -0.82787,1.21522 -0.36457,0.32912 -0.81774,0.58229 -1.35952,0.7595 -0.53672,0.17722 -1.15445,0.26583 -1.8532,0.26583 -0.27849,0 -0.55444,-0.0127 -0.82786,-0.038 -0.27343,-0.0253 -0.53672,-0.0633 -0.78989,-0.11393 -0.24811,-0.0456 -0.48609,-0.10633 -0.71394,-0.18228 -0.22279,-0.076 -0.42533,-0.16456 -0.60761,-0.26583 l 0,-2.02789 c 0.17722,0.10127 0.38229,0.19748 0.61521,0.28862 0.23291,0.0861 0.47342,0.16203 0.72153,0.22785 0.25317,0.0608 0.50634,0.11139 0.75951,0.1519 0.25316,0.0354 0.49367,0.0532 0.72153,0.0532 0.67849,0 1.19496,-0.13925 1.5494,-0.41773 0.35443,-0.28355 0.53165,-0.73166 0.53165,-1.34433 0,-0.54685 -0.17469,-0.96204 -0.52406,-1.2456 -0.34431,-0.28861 -0.8785,-0.43291 -1.60256,-0.43292 -0.13165,1e-5 -0.27343,0.008 -0.42532,0.0228 -0.14685,0.0152 -0.29368,0.0354 -0.44052,0.0608 -0.14178,0.0253 -0.27849,0.0532 -0.41013,0.0835 -0.13165,0.0253 -0.24558,0.0532 -0.34178,0.0836 l -0.9342,-0.50128 0.41773,-5.65834 5.86341,0 0,1.98992 -3.82793,0 -0.18228,2.17979 c 0.16203,-0.0354 0.34937,-0.0709 0.56204,-0.10633 0.21772,-0.0354 0.49621,-0.0532 0.83546,-0.0532"
           style="line-height:125%;fill:url(#linearGradient65174);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3608"
           inkscape:connector-curvature="0" />
      </g>
      <path
         id="path8684"
         d="m 112.625,147 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         style="opacity:0.66666667;fill:url(#radialGradient8748);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <g
         id="g8686"
         transform="matrix(6.4551507,0,0,5.0714902,99.26386,38.792791)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8752);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8688"
           style="fill:none;stroke:url(#linearGradient8750);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient8758);fill-opacity:1;stroke:url(#linearGradient8760);stroke-opacity:1;filter:url(#filter8528)"
         transform="matrix(6.4551507,0,0,-5.0714902,99.26386,255.96696)"
         id="g8690">
        <rect
           style="fill:url(#radialGradient8754);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8756);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8692"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <path
         id="path8694"
         d="m 148.88145,155 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient8762);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.63943094"
         y="124"
         x="77.5"
         height="1.625"
         width="17"
         id="rect8696"
         style="opacity:0.25862068;fill:url(#radialGradient8764);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         transform="matrix(1.2706611,0,0,1,51.517047,30)" />
      <path
         transform="matrix(1.5453986,0,0,1.2162162,73.513221,3.087838)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8698"
         style="opacity:0.3103448;fill:url(#radialGradient8766);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8768);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8700">
        <path
           d="m 156.8217,148.28345 c 0,-0.53165 0.0279,-1.06077 0.0836,-1.58737 0.0608,-0.52659 0.16456,-1.03039 0.3114,-1.51142 0.1519,-0.48608 0.35443,-0.93672 0.6076,-1.35193 0.25824,-0.41519 0.58229,-0.77469 0.97218,-1.0785 0.39494,-0.30886 0.86583,-0.54937 1.41268,-0.72153 0.55191,-0.17721 1.19496,-0.26582 1.92915,-0.26583 0.10633,10e-6 0.22279,0.003 0.34938,0.008 0.12658,0.005 0.25316,0.0127 0.37975,0.0228 0.13164,0.005 0.25823,0.0152 0.37976,0.0304 0.12151,0.0152 0.23037,0.0329 0.32658,0.0532 l 0,1.87599 c -0.19241,-0.0456 -0.39748,-0.081 -0.6152,-0.10633 -0.21267,-0.0304 -0.42786,-0.0456 -0.64558,-0.0456 -0.68356,1e-5 -1.2456,0.0861 -1.68611,0.25823 -0.44052,0.1671 -0.78989,0.40255 -1.04812,0.70635 -0.25824,0.30381 -0.44305,0.66837 -0.55444,1.09369 -0.10634,0.42533 -0.17216,0.89622 -0.19747,1.41268 l 0.0911,0 c 0.10126,-0.18227 0.22278,-0.3519 0.36456,-0.50887 0.14684,-0.16202 0.31646,-0.29873 0.50887,-0.41013 0.19241,-0.11645 0.4076,-0.20759 0.64558,-0.27343 0.24304,-0.0658 0.51393,-0.0987 0.81268,-0.0987 0.48101,1e-5 0.91393,0.0785 1.29876,0.23545 0.38481,0.15697 0.70886,0.38482 0.97217,0.68355 0.26835,0.29875 0.47342,0.66585 0.6152,1.10129 0.14177,0.43546 0.21265,0.9342 0.21266,1.49623 -1e-5,0.60255 -0.0861,1.1418 -0.25823,1.61776 -0.1671,0.47596 -0.40761,0.88103 -0.72153,1.21521 -0.31394,0.32912 -0.69369,0.58229 -1.13927,0.75951 -0.44558,0.17215 -0.94686,0.25823 -1.50382,0.25823 -0.54685,0 -1.05826,-0.0962 -1.53421,-0.28861 -0.47596,-0.19747 -0.89116,-0.49621 -1.24559,-0.89622 -0.34938,-0.40001 -0.62533,-0.90381 -0.82787,-1.51142 -0.19747,-0.61267 -0.29621,-1.33673 -0.29621,-2.1722 m 3.85831,2.99247 c 0.20759,0 0.39494,-0.038 0.56203,-0.11393 0.17215,-0.081 0.31899,-0.2 0.44052,-0.35697 0.12658,-0.16203 0.22278,-0.36456 0.28861,-0.60761 0.0709,-0.24304 0.10633,-0.53165 0.10633,-0.86584 0,-0.54177 -0.11393,-0.9671 -0.34178,-1.27597 -0.22279,-0.31393 -0.56457,-0.47089 -1.02533,-0.4709 -0.23292,1e-5 -0.44559,0.0456 -0.63799,0.13672 -0.19241,0.0911 -0.35697,0.21013 -0.49368,0.35696 -0.13672,0.14685 -0.24305,0.31141 -0.31899,0.49369 -0.0709,0.18228 -0.10634,0.36709 -0.10634,0.55444 0,0.25823 0.0304,0.51647 0.0911,0.7747 0.0658,0.25317 0.16202,0.48355 0.28861,0.69115 0.13164,0.20254 0.29114,0.3671 0.47849,0.49368 0.1924,0.12658 0.41519,0.18988 0.66837,0.18988"
           style="line-height:125%;fill:url(#linearGradient65176);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3617"
           inkscape:connector-curvature="0" />
      </g>
      <path
         style="opacity:0.66666667;fill:url(#radialGradient8770);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 148.625,147 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         id="path8704"
         inkscape:connector-curvature="0" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8834);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(6.4551507,0,0,5.0714902,27.263865,68.792791)"
         id="g8772">
        <rect
           style="fill:none;stroke:url(#linearGradient8832);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8774"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <g
         id="g8776"
         transform="matrix(6.4551507,0,0,5.0714902,27.263865,67.892765)"
         style="fill:url(#radialGradient8840);fill-opacity:1;stroke:url(#linearGradient8842);stroke-opacity:1;filter:url(#filter8528)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="-23.50001"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8778"
           style="fill:url(#radialGradient8836);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8838);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           transform="scale(1,-1)" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient8844);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 76.881451,185 0,-16.25 0.952996,-1.125 21.918903,0 0.63533,0.75 0,16.875 -1.111828,-16.5 -21.12474,0 -1.270661,16.25 z"
         id="path8780"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.2706611,0,0,1,-20.482953,60)"
         style="opacity:0.25862068;fill:url(#radialGradient8846);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect8782"
         width="17"
         height="1.625"
         x="77.5"
         y="124"
         rx="0.63943094"
         ry="0.8125" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient8848);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path8784"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.5453986,0,0,1.2162162,1.5132209,33.087838)" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8850);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8786">
        <path
           d="m 90.449661,183 -2.346881,0 0,-6.42544 c -4e-6,-0.13164 -4e-6,-0.28861 0,-0.4709 0.0051,-0.18734 0.01012,-0.37974 0.01519,-0.57722 0.01012,-0.20253 0.01772,-0.40507 0.02278,-0.60761 0.01012,-0.20253 0.01772,-0.38734 0.02278,-0.55444 -0.02532,0.0304 -0.06836,0.076 -0.129116,0.13671 -0.06076,0.0608 -0.12912,0.12912 -0.205067,0.20507 -0.07596,0.0709 -0.154437,0.14431 -0.235448,0.22025 -0.08102,0.076 -0.1595,0.14432 -0.235448,0.20507 l -1.275974,1.02534 -1.139263,-1.41269 3.577285,-2.84816 1.929152,0 0,11.10402"
           style="line-height:125%;fill:url(#linearGradient65178);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3623"
           inkscape:connector-curvature="0" />
      </g>
      <path
         id="path8790"
         d="m 76.625,177 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         style="opacity:0.66666667;fill:url(#radialGradient8852);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <g
         id="g8792"
         transform="matrix(6.4551507,0,0,5.0714902,63.263865,68.792791)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8856);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8794"
           style="fill:none;stroke:url(#linearGradient8854);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient8862);fill-opacity:1;stroke:url(#linearGradient8864);stroke-opacity:1;filter:url(#filter8528)"
         transform="matrix(6.4551507,0,0,5.0714902,63.263865,67.892765)"
         id="g8796">
        <rect
           style="fill:url(#radialGradient8858);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8860);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8798"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="-23.50001"
           rx="0.15746589"
           ry="0.20042747"
           transform="scale(1,-1)" />
      </g>
      <path
         id="path8800"
         d="m 112.88145,185 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient8866);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.63943094"
         y="124"
         x="77.5"
         height="1.625"
         width="17"
         id="rect8802"
         style="opacity:0.25862068;fill:url(#radialGradient8868);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         transform="matrix(1.2706611,0,0,1,15.517047,60)" />
      <path
         transform="matrix(1.5453986,0,0,1.2162162,37.513221,33.087838)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8804"
         style="opacity:0.3103448;fill:url(#radialGradient8870);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8872);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8806">
        <path
           d="m 128.31805,183 -7.45078,0 0,-1.63294 2.61271,-2.81778 c 0.32912,-0.35443 0.62786,-0.68102 0.89622,-0.97977 0.26836,-0.29873 0.49874,-0.58988 0.69116,-0.87343 0.1924,-0.28354 0.34177,-0.57216 0.44811,-0.86584 0.10632,-0.29367 0.15949,-0.61013 0.15949,-0.94939 0,-0.37468 -0.11393,-0.66582 -0.34178,-0.87343 -0.22279,-0.20759 -0.52406,-0.31139 -0.90381,-0.3114 -0.40001,1e-5 -0.78483,0.0987 -1.15445,0.29621 -0.36963,0.19748 -0.75698,0.4785 -1.16205,0.84305 l -1.27598,-1.51142 c 0.22785,-0.20759 0.46583,-0.40506 0.71394,-0.59242 0.24811,-0.19239 0.52153,-0.36202 0.82027,-0.50887 0.29874,-0.14682 0.62786,-0.26328 0.98736,-0.34937 0.3595,-0.0911 0.76204,-0.1367 1.20762,-0.13671 0.53165,1e-5 1.00761,0.0734 1.42788,0.22026 0.42531,0.14684 0.78735,0.35698 1.08609,0.63039 0.29874,0.26837 0.52659,0.59496 0.68356,0.97976 0.16202,0.38483 0.24304,0.81775 0.24304,1.29876 0,0.43546 -0.076,0.85319 -0.22785,1.25319 -0.15191,0.39495 -0.35951,0.78483 -0.6228,1.16965 -0.2633,0.37976 -0.56963,0.75951 -0.919,1.13926 -0.34432,0.37469 -0.71394,0.75698 -1.10888,1.14686 l -1.33674,1.34433 0,0.10633 4.52667,0 0,1.97472"
           style="line-height:125%;fill:url(#linearGradient65180);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3611"
           inkscape:connector-curvature="0" />
      </g>
      <path
         style="opacity:0.66666667;fill:url(#radialGradient8874);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 112.625,177 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         id="path8810"
         inkscape:connector-curvature="0" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8878);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(6.4551507,0,0,5.0714902,99.26386,68.792791)"
         id="g8812">
        <rect
           style="fill:none;stroke:url(#linearGradient8876);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8814"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <g
         id="g8816"
         transform="matrix(6.4551507,0,0,-5.0714902,99.26386,285.96696)"
         style="fill:url(#radialGradient8884);fill-opacity:1;stroke:url(#linearGradient8886);stroke-opacity:1;filter:url(#filter8528)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8818"
           style="fill:url(#radialGradient8880);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8882);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient8888);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 148.88145,185 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         id="path8820"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.2706611,0,0,1,51.517047,60)"
         style="opacity:0.25862068;fill:url(#radialGradient8890);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect8822"
         width="17"
         height="1.625"
         x="77.5"
         y="124"
         rx="0.63943094"
         ry="0.8125" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient8892);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path8824"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.5453986,0,0,1.2162162,73.513221,33.087838)" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8894);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text8826">
        <path
           d="m 163.88513,174.37958 c -1e-5,0.38482 -0.0633,0.73167 -0.18987,1.04052 -0.12153,0.30382 -0.29116,0.57217 -0.50888,0.80508 -0.21266,0.22786 -0.46583,0.42027 -0.7595,0.57723 -0.28862,0.15191 -0.60255,0.26837 -0.94179,0.34937 l 0,0.0456 c 0.89621,0.1114 1.5747,0.38483 2.03548,0.82027 0.46076,0.4304 0.69114,1.01269 0.69115,1.74687 -1e-5,0.48609 -0.0886,0.93673 -0.26583,1.35193 -0.17216,0.41013 -0.44052,0.7671 -0.80508,1.07091 -0.3595,0.3038 -0.81521,0.54178 -1.36711,0.71393 -0.54685,0.1671 -1.19243,0.25064 -1.93675,0.25064 -0.59748,0 -1.15952,-0.0506 -1.68611,-0.1519 -0.52659,-0.0962 -1.01774,-0.24557 -1.47344,-0.44811 l 0,-1.99751 c 0.22785,0.12153 0.46836,0.22786 0.72153,0.319 0.25317,0.0911 0.50634,0.16962 0.75951,0.23544 0.25317,0.0608 0.50127,0.10634 0.74432,0.13672 0.2481,0.0304 0.48102,0.0456 0.69874,0.0456 0.43545,0 0.79748,-0.0405 1.0861,-0.12153 0.28861,-0.081 0.51899,-0.19493 0.69115,-0.34177 0.17215,-0.14684 0.29368,-0.32153 0.36457,-0.52407 0.0759,-0.20759 0.11392,-0.43291 0.11392,-0.67596 0,-0.22785 -0.0481,-0.43291 -0.1443,-0.6152 -0.0911,-0.18734 -0.24305,-0.34431 -0.45571,-0.4709 -0.2076,-0.13164 -0.48102,-0.23291 -0.82027,-0.3038 -0.33925,-0.0709 -0.75698,-0.10632 -1.25319,-0.10633 l -0.78988,0 0,-1.64813 0.77469,0 c 0.46583,0 0.85318,-0.0405 1.16205,-0.12152 0.30886,-0.0861 0.55444,-0.2 0.73673,-0.34178 0.18734,-0.14683 0.31898,-0.31646 0.39494,-0.50887 0.076,-0.19241 0.11392,-0.39747 0.11393,-0.61521 -1e-5,-0.39493 -0.12406,-0.7038 -0.37216,-0.9266 -0.24305,-0.22278 -0.6304,-0.33417 -1.16205,-0.33418 -0.24305,1e-5 -0.4709,0.0253 -0.68356,0.076 -0.2076,0.0456 -0.40254,0.10634 -0.58482,0.18228 -0.17722,0.0709 -0.34178,0.15191 -0.49368,0.24305 -0.14684,0.0861 -0.28102,0.17216 -0.40254,0.25823 l -1.18483,-1.56459 c 0.21266,-0.15695 0.44304,-0.30126 0.69115,-0.43292 0.25317,-0.13164 0.52659,-0.24556 0.82027,-0.34178 0.29367,-0.10126 0.61013,-0.17974 0.94938,-0.23545 0.33925,-0.0557 0.70128,-0.0835 1.0861,-0.0835 0.54684,1e-5 1.04305,0.0608 1.48864,0.18228 0.45063,0.11647 0.83545,0.28862 1.15445,0.51647 0.31899,0.2228 0.56456,0.49875 0.73672,0.82786 0.17722,0.32407 0.26582,0.69623 0.26583,1.11648"
           style="line-height:125%;fill:url(#linearGradient65182);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3614"
           inkscape:connector-curvature="0" />
      </g>
      <path
         id="path8830"
         d="m 148.625,177 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         style="opacity:0.66666667;fill:url(#radialGradient8896);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <g
         id="g8898"
         transform="matrix(6.4551507,0,0,5.0714902,27.263865,99.792791)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient8920);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect8900"
           style="fill:none;stroke:url(#linearGradient8918);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient8926);fill-opacity:1;stroke:url(#linearGradient8928);stroke-opacity:1;filter:url(#filter8528)"
         transform="matrix(6.4551507,0,0,-5.0714902,27.263865,316.96695)"
         id="g8902">
        <rect
           style="fill:url(#radialGradient8922);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient8924);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect8904"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <path
         id="path8906"
         d="m 76.881451,216 0,-16.25 0.952996,-1.125 21.918903,0 0.63533,0.75 0,16.875 -1.111828,-16.5 -21.12474,0 -1.270661,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient8930);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.63943094"
         y="124"
         x="77.5"
         height="1.625"
         width="17"
         id="rect8908"
         style="opacity:0.25862068;fill:url(#radialGradient8932);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         transform="matrix(1.2706611,0,0,1,-20.482953,91)" />
      <path
         transform="matrix(1.5453986,0,0,1.2162162,1.5132209,64.087838)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path8910"
         style="opacity:0.3103448;fill:url(#radialGradient8934);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="font-size:15.76510906px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient8936);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Myriad"
         id="text8912">
        <path
           d="m 88.611412,214.17342 c 2.585475,0 3.862451,-2.19136 3.862451,-5.34438 0,-2.80618 -1.087795,-5.24978 -3.815156,-5.24978 -2.648536,0 -3.893982,2.33324 -3.893982,5.31284 0.01577,2.90078 1.182386,5.28132 3.830921,5.28132 l 0.01577,0 m 0,-1.81299 c -0.914376,0 -1.481921,-1.13509 -1.466156,-3.49986 0,-2.31746 0.567545,-3.46832 1.466156,-3.46832 0.96167,0 1.45039,1.19815 1.45039,3.46832 0,2.33324 -0.504485,3.49986 -1.434625,3.49986 l -0.01577,0"
           style="fill:url(#linearGradient65184);marker:none"
           id="path3596"
           inkscape:connector-curvature="0" />
      </g>
      <path
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;opacity:0.66666667;fill:url(#radialGradient8938);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         d="m 76.625,208 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         id="path8916"
         inkscape:connector-curvature="0" />
      <path
         id="text8940"
         d="m 64.956671,33.150809 c -0.447555,0.194589 -0.992406,0.311343 -1.692927,0.311343 -1.43996,0 -2.607497,-0.934031 -2.607497,-2.685333 -0.01946,-1.556713 0.992407,-2.665874 2.54912,-2.665874 0.778357,0 1.303749,0.136213 1.65401,0.291884 l 0.467014,-2.19886 c -0.622685,-0.233507 -1.47888,-0.36972 -2.257236,-0.36972 -3.541523,0 -5.448502,2.276699 -5.448502,5.059324 0,2.996673 1.965355,4.884192 5.039864,4.884192 1.128617,0 2.121024,-0.194589 2.646415,-0.447555 l -0.350261,-2.179401 m 9.907943,-3.210724 c 0,-2.237776 -0.992409,-4.105836 -4.164212,-4.105836 -1.731844,0 -3.035595,0.486474 -3.697198,0.856194 l 0.544851,1.887516 c 0.622685,-0.369719 1.65401,-0.700521 2.626956,-0.700521 1.459418,0 1.731845,0.719981 1.731845,1.225913 l 0,0.116753 c -3.366392,0 -5.584714,1.167539 -5.584714,3.638821 0,1.517795 1.148079,2.91884 3.074511,2.91884 1.128617,0 2.101566,-0.408638 2.724251,-1.167536 l 0.05838,0 0.17513,0.953488 2.665874,0 c -0.116753,-0.525391 -0.155671,-1.401044 -0.155671,-2.296154 l 0,-3.327478 m -2.860463,2.159941 c 0,0.175131 -0.01946,0.350261 -0.05838,0.505933 -0.194589,0.603226 -0.817276,1.0897 -1.537256,1.0897 -0.661603,0 -1.167536,-0.36972 -1.167536,-1.128618 0,-1.128617 1.206455,-1.498338 2.763169,-1.498338 l 0,1.031323 m 11.993393,1.050783 c -0.447555,0.194589 -0.992407,0.311343 -1.692927,0.311343 -1.43996,0 -2.607498,-0.934031 -2.607498,-2.685333 -0.01946,-1.556713 0.992407,-2.665874 2.549121,-2.665874 0.778356,0 1.303749,0.136213 1.654009,0.291884 l 0.467015,-2.19886 c -0.622686,-0.233507 -1.47888,-0.36972 -2.257237,-0.36972 -3.541522,0 -5.448502,2.276699 -5.448502,5.059324 0,2.996673 1.965356,4.884192 5.039865,4.884192 1.128617,0 2.121024,-0.194589 2.646415,-0.447555 l -0.350261,-2.179401 m 9.907944,-3.210724 c 0,-2.237776 -0.992409,-4.105836 -4.164213,-4.105836 -1.731843,0 -3.035594,0.486474 -3.697197,0.856194 l 0.54485,1.887516 c 0.622685,-0.369719 1.65401,-0.700521 2.626956,-0.700521 1.459419,0 1.731845,0.719981 1.731845,1.225913 l 0,0.116753 c -3.366392,0 -5.584714,1.167539 -5.584714,3.638821 0,1.517795 1.148079,2.91884 3.074512,2.91884 1.128617,0 2.101565,-0.408638 2.724251,-1.167536 l 0.05838,0 0.17513,0.953488 2.665874,0 c -0.116753,-0.525391 -0.155671,-1.401044 -0.155671,-2.296154 l 0,-3.327478 m -2.860464,2.159941 c 0,0.175131 -0.01946,0.350261 -0.05838,0.505933 -0.194589,0.603226 -0.817276,1.0897 -1.537256,1.0897 -0.661603,0 -1.167536,-0.36972 -1.167536,-1.128618 0,-1.128617 1.206456,-1.498338 2.763169,-1.498338 l 0,1.031323 m 9.599946,3.677739 c 2.52966,0 5.00094,-1.595636 5.00094,-5.059323 0,-2.879919 -1.94589,-4.884193 -4.84527,-4.884193 -3.07451,0 -5.098242,1.965356 -5.098242,5.039865 0,3.074508 2.140486,4.903651 4.923112,4.903651 l 0.0195,0 m 0.0195,-2.121024 c -1.245374,0 -1.926438,-1.225914 -1.926438,-2.841004 0,-1.420501 0.544851,-2.860464 1.945898,-2.860464 1.34266,0 1.88751,1.439963 1.88751,2.841005 0,1.712384 -0.71998,2.860463 -1.88751,2.860463 l -0.0195,0"
         style="font-size:19.45893478px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;opacity:0.66666667;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Myriad"
         transform="scale(0.8893153,1.1244605)"
         inkscape:connector-curvature="0" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient9072);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(6.4551507,0,0,5.0714902,63.263865,99.792791)"
         id="g9050">
        <rect
           style="fill:none;stroke:url(#linearGradient9070);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect9052"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <g
         id="g9054"
         transform="matrix(6.4551507,0,0,-5.0714902,63.263865,316.96695)"
         style="fill:url(#radialGradient9078);fill-opacity:1;stroke:url(#linearGradient9080);stroke-opacity:1;filter:url(#filter8528)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect9056"
           style="fill:url(#radialGradient9074);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9076);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient9082);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 112.88145,216 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         id="path9058"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.2706611,0,0,1,15.517047,91)"
         style="opacity:0.25862068;fill:url(#radialGradient9084);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect9060"
         width="17"
         height="1.625"
         x="77.5"
         y="124"
         rx="0.63943094"
         ry="0.8125" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient9086);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path9062"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.5453986,0,0,1.2162162,37.513221,64.087838)" />
      <path
         id="text9064"
         d="m 124.93583,213.17342 c 0.85131,0 1.41886,-0.61484 1.41886,-1.45039 -0.0158,-0.88285 -0.58331,-1.46616 -1.4031,-1.46616 -0.83555,0 -1.41886,0.59908 -1.41886,1.46616 0,0.83555 0.58331,1.45039 1.38733,1.45039 l 0.0158,0"
         style="font-size:15.76510906px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient9135);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Myriad"
         inkscape:connector-curvature="0" />
      <path
         id="path9068"
         d="m 112.625,208 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         style="opacity:0.66666667;fill:url(#radialGradient9090);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <g
         id="g9092"
         transform="matrix(6.4551507,0,0,5.0714902,99.26386,99.792791)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient9114);stroke-width:0.17477489;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.15746589"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect9094"
           style="fill:none;stroke:url(#linearGradient9112);stroke-width:0.17477489;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient9120);fill-opacity:1;stroke:url(#linearGradient9122);stroke-opacity:1;filter:url(#filter8528)"
         transform="matrix(6.4551507,0,0,-5.0714902,99.26386,316.96695)"
         id="g9096">
        <rect
           style="fill:url(#radialGradient9116);fill-opacity:1;fill-rule:nonzero;stroke:url(#linearGradient9118);stroke-width:0.19701266;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect9098"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.15746589"
           ry="0.20042747" />
      </g>
      <path
         id="path9100"
         d="m 148.88145,216 0,-16.25 0.953,-1.125 21.9189,0 0.63533,0.75 0,16.875 -1.11183,-16.5 -21.12474,0 -1.27066,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient9124);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.63943094"
         y="124"
         x="77.5"
         height="1.625"
         width="17"
         id="rect9102"
         style="opacity:0.25862068;fill:url(#radialGradient9126);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         transform="matrix(1.2706611,0,0,1,51.517047,91)" />
      <path
         transform="matrix(1.5453986,0,0,1.2162162,73.513221,64.087838)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path9104"
         style="opacity:0.3103448;fill:url(#radialGradient9128);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="font-size:15.55473518px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;fill:url(#linearGradient3652);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text9106"
         transform="matrix(0.7905661,0,0,0.7905661,33.490674,43.799584)">
        <path
           d="m 152.74832,208.0003 c 0,-0.63292 0.0456,-1.25572 0.13671,-1.8684 0.0911,-0.61772 0.23038,-1.2152 0.41773,-1.79244 0.18734,-0.58228 0.42279,-1.13925 0.70634,-1.67091 0.28861,-0.53671 0.63039,-1.04052 1.02534,-1.51143 l 1.89877,0 c -0.71394,0.97725 -1.25319,2.05069 -1.61776,3.22032 -0.36456,1.16965 -0.54684,2.3722 -0.54684,3.60767 0,0.60254 0.0456,1.20255 0.13671,1.80003 0.0911,0.59748 0.22785,1.1823 0.41013,1.75447 0.18228,0.57216 0.4076,1.1266 0.67597,1.66332 0.26835,0.53672 0.57722,1.04306 0.9266,1.51902 l -1.88358,0 c -0.39495,-0.45571 -0.73673,-0.94433 -1.02534,-1.46585 -0.28355,-0.52153 -0.519,-1.06585 -0.70634,-1.63295 -0.18735,-0.57216 -0.32659,-1.16204 -0.41773,-1.76965 -0.0911,-0.60761 -0.13671,-1.22534 -0.13671,-1.8532"
           style="line-height:125%;fill:url(#linearGradient3646);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3626"
           inkscape:connector-curvature="0" />
        <path
           d="m 157.875,209.04082 0,-1.89877 4.07856,0 0,1.89877 -4.07856,0"
           style="line-height:125%;fill:url(#linearGradient3648);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3628"
           inkscape:connector-curvature="0" />
        <path
           d="m 167.07265,208.0003 c -1e-5,0.62786 -0.0456,1.24559 -0.13671,1.8532 -0.0911,0.60761 -0.23039,1.19749 -0.41773,1.76965 -0.18735,0.5671 -0.42533,1.11142 -0.71394,1.63295 -0.28356,0.52152 -0.6228,1.01014 -1.01774,1.46585 l -1.88358,0 c 0.34937,-0.47596 0.65823,-0.9823 0.9266,-1.51902 0.26835,-0.53672 0.49367,-1.09116 0.67596,-1.66332 0.18228,-0.57217 0.31899,-1.15699 0.41013,-1.75447 0.0911,-0.59748 0.13671,-1.19749 0.13671,-1.80003 0,-1.23547 -0.18228,-2.43802 -0.54684,-3.60767 -0.36457,-1.16963 -0.90382,-2.24307 -1.61776,-3.22032 l 1.89878,0 c 0.39494,0.47091 0.73418,0.97472 1.01774,1.51143 0.28861,0.53166 0.52659,1.08863 0.71394,1.67091 0.18734,0.57724 0.32658,1.17472 0.41773,1.79244 0.0911,0.61268 0.1367,1.23548 0.13671,1.8684"
           style="line-height:125%;fill:url(#linearGradient3650);marker:none;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3630"
           inkscape:connector-curvature="0" />
      </g>
      <path
         style="opacity:0.66666667;fill:url(#radialGradient9132);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 148.625,208 0.125,-8.25 0.875,-1.125 22.125,-0.125 0.875,1.25 0,9.625 -24,-1.375 z"
         id="path9110"
         inkscape:connector-curvature="0" />
      <g
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient9157);stroke-width:0.15743744;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(7.9551498,0,0,5.0714902,122.01387,8.1927877)"
         id="g9137">
        <rect
           style="fill:none;stroke:url(#linearGradient9155);stroke-width:0.15743744;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect9139"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.1277746"
           ry="0.20042747" />
      </g>
      <g
         id="g9141"
         transform="matrix(7.9551498,0,0,5.0714902,122.01387,7.892765)"
         style="fill:url(#radialGradient9161);fill-opacity:1;stroke:none;filter:url(#filter4455)">
        <rect
           ry="0.20042747"
           rx="0.1277746"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect9143"
           style="fill:url(#radialGradient12462);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.19701266;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <path
         style="opacity:0.45402299;fill:url(#radialGradient9163);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 183.16122,125 0,-16.25 1.17444,-1.125 27.01225,0 0.78297,0.75 0,16.875 -1.37019,-16.5 -26.03355,0 -1.56592,16.25 z"
         id="path9145"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(1.5659277,0,0,1,-102.81632,0)"
         style="opacity:0.25862068;fill:url(#radialGradient9165);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         id="rect9147"
         width="17"
         height="1.625"
         x="183.5"
         y="124"
         rx="0.51886177"
         ry="0.8125" />
      <path
         sodipodi:type="arc"
         style="opacity:0.3103448;fill:url(#radialGradient9167);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         id="path9153"
         sodipodi:cx="56.375"
         sodipodi:cy="121"
         sodipodi:rx="4.625"
         sodipodi:ry="2"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         transform="matrix(1.9045066,0,0,1.2162162,90.279485,-26.912162)" />
      <g
         id="g9173"
         transform="matrix(7.9551498,0,0,5.0714902,122.01387,37.692788)"
         style="opacity:0.45402299;fill:none;stroke:url(#linearGradient9189);stroke-width:0.15743744;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.1277746"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect9175"
           style="fill:none;stroke:url(#linearGradient9187);stroke-width:0.15743744;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="fill:url(#radialGradient9193);fill-opacity:1;stroke:none;filter:url(#filter4451)"
         transform="matrix(7.9551498,0,0,5.0714902,122.01387,37.392765)"
         id="g9177">
        <rect
           style="fill:url(#radialGradient9159);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.19701266;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
           id="rect9179"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.1277746"
           ry="0.20042747" />
      </g>
      <path
         id="path9181"
         d="m 183.16122,154.5 0,-16.25 1.17444,-1.125 27.01225,0 0.78297,0.75 0,16.875 -1.37019,-16.5 -26.03355,0 -1.56592,16.25 z"
         style="opacity:0.45402299;fill:url(#radialGradient9195);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <rect
         ry="0.8125"
         rx="0.51886177"
         y="124"
         x="183.5"
         height="1.625"
         width="17"
         id="rect9183"
         style="opacity:0.25862068;fill:url(#radialGradient9197);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter7763);enable-background:accumulate"
         transform="matrix(1.5659277,0,0,1,-102.81632,29.5)" />
      <path
         transform="matrix(1.9045066,0,0,1.2162162,90.279485,2.587838)"
         d="m 61,121 c 0,1.10457 -2.070683,2 -4.625,2 -2.554317,0 -4.625,-0.89543 -4.625,-2 0,-1.10457 2.070683,-2 4.625,-2 2.554317,0 4.625,0.89543 4.625,2 z"
         sodipodi:ry="2"
         sodipodi:rx="4.625"
         sodipodi:cy="121"
         sodipodi:cx="56.375"
         id="path9185"
         style="opacity:0.3103448;fill:url(#radialGradient9199);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter8148);enable-background:accumulate"
         sodipodi:type="arc" />
      <g
         style="font-size:12.82951927px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;opacity:0.515625;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text9207">
        <path
           d="m 197.95579,114.14293 c -0.3717,0 -0.70162,0.0731 -0.98978,0.21925 -0.28399,0.142 -0.52413,0.34873 -0.72041,0.62018 -0.19211,0.26729 -0.33828,0.59512 -0.43851,0.98351 -0.10023,0.38422 -0.15035,0.81647 -0.15034,1.29673 -10e-6,0.48863 0.0438,0.92297 0.13155,1.303 0.0919,0.38005 0.22969,0.70162 0.41345,0.96472 0.18793,0.25893 0.42598,0.45731 0.71414,0.59512 0.29234,0.13364 0.63897,0.20046 1.0399,0.20046 0.37168,0 0.74337,-0.0418 1.11506,-0.12529 0.37586,-0.0835 0.78305,-0.20254 1.22156,-0.35707 l 0,1.62875 c -0.20047,0.0835 -0.39884,0.15452 -0.59512,0.21299 -0.19629,0.0585 -0.39675,0.1065 -0.60138,0.14408 -0.20464,0.0376 -0.41555,0.0647 -0.63271,0.0814 -0.21299,0.0209 -0.44269,0.0313 -0.68908,0.0313 -0.7058,0 -1.31762,-0.11276 -1.83547,-0.33828 -0.51787,-0.22552 -0.94593,-0.54291 -1.28421,-0.95219 -0.33828,-0.40927 -0.58886,-0.90207 -0.75173,-1.4784 -0.16287,-0.57632 -0.24431,-1.21738 -0.24431,-1.92317 0,-0.69326 0.094,-1.32805 0.2819,-1.90439 0.18793,-0.58049 0.46356,-1.07956 0.8269,-1.49719 0.36333,-0.41762 0.81228,-0.74128 1.34685,-0.97098 0.53456,-0.23387 1.14847,-0.3508 1.84174,-0.35081 0.4552,1e-5 0.91042,0.0585 1.36564,0.1754 0.45938,0.11277 0.89789,0.26938 1.31553,0.46983 l -0.62645,1.57863 c -0.34246,-0.16286 -0.687,-0.30486 -1.03362,-0.42598 -0.34664,-0.1211 -0.68701,-0.18166 -1.0211,-0.18166"
           style="line-height:125%;fill:#ffffff;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3641"
           inkscape:connector-curvature="0" />
      </g>
      <g
         style="font-size:12.75021553px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;opacity:0.515625;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
         id="text9213">
        <path
           d="m 192.32816,151.03154 -1.99845,-7.14087 -0.056,0 c 0.0249,0.38185 0.0456,0.75124 0.0623,1.10818 0.008,0.15357 0.0145,0.31129 0.0187,0.47315 0.008,0.16187 0.0145,0.32166 0.0187,0.47938 0.008,0.15772 0.0125,0.30921 0.0125,0.45447 0.004,0.14527 0.006,0.27601 0.006,0.39222 l 0,4.23347 -1.72452,0 0,-9.10196 2.62725,0 1.96731,6.96032 0.0374,0 2.09183,-6.96032 2.62724,0 0,9.10196 -1.79922,0 0,-4.30818 c -1e-5,-0.10791 -1e-5,-0.23034 0,-0.36731 0.004,-0.13696 0.008,-0.28223 0.0125,-0.4358 0.004,-0.15356 0.008,-0.30921 0.0125,-0.46693 0.008,-0.15771 0.0145,-0.31128 0.0187,-0.4607 0.0166,-0.34863 0.0311,-0.7118 0.0436,-1.0895 l -0.0498,0 -2.15409,7.12842 -1.77432,0"
           style="line-height:125%;fill:#ffffff;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3636"
           inkscape:connector-curvature="0" />
        <path
           d="m 204.1881,143.40507 c -0.36939,1e-5 -0.69728,0.0726 -0.98366,0.2179 -0.28223,0.14112 -0.52088,0.34657 -0.71595,0.61634 -0.19093,0.26564 -0.33619,0.59145 -0.4358,0.97743 -0.0996,0.38185 -0.14942,0.81142 -0.14942,1.28872 0,0.48561 0.0436,0.91726 0.13074,1.29495 0.0913,0.37769 0.22828,0.69728 0.4109,0.95875 0.18677,0.25733 0.42334,0.45448 0.70973,0.59144 0.29053,0.13282 0.63501,0.19923 1.03346,0.19923 0.36939,0 0.73878,-0.0415 1.10818,-0.12452 0.37353,-0.083 0.7782,-0.20129 1.21401,-0.35486 l 0,1.61868 c -0.19923,0.083 -0.39638,0.15356 -0.59145,0.21167 -0.19507,0.0581 -0.3943,0.10584 -0.59766,0.14319 -0.20338,0.0374 -0.41298,0.0643 -0.6288,0.0809 -0.21168,0.0207 -0.43995,0.0311 -0.68482,0.0311 -0.70143,0 -1.30948,-0.11206 -1.82413,-0.33618 -0.51466,-0.22413 -0.94008,-0.53956 -1.27627,-0.94631 -0.33619,-0.40674 -0.58521,-0.8965 -0.74708,-1.46926 -0.16187,-0.57276 -0.2428,-1.20986 -0.2428,-1.91129 0,-0.68897 0.0934,-1.31984 0.28015,-1.89261 0.18677,-0.57691 0.4607,-1.07289 0.8218,-1.48794 0.36108,-0.41504 0.80726,-0.7367 1.33852,-0.96498 0.53125,-0.23242 1.14137,-0.34863 1.83035,-0.34864 0.4524,1e-5 0.9048,0.0581 1.3572,0.17432 0.45655,0.11207 0.89235,0.26771 1.3074,0.46693 l -0.62257,1.56887 c -0.34035,-0.16186 -0.68276,-0.30298 -1.02724,-0.42335 -0.34449,-0.12035 -0.68276,-0.18053 -1.01479,-0.18054"
           style="line-height:125%;fill:#ffffff;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Droid Sans;-inkscape-font-specification:Droid Sans Bold"
           id="path3638"
           inkscape:connector-curvature="0" />
      </g>
      <path
         id="text9227"
         d="m 169.63876,32.362961 0.5306,2.635574 0.5306,0 0.18181,-0.927031 c 0.0445,-0.242538 0.0816,-0.490465 0.11502,-0.819238 l 0.007,0 c 0.0371,0.328773 0.0705,0.56592 0.11873,0.824628 l 0.17068,0.921641 0.52689,0 0.55656,-2.635574 -0.55285,0 -0.15213,1.045607 c -0.0445,0.301824 -0.0816,0.603649 -0.10761,0.900084 l -0.007,0 c -0.0334,-0.301824 -0.0816,-0.59287 -0.13357,-0.894694 l -0.18182,-1.050997 -0.44525,0 -0.19294,1.088724 c -0.0408,0.258707 -0.0965,0.560532 -0.12987,0.856967 l -0.0111,0 c -0.0297,-0.301824 -0.0668,-0.59287 -0.10018,-0.862357 l -0.14842,-1.083334 -0.57512,0 m 3.00461,2.635574 0.56399,0 0,-1.563018 c 0,-0.05929 0.004,-0.129354 0.0186,-0.177862 0.0408,-0.150911 0.13358,-0.291044 0.282,-0.291044 0.21149,0 0.29312,0.237148 0.29312,0.58209 l 0,1.449834 0.56399,0 0,-1.53607 c 0,-0.797678 -0.27458,-1.15879 -0.63449,-1.15879 -0.10389,0 -0.20779,0.03773 -0.29312,0.102405 -0.0891,0.06468 -0.16327,0.156302 -0.22263,0.274875 l -0.007,0 0,-1.509122 -0.56399,0 0,3.826702 m 1.97002,-2.635574 0.66788,2.409206 c 0.0186,0.06468 0.0223,0.107794 0.0223,0.134743 0,0.03773 -0.0111,0.07546 -0.0297,0.118574 -0.052,0.129354 -0.14842,0.264097 -0.23377,0.328773 -0.0853,0.07007 -0.17439,0.118574 -0.24489,0.140133 l 0.11874,0.689884 c 0.1447,-0.02156 0.35249,-0.113185 0.54543,-0.361111 0.20408,-0.264097 0.37847,-0.679106 0.63821,-1.724712 l 0.42299,-1.73549 -0.60481,0 -0.22262,1.293534 c -0.026,0.150912 -0.0557,0.350331 -0.0816,0.490464 l -0.0111,0 c -0.0223,-0.140133 -0.0594,-0.334162 -0.089,-0.490464 l -0.27086,-1.293534 -0.62707,0 m 4.40287,1.077946 c 0,-0.619818 -0.18924,-1.137232 -0.79404,-1.137232 -0.33023,0 -0.57883,0.134743 -0.70499,0.237148 l 0.10389,0.522803 c 0.11874,-0.102405 0.31539,-0.19403 0.50092,-0.19403 0.27828,0 0.33023,0.199419 0.33023,0.339553 l 0,0.03234 c -0.64192,0 -1.06491,0.323384 -1.06491,1.007878 0,0.420398 0.21893,0.808459 0.58626,0.808459 0.2152,0 0.40073,-0.113184 0.51946,-0.323383 l 0.0111,0 0.0334,0.264095 0.50833,0 c -0.0223,-0.145522 -0.0297,-0.388059 -0.0297,-0.635987 l 0,-0.921641 m -0.54544,0.598258 c 0,0.04851 -0.004,0.09702 -0.0111,0.140133 -0.0371,0.167081 -0.15583,0.301824 -0.29312,0.301824 -0.12616,0 -0.22263,-0.102404 -0.22263,-0.312603 0,-0.312604 0.23005,-0.415009 0.52689,-0.415009 l 0,0.285655 m 0.99197,0.95937 0.56399,0 0,-3.826702 -0.56399,0 0,3.826702 m 1.01458,0 0.56398,0 0,-3.826702 -0.56398,0 0,3.826702 m 1.83894,-3.131427 0,0.495853 -0.24119,0 0,0.60365 0.24119,0 0,1.083334 c 0,0.37189 0.0519,0.625207 0.15583,0.781509 0.0928,0.134742 0.2449,0.226369 0.4267,0.226369 0.15585,0 0.29313,-0.03234 0.36364,-0.07007 l -0.004,-0.619818 c -0.0519,0.01617 -0.089,0.02156 -0.16697,0.02156 -0.16697,0 -0.22263,-0.145523 -0.22263,-0.463516 l 0,-0.95937 0.40444,0 0,-0.60365 -0.40444,0 0,-0.716832 -0.55285,0.220979 m 1.28451,3.131427 0.56399,0 0,-1.563018 c 0,-0.05929 0.004,-0.129354 0.0186,-0.177862 0.0408,-0.150911 0.13358,-0.291044 0.282,-0.291044 0.21149,0 0.29312,0.237148 0.29312,0.58209 l 0,1.449834 0.564,0 0,-1.53607 c 0,-0.797678 -0.27458,-1.15879 -0.6345,-1.15879 -0.10389,0 -0.20778,0.03773 -0.29312,0.102405 -0.0891,0.06468 -0.16327,0.156302 -0.22263,0.274875 l -0.007,0 0,-1.509122 -0.56399,0 0,3.826702 m 2.73809,0 0,-2.635574 -0.56399,0 0,2.635574 0.56399,0 m -0.282,-2.980515 c 0.19666,0 0.3191,-0.194031 0.3191,-0.436567 -0.004,-0.247928 -0.12244,-0.436568 -0.31538,-0.436568 -0.19295,0 -0.31911,0.18864 -0.31911,0.436568 0,0.242536 0.12245,0.436567 0.31168,0.436567 l 0.004,0 m 0.62869,2.851162 c 0.13729,0.107794 0.34878,0.188641 0.58626,0.188641 0.51946,0 0.7829,-0.361112 0.7829,-0.856966 -0.004,-0.382671 -0.14471,-0.641378 -0.48978,-0.808458 -0.22263,-0.113185 -0.29312,-0.177862 -0.29312,-0.307214 0,-0.129354 0.0779,-0.210199 0.2152,-0.210199 0.15213,0 0.31168,0.08624 0.39331,0.145521 l 0.0965,-0.56053 c -0.11131,-0.08085 -0.29684,-0.156302 -0.50833,-0.156302 -0.44897,0 -0.73838,0.371891 -0.73838,0.867745 -0.004,0.307214 0.141,0.609039 0.51947,0.7869 0.20777,0.102404 0.26343,0.16708 0.26343,0.307213 0,0.134744 -0.0705,0.215589 -0.24117,0.215589 -0.16698,0 -0.38218,-0.102404 -0.48608,-0.194029 l -0.10018,0.582089 m 3.65393,-3.697349 0,1.428276 -0.007,0 c -0.0816,-0.17786 -0.25232,-0.296434 -0.47865,-0.296434 -0.43413,0 -0.8163,0.517414 -0.81259,1.401327 0,0.819237 0.34507,1.352821 0.77548,1.352821 0.23376,0 0.45639,-0.150913 0.5677,-0.441957 l 0.0111,0 0.0223,0.382669 0.50092,0 c -0.007,-0.17786 -0.0148,-0.485075 -0.0148,-0.786899 l 0,-3.039803 -0.564,0 m 0,2.657133 c 0,0.06468 -0.004,0.129354 -0.0111,0.18325 -0.0334,0.231758 -0.16698,0.393451 -0.33024,0.393451 -0.23376,0 -0.38588,-0.280267 -0.38588,-0.722224 0,-0.415008 0.12986,-0.749171 0.38959,-0.749171 0.1744,0 0.29684,0.177862 0.33024,0.398839 0.007,0.04851 0.007,0.102406 0.007,0.150913 l 0,0.344942 m 2.61849,0.113184 c 0.007,-0.06468 0.0186,-0.18864 0.0186,-0.328773 0,-0.652156 -0.22263,-1.315092 -0.80888,-1.315092 -0.62706,0 -0.91649,0.738393 -0.91649,1.406717 0,0.830017 0.3525,1.347431 0.96843,1.347431 0.2449,0 0.47123,-0.0539 0.65676,-0.167082 l -0.0742,-0.555141 c -0.15213,0.07546 -0.30797,0.113184 -0.50091,0.113184 -0.26344,0 -0.49349,-0.161691 -0.51204,-0.506634 l 1.16879,0.0054 m -1.1725,-0.565921 c 0.0148,-0.215589 0.1113,-0.533582 0.35249,-0.533582 0.25601,0 0.31539,0.339553 0.31539,0.533582 l -0.66788,0 m 1.60419,-1.509121 0,0.495853 -0.24118,0 0,0.60365 0.24118,0 0,1.083334 c 0,0.37189 0.0519,0.625207 0.15584,0.781509 0.0928,0.134742 0.24489,0.226369 0.4267,0.226369 0.15584,0 0.29313,-0.03234 0.36362,-0.07007 l -0.004,-0.619818 c -0.0519,0.01617 -0.089,0.02156 -0.16697,0.02156 -0.16696,0 -0.22262,-0.145523 -0.22262,-0.463516 l 0,-0.95937 0.40444,0 0,-0.60365 -0.40444,0 0,-0.716832 -0.55286,0.220979 m 2.79467,1.573799 c 0,-0.619818 -0.18924,-1.137232 -0.79404,-1.137232 -0.33023,0 -0.57883,0.134743 -0.70499,0.237148 l 0.1039,0.522803 c 0.11873,-0.102405 0.31539,-0.19403 0.50091,-0.19403 0.27828,0 0.33023,0.199419 0.33023,0.339553 l 0,0.03234 c -0.64191,0 -1.0649,0.323384 -1.0649,1.007878 0,0.420398 0.21891,0.808459 0.58625,0.808459 0.21521,0 0.40073,-0.113184 0.51947,-0.323383 l 0.0111,0 0.0334,0.264095 0.50833,0 c -0.0223,-0.145522 -0.0297,-0.388059 -0.0297,-0.635987 l 0,-0.921641 m -0.54543,0.598258 c 0,0.04851 -0.004,0.09702 -0.0111,0.140133 -0.0371,0.167081 -0.15584,0.301824 -0.29312,0.301824 -0.12616,0 -0.22263,-0.102404 -0.22263,-0.312603 0,-0.312604 0.23005,-0.415009 0.52689,-0.415009 l 0,0.285655 m 1.55595,0.95937 0,-2.635574 -0.56399,0 0,2.635574 0.56399,0 m -0.282,-2.980515 c 0.19665,0 0.3191,-0.194031 0.3191,-0.436567 -0.004,-0.247928 -0.12245,-0.436568 -0.31539,-0.436568 -0.19294,0 -0.3191,0.18864 -0.3191,0.436568 0,0.242536 0.12245,0.436567 0.31168,0.436567 l 0.004,0 m 0.73259,2.980515 0.56399,0 0,-3.826702 -0.56399,0 0,3.826702 m 1.79377,-1.180349 0,-0.09701 c -0.004,-0.242538 0.0557,-0.452737 0.18924,-0.668326 0.14099,-0.231758 0.3191,-0.495855 0.3191,-0.910863 0,-0.441956 -0.22634,-0.835407 -0.71241,-0.835407 -0.26716,0 -0.48607,0.107795 -0.61965,0.220979 l 0.12244,0.58209 c 0.10019,-0.09701 0.2449,-0.156302 0.37105,-0.156302 0.18181,0.0054 0.26716,0.134743 0.26716,0.317993 0,0.18325 -0.0965,0.361112 -0.21521,0.565921 -0.16697,0.285655 -0.22634,0.565921 -0.21892,0.840796 l 0.007,0.140133 0.48978,0 m -0.25602,1.239637 c 0.20037,0 0.33023,-0.2102 0.33023,-0.490465 -0.004,-0.291045 -0.13357,-0.490464 -0.33394,-0.490464 -0.19294,0 -0.33023,0.199419 -0.33023,0.490464 0,0.280265 0.13358,0.490465 0.33023,0.490465 l 0.004,0"
         style="font-size:4.47195053px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-indent:0;text-align:start;text-decoration:none;line-height:125%;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;text-anchor:start;opacity:0.515625;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate;font-family:Myriad"
         inkscape:connector-curvature="0" />
      <rect
         style="opacity:0.32400004;fill:none;stroke:#000000;stroke-width:2.84324098;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter4401)"
         id="rect4389"
         width="111.76333"
         height="25.35745"
         x="73.618324"
         y="53.536179"
         clip-path="url(#clipPath4393)"
         transform="matrix(1,0,0,1.1133076,0,-6.2360172)" />
      <g
         transform="matrix(0.5783885,0,0.07202846,0.5783885,73.643581,33.898189)"
         style="font-size:40px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;opacity:0.59200003;fill:#000000;fill-opacity:1;stroke:none;font-family:Digital2;-inkscape-font-specification:Digital2"
         id="text4405">
        <path
           d="m 119.16872,44.56 c 0.23998,2.7e-5 0.53332,-0.159972 0.88,-0.48 l 3.84,-3.44 c 0.13331,-0.106635 0.17331,-0.226635 0.12,-0.36 -0.0533,-0.133301 -0.18669,-0.199968 -0.4,-0.2 l -15.12,0 c -0.24,3.2e-5 -0.38667,0.05336 -0.44,0.16 -0.0533,0.08003 -0.08,0.146698 -0.08,0.2 0,0.05336 0.0267,0.106698 0.08,0.16 0.37333,0.426698 1.41333,1.586696 3.12,3.48 0.29333,0.320028 0.54666,0.480027 0.76,0.48 l 7.24,0 m 0.08,10.32 c -0.0267,0.160017 -2e-5,0.266684 0.08,0.32 0.10665,0.05335 0.22665,0.04002 0.36,-0.04 l 3.64,-1.96 c 0.45331,-0.239981 0.70665,-0.546647 0.76,-0.92 l 1.16,-10.28 c 0.0266,-0.213303 -0.0134,-0.346636 -0.12,-0.4 -0.08,-0.0533 -0.13335,-0.07997 -0.16,-0.08 -0.08,3e-5 -0.14669,0.0267 -0.2,0.08 -0.0267,0.0267 -1.34669,1.200029 -3.96,3.52 -0.34668,0.29336 -0.53335,0.57336 -0.56,0.84 l -1,8.92 m -8.24,0.56 3.04,-1.64 c 0.34666,-0.186648 0.65332,-0.186648 0.92,0 0.90665,0.586684 1.81332,1.146684 2.72,1.68 0.42665,0.240016 0.62665,0.440016 0.6,0.6 -0.0267,0.213349 -0.29335,0.453349 -0.8,0.72 -1.78668,0.933348 -2.81334,1.480014 -3.08,1.64 -0.32001,0.18668 -0.62668,0.18668 -0.92,0 -0.61334,-0.399986 -1.52001,-0.973319 -2.72,-1.72 -0.34667,-0.213318 -0.50667,-0.439984 -0.48,-0.68 0.0267,-0.159984 0.26666,-0.359984 0.72,-0.6 m 7.24,-3.36 c 0.0266,-0.213313 -0.04,-0.333313 -0.2,-0.36 -0.08,2e-5 -0.56001,0.213353 -1.44,0.64 -0.45335,0.240019 -0.50668,0.466686 -0.16,0.68 0.23999,0.133352 0.62665,0.360019 1.16,0.68 0.26665,0.160018 0.45332,-0.02665 0.56,-0.56 0.0267,-0.346647 0.0533,-0.706647 0.08,-1.08 m -1.72,15.48 c 0.23999,4e-6 0.50665,0.160004 0.8,0.48 l 3.04,3.44 c 0.10665,0.133334 0.11998,0.266667 0.04,0.4 -0.08,0.106667 -0.24002,0.16 -0.48,0.16 l -15.08,0 c -0.24,0 -0.38667,-0.05333 -0.44,-0.16 -0.08,-0.186666 0.50667,-0.826666 1.76,-1.92 0.77333,-0.639997 1.53333,-1.279997 2.28,-1.92 0.37333,-0.319996 0.66666,-0.479996 0.88,-0.48 l 7.2,0 m 2.44,-10.32 c 0.0533,-0.373318 0.22665,-0.466651 0.52,-0.28 l 3.2,1.96 c 0.39998,0.240013 0.57331,0.560013 0.52,0.96 l -1.16,10.24 c -0.0267,0.320002 -0.16002,0.480001 -0.4,0.48 -0.08,1e-6 -0.13335,-0.02666 -0.16,-0.08 -0.29335,-0.319998 -1.34668,-1.49333 -3.16,-3.52 -0.26668,-0.293328 -0.38668,-0.573328 -0.36,-0.84 l 1,-8.92 m -8.8,2.8 c -0.0267,0.213345 0.04,0.333345 0.2,0.36 0.13333,1.2e-5 0.62666,-0.213322 1.48,-0.64 0.26666,-0.133321 0.39999,-0.266654 0.4,-0.4 -1e-5,-0.106654 -0.08,-0.199987 -0.24,-0.28 -0.29334,-0.159987 -0.69334,-0.386653 -1.2,-0.68 -0.24001,-0.13332 -0.41334,0.06668 -0.52,0.6 -0.0267,0.346679 -0.0667,0.693346 -0.12,1.04"
           id="path4410"
           inkscape:connector-curvature="0" />
        <path
           d="m 125.95372,68.28 c 0.18667,-0.159996 0.34667,-0.159996 0.48,0 l 1.36,1.36 c 0.18667,0.186669 0.28,0.346669 0.28,0.48 -0.0267,0.160002 -0.17333,0.346668 -0.44,0.56 l -1.64,1.32 c -0.16,0.133333 -0.30666,0.133333 -0.44,0 -0.45333,-0.48 -0.90666,-0.933332 -1.36,-1.36 -0.16,-0.159998 -0.22666,-0.346665 -0.2,-0.56 1e-5,-0.106665 0.65334,-0.706664 1.96,-1.8"
           id="path4412"
           inkscape:connector-curvature="0" />
        <path
           d="m 147.51372,56.08 c -2e-5,0.160016 0.42665,0.480015 1.28,0.96 0.23998,0.186681 0.37331,0.106682 0.4,-0.24 l 0.16,-1.64 c 0.0266,-0.07998 -0.0134,-0.133316 -0.12,-0.16 -0.10669,1.7e-5 -0.20002,0.02668 -0.28,0.08 -0.45335,0.21335 -0.93335,0.546683 -1.44,1 m -2.64,-1.2 c -0.0267,0.160017 -2e-5,0.266684 0.08,0.32 0.10665,0.05335 0.22665,0.04002 0.36,-0.04 l 3.64,-1.96 c 0.45331,-0.239981 0.70665,-0.546647 0.76,-0.92 l 1.16,-10.28 c 0.0266,-0.213303 -0.0134,-0.346636 -0.12,-0.4 -0.08,-0.0533 -0.13335,-0.07997 -0.16,-0.08 -0.08,3e-5 -0.14669,0.0267 -0.2,0.08 -0.0267,0.0267 -1.34669,1.200029 -3.96,3.52 -0.34668,0.29336 -0.53335,0.57336 -0.56,0.84 l -1,8.92 m -0.28,2.36 c 0.0533,-0.373318 0.22665,-0.466651 0.52,-0.28 l 3.2,1.96 c 0.39998,0.240013 0.57331,0.560013 0.52,0.96 l -1.16,10.24 c -0.0267,0.320002 -0.16002,0.480001 -0.4,0.48 -0.08,1e-6 -0.13335,-0.02666 -0.16,-0.08 -0.29335,-0.319998 -1.34668,-1.49333 -3.16,-3.52 -0.26668,-0.293328 -0.38668,-0.573328 -0.36,-0.84 l 1,-8.92"
           id="path4414"
           inkscape:connector-curvature="0" />
        <path
           d="m 173.13872,56.08 c -2e-5,0.160016 0.42665,0.480015 1.28,0.96 0.23998,0.186681 0.37331,0.106682 0.4,-0.24 l 0.16,-1.64 c 0.0266,-0.07998 -0.0134,-0.133316 -0.12,-0.16 -0.10669,1.7e-5 -0.20002,0.02668 -0.28,0.08 -0.45335,0.21335 -0.93335,0.546683 -1.44,1 m -2.64,-1.2 c -0.0267,0.160017 -2e-5,0.266684 0.08,0.32 0.10665,0.05335 0.22665,0.04002 0.36,-0.04 l 3.64,-1.96 c 0.45331,-0.239981 0.70665,-0.546647 0.76,-0.92 l 1.16,-10.28 c 0.0266,-0.213303 -0.0134,-0.346636 -0.12,-0.4 -0.08,-0.0533 -0.13335,-0.07997 -0.16,-0.08 -0.08,3e-5 -0.14669,0.0267 -0.2,0.08 -0.0267,0.0267 -1.34669,1.200029 -3.96,3.52 -0.34668,0.29336 -0.53335,0.57336 -0.56,0.84 l -1,8.92 m -8.24,0.56 3.04,-1.64 c 0.34666,-0.186648 0.65332,-0.186648 0.92,0 0.90665,0.586684 1.81332,1.146684 2.72,1.68 0.42665,0.240016 0.62665,0.440016 0.6,0.6 -0.0267,0.213349 -0.29335,0.453349 -0.8,0.72 -1.78668,0.933348 -2.81334,1.480014 -3.08,1.64 -0.32001,0.18668 -0.62668,0.18668 -0.92,0 -0.61334,-0.399986 -1.52001,-0.973319 -2.72,-1.72 -0.34667,-0.213318 -0.50667,-0.439984 -0.48,-0.68 0.0267,-0.159984 0.26666,-0.359984 0.72,-0.6 m 7.96,1.8 c 0.0533,-0.373318 0.22665,-0.466651 0.52,-0.28 l 3.2,1.96 c 0.39998,0.240013 0.57331,0.560013 0.52,0.96 l -1.16,10.24 c -0.0267,0.320002 -0.16002,0.480001 -0.4,0.48 -0.08,1e-6 -0.13335,-0.02666 -0.16,-0.08 -0.29335,-0.319998 -1.34668,-1.49333 -3.16,-3.52 -0.26668,-0.293328 -0.38668,-0.573328 -0.36,-0.84 l 1,-8.92 m -1.48,1.64 c -0.0267,0.213346 -0.08,0.600013 -0.16,1.16 -0.0533,0.426678 -0.26668,0.506678 -0.64,0.24 -0.21335,-0.106655 -0.52001,-0.279988 -0.92,-0.52 -0.21335,-0.133321 -0.32001,-0.253321 -0.32,-0.36 -1e-5,-0.106654 0.0933,-0.213321 0.28,-0.32 0.42665,-0.186654 0.87999,-0.41332 1.36,-0.68 0.26665,-0.159986 0.39999,1.4e-5 0.4,0.48 m -8.04,-4 c -0.0533,0.346683 -0.21334,0.440017 -0.48,0.28 l -3.2,-1.96 c -0.42667,-0.266648 -0.61334,-0.573314 -0.56,-0.92 l 1.16,-10.28 c 0.0267,-0.213303 0.10666,-0.35997 0.24,-0.44 0.18666,-0.106636 0.77333,0.40003 1.76,1.52 0.58666,0.693362 1.15999,1.373361 1.72,2.04 0.29333,0.320027 0.42666,0.600026 0.4,0.84 l -1.04,8.92 m 1.52,-1.64 c 0.0267,-0.213314 0.0667,-0.599981 0.12,-1.16 0.0533,-0.426646 0.27999,-0.506646 0.68,-0.24 0.29332,0.186687 0.59999,0.36002 0.92,0.52 0.37332,0.266686 0.37332,0.493352 0,0.68 -0.26668,0.133352 -0.72001,0.360019 -1.36,0.68 -0.16001,0.08002 -0.26667,0.06668 -0.32,-0.04 -0.0533,-0.133315 -0.0667,-0.279981 -0.04,-0.44"
           id="path4416"
           inkscape:connector-curvature="0" />
      </g>
      <path
         style="opacity:0.41999996;fill:url(#radialGradient4477);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 46.625,116.9 0.0957,-8.25 0.669921,-1.125 L 64.330078,107.4 65,108.65 65,118.275 46.625,116.9 z"
         id="path4475"
         inkscape:connector-curvature="0" />
      <path
         id="path4479"
         d="m 46.625,147 0.0957,-8.25 0.669921,-1.125 L 64.330078,137.5 65,138.75 65,148.375 46.625,147 z"
         style="opacity:0.41999996;fill:url(#radialGradient4481);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <path
         style="opacity:0.41999996;fill:url(#radialGradient4485);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 46.625,177 0.0957,-8.25 0.669921,-1.125 L 64.330078,167.5 65,168.75 65,178.375 46.625,177 z"
         id="path4483"
         inkscape:connector-curvature="0" />
      <path
         id="path4487"
         d="m 46.625,209 0.0957,-8.25 0.669921,-1.125 L 64.330078,199.5 65,200.75 65,210.375 46.625,209 z"
         style="opacity:0.41999996;fill:url(#radialGradient4489);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <path
         style="opacity:0.41999996;fill:url(#radialGradient4493);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 183.29492,146.5 0.1495,-8.25 1.04654,-1.125 26.4625,-0.125 1.04654,1.25 0,9.625 -28.70508,-1.375 z"
         id="path4491"
         inkscape:connector-curvature="0" />
      <path
         id="path4495"
         d="m 183.29492,117.25 0.1495,-8.25 1.04654,-1.125 26.4625,-0.125 L 212,109 l 0,9.625 -28.70508,-1.375 z"
         style="opacity:0.41999996;fill:url(#radialGradient4499);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         inkscape:connector-curvature="0" />
      <path
         style="opacity:0.41999996;fill:url(#radialGradient4503);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         d="m 184,190.89282 0.14583,-20.64311 1.02083,-2.54224 L 210.97917,167.425 212,170.24971 212,192 184,190.89282 z"
         id="path4501"
         sodipodi:nodetypes="ccccccc"
         inkscape:connector-curvature="0" />
      <rect
         transform="matrix(5.0801515,0,0,-5.2214902,119.33969,320.53222)"
         style="opacity:0.6;fill:none;stroke:url(#linearGradient4507);stroke-width:0.19416213;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:6;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible;filter:url(#filter9038)"
         id="rect4505"
         width="6"
         height="10"
         x="12.5"
         y="19.5"
         rx="0.40360424"
         ry="0.39200974" />
      <g
         style="opacity:0.42000002;fill:none;stroke:url(#linearGradient4515);stroke-width:0.15743744;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(7.9551498,0,0,-5.0714902,122.01387,255.76698)"
         id="g4509">
        <rect
           style="fill:none;stroke:url(#linearGradient4513);stroke-width:0.15743744;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect4511"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.1277746"
           ry="0.20042747" />
      </g>
      <g
         id="g4517"
         transform="matrix(7.9551498,0,0,-5.0714902,122.01387,226.26698)"
         style="opacity:0.42000002;fill:none;stroke:url(#linearGradient4523);stroke-width:0.15743744;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.1277746"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect4519"
           style="fill:none;stroke:url(#linearGradient4521);stroke-width:0.15743744;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="opacity:0.42000002;fill:none;stroke:url(#linearGradient4531);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(5.0801515,0,0,-5.0714902,7.5763597,226.06698)"
         id="g4525">
        <rect
           style="fill:none;stroke:url(#linearGradient4529);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect4527"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.20008577"
           ry="0.20042747" />
      </g>
      <g
         id="g4533"
         transform="matrix(5.0801515,0,0,-5.0714902,7.5763597,256.06698)"
         style="opacity:0.42000002;fill:none;stroke:url(#linearGradient4539);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.20008577"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect4535"
           style="fill:none;stroke:url(#linearGradient4537);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
      <g
         style="opacity:0.42000002;fill:none;stroke:url(#linearGradient4551);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)"
         transform="matrix(5.0801515,0,0,-5.0714902,7.5763597,286.06698)"
         id="g4545">
        <rect
           style="fill:none;stroke:url(#linearGradient4549);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible"
           id="rect4547"
           width="4.0000024"
           height="3.9999957"
           x="7.500001"
           y="19.500013"
           rx="0.20008577"
           ry="0.20042747" />
      </g>
      <g
         id="g4553"
         transform="matrix(5.0801515,0,0,-5.0714902,7.5763597,318.06698)"
         style="opacity:0.42000002;fill:none;stroke:url(#linearGradient4559);stroke-width:0.19701254;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;filter:url(#filter7615)">
        <rect
           ry="0.20042747"
           rx="0.20008577"
           y="19.500013"
           x="7.500001"
           height="3.9999957"
           width="4.0000024"
           id="rect4555"
           style="fill:none;stroke:url(#linearGradient4557);stroke-width:0.19701254;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:1.4;marker:none;visibility:visible;display:inline;overflow:visible" />
      </g>
    </g>
  </g>
</svg>
'''
			)

	# Create explanatory README.rst
	(package_root / "svg_src" / "README.rst").write_text(
			'''In this directory you can put source SVGs that will be converted into minified SVGs and png images when building the package.

There is an example icon in this folder from the gnome-icon-theme (GPLv3 Licensed).

You can use this as the basis for your own icons or, more likely, you will be copying SVGs into this folder that follow the same layout as the example.

Delete the example SVG and this file when you are finished.
'''
			)

# Create COPYING file with a few TODOs
(package_root / "COPYING").write_text(
		f"""{package_name} {author_copyright_string}

TODO: Say here which theme you based this off and provide a link

TODO: Say which license this work is licensed under
This work is licenced under the terms of the ...

TODO: If the original project asked for attribution, give that here
When attributing the artwork, using "ACME Project" is enough.
Please link to http://www.example.org where available.
"""
		)

# Create MANIFEST.in
(package_root / "MANIFEST.in"
	).write_text(f"""include __pkginfo__.py
include requirements.txt
recursive-include {package_name} *
""")

# Create README.rst
(package_root / "README.rst").write_text(
		f"""********************************
{THEME_NAME} Icon Theme for wxPython
********************************

This package provides a wxPython wxArtProvider class with icons from the {THEME_NAME} Icon Theme.

To use it in your application:

.. code-block:: python

	from {package_name} import wx{THEME_NAME}IconTheme

	class MyApp(wx.App):
		def OnInit(self):
			wx.ArtProvider.Push(wx{THEME_NAME}IconTheme())
			self.frame = TestFrame(None, wx.ID_ANY)
			self.SetTopWindow(self.frame)
			self.frame.Show()
			return True

And then the icons can be accessed through wx.ArtProvider:

.. code-block:: python

	wx.ArtProvider.GetBitmap('document-new', wx.ART_OTHER, wx.Size(48, 48))

Any `FreeDesktop Icon Theme Specification <https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html>`_ name can be used.

Currently the `Client ID` is not used, so just pass `wx.ART_OTHER`.
"""
		)

# Create requirements.txt
(package_root / "requirements.txt").write_text(f"""wx_icons_{INHERITS_FROM.lower()}
importlib_resources>=1.0.2
""")

# Create setup.py
(package_root / "setup.py").write_text(
		f'''{shebang}
"""
custom_wx_icons Setup script
"""
#
#  Copyright (C) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
{license_placeholder}
#
# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py
#

# stdlib
import pathlib

# 3rd party
from setuptools import find_packages, setup

# this package
from __pkginfo__ import (
	author, author_email, general_trove_classifiers, get_requirements_and_readme, prepare_data_files, web,
	)


theme_name = "{THEME_NAME}"
VERSION = "0.1.0"
modname = f"wx_icons_{{theme_name.lower()}}"
# TODO: Set your license here
license = ''
short_desc = 'description goes here'

install_requires, long_description = get_requirements_and_readme(pathlib.Path.cwd())

classifiers = [
		# "Development Status :: 1 - Planning",
		# "Development Status :: 2 - Pre-Alpha",
		"Development Status :: 3 - Alpha",
		# "Development Status :: 4 - Beta",
		# "Development Status :: 5 - Production/Stable",
		# "Development Status :: 6 - Mature",
		# "Development Status :: 7 - Inactive",

		# TODO: Uncomment your license from the list below
		# "License :: OSI Approved :: Academic Free License (AFL)",
		# "License :: OSI Approved :: Apache Software License",
		# "License :: OSI Approved :: BSD License",
		# "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
		# "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
		# "License :: OSI Approved :: GNU Free Documentation License (FDL)",
		# "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		# "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",,
		# "License :: OSI Approved :: MIT License",
		# "License :: OSI Approved :: Python Software Foundation License",
		# "License :: Other/Proprietary License",
		# "License :: Public Domain",

		] + general_trove_classifiers


setup(
		author=author,
		author_email=author_email,
		classifiers=classifiers,
		description=short_desc,
		install_requires=install_requires,
		license=license,
		long_description=long_description,
		name=modname,
		packages=find_packages(exclude=("tests",)),
		url=web,
		version=VERSION,
		package_data={{modname: prepare_data_files(modname, theme_name)}},
		include_package_data=True,
		# data_files=[
		# 	(theme_name, prepare_data_files(modname, theme_name)),
		# 	]
		)

'''
		)

print("Some files have TODO items in them. Please finish those manually.")
print(
		"Please add a file to the package root called `LICENSE` or `LICENCE` that contains "
		"the text of the license the UPSTREAM theme this package is based on is licensed under."
		)
