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
import astropy.io.fits as fits
import numpy as np

from gdt.core.response import Rsp
from gdt.core.data_primitives import Bins, Ebounds, ResponseMatrix
from gdt.core.file import FitsFileContextManager
from .detectors import GscDetectors
from .headers import ArfHeaders, RmfHeaders
from ..time import *

__all__ = ['GscArf', 'GscRmf', 'GscRsp']

class GscArf(FitsFileContextManager):
    """A MAXI GSC Ancillary Response File (ARF)
    """    
    def __init__(self):
        self._headers = None
        self._arf_803 = None
        self._arf_854 = None
        self._detector = None
    
    @property
    def detector(self):
        """(str): The detector name"""
        return self._detector
    
    def get_arf(self, hv):
        """Retrieve the ARF
        
        Args:
            hv (int): The HV bit corresponding to the ARF to retrieve.  Valid
                      values are 803 and 854.
        Returns:
            (:class:`~gdt.core.data_primitives.Bins`)
        """
        if hv == 803:
            return self._arf_803
        elif hv == 854:
            return self._arf_854
        else:
            raise ValueError('hv must be either 803 or 854')
        
    @classmethod
    def open(cls, file_path, **kwargs):
        """Read an ARF from disk.

        Args:
            file_path (str): The file path

        Returns:
            (:class:`GscArf`)
        """
        obj = super().open(file_path, **kwargs)
        
        hdrs = [hdu.header for hdu in obj.hdulist]
        obj._headers = ArfHeaders.from_headers(hdrs)
        
        obj._arf_803 = Bins(obj.column(1, 'SPECRESP'), 
                           obj.column(1, 'ENERG_LO'), obj.column(1, 'ENERG_HI'))

        obj._arf_854 = Bins(obj.column(2, 'SPECRESP'), 
                           obj.column(2, 'ENERG_LO'), obj.column(2, 'ENERG_HI'))
        
        obj._detector = GscDetectors.from_full_name(hdrs[1]['INSTRUME']).name
        
        obj.close()
        return obj


class GscRmf(Rsp):
    """A MAXI GSC Response Matrix File (RMF)
    """
    def apply_arf(self, arf_obj):
        """Apply an ARF to the RMF and return a complete detector response.
        
        Args:
            arf_obj (:class:`GscArf`): The ARF object
        
        Returns:
            (:class:`GscRsp`)
        """
        if 'hv803' in self.filename:
            arf = arf_obj.get_arf(803)
        elif 'hv854' in self.filename:
            arf = arf_obj.get_arf(854)
        else:
            raise RuntimeError('Unkown RMF type')
        
        drm = ResponseMatrix(self.drm.matrix * arf.counts[np.newaxis, :],
                             self.drm.photon_bins.low_edges(),
                             self.drm.photon_bins.high_edges(),
                             self.drm.ebounds.low_edges(),
                             self.drm.ebounds.high_edges())
        
        fname = '.'.join(self.filename.split('.')[:-1]) + '.rsp'
        obj = GscRsp.from_data(drm, filename=fname, headers=self.headers, 
                               detector=self.detector, start_time=self.tstart,
                               stop_time=self.tstop)
        return obj
    
    @classmethod
    def open(cls, file_path, **kwargs):
        """Read a RMF from disk.

        Args:
            file_path (str): The file path

        Returns:
            (:class:`GscRmf`)
        """
        obj = super().open(file_path, **kwargs)
        
        hdrs = [hdu.header for hdu in obj.hdulist]
        headers = RmfHeaders.from_headers(hdrs)
        
        det = GscDetectors.from_full_name(hdrs[0]['INSTRUME'])

        matrix = obj._decompress_drm(obj.column(1, 'MATRIX'), hdrs[1]['NAXIS2'],
                                  hdrs[1]['DETCHANS'], obj.column(1, 'F_CHAN'),
                                  obj.column(1, 'N_CHAN'))
        
        drm = ResponseMatrix(matrix, obj.column(1, 'ENERG_LO'),
                             obj.column(1, 'ENERG_HI'), obj.column(2, 'E_MIN'),
                             obj.column(2, 'E_MAX'))

        obj.close()
        obj = cls.from_data(drm, filename=obj.filename, headers=headers,
                            detector=det.name, start_time=0.0, stop_time=0.0)
                
        return obj
    
    @staticmethod
    def _decompress_drm(matrix, num_photon_bins, num_channels, _fchan, _nchan):
        """Decompresses a DRM using the standard F_CHAN, N_CHAN, and N_GRP
        keywords.
        
        Args:
            drm_data (np.recarray): The DRM data
        
        Returns:        
            (np.array)
        """
        # The format of the compress matrix is a series of groups, for each
        # energy bin, of channels with non-zero values.
        # fchan stands for the first channel of each of these groups
        # and nchan for the number of channels in the group group.
        # Each row in the matrix is a 1D list consisting on the contatenated
        # values of all groups for a given energy bin 
        # Note that in FITS the first index is 1
        drm = np.zeros((num_photon_bins, num_channels))
        for fchan, nchan, effective_area, drm_row \
            in zip(_fchan, _nchan, matrix, drm):

            channel_offset = 0
                
            start_idx = fchan - 1
            end_idx = start_idx + nchan
            drm_row[start_idx:end_idx] = \
                           effective_area[channel_offset:channel_offset + nchan]    
            channel_offset += nchan

        return drm


class GscRsp(Rsp):
    """Class for MAXI GSC response files
    """
    pass