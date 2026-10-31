from setuptools import setup
from ThreeDToLD._version import __version__

setup(
    name='3DToLD',
    version=__version__,
    description='This is a graphical Python program for converting various 3D file formats(stl,3mf,obj,stp, etc.) to the LDraw file format (.dat).',
    url='https://github.com/Nexusnui/Convert-To-LDraw',
    author='Nexusnui',
    author_email='developer@nexusnui.de',
    license='GPL 3.0',
    packages=['ThreeDToLD',
              'ThreeDToLD.brick_data',
              'ThreeDToLD.icons',
              'ThreeDToLD.ui_elements',
              'ThreeDToLD.model_loaders',
              'colorpicker',
              'ThreeDToLD.ui_elements.js-libraries'
              ],
    package_data={
        'ThreeDToLD.brick_data': ['colour_definitions.csv'],
        'ThreeDToLD.icons': ['3DToLD_icon.ico', '3DToLD_icon*.png',
                                 'reload-icon.svg', 'loading_animation.webm',
                                 'Loading_Symbol.png'],
        'ThreeDToLD.ui_elements': ['viewer_template.html'],
        'ThreeDToLD.ui_elements.js-libraries': ['*'],
        'ThreeDToLD': ['default_config.toml']
    },
    install_requires=["numpy>=2.2.6,<=2.5.4",
                      "cascadio==0.1.1",
                      "charset-normalizer==3.5.2",
                      "lxml==6.1.3",
                      "manifold3d==3.5.4",
                      "meshio==5.3.5",
                      "networkx>=3.4.2,<=3.7",
                      "pillow>=12.3.0,<=13.0.0",
                      "pycollada==0.9.3",
                      "PyQt6==6.11.0",
                      "PyQt6-WebEngine>=6.11.0,<=6.11.2",
                      "scipy>=1.15.3,<=1.18.1",
                      "trimesh==5.2.0",
                      "platformdirs>=4.12.4,<=4.14.2",
                      "tomlkit==0.15.2",
                      "pyqtdarktheme-fork==2.3.6"
                      ],
    entry_points={
        'gui_scripts': [
            '3DToLD = ThreeDToLD.app:run',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: JavaScript',
        'Natural Language :: English',
        'Topic :: File Formats',
        'Topic :: Multimedia :: Graphics :: 3D Modeling'
    ],
)
'''
'Development Status :: 4 - Beta' is used for Snapshots
'Development Status :: 5 - Production/Stable' for full releases
'''
