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
import numpy as np
import astropy.io.fits as fits

from gdt.core.tte import PhotonList
from gdt.core.data_primitives import Ebounds, Gti, EventList
from .detectors import GscDetectors
from .headers import EventsHeaders
from ..time import Time
from gdt.core.phaii import Phaii

__all__ = ['GscTte']


class GscTte(PhotonList):
    """Class for Time-Tagged Event data.
    """ 
    _event_deadtime = 3e-5
    """(float) Deadtime per event (30 microsec).  
    From https://academic.oup.com/pasj/article/63/sp3/S623/1506699
    """
    
    @property
    def detector(self):
        """(str): The detector name"""
        try:
            return GscDetectors.from_full_name(self.headers[1]['DETNAM']).name
        except:
            return self.headers[1]['DETNAM']

    def to_phaii(self, bin_method, *args, time_range=None, energy_range=None,
                 channel_range=None, **kwargs):
        """Convert the PhotonList data to PHAII data by binning the data in 
        time.

        Note:
          If the data has no energy calibration, then ``energy_range`` is 
          ignored, and only ``channel_range`` is used.
        
        Args:
            bin_method (<function>): A binning function for unbinned data
            *args: Arguments to pass to the binning function
            time_range ([(float, float), ...], optional):
                The time range of the spectrum. If omitted, uses the entire 
                time range of the data.
            energy_range ((float, float), optional): 
                The energy range of the spectrum. If omitted, uses the entire 
                energy range of the data.
            channel_range ((int, int), optional): 
                The channel range of the spectrum. If omitted, uses the entire 
                energy range of the data.
            **kwargs: Options to pass to the binning function
        
        Returns:
            (:class:`~gdt.core.phaii.Phaii`)
        """
        headers = None
        return super().to_phaii(bin_method, *args, time_range=time_range, 
                                energy_range=energy_range, 
                                channel_range=channel_range, 
                                phaii_class=Phaii, headers=headers, **kwargs)
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open an events FITS file and return the TTE object

        Args:
            file_path (str): The file path of the FITS file
        
        Returns:        
            (:class:`GscTte`)
        """
        obj = super().open(file_path, **kwargs)
        trigtime = None
        
        # get the headers
        hdrs = [hdu.header for hdu in obj.hdulist]
        headers = EventsHeaders.from_headers(hdrs)
        
        # data
        times = obj.column(1, 'TIME')
        data = EventList(times=times, channels=obj.column(1, 'PI'))
        
        # the good time intervals
        gti_start = obj.column(2, 'START')
        gti_stop = obj.column(2, 'STOP')
        gti = Gti.from_bounds(gti_start, gti_stop)

        obj.close()
        
        return cls.from_data(data, gti=gti, filename=obj.filename,
                             headers=headers, 
                             event_deadtime=cls._event_deadtime,
                             overflow_deadtime=cls._event_deadtime)

    def _build_headers(self, trigtime, tstart, tstop, num_chans):
        
        headers = self.headers.copy()
        for hdu in headers:
            hdu['TSTART'] = tstart
            hdu['TSTOP'] = tstop
            try:
                hdu['DETCHANS'] = num_chans
            except:
                pass
        
        return headers
