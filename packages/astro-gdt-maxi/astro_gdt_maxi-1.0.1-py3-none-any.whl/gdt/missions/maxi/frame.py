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
from astropy.coordinates import FunctionTransform, ICRS, frame_transform_graph
import astropy.coordinates.representation as r
from gdt.core.coords import *
from gdt.core.coords.spacecraft.frame import spacecraft_to_icrs, icrs_to_spacecraft
from gdt.core.time import time_range

__all__ = ['MaxiFrame', 'maxi_to_icrs', 'icrs_to_maxi']

class MaxiFrame(SpacecraftFrame):
    """
    The MAXI reference frame in azimuth and elevation.  The frame is defined
    as a quaternion that represents a rotation from the MAXI frame to the ICRS
    frame. This class is a wholesale inheritance of SpacecraftFrame

    Example use:

        >>> from gdt.core.coords import Quaternion
        >>> quat = Quaternion([-0.218,  0.009,  0.652, -0.726], scalar_first=False)
        >>> maxi_frame = MaxiFrame(quaternion=quat)
        >>> coord = SkyCoord(100.0, -30.0, unit='deg')
        >>> az_el = SkyCoord.transform_to(maxi_frame)
    """
    # mark TODO: This should be fixed in core
    def at(self, obstime):
        """Retrieve the interpolated spacecraft positions and quaternions for 
        the specified time(s).
        
        Args:
            obstime (astropy.time.Time): The times for which the frames are 
                                         requested.
        
        Returns:
            (:class:`MaxiFrame`)
        """
        if not self._interp:
            self.init_interpolation()

        t = obstime.unix_tai

        if self._interp_geovel is None:
            geovel = None
        else:
            geovel = r.CartesianRepresentation(self._interp_geovel(t), unit=self.obsgeovel.x.unit)

        if self._interp_quat is None:
            quat = None
        else:
            quat = Quaternion.from_rotation(self._interp_quat(t))
        
        if self._interp_geoloc is not None:
            obsgeoloc = r.CartesianRepresentation(self._interp_geoloc(t), 
                                                  unit=self.obsgeoloc.x.unit)
        else:
            obsgeoloc = None
            
        
        obj = self.__class__(obstime=obstime, obsgeoloc=obsgeoloc, 
                             obsgeovel=geovel, quaternion=quat, 
                             detectors=self.detectors)
        return obj
    
    @classmethod
    def combine_orbit_attitude(cls, orb_frame, att_frame, sample_period=1.0):
        """Combine the orbit and attitude information into a single frame.
        
        Note:
            Since the orbital and attitude frames may have different ranges
            and sampling periods, the frames must be interpolated onto a common
            grid of times, the period of which is set by the keyword argument
            ``sample_period``.
            
        Args:
            orb_frame (:class:`MaxiFrame`): The orbital frame
            att_frame (:class:`MaxiFrame`): The attitude (orientation) frame
            sample_period (float, optional): The sampling period of the frame in
                                             unit of seconds.
            
        Returns:
            (:class:`MaxiFrame`)
        """
        if sample_period <= 0.0:
            raise ValueError('sample_period must be > 0')
        
        if (orb_frame.obstime.size > 1) and (orb_frame.obsgeoloc.size == 1):
            raise TypeError('orb_frame has no orbital data')
        
        if (att_frame.quaternion is None):
            raise TypeError('att_frame has no attitude data')
        
        # must select the intersection of the two times because we cannot 
        # extrapolate.
        tstart = max(orb_frame.obstime[0], att_frame.obstime[0])
        tstop = min(orb_frame.obstime[-1], att_frame.obstime[-1])
        times = time_range(tstart, tstop, step=sample_period)
        
        orb_frame_interp = orb_frame.at(times)
        att_frame_interp = att_frame.at(times)
        
        sc_frame = cls(obsgeoloc=orb_frame_interp.obsgeoloc,
                       obsgeovel=orb_frame_interp.obsgeovel,
                       quaternion=att_frame_interp.quaternion,
                       obstime=att_frame_interp.obstime,
                       detectors=att_frame_interp.detectors)
        return sc_frame


@frame_transform_graph.transform(FunctionTransform, MaxiFrame, ICRS)
def maxi_to_icrs(maxi_frame, icrs_frame):
    """Convert from the MAXI frame to the ICRS frame.

    Args:
        maxi_frame (:class:`MaxiFrame`): The MAXI frame
        icrs_frame (:class:`astropy.coordinates.ICRS`)

    Returns:
        (:class:`astropy.coordinates.ICRS`)
    """
    return spacecraft_to_icrs(maxi_frame, icrs_frame)

@frame_transform_graph.transform(FunctionTransform, ICRS, MaxiFrame)
def icrs_to_maxi(icrs_frame, maxi_frame):
    """Convert from the ICRS frame to the MAXI frame.

    Args:
        icrs_frame (:class:`astropy.coordinates.ICRS`)
        maxi_frame (:class:`MaxiFrame`): The MAXI frame

    Returns:
        (:class:`MaxiFrame`)
    """
    return icrs_to_spacecraft(icrs_frame, maxi_frame)
