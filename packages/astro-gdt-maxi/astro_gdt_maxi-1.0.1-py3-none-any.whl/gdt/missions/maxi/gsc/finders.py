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

from gdt.core.heasarc import BaseFinder
from ..finders import MaxiEventsFinder
from ..time import *

__all__ = ['GscEventsFinder']


class GscEventsFinder(MaxiEventsFinder):
    """The finder for GSC event files stored on HEASARC.
    """
    def cd(self, time, bitrate):
        """Set the time. If the object was previously associated with a 
        different time, this will effectively change the working directory to 
        that of the new time. If the time is invalid, an exception will be 
        raised, and no directory change will be made.
        
        Args:
            time (astropy.time.Time, optional): The time object
            bitrate (str): Either 'low' or 'med' for low and medium bitrates,
                           respectively.
        """
        BaseFinder.cd(self, time, bitrate)

    def get_event(self, download_dir, pixels=None, **kwargs):
        """Download the MAXI GSC event files for the day.
        
        Args:
            download_dir (str): The download directory
            pixels (list, optional): The file associated with the HEALPixel(s) 
                                     to download (0-767). If omitted, downloads
                                     all available files.
           verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'evt', 'gz', pixels=pixels)
        return self.get(download_dir, files, **kwargs)

    def ls_event(self):
        """List the MAXI GSC event files for the day. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'evt', 'gz')
        
    def _construct_path(self, time_obj, bitrate):
        path = super()._construct_path(time_obj)
        if bitrate == 'low':
            return os.path.join(path, 'gsc_low')
        elif bitrate == 'med':
            return os.path.join(path, 'gsc_med')
        else:
            raise ValueError("bitrate must be either 'low' or 'med'")
            
