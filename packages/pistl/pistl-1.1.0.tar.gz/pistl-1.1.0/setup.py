# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pistl']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=7.3.2,<8.0.0',
 'ipykernel>=6.27.1,<7.0.0',
 'matplotlib>=3.8.2,<4.0.0',
 'numpy>=1.26.2,<2.0.0',
 'pdoc>=14.1.0,<15.0.0',
 'pip>=23.3.1,<24.0.0',
 'pytest>=7.4.3,<8.0.0',
 'pyvista[jupyter]>=0.38.1',
 'trame-components>=2.2.1,<3.0.0',
 'trame-vuetify>=2.3.1,<3.0.0',
 'trame>=3.3.0,<4.0.0',
 'vtk>=9.3.0,<10.0.0']

setup_kwargs = {
    'name': 'pistl',
    'version': '1.1.0',
    'description': 'Python library to generate STL files for common shapes and geometries.',
    'long_description': '# <h1 style="text-align:center; color:\'red\'">PISTL (pronounced as "Pistol")</h1>\n\n<p text-align="center"><img src=".\\assets\\pystl_readme_cover.PNG" alt="Pystl_cover_image"></p>\n\n<u>About the figure above</u>: Multiple shapes generated using PISTL as STL file and visualized in **Meshmixer** for the purpose of this picture. The visualization in PISTL can be done using pyvista, which is installed as a dependency.\\_\n\n### What is PISTL?\n\nPISTL is a small (micro) library that can be used in python to programatically create stereolithographic (stl) files of regular geometric shapes like circle, cylinder, tetrahedron, sphere, pyramid and others by morphing these shapes. pystl also provide functions that can be used to translate and rotate these stl objects.\n\nIn summary:\nPISTL can be used for the following purposes:\n\n- to create simple geometric shape files in .stl format.\n- visualize this stl files. [PySTL uses pyvista for such visualizations].\n- perform simple transformations like translate, rotate and scale shapes.\n\n<u>PISTL is an open source project that welcomes contributions from developers from diverse community and backgrounds.\\_</u>\n\ncontact : sumanan047@gmail.com to get added on the project formally.\n',
    'author': 'Suman Saurabh',
    'author_email': 'sumanan047@gmail.com',
    'maintainer': 'Suman Saurabh',
    'maintainer_email': 'sumanan047@gmail.com',
    'url': 'https://github.com/sumanan047/pistl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
