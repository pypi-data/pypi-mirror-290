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

import datetime
import re

import erfa
import numpy as np
from astropy.time import TimeFromEpoch, TimeUnique, ScaleValueError, Time
from astropy.time.utils import day_frac

__all__ = ['MaxiSecTime', 'Time']

class MaxiSecTime(TimeFromEpoch):
    """Represents the number of seconds elapsed since Jan 1, 2000, 00:00:00 UTC,
    including leap seconds
    """
    name = 'maxi'
    """(str): Name of the mission"""

    unit = 1.0 / 86400
    """(float): unit in days"""

    epoch_val = '2000-01-01 00:01:04.184'
    """(str): The epoch in Terrestrial Time"""

    epoch_val2 = None

    epoch_scale = 'tt'
    """(str): The scale of :attr:`epoch_val`"""

    epoch_format = 'iso'
    """(str): Format of :attr:`epoch_val`"""
