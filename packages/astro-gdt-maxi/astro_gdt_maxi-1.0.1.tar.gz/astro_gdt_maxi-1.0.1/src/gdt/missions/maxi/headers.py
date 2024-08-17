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

from gdt.core.headers import Header, FileHeaders
from .time import Time

__all__ = ['AttitudeHeaders', 'OrbitHeaders']

# mission definitions
_telescope = 'MAXI'
_origin = 'ISAS/JAXA'
_equinox = 2000.0
_radecsys = 'FK5'
_mjdrefi = 51544
_mjdreff = 0.00074287037037037
_timesys = 'TT'
_creator = Header.creator()[1]

# common keyword cards
_creator_card = ('CREATOR', '', 'Software')
_date_card = ('DATE', '', 'date of file creation (GMT)')
_date_end_card = ('DATE-END', '', 'observation end date and time')
_date_obs_card = ('DATE-OBS', '', 'observation start date and time')
_equinox_card = ('EQUINOX', _equinox, 'Equinox for coordinate system')
_extname_card = ('EXTNAME', '', 'name of this binary table extension')
_mjdrefi_card = ('MJDREFI', _mjdrefi, 'MJD reference day')
_mjdreff_card = ('MJDREFF', _mjdreff, 'MJD reference (fraction of day)')
_origin_card = ('ORIGIN', _origin, 'Tape writing institution')
_procver_card = ('PROCVER', '', 'Major.Minor.Tool.CALDB')
_radecsys_card = ('RADECSYS', _radecsys, 'World Coordinate System')
_telescope_card = ('TELESCOP', _telescope, 'Mission name')
_timeref_card = ('TIMEREF', 'LOCAL', 'reference time')
_timesys_card = ('TIMESYS', _timesys, 'time measured from')
_timeunit_card = ('TIMEUNIT', 's', 'unit for time keyword')
_tstart_card = ('TSTART', 0.0, 'time of first data ')
_tstop_card = ('TSTOP', 0.0, 'time of last data ')


#----------------

class MaxiHeader(Header):

    def __setitem__(self, key, val):
        if not isinstance(key, tuple):
            if key.upper() == 'TSTART':
                self['DATE-OBS'] = Time(val, format='maxi').isot
            elif key.upper() == 'TSTOP':
                self['DATE-END'] = Time(val, format='maxi').isot
            else:
                pass

        super().__setitem__(key, val)

class PrimaryHeader(MaxiHeader):
    name = 'PRIMARY'
    keywords = [_telescope_card, _origin_card, _radecsys_card, _equinox_card, 
                _mjdrefi_card, _mjdreff_card, _timeref_card, _timesys_card, 
                _timeunit_card, _date_card, _creator_card]

class OrbitHeader(MaxiHeader):
    name = 'ORBIT'
    keywords = [_extname_card, ('VERSION', '', 'orb file version'), 
                _telescope_card, _origin_card, _radecsys_card, _equinox_card,
                _mjdrefi_card, _mjdreff_card, _timeref_card, _timesys_card,
                _timeunit_card, _date_card, _creator_card, _tstart_card, 
                _tstop_card, _date_obs_card, _date_end_card, _procver_card]

class AttitudeHeader(MaxiHeader):
    name = 'ATTITUDE'
    keywords = [_extname_card, _telescope_card, _origin_card, _radecsys_card, 
                _equinox_card, _mjdrefi_card, _mjdreff_card, _timeref_card, 
                _timesys_card, _timeunit_card, _date_card, _creator_card, 
                _tstart_card,  _tstop_card, _date_obs_card, _date_end_card, 
                _procver_card]


# -----------------------------------------------------------------------------

class OrbitHeaders(FileHeaders):
    """FITS headers for orbit file"""
    _header_templates = [PrimaryHeader(), OrbitHeader()]


class AttitudeHeaders(FileHeaders):
    """FITS headers for attitude file"""
    _header_templates = [PrimaryHeader(), AttitudeHeader()]

