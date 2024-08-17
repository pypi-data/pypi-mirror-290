# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT 
# WITH UNLIMITED RIGHTS
#
# Grant No.: 80NSSC21K0651
# Grantee Name: Universities Space Research Association
# Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
# Copyright 2024 by Universities Space Research Association (USRA). All rights 
# reserved.
#
# Developed by: Adam Goldstein
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# This work is a derivative of the Gamma-ray Data Tools (GDT), including the 
# Core and Fermi packages, originally developed by the following:
#
#     William Cleveland and Adam Goldstein
#     Universities Space Research Association
#     Science and Technology Institute
#     https://sti.usra.edu
#     
#     Daniel Kocevski
#     National Aeronautics and Space Administration (NASA)
#     Marshall Space Flight Center
#     Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not 
# use this file except in compliance with the License. You may obtain a copy of 
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
# License for the specific language governing permissions and limitations under 
# the License.
import os
from math import floor
from gdt.core.heasarc import BaseFinder
from .time import *

__all__ = ['MaxiAuxilFinder']


class MaxiFinder(BaseFinder):
    """
    Base class for finding MAXI data on HEASARC.
    
    Parameters:
        time (astropy.time.Time, optional): The time object
    """  
    _root = '/maxi/data/obs'
    
    def cd(self, time):
        """Set the time. If the object was previously associated with a 
        different time, this will effectively change the working directory to 
        that of the new time. If the time is invalid, an exception will be 
        raised, and no directory change will be made.
        
        Args:
            time (astropy.time.Time, optional): The time object
        """
        super().cd(time)

    def _construct_path(self, time_obj):
        """Constructs the FTP path for a time.
        
        MAXI data are separated into super directories spanning 1000
        units of MJD. Each super directory is subdivided into directories
        for each MJD.
        
        Args:
            time_obj (astropy.time.Time): The time object

        Returns:
            (str): The path of the FTP directory for the time
        """
        mjd = time_obj.mjd
        mjd_1000 = int( mjd - (mjd % 1000) )
        super_dir = f'MJD{mjd_1000}'
        sub_dir = f'MJD{floor(mjd)}'
        
        path = os.path.join(self._root, super_dir, sub_dir)
        return path
    
    #mark TODO: have this accept a SkyCoord and convert to pixel.
    def _file_filter(self, file_list, filetype, extension, dets=None, 
                     pixels=None):
        """Filters the directory for the requested filetype, extension, and 
        optionally detectors or HEALPixels.
        
        Args:
            filetype (str): The type of file, e.g. 'gti'
            extension (str): The file extension, e.g. '.gz'
            dets (list, optional): The detectors. If omitted, then files for 
                                   all detectors are returned
            pixels (list, optional): The HEALPixels to request. If omitted, 
                                     then files for all pixels are returned.

        Returns:
            (list): The filtered file list
        """
        files = super()._file_filter(file_list, filetype, extension)

        if dets is not None:
            if not isinstance(dets, (list, tuple)):
                dets = [dets]
            files = [f for f in files if
                     any(f'_gsc{det}_' in f for det in dets) or 
                     any(f'_gsc{det}.' in f for det in dets)]

        if pixels is not None:
            if not isinstance(pixels, (list, tuple)):
                pixels = [pixels]
            files = [f for f in files if any(f'_{str(pix).zfill(3)}.' in f \
                     for pix in pixels)]

        return files
    
    
class MaxiAuxilFinder(MaxiFinder):
    """Finder for MAXI auxiliary data files.
    """
    def get_attitude(self, download_dir, **kwargs):
        """Download the MAXI attitude file for the day.
        
        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, '.att', 'gz')
        return self.get(download_dir, files, **kwargs)

    def get_gti_low(self, download_dir, dets=None, **kwargs):
        """Download the MAXI low-bitrate GTI files for the day.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
           verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'low', 'gti.gz', dets=dets)
        return self.get(download_dir, files, **kwargs)

    def get_gti_med(self, download_dir, dets=None, **kwargs):
        """Download the MAXI medium-bitrate GTI files for the day.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
           verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'med', 'gti.gz', dets=dets)
        return self.get(download_dir, files, **kwargs)
    
    def get_orbit(self, download_dir, **kwargs):
        """Download the MAXI orbit file for the day.
        
        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, '.orb', 'gz')
        return self.get(download_dir, files, **kwargs)

    def ls_attitude(self):
        """List the MAXI attitude file for the day. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '.att', 'gz')
    
    def ls_gti_low(self):
        """List the MAXI GSC low-bitrate GTI files for the day. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'low', 'gti.gz')

    def ls_gti_med(self):
        """List the MAXI GSC medium-bitrate GTI files for the day. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'med', 'gti.gz')

    def ls_orbit(self):
        """List the MAXI orbit file for the day. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '.orb', 'gz')
        
    def _construct_path(self, time_obj):
        path = super()._construct_path(time_obj)
        return os.path.join(path, 'auxil')


class MaxiEventsFinder(MaxiFinder):
    """Subclassed finder because events are in their own subdirectories.
    """
    def _construct_path(self, time_obj):
        path = super()._construct_path(time_obj)
        return os.path.join(path, 'events')
