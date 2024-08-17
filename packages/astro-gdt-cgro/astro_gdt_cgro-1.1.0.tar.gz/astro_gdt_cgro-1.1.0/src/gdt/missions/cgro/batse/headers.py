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

__all__ = ['PhaiiContHeaders', 'PhaiiContHeadersAlt1', 'PhaiiContHeadersAlt2',
           'PhaiiDisclaHeaders', 'PhaiiDisclaHeadersAlt1', 'PhaiiDisclaHeadersAlt2',
           'PhaiiTriggerHeaders', 'PhaiiTriggerTtsHeaders', 'TteTriggerHeaders',
           'RspHeaders', 'RspHeadersAlt']

# mission definitions
_telescope = 'COMPTON GRO'
_instrument = 'BATSE'
_observer = 'G. J. FISHMAN'
_origin = 'MSFC'
_equinox = 2000.0
_creator = Header.creator()[1]

# common keyword cards
_basetime_card = ('BASETIME', 0.0, 'Reference epoch, days past JD 2440000.5')
_batse_tr_card = ('BATSE_TR', 0, 'BATSE trigger number')
_bckgsubt_card = ('BCKGSUBT', False, 'Set to T if background was subtracted')
_bstacc_card = ('BSTACC', 0, 'Packets in a burst readout (DISCSC,HERB,SHERB)')
_datatype_card = ('DATATYPE', '', 'BATSE data types used')
_date_card = ('DATE', '', 'FITS file creation date (dd/mm/yy)')
_det_mode_card = ('DET_MODE', '', 'LAD or SD Detectors')
_dselect_card = ('DSELECT', '', 'Detectors summed in order [76543210]')
_end_day_card = ('END-DAY', 0.0, 'YYYY.DDD at end of data')
_end_tim_card = ('END-TIM', 0.0, 'seconds of day at end of data')
_equinox_card = ('EQUINOX', _equinox, 'J2000 coordinates')
_extname_card = ('EXTNAME', '', 'name of this binary table extension')
_file_id_card = ('FILE-ID', '', 'Name of FITS file')
_filetype_card = ('FILETYPE', '')
_file_ver_card = ('FILE-VER', '', 'Version of FITS file format')
_geoc_az_card = ('GEOC-AZ', 0.0, 'Geocenter Azimuth in GRO coords, degrees')
_geoc_el_card = ('GEOC-EL', 0.0, 'Geocenter Elevation in GRO coords, degrees')
_instrument_card = ('INSTRUME', _instrument)
_is_error_card = ('IS_ERROR', True, 'Set to T if ERRORS field is not empty')
_is_spec_card = ('IS_SPEC', True, 'Set to T if RATES field is not empty')
_lochan_card = ('LO_CHAN', 0, 'Lower channel')
_ltimecor_card = ('LTIMECOR', True, 'Set to T if deadtime correction was used')
_mnemonic_card = ('MNEMONIC', _creator, 'Program creating this file')
_objctdec_card = ('OBJCTDEC', 0.0, 'J2000 DEC of source, degrees')
_objctra_card = ('OBJCTRA', 0.0, 'J2000 RA of source, degrees')
_object_card = ('OBJECT', '')
_observer_card = ('OBSERVER', _observer, 'Principal investigator (256) 544-7691')
_origin_card = ('ORIGIN', _origin, 'Tape writing institution')
_overflw_card = ('OVERFLW', False, 'Set to T if HER_COR or SHER_COR was used')
_r_exp_card = ('R_EXP', 0.0, 'Power-law exponent of resolution model (LADs)')
_rf_511_card = ('RF_511', 0.0, 'Resolution fraction at 511 keV (LADs)')
_sc_x_dec_card = ('SC-X-DEC', 0.0, 'X axis Dec in degrees')
_sc_x_pos_card = ('SC-X-POS', 0.0, 'Spacecraft position at time of trigger (km)')
_sc_x_ra_card = ('SC-X-RA', 0.0, 'X axis RA in degrees')
_sc_y_pos_card = ('SC-Y-POS', 0.0)
_sc_z_dec_card = ('SC-Z-DEC', 0.0, 'Z axis Dec in degrees')
_sc_z_pos_card = ('SC-Z-POS', 0.0)
_sc_z_ra_card = ('SC-Z-RA', 0.0, 'Z axis RA in degrees')
_srce_az_card = ('SRCE-AZ', 0.0, 'Source Azimuth in GRO coords, degrees')
_srce_el_card = ('SRCE-EL', 0.0, 'Source Elevation in GRO coords, degrees')
_strt_day_card = ('STRT-DAY', 0.0, 'YYYY.DDD at start of data')
_strt_tim_card = ('STRT-TIM', 0.0, 'seconds of day at start of data')
_telescope_card = ('TELESCOP', _telescope)
_tjd_card = ('TJD', 0, 'TJD at start of data')
_trig_day_card = ('TRIG-DAY', 0.0, 'YYYY.DDD at burst trigger')
_trig_tim_card = ('TRIG-TIM', 0.0, 'seconds of day at burst trigger ')
_upchan_card = ('UP_CHAN', 0, 'Upper channel')


#----------------

class PrimaryHeader(Header):
    name = 'PRIMARY'
    keywords = [_telescope_card, _instrument_card, _origin_card, _filetype_card,
                _observer_card, _tjd_card, _strt_day_card, _strt_tim_card, 
                _end_day_card, _end_tim_card, 
                ('N_E_CHAN', 0, 'number of energy channels'),
                ('TIME_RES', 0.0, 'Time resolution of data (second)'),
                _equinox_card, _sc_z_ra_card, _sc_z_dec_card, _sc_x_ra_card, 
                _sc_x_dec_card,
                ('SC-Z-LII', 0.0, 'Z axis Galactic coordinate LII in degr'),
                ('SC-Z-BII', 0.0, 'Z axis Galactic coordinate BII in degr'),
                ('SC-X-LII', 0.0, 'X axis Galactic coordinate LII in degr'),
                ('SC-X-BII', 0.0, 'X axis Galactic coordinate BII in degr'),
                ('QMASKDAT', '', 'mask used for data filtering'),
                ('QMASKHKG', '', 'mask used for housekeeping data filtering'),
                _file_id_card, _file_ver_card, 
                ('FILENAME', '', 'Original File'),
                ('CDATE', '', 'Date FITS file created'), _mnemonic_card, 
                ('PRIMTYPE', 'NONE', 'No primary array')]


class PrimaryHeaderAlt(PrimaryHeader):
    keywords = [] + PrimaryHeader.keywords
    keywords[-3] = ('DATE', '', 'Date FITS file created') 
    

class PrimaryTriggerHeader(Header):
    name = 'PRIMARY'
    keywords = [('COMMENT', 'FITS (Flexible Image Transport System) format ' \
                            'defined in Astronomy and'),
                ('COMMENT', 'Astrophysics Supplement Series v44/p363, ' \
                            'v44/p371, v73/p359, v73/p365.'),
                ('COMMENT', 'Contact the NASA Science Office of Standards ' \
                            'and Technology for the'),
                ('COMMENT', 'FITS Definition document #100 and other FITS ' \
                            'information.'),
                _telescope_card, _instrument_card, _origin_card,_filetype_card,
                _object_card, _batse_tr_card, _observer_card, _strt_day_card,
                _strt_tim_card, _end_day_card, _end_tim_card, _trig_day_card,
                _trig_tim_card, _equinox_card, _sc_z_ra_card, _sc_z_dec_card,
                _sc_x_ra_card, _sc_x_dec_card, _objctra_card, _objctdec_card,
                _sc_x_pos_card, _sc_y_pos_card, _sc_z_pos_card, _srce_az_card,
                _srce_el_card, _geoc_az_card, _geoc_el_card, _file_id_card,
                _file_ver_card, _date_card, _mnemonic_card,
                ('COMMENT', 
                 'This file contains BATSE time-sequenced spectral data'),
                 ('PRIMTYPE', 'NONE', 'No primary array')]


class PrimaryRspHeader(Header):
    name = 'PRIMARY'
    keywords = [_telescope_card, _instrument_card, _origin_card, _filetype_card,
                _object_card, _strt_day_card, _strt_tim_card, _end_day_card, 
                _end_tim_card, _trig_day_card, _trig_tim_card, _sc_z_ra_card, 
                _sc_z_dec_card, _sc_x_ra_card, _sc_x_dec_card, _objctra_card, 
                _objctdec_card, _sc_x_pos_card, _sc_y_pos_card, _sc_z_pos_card,
                _det_mode_card, 
                ('ALPHA', 0.0, 'Weighting Across Input Bins for Direct Matrix'),
                ('N_E_CHAN', 0, 'Number of Energy Channels (4 or 16)'),
                ('N_E_BINS', 0, 'Number of Input Energy Bins'), _equinox_card,
                _file_id_card, _file_ver_card, 
                ('FILENAME', ''),
                ('DEF_NML', '', 'Default namelist used for input data'),
                ('USR_NML', '', 'User override namelist for input data'),
                _date_card, _mnemonic_card, 
                ('PRIMTYPE', 'NONE', 'No primary array')]
                

class EcalibHeader(Header):
    name = 'BATSE_E_CALIB'
    keywords = [_extname_card]


class EcalibTriggerHeader(Header):
    name = 'BATSE_E_CALIB'
    keywords = [_extname_card,
                ('COMMENT', 
                 'The energy calibration table contains the energy thresholds'),
                ('COMMENT', 
                 'computed for each DSELECT detector. There are NAXIS2 rows'),
                ('COMMENT', 
                 'of data in the table - one for each detector selected')]


class BatseCountsHeader(Header):
    name = 'BATSE_CNTS'
    keywords = [_extname_card,
      ('COMMENT', 'The following is a summary of the condition code bits in FLAGS'),
      ('COMMENT', ' BYTE 1:'),
      ('COMMENT', '   BIT 0:  DISCLA overflow in some detectors(s)'),
      ('COMMENT', '       1:  GRO reorientation in progress'),
      ('COMMENT', '       2:  LAD gains out of balance'),
      ('COMMENT', '       3:  Background variation on timescales < 32 sec in some LAD(s)'),
      ('COMMENT', '       4:  Background variation on timescales > 32 sec in some LAD(s)'),
      ('COMMENT', '       5:  1Kbit telemetry data'),
      ('COMMENT', '     6-15:  Spare'),
      ('COMMENT', ' BYTE 2: Spare'),
      ('COMMENT', ' BYTE 3: BIT i: Background variation on timescales < 32 sec in LAD i'),
      ('COMMENT', ' BYTE 4: BIT i: Background variation on timescales > 32 sec in LAD i') ]


class BatseContCountsHeader(BatseCountsHeader):
    keywords = [('COMMENT', ' COUNTS(i,j) contains the counts in detector i (0 to 7) for channel j'),
                ('COMMENT', '(0 to 15).')] + BatseCountsHeader.keywords


class BatseDisclaCountsHeader(BatseCountsHeader):
    keywords = [('COMMENT', ' COUNTS(i,j) contains the counts in detector i (0 to 7) for channel j'),
      ('COMMENT', '(1 to 6). Channel 1 to 4 are 4 differential energy channels of'),
      ('COMMENT', 'charge particle anticoincidenced discriminator rates in the LADS.'),
      ('COMMENT', 'Channel 5 is the uncoincidenced total LAD rate. Channel 6 is the'),
      ('COMMENT', 'total charge particle detector rate.')] + BatseCountsHeader.keywords


class RunLogHeader(Header):
    name = 'RUN_LOG'
    keywords = [_extname_card, ('COMMENT', 'CONT_DISCLA_FITS LOG FILE')]
    keywords.extend([('COMMENT', '')]*11)


class BurstSpectraHeader(Header):
    name = 'BATSE BURST SPECTRA'
    keywords = [_extname_card, _dselect_card, _lochan_card, _upchan_card,
                _rf_511_card, _r_exp_card, _det_mode_card, _datatype_card,
                _is_spec_card, _is_error_card, _overflw_card, _ltimecor_card,
                _bckgsubt_card, _bstacc_card,
                ('COMMENT', 
                 'Bad or missing data indicated by IEEE NAN in Rate errors.'),
                _basetime_card,
                ('NOTE', 'Burst number:   {}'),
                ('NOTE', 'Detectors:  {}'),
                ('NOTE', 'Data types: {}'),
                ('NOTE', 'Start day:  {}'),
                ('NOTE', 'Start sec:  {}'),
                ('NOTE', 'Min. Resolution (s):   {}'),
                ('NOTE', 'Creation time: {}')]


class BurstSpectraTtsHeader(BurstSpectraHeader):
     keywords = BurstSpectraHeader.keywords[:14] +  \
                [('COR_TTS', True), ('MAXTTSER', 0.0), ('TOTTTSER', 0.0)] + \
                BurstSpectraHeader.keywords[14:]


class PhotonListHeader(Header):
    name = 'BATSE PHOTON LIST'
    keywords = BurstSpectraHeader.keywords


class DrmHeader(Header):
    name = 'BATSEDRM'
    keywords = [('EXTTYPE', 'BATSEDRM'),
        ('COMMENT', 'THE DETECTOR RESPONSE MATRIX IS STORED IN A COMPRESSED FORMAT:'),
        ('COMMENT', 'ELEMENTS ARE LISTED IN ORDER OF ROW BY COLUMN (N_E_BIN BY N_E_CHAN),'),
        ('COMMENT', 'WITH ALL ELEMENTS EQUAL TO 0 AT THE TOP OF THE COLUMN OMMITED. THE'),
        ('COMMENT', 'ROW INDEX OF THE FIRST NON-ZERO ELEMENT FOR EACH COLUMN IS GIVEN'),
        ('COMMENT', 'BY N_ZEROS.'),
        ('COMMENT', 'THUS, FOR THE ITH COLUMN: INSERT N_ZEROS(I) - 1 0S, FOLLOWED BY THE'),
        ('COMMENT', 'NEXT N_E_BIN - N_ZEROS(I) + 1 ELEMENTS OF THE DRM (EITHER DRM_DIR,'),
        ('COMMENT', 'DRM_SCT OR DRM_SUM).  THE LAST COLUMN SHOULD EXHAUST THE ELEMENTS OF'),
        ('COMMENT', 'THE COMPRESSED DRM.')
    ]


class DrmHeaderAlt(DrmHeader):
    keywords = [('EXTTYPE', 'BATSEDRM'),
        ('COMMENT', 'THE DETECTOR RESPONSE MATRIX IS STORED IN A COMPRESSED FORMAT'),
        ('COMMENT', 'ELEMENTS ARE LISTED IN COLUMS BY COLUMN (CHANNEL BY CHANNEL)'),
        ('COMMENT', 'WITH 0 ELEMENTS AT THE TOP OF THE COLUMN OMMITED. THE NUMBER 0'),
        ('COMMENT', 'ELEMENTS FOR EACH COLUMN IS GIVEN AT THE TOP OF EACH COLUMN IS'),
        ('COMMENT', 'GIVER BY NUM_ZERO_TOP')
    ]

# -----------------------------------------------------------------------------

class PhaiiContHeaders(FileHeaders):
    """FITS Headers for non-trigger CONT data."""
    _header_templates = [PrimaryHeader(), EcalibHeader(), BatseContCountsHeader()]


class PhaiiContHeadersAlt1(FileHeaders):
    """Alternate FITS headers for non-trigger CONT data."""
    _header_templates = [PrimaryHeaderAlt(), EcalibHeader(), 
                         BatseContCountsHeader(), RunLogHeader()]


class PhaiiContHeadersAlt2(FileHeaders):
    """Alternate FITS headers for non-trigger CONT data."""
    _header_templates = [PrimaryHeaderAlt(), EcalibHeader(), 
                         BatseContCountsHeader()]
    

class PhaiiDisclaHeaders(FileHeaders):
    """FITS Headers for non-trigger LAD discriminator data."""
    _header_templates = [PrimaryHeader(), EcalibHeader(), BatseDisclaCountsHeader()]


class PhaiiDisclaHeadersAlt1(FileHeaders):
    """Alternate FITS headers for non-trigger LAD discriminator data."""
    _header_templates = [PrimaryHeaderAlt(), EcalibHeader(), 
                         BatseDisclaCountsHeader(), RunLogHeader()]


class PhaiiDisclaHeadersAlt2(FileHeaders):
    """Alternate FITS headers for non-trigger LAD discriminator data."""
    _header_templates = [PrimaryHeaderAlt(), EcalibHeader(), 
                         BatseDisclaCountsHeader()]


class PhaiiTriggerHeaders(FileHeaders):
    """FITS Headers for trigger PHAII data."""
    _header_templates = [PrimaryTriggerHeader(), EcalibTriggerHeader(), 
                         BurstSpectraHeader()]


class PhaiiTriggerTtsHeaders(FileHeaders):
    """FITS Headers for trigger TTS data."""
    _header_templates = [PrimaryTriggerHeader(), EcalibTriggerHeader(), 
                         BurstSpectraTtsHeader()]


class TteTriggerHeaders(FileHeaders):
    """FITS Headers for trigger TTE data."""
    _header_templates = [PrimaryTriggerHeader(), EcalibTriggerHeader(), 
                         PhotonListHeader()]


class RspHeaders(FileHeaders):
    """FITS Headers for BATSE DRM files."""
    _header_templates = [PrimaryRspHeader(), DrmHeader()]


class RspHeadersAlt(FileHeaders):
    """Alternate FITS headers for BATSE DRM files."""
    _header_templates = [PrimaryRspHeader(), DrmHeaderAlt()]