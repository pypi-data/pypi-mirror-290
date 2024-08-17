# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT WITH UNLIMITED RIGHTS
#
# Contract No.: CA 80MSFC17M0022
# Contractor Name: Universities Space Research Association
# Contractor Address: 7178 Columbia Gateway Drive, Columbia, MD 21046
#
# Copyright 2017-2022 by Universities Space Research Association (USRA). All rights reserved.
#
# Developed by: William Cleveland and Adam Goldstein
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# Developed by: Daniel Kocevski
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
from gdt.core.coords import Quaternion
from gdt.core.coords.spacecraft import SpacecraftFrameModelMixin
from gdt.core.file import FitsFileContextManager
from .frame import MaxiFrame
from .headers import AttitudeHeaders
from .time import Time
from .gsc.detectors import GscFov

__all__ = ['MaxiAttitude']


class MaxiAttitude(SpacecraftFrameModelMixin, FitsFileContextManager):
    """Class for reading a MAXI attitude file.
    """
    def get_spacecraft_frame(self):
        sc_frame = MaxiFrame(
            quaternion=Quaternion(self.column(1, 'QPARAM')),
            obstime=Time(self.column(1, 'TIME'), format='maxi'),
            detectors=GscFov
        )
        return sc_frame
    
    @property
    def headers(self):
        return self._headers
    
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a MAXI attitude FITS file.
        
        Args:
            file_path (str): The file path of the FITS file
        
        Returns:        
            (:class:`MaxiAttitude`)
        """
        obj = super().open(file_path, **kwargs)
        hdrs = [hdu.header for hdu in obj.hdulist]
        obj._headers = AttitudeHeaders.from_headers(hdrs)
        return obj
