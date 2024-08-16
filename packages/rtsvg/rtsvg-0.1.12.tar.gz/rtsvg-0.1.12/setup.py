from setuptools import setup, find_packages
setup(
name='rtsvg',
version='0.1.12',
author='D. Trimm',
author_email='dave.trimm@gmail.com',
description='Visualization Package Leveraging SVG in Jupyter Notebooks',
packages=['rtsvg'],
extras_require={
    'stable':[
      'geopandas',
      'hdbscan',
      'jupyter_bokeh',
      'networkx',
      'numpy',
      'pandas',
      'panel',
      'pyarrow',
      'polars',
      'shapely',
      'squarify',
      'svglib',
      'umap-learn',
      'wordcloud',
    ]
},
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: Apache Software License',
'Operating System :: OS Independent',
],
python_requires='>=3.11',
url='https://github.com/datrcode/racetrack_svg_framework'
)

