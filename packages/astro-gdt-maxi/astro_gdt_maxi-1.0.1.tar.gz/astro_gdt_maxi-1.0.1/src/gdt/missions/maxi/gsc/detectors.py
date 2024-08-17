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

import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from gdt.core.detector import Detectors

__all__ = ['GscDetectors', 'GscFov']

class GscFov(Detectors):
    """The MAXI GSC detector fields of view for the two GSC instruments:
    GSC-H (Horizontal) and GSC-Z (Zenith).  The FOVs each are 
    ~160 degrees x ~3 degrees.   

    .. rubric:: Attributes Summary
    .. autosummary::

      azimuth
      elevation
      fov
      full_name
      number
      zenith

    .. rubric:: Methods Summary

    .. autosummary::
      
      from_full_name
      from_num
      from_str
      pointing
      skycoord
  
    .. rubric:: Attributes Documentation

    .. autoattribute:: azimuth
    .. autoattribute:: elevation
    .. autoattribute:: fov
    .. autoattribute:: full_name
    .. autoattribute:: number
    .. autoattribute:: zenith

    .. rubric:: Methods Documentation

    .. automethod:: from_full_name
    .. automethod:: from_num
    .. automethod:: from_str
    .. automethod:: pointing
    .. automethod:: skycoord
    """
    H = ('GSC-H', 0, 0.0 * u.deg, 90.0 * u.deg, [(280.0, 91.5), (80.0, 91.5), 
                                                 (80.0, 88.5), (280.0, 88.5), 
                                                 (280.0, 91.5)])
    Z = ('GSC-Z', 1, 0.0 * u.deg, 180.0 * u.deg, [(268.5, 100.0), (91.5, 100.0),
                                                  (88.5, 100.0), (271.5, 100.0),
                                                  (268.5, 100.0)])

    def __init__(self, full_name, number, azimuth, zenith, fov_box):
        super().__init__(full_name, number, azimuth, zenith)
        self._fov_box = fov_box
    
    @property
    def fov(self):
        """(list of tuples): The bounding box of the FOV"""
        return self._fov_box
    
    def skycoord(self, frame):
        """Creates a polygon in the MAXI frame based on the bounding box of the
        FOV.  The last coordinate represents the center of the FOV, while the 
        remaining coordinates (0, N-1) represent the closed polygon of the FOV.
        
        Args:
            frame (MaxiFrame): The MAXI coordinate frame
        
        Returns:
            (astropy.coordinate.SkyCoord)
        """
        
        fov = self.fov
        
        # number of points along each edge of the box
        num_points = [101, 3, 101, 3]
        
        segs = []
        for i in range(4):
            arc_fracs = np.linspace(0.0, 1.0, num_points[i])
            coord1 = SkyCoord(fov[i][0], 90.0-fov[i][1], unit='deg')
            coord2 = SkyCoord(fov[i+1][0], 90.0-fov[i+1][1], unit='deg')
            segs.append( point_on_arc(coord1, coord2, arc_fracs) )
        
        
        az = np.concatenate([seg.ra for seg in segs])
        el = np.concatenate([seg.dec for seg in segs])
        
        # include the center of the FOV as the last coordinate
        az = np.append(az, self.azimuth)
        el = np.append(el, self.elevation)
        
        return SkyCoord(az, el, frame=frame, unit='deg')

    
# mark: FIXME The pointings transformed from the quaternions in the teldef files
# do not appear to correctly rotate into J2000.  found no documentation so far
# on how they should be used.
class GscDetectors(Detectors):
    """The MAXI GSC detectors.
    
    .. rubric:: Attributes Summary
    .. autosummary::

      azimuth
      elevation
      full_name
      number
      zenith

    .. rubric:: Methods Summary

    .. autosummary::
      
      from_full_name
      from_num
      from_str
      h_detectors
      is_h_detector
      is_z_detector
      pointing
      skycoord
      z_detectors
  
    .. rubric:: Attributes Documentation

    .. autoattribute:: azimuth
    .. autoattribute:: elevation
    .. autoattribute:: full_name
    .. autoattribute:: number
    .. autoattribute:: zenith

    .. rubric:: Methods Documentation

    .. automethod:: from_full_name
    .. automethod:: from_num
    .. automethod:: from_str
    .. automethod:: h_detectors
    .. automethod:: is_h_detector
    .. automethod:: is_z_detector
    .. automethod:: pointing
    .. automethod:: skycoord
    .. automethod:: z_detectors
    """
    HA0 = ('GSC_0', 0, None, None)
    HA1 = ('GSC_1', 1, None, None)
    HA2 = ('GSC_2', 2, None, None)
    HB0 = ('GSC_6', 6, None, None)
    HB1 = ('GSC_7', 7, None, None)
    HB2 = ('GSC_8', 8, None, None)

    ZA0 = ('GSC_3', 3, None, None)
    ZA1 = ('GSC_4', 4, None, None)
    ZA2 = ('GSC_5', 5, None, None)
    ZB0 = ('GSC_9', 9, None, None)
    ZB1 = ('GSC_A', 10, None, None)
    ZB2 = ('GSC_B', 11, None, None)

    def __init__(self, full_name, number, azimuth, zenith):
        super().__init__(full_name, number, azimuth, zenith)

    @classmethod
    def h_detectors(cls):
        """Get all detectors that are in the horizontal direction.
        
        Returns:
            (list of :class:`GscDetectors`)    
        """
        return [x for x in cls if x.is_h_detector()]

    @classmethod
    def z_detectors(cls):
        """Get all detectors that are in the zenith direction.
    
        Returns:
            (list of :class:`GscDetectors`)
        """
        return [x for x in cls if x.is_z_detector()]

    def is_h_detector(self):
        """Check if detector is a horizontal detector.
    
        Returns:
            (bool)
        """
        return self.name[0] == 'H'

    def is_z_detector(self):
        """Check if detector is a zenith detector.
    
        Returns:
            (bool)
        """
        return self.name[0] == 'Z'
        

def point_on_arc(coord1, coord2, frac):
    """Given two bounding coordinates of the segment of a great circle, return 
    a point that is ``frac`` fraction of the way along the path between 
    ``coord1`` and ``coord2``.
    
    Args:
        coord1 (astropy.coordinates.SkyCoord): The coordinate at the start of
                                               the bounding path
        coord2 (astropy.coordinates.SkyCoord): The coordinate at the end of
                                               the bounding path
        frac (float or np.array): The fractional distance(s) along the path
    
    Returns:
        (astropy.coordinates.SkyCoord)                                        
    """
    
    lon1, lat1 = coord1.ra.to('rad').value, coord1.dec.to('rad').value
    lon2, lat2 = coord2.ra.to('rad').value, coord2.dec.to('rad').value

    delta = coord1.separation(coord2).to('rad').value
    a = np.sin( (1.0 - frac) * delta) / np.sin(delta)
    b = np.sin(frac * delta) / np.sin(delta)
    x = a * np.cos(lat1) * np.cos(lon1) + b * np.cos(lat2) * np.cos(lon2)
    y = a * np.cos(lat1) * np.sin(lon1) + b * np.cos(lat2) * np.sin(lon2)
    z = a * np.sin(lat1) + b * np.sin(lat2)
    lat3 = np.arctan2(z, (x**2 + y**2)**0.5)
    lon3 = np.arctan2(y, x)
    
    return SkyCoord(lon3, lat3, unit='rad')
 