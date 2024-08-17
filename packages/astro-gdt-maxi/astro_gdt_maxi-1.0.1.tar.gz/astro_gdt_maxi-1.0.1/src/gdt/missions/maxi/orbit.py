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
import astropy.units as u
import astropy.coordinates.representation as r
from gdt.core.coords.spacecraft import SpacecraftFrameModelMixin
from gdt.core.file import FitsFileContextManager
from .frame import MaxiFrame
from .headers import OrbitHeaders
from .time import Time
from .gsc.detectors import GscFov

__all__ = ['MaxiOrbit']


class MaxiOrbit(SpacecraftFrameModelMixin, FitsFileContextManager):
    """Class for reading a MAXI orbit file.
    """
    def get_spacecraft_frame(self):
        sc_frame = MaxiFrame(
            obsgeoloc=r.CartesianRepresentation(x=self.column(1, 'X'),
                                                y=self.column(1, 'Y'),
                                                z=self.column(1, 'Z'), unit=u.km),
            obsgeovel=r.CartesianRepresentation(
                x=self.column(1, 'VELOCITY_X') * u.km / u.s,
                y=self.column(1, 'VELOCITY_Y') * u.km / u.s,
                z=self.column(1, 'VELOCITY_Z') * u.km / u.s,
                unit=u.km / u.s
            ),
            obstime=Time(self.column(1, 'TIME'), format='maxi'),
            detectors=GscFov
        )
        return sc_frame
    
    @property
    def headers(self):
        return self._headers
    
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a MAXI orbit FITS file.
        
        Args:
            file_path (str): The file path of the FITS file
        
        Returns:        
            (:class:`MaxiOrbit`)
        """
        obj = super().open(file_path, **kwargs)
        hdrs = [hdu.header for hdu in obj.hdulist]
        obj._headers = OrbitHeaders.from_headers(hdrs)
        return obj
