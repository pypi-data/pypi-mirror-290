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
from gdt.core.plot.plot import SkyPolygon, DetectorPointing
from gdt.core.plot.sky import SkyPlot, EquatorialPlot, SpacecraftPlot, \
                              GalacticPlot, get_lonlat

__all__ = ['MaxiDetectorFov', 'MaxiEquatorialPlot', 'MaxiGalacticPlot', 
           'MaxiSpacecraftPlot', 'MaxiSkyPlot']

class MaxiSkyPlot(SkyPlot):
    """Custom base class for plotting the MAXI pointings on the sky.
    """
    def plot_detector(self, det_coord, det, **kwargs):
        """Plot the detector FOV on the sky.
        
        Args:
            det_coord (astropy.coordinates.SkyCoord): The coordinates of the 
                                                      FOV to plot.
            det (str): The detector name
            kwargs: Keywords to pass to :class:`MaxiDetectorFov`
        """
        x, y = get_lonlat(det_coord.transform_to(self._astropy_frame))
        pointing = MaxiDetectorFov(x.value, y.value, det, self.ax, 
                                   frame=self._frame, flipped=self._flipped, 
                                   face_alpha=0.0, **kwargs)
        pointing.linewidth=2.5
                                   
        self._detectors.include(pointing, det)
    
    
class MaxiEquatorialPlot(MaxiSkyPlot, EquatorialPlot):
    """Custom class for plotting in equatorial coordinates with the MAXI FOVs.
    """
    pass


class MaxiGalacticPlot(MaxiSkyPlot, GalacticPlot):
    """Custom class for plotting in galactic coordinates with the MAXI FOVs.
    """
    pass


class MaxiSpacecraftPlot(MaxiSkyPlot, SpacecraftPlot):
    """Custom class for plotting in MAXI coordinates with the MAXI FOVs.
    """
    pass


class MaxiDetectorFov(SkyPolygon):
    """Plot a MAXI FOV on the sky in equatorial, galactic, or spacecraft 
    coordinates.
    
    Note:
        The last x and y coordinates are assumed to be represent the center
        of the FOV (used for the detector annotation), while the rest of the
        coordinates are assumed to represent the closed polygon of the FOV.

    Parameters:
        x (float): The azimuthal coordinate, in degrees
        y (float): The polar coordinate, in degrees
        radius (float):  The radius of the circle, in degrees
        det (str): The name of the detector
        ax (:class:`matplotlib.axes`): The axis on which to plot
        flipped (bool, optional): If True, the azimuthal axis is flipped, 
                                  following equatorial convention
        frame (str, optional): Either 'equatorial', 'galactic', 'spacecraft'.
                               Default is 'equatorial'
        face_color (str, optional): The color of the circle fill
        face_alpha (float, optional): The alpha opacity of the circle fill
        edge_color (str, optional): The color of the circle edge
        edge_alpha (float, optional): The alpha opacity of the circle edge
        color (str, optional): The color of the circle. If set, overrides 
                               ``face_color`` and ``edge_color``.
        alpha (float, optional): The alpha of the circle. If set, overrides 
                               ``face_alpha`` and ``edge_alpha``.
        fontsize (float, optional): The size of the detector label
        font_alpha (float, optional): The alpha opacity of the detector label
        font_color (str, optional): The font color.
        **kwargs: Other plotting options
    """
    def __init__(self, x, y, det, ax, flipped=True, frame='equatorial', 
                 color='dimgray', alpha=None, face_color=None, face_alpha=0.25,
                 edge_alpha=0.5, fontsize=10, font_alpha=0.8, font_color=None,
                 **kwargs):
        
        super().__init__(x[:-1], y[:-1], ax, flipped=flipped, color=color, alpha=alpha, 
                         face_alpha=face_alpha, edge_alpha=edge_alpha, 
                         frame=frame)

        self._det = det
        self._fontsize = fontsize
        self._fontalpha = font_alpha
        self._font_color = font_color
        if font_color is None:
            self._font_color = self._color
        
        # the last coordinate is the center of the FOV
        self._annotate(x[-1], y[-1], ax, flipped, frame)

    @property
    def font_alpha(self):
        """(float): The alpha opacity of the detector label"""
        return self._fontalpha
    @font_alpha.setter
    def font_alpha(self, alpha):
        self._artists[-1].set_alpha(alpha)
        self._fontalpha = alpha

    @property
    def font_color(self):
        """(float): The color of the detector label"""
        return self._font_color
    @font_color.setter
    def font_color(self, color):
        self._artists[-1].set_color(color)
        self._font_color = color

    @property
    def fontsize(self):
        """(float): The size of the detector label"""
        return self._fontsize
    @fontsize.setter
    def fontsize(self, size):
        self._artists[-1].set_fontsize(size)
        self._fontsize = size

    def _annotate(self, x, y, ax, flipped, frame):
        theta = np.deg2rad(y)
        phi = np.deg2rad(180.0 - x)
        if frame == 'spacecraft':
            phi -= np.pi
            if phi < -np.pi:
                phi += 2 * np.pi
        elif frame == 'galactic':
            phi -= np.pi
            if phi < -np.pi:
                phi += 2 * np.pi
        else:
            pass            

        if not flipped:
            phi *= -1.0
        
        txt = ax.text(phi, theta, self._det, fontsize=self._fontsize,
                      ha='center', va='center', color=self._font_color,
                      alpha=self._fontalpha, **self._kwargs)
        self._artists.append(txt)

    def __repr__(self):
        spaces = ' '*18
        s = "<MaxiDetectorFov: '{}';\n".format(self._det)
        s += '{0}face_color={1};\n'.format(spaces, self.face_color) 
        s += "{0}face_alpha={1};\n".format(spaces, self.face_alpha)
        s += "{0}edge_color={1};\n".format(spaces, self.edge_color)
        s += "{0}edge_alpha={1};\n".format(spaces, self.edge_alpha)
        s += "{0}linestyle='{1}';\n".format(spaces, self.linestyle)
        s += '{0}linewidth={1};\n'.format(spaces, self.linewidth)
        s += '{0}fontsize={1};\n'.format(spaces, self.fontsize)
        s += '{0}font_color={1};\n'.format(spaces, self.font_color)
        s += '{0}font_alpha={1}>'.format(spaces, self.font_alpha)
        return s

 