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

__all__ = ['ArfHeaders', 'EventsHeaders', 'RmfHeaders']

from gdt.core.headers import Header, FileHeaders
from ..time import Time

from ..headers import _creator_card, _date_card, _date_end_card, _date_obs_card, \
                      _equinox_card, _extname_card, _mjdrefi_card, _mjdreff_card, \
                      _origin_card, _procver_card, _radecsys_card, \
                      _telescope_card, _timeref_card, _timesys_card, \
                      _timeunit_card, _tstart_card, _tstop_card

_caldbver_card = ('CALDBVER', '', 'CALDB version')
_chantype_card = ('CHANTYPE', 'PI', 'Detector Channel Type in use (PHA or PI)')
_clockapp_card = ('CLOCKAPP', 'T', 'If clock correction are applied (F/T)')
_col_phi_card = ('COL_PHI', 0.0, 'COL phi of incident angle')
_col_tha_card = ('COL_THA', 0.0, 'COL theta of incident angle')
_dataform_card = ('DATAFORM', 0, 'Event Data Format ID')
_datamode_card = ('DATAMODE', '', 'Data mode (32 or 64 BIT for GSC, STANDARD for S')
_datatype_card = ('DATATYPE', 0, 'Data Type ID: Obs./Sim./Ground Cal.')
_dec_nom_card = ('DEC_NOM', 0.0, 'DEc of the tile center [deg]')
_detchans_card = ('DETCHANS', 0, 'total number of detector channels')
_detnam_card = ('DETNAM', '', 'Detector')
_det_phi_card = ('DET_PHI', 0.0, 'DET phi of incident angle')
_det_tha_card = ('DET_THA', 0.0, 'DET theta of incident angle')
_detxcntr_card = ('DETXCNTR', 0.0, 'DETX center on Be window')
_detxmax_card = ('DETXMAX', 0.0, 'DETX average max on Be window')
_detxmin_card = ('DETXMIN', 0.0, 'DETX average min on Be window')
_detycntr_card = ('DETYCNTR', 0.0, 'DETY center on Be window')
_detymax_card = ('DETYMAX', 0.0, 'DETY average max on Be window')
_detymin_card = ('DETYMIN', 0.0, 'DETY average min on Be window')
_exposure_card = ('EXPOSURE', 0.0, 'Exposure time')
_filin001_card = ('FILIN001', '', 'Input file name')
_formver_card = ('FORMVER', '', 'Event file format version')
_gpcmoid_card = ('GPCMOID', 'NA', 'Gas Proportional Counter ID')
_hduclass_card = ('HDUCLASS', 'OGIP', 'Format conform to OGIP standard')
_hpx_nsid_card = ('HPX_NSID', 8, 'HEALPIX nside')
_hpx_ordr_card = ('HPX_ORDR', 'RING', 'HEALPIX order scheme (RING or NEST)')
_instrume_card = ('INSTRUME', 'GSC', 'Instrument name (GSC, SSC_H or SSC_Z)')
_livetime_card = ('LIVETIME', 0.0, 'On-source time')
_mjd_obs_card = ('MJD-OBS', 0.0, 'MJD of data start time')
_networki_card = ('NETWORKI', '', 'Network interface (1553B/Ether)')
_nevents_card = ('NEVENTS', 0, 'Number of events')
_npixsou_card = ('NPIXSOU', 0, 'Number of pixels in selected region')
_numdetx_card = ('NUMDETX', 1, 'Num of DETX average sampling')
_numdety_card = ('NUMDETY', 1, 'Num of DETY average sampling')
_object_card = ('OBJECT', '', 'HEALPix tile number')
_observer_card = ('OBSERVER', 'MAXI Team', 'Principal Investigator')
_obs_id_card = ('OBS_ID', '', 'Observation ID')
_ontime_card = ('ONTIME', 0.0, 'Actual time')
_ra_nom_card = ('RA_NOM', 0.0, 'RA of the tile center [deg]')
_radius_i_card = ('RADIUS_I', 0.0, 'inner radius for event extraction [degree]')
_radius_o_card = ('RADIUS_O', 0.0, 'outer radius for event extraction [degree]')
_rmftype_card = ('RMFTYPE', 0, 'RMF type. 0:Slit Scan, 1:Pencil Beam, 2:LRF')
_seqpnum_card = ('SEQPNUM', 1, 'Number of the processing with this PROCVER')
_softver_card = ('SOFTVER', '', 'HEASOFT version')
_telapse_card = ('TELAPSE', 0.0, 'TSTOP-TSTART')
_timedel_card = ('TIMEDEL', 0.0, 'Smallest time increment')
_time_end_card = ('TIME-END', '', 'Stop time')
_time_obs_card = ('TIME-OBS', '', 'Start time')
_timezero_card = ('TIMEZERO', 0.0, 'Time Zero')
_user_card = ('USER', '', 'user name of the creator')

#----------------

class MaxiGscHeader(Header):

    def __setitem__(self, key, val):
        if not isinstance(key, tuple):
            if key.upper() == 'TSTART':
                time = Time(val, format='maxi')
                d, t = time.isot.split('T')
                self['DATE-OBS'] = d
                self['TIME-OBS'] = t
                self['MJD-OBS'] = time.mjd
            elif key.upper() == 'TSTOP':
                d, t = Time(val, format='maxi').isot.split('T')
                self['DATE-END'] = d
                self['TIME-END'] = t                
            else:
                pass
    
        super().__setitem__(key, val)


class PrimaryHeader(MaxiGscHeader):
    name = 'PRIMARY'
    keywords = [_telescope_card, _instrume_card, _gpcmoid_card, _datamode_card,
                _observer_card, _networki_card, _formver_card, _datatype_card,
                _dataform_card, _date_obs_card, _time_obs_card, _date_end_card,
                _time_end_card, _tstart_card, _tstop_card, _telapse_card,
                _ontime_card, _radecsys_card, _equinox_card, _mjdrefi_card,
                _mjdreff_card, _timeref_card, _timesys_card, _timeunit_card,
                _timedel_card, _object_card, _ra_nom_card, _dec_nom_card,
                _radius_i_card, _radius_o_card, _creator_card, _user_card, 
                _origin_card, _hpx_ordr_card, _hpx_nsid_card, _procver_card,
                _seqpnum_card, _softver_card, _caldbver_card, _nevents_card,
                _detnam_card, _exposure_card, _livetime_card, _mjd_obs_card,
                _timezero_card, _date_card]


class EventsHeader(MaxiGscHeader):
    name = 'EVENTS'
    keywords = [_extname_card, _hduclass_card, 
                ('HDUCLAS1', 'EVENTS', 'Event data'), _clockapp_card,
                _telescope_card, _instrume_card, _gpcmoid_card, _datamode_card,
                _observer_card, _networki_card, _formver_card, _datatype_card,
                _dataform_card, _date_obs_card, _time_obs_card, _date_end_card,
                _time_end_card, _tstart_card, _tstop_card, _telapse_card,
                _ontime_card, _radecsys_card, _equinox_card, _mjdrefi_card,
                _mjdreff_card, _timeref_card, _timesys_card, _timeunit_card,
                _timedel_card, _object_card, _ra_nom_card, _dec_nom_card, 
                _radius_i_card, _radius_o_card, _creator_card, _user_card,
                _origin_card, _hpx_ordr_card, _hpx_nsid_card, _procver_card,
                _seqpnum_card, _softver_card, _caldbver_card, _timezero_card,
                _detnam_card, _exposure_card, _livetime_card, _mjd_obs_card,
                _filin001_card, _npixsou_card, _obs_id_card, _date_card]


class GtiHeader(MaxiGscHeader):
    name = 'STDGTI'
    keywords = [_extname_card, _hduclass_card, 
                ('HDUCLAS1', 'GTI', 'File contains Good Time Intervals'),
                ('HDUCLAS2', 'STANDARD', 'File contains Good Time Intervals'),
                _telescope_card, _datamode_card, _detnam_card, _instrume_card, 
                _object_card, _ontime_card, _exposure_card, _livetime_card,
                _date_obs_card, _time_obs_card, _date_end_card, _time_end_card,
                _tstart_card, _tstop_card, _telapse_card, _mjd_obs_card,
                _mjdrefi_card, _mjdreff_card, _timeref_card, _timesys_card,
                _timeunit_card, _equinox_card, _radecsys_card, _user_card,
                _filin001_card, _creator_card, _origin_card,
                ('HDUNAME', 'STDGTI', 'ASCDM block name'),
                ('MTYPE1', 'TIME', 'Data type'),
                ('MFORM1', 'START,STOP', 'names of the start and stop columns'),
                ('METYP1', 'R', 'data descriptor type: Range, binned data'),
                _procver_card, _caldbver_card, _softver_card, _seqpnum_card,
                _obs_id_card, _clockapp_card, _gpcmoid_card, _observer_card,
                _networki_card, _formver_card, _datatype_card, _dataform_card,
                _timedel_card, _ra_nom_card, _dec_nom_card, _radius_i_card,
                _radius_o_card, _hpx_ordr_card, _hpx_nsid_card, _date_card]


class ArfPrimaryHeader(MaxiGscHeader):
    name = 'PRIMARY'
    keywords = []


class ArfHvbHeader(MaxiGscHeader):
    name = 'HVB'
    keywords = [_extname_card, _telescope_card, _instrume_card, _hduclass_card,
                ('HDUCLAS1', 'RESPONSE'), ('HDUCLAS2', 'SPECRESP'),
                ('HDUVERS', '1.1.0'), _origin_card, _creator_card, 
                ('VERSION', '', 'Version'), 
                ('CCLS0001', 'CPF', 'Calibration Product File'),
                ('CCNM0001', 'ARFCORR', 'Type of calibration data '),
                ('CDTP0001', 'DATA', 'real data, not subroutine '),
                ('CVSD0001', '', 'Validity start date'),
                ('CVST0001', '', 'Validity start time'),
                ('CDES0001', 'ARF for HVBIT()', 'Brief descriptive summary'),
                ('CBD10001', 'HVBIT()', 'HVBIT value')]

class ArfHvb803Header(ArfHvbHeader):
    name = 'HVB803'

class ArfHvb854Header(ArfHvbHeader):
    name = 'HVB854'


class RmfPrimaryHeader(MaxiGscHeader):
    name = 'PRIMARY'
    keywords = [_rmftype_card, _col_tha_card, _col_phi_card, _det_tha_card,
                _det_phi_card, _numdetx_card, _detxcntr_card, _detxmin_card,
                _detxmax_card, _numdety_card, _detycntr_card, _detymin_card,
                _detymax_card,
                ('CONTENT', 'RESPONSE', 'spectrum file contains time intervals and event'),
                _origin_card, _telescope_card, _instrume_card, _detnam_card,
                _date_card]


class RmfMatrixHeader(MaxiGscHeader):
    name = 'MATRIX'
    keywords = [_extname_card, _rmftype_card, _col_tha_card, _col_phi_card, 
                _det_tha_card, _det_phi_card, _numdetx_card, _detxcntr_card, 
                _detxmin_card, _detxmax_card, _numdety_card, _detycntr_card, 
                _detymin_card, _detymax_card, _telescope_card, _instrume_card,
                _detnam_card, _chantype_card, _detchans_card, _hduclass_card,
                ('HDUCLAS1', 'RESPONSE', 'Format conforms to OGIP/GSFC conventions'),
                ('HDUCLAS2', 'RSP_MATRIX', 'dataset is a spectral response matrix'),
                ('HDUVERS', '1.3.0', 'Version of format (OGIP memo CAL/GEN/92-002a)'),
                ('HDUCLAS3', 'DETECTOR', 'dataset is a spectral response matrix'),
                ('RMFVERSN', '1992a', 'OGIP classification of FITS format'),
                ('HDUVERS1', '1.1.0', 'Version of family of formats'),
                _date_card, ('VERSION', '1', 'Version'), _origin_card,
                ('CCLS0001', 'CPF', 'Calibration Product File'),
                ('CCNM0001', 'SPECRESP MATRIX', 'Type of calibration data'),
                ('CDTP0001', 'DATA', 'real data, not subroutine'),
                ('CVSD0001', '', 'Validity start date'),
                ('CVST0001', '', 'Validity start time'),
                ('CDES0001', 'MAXI/GSC Response Matrix', 'Brief descriptive summary'),
                ('CBD10001', 'HV()V', 'High Voltage value'),
                ('CBD20001', 'DETX()', 'DETX range'),
                ('CBD30001', 'ANODE()', 'ANODE number')]


class RmfEboundsHeader(MaxiGscHeader):
    name = 'EBOUNDS'
    keywords = [_extname_card, _rmftype_card, _col_tha_card, _col_phi_card, 
                _det_tha_card, _det_phi_card, _numdetx_card, _detxcntr_card, 
                _detxmin_card, _detxmax_card, _numdety_card, _detycntr_card, 
                _detymin_card, _detymax_card, _telescope_card, _instrume_card,
                _detnam_card, _chantype_card, _detchans_card, _hduclass_card,
                ('HDUCLAS1', 'RESPONSE', 'Format conforms to OGIP/GSFC conventions'),
                ('HDUCLAS2', 'EBOUNDS', 'dataset is a spectral response matrix'),
                ('HDUVERS', '1.2.0', 'Version of format (OGIP memo CAL/GEN/92-002a)'),
                ('HDUCLAS3', 'DETECTOR', 'dataset is a spectral response matrix'),
                ('RMFVERSN', '1992a', 'OGIP classification of FITS format'),
                ('HDUVERS1', '1.1.0', 'Version of family of formats'),
                _date_card, ('VERSION', '1', 'Version'), _origin_card,
                ('CCLS0001', 'CPF', 'Calibration Product File'),
                ('CCNM0001', 'EBOUNDS', 'Type of calibration data'),
                ('CDTP0001', 'DATA', 'real data, not subroutine'),
                ('CVSD0001', '', 'Validity start date'),
                ('CVST0001', '', 'Validity start time'),
                ('CDES0001', 'MAXI/GSC Response Matrix', 'Brief descriptive summary'),
                ('CBD10001', 'HV()V', 'High Voltage value'),
                ('CBD20001', 'DETX()', 'DETX range'),
                ('CBD30001', 'ANODE()', 'ANODE number')]
    

# -----------------------------------------------------------------------------

class EventsHeaders(FileHeaders):
    """FITS headers for event file"""
    _header_templates = [PrimaryHeader(), EventsHeader(), GtiHeader()]


class ArfHeaders(FileHeaders):
    """FITS headers for ARFs"""
    _header_templates = [ArfPrimaryHeader(), ArfHvb803Header(), ArfHvb854Header()]


class RmfHeaders(FileHeaders):
    """FITS headers for RMFs"""
    _header_templates = [RmfPrimaryHeader(), RmfMatrixHeader(), 
                         RmfEboundsHeader()]
    