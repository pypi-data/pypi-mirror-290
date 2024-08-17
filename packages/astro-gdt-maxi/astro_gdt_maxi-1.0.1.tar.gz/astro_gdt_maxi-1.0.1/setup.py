# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT WITH UNLIMITED RIGHTS
#
# Based on the work by:
#               William Cleveland and Adam Goldstein
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
# and
#               Daniel Kocevski
#               National Aeronautics and Space Administration (NASA)
#               Marshall Space Flight Center
#               Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing permissions and limitations under the
# License.
#
import sys
from pathlib import Path

from setuptools import setup, find_namespace_packages

if __name__ == '__main__':
    pwd = Path(__file__).parent
    sys.path.append(str(pwd / 'src'))
    import gdt.missions.maxi as maxi

    setup(
        name="astro-gdt-maxi",
        version=maxi.__version__,
        description="Gamma-ray Data Tools: MAXI Mission",
        long_description=(pwd / "PYPI-README.rst").read_text(),
        author='A. Goldstein',
        url='https://github.com/USRA-STI/gdt-maxi',
        packages=find_namespace_packages(where='src', include=["*"]),
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: MacOS",
            "Operating System :: POSIX :: Linux",
            "Topic :: Scientific/Engineering :: Astronomy",
            "Topic :: Software Development :: Libraries",
        ],
        license_files=['license.txt'],
        keywords=['astronomy', 'gammaray', 'gamma-ray', 'usra'],
        package_dir={"": "src"},
        package_data={
            'gdt.data': ['maxi.urls']
        },
        include_package_data=True,
        python_requires='>=3.8',
        install_requires=[
            'astro-gdt>=2.1.0',
            'pyproj>=1.9.6',
            'numpy>=1.17.3',
            'scipy>=1.1.0',
            'matplotlib>=3.6.3',
            'astropy>=3.1',
            'healpy>=1.12.4',
            'cartopy>=0.21.1',
        ],
        project_urls={
            'Documentation': 'https://astro-gdt-maxi.readthedocs.io/en/latest/',
            'Source': 'https://github.com/USRA-STI/gdt-maxi',
            'Tracker': 'https://github.com/USRA-STI/gdt-maxi/issues',
        }

    )
