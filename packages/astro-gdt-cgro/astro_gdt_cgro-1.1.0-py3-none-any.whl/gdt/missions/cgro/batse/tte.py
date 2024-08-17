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
import astropy.io.fits as fits

from gdt.core.data_primitives import Ebounds, Gti, EventList
from gdt.core.file import FitsFileContextManager
from gdt.core.tte import PhotonList

from .detectors import BatseDetectors
from .headers import PhaiiTriggerHeaders, TteTriggerHeaders
from .phaii import BatsePhaiiTrigger, BatseEnergyCalib
from ..time import *

__all__ = ['BatseTte', 'BatseTteMulti', 'BatseTteTrigger']

class BatseTte(PhotonList):
    """Class for BATSE Time-Tagged Event data.
    
    Note:
      The deadtime for BATSE TTE is assumed to be 3.3 microsec per event based
      on the analysis of Gjesteland et al. (2010).

    References:
        `Gjesteland, T. et al. 2010, Journal of Geophysical Research: Space 
         Physics, 115, A00E21
        <https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2009JA014578>`_
    """ 
    event_deadtime = 3.3e-6
    """Per event deadtime for non-overflow channels"""
    overflow_deadtime = 3.3e-6
    """Per event deadtime for overflow channels"""
    
    def __init__(self):
        super().__init__()
        self._ecalib = None
        self._detector = None

    @property
    def detector(self):
        """(:class:`BatseDetector`) or list: The BATSE detector(s)"""
        return self._detector

    @property
    def ecalib(self):
        """(:class:`BatseEnergyCalib`): Energy calibration data"""
        return self._ecalib

    @classmethod
    def from_data(cls, data, gti=None, trigger_time=None, filename=None,
                  headers=None, ecalib=None, detector=None, **kwargs):
        """Create a BATSE TTE object from data.
        
        Args:
            data (:class:`~.data_primitives.TimeEnergyBins`): The PHAII data
            gti (:class:`~.data_primitives.Gti`, optional): 
                The Good Time Intervals object. If omitted, the GTI spans 
                (tstart, tstop) 
            trigger_time (float, optional): 
                The trigger time, if applicable. If provided, the data times 
                will be shifted relative to the trigger time.
            filename (str, optional): The name of the file
            headers (:class:`~.headers.FileHeaders`): The file headers
            ecalib (:class:`BatseEnergyCalib`): The detector calibration
                 
        Returns:
            (:class:`BatseTte`)
        """
        obj = super().from_data(data, gti=gti, trigger_time=trigger_time, 
                                filename=filename, headers=headers, 
                                event_deadtime=cls.event_deadtime, 
                                overflow_deadtime=cls.overflow_deadtime)
        obj._ecalib = ecalib
        obj._detector = detector
        return obj

    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a BATSE TTE FITS file and return either a 
        :class:`BatseTteTrigger` or :class:`BatseTteMulti` object depending
        on the type of file.
        
        Args:
            file_path (str): The file path of the FITS file
        
        Returns:        
            (:class:`BatseTteTrigger` or :class:`BatseTteMulti`)
        """
        with fits.open(file_path) as f:
            if f[1].data['CAL_DET'].shape[0] > 1:
                return BatseTteMulti.open(file_path, **kwargs)
            else:
                return BatseTteTrigger.open(file_path, **kwargs)

    def slice_energy(self, energy_ranges):
        """Slice the BatseTte by one or more energy range. 
        Produces a new BatseTte object.
        
        Args:
            energy_ranges ([(float, float), ...]): 
                The energy ranges to slice the data to.

        Returns:
            (:class:`BatseTte`)
        """
        return super().slice_energy(energy_ranges=energy_ranges, 
                                  ecalib=self.ecalib, detector=self.detector)

    def slice_time(self, time_ranges):
        """Slice the BatseTte by one or more time range. Produces a new 
        BatseTte object.
        
        Args:
            time_ranges ([(float, float), ...]): 
                The time ranges to slice the data to.
        
        Returns:
            (:class:`BatseTte`)
        """
        return super().slice_time(time_ranges=time_ranges, ecalib=self.ecalib, 
                                  detector=self.detector)

    def to_phaii(self, bin_method, *args, time_range=None, energy_range=None,
                 channel_range=None, **kwargs):
        """Convert the TTE data to PHAII data by binning the data in 
        time.
        
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
            phaii_class (class): The Phaii subclass that the data will be 
                                 converted to.  Default is the base 
                                 :class:`~.phaii.Phaii` class.
            headers (:class:`~.headers.FileHeaders`, optional): 
                The PHAII headers 
            **kwargs: Options to pass to the binning function
        
        Returns:
            (:class:`~.phaii.BatsePhaiiTrigger`)
        """
        headers = PhaiiTriggerHeaders()

        # do not copy the value of these keys
        exceptions = ['MNEMONIC', 'DATATYPE', 'EXTNAME', 'FILE-ID', 'FILETYPE',
                      'HDUCLAS1']
        # copy over the key values for each header
        for i in range(self.headers.num_headers):
            for key, val in self.headers[i].items():
                if key in exceptions:
                    continue
                try:
                    headers[i][key] = val        
                except:
                    # header key is present in TTE but not in PHAII
                    pass
        
        headers[0]['FILETYPE'] = 'PHAII'
        headers[2]['DATATYPE'] = 'PHAII'
                
        obj = super().to_phaii(bin_method, *args, time_range=time_range, 
                               energy_range=energy_range, 
                               channel_range=channel_range, headers=headers,
                               phaii_class=BatsePhaiiTrigger, **kwargs)
        obj._detector = self.detector
        return obj
    
    def _build_hdulist(self):
        raise NotImplementedError
        # if trigtime is None, remove from headers
        if self.trigtime is None:
            self.headers['PRIMARY'].pop('TRIGTIME', None)
            self.headers['EBOUNDS'].pop('TRIGTIME', None)
            self.headers['EVENTS'].pop('TRIGTIME', None)
            self.headers['GTI'].pop('TRIGTIME', None)

        # create FITS and primary header
        hdulist = fits.HDUList()
        primary_hdu = fits.PrimaryHDU(header=self.headers['PRIMARY'])
        primary_hdu.header['TRIGTIME'] = self.trigtime
        hdulist.append(primary_hdu)
        
        # the ebounds extension
        ebounds_hdu = self._ebounds_table()
        hdulist.append(ebounds_hdu)
        
        # the events extension
        events_hdu = self._events_table()
        hdulist.append(events_hdu)        
        
        # the GTI extension
        gti_hdu = self._gti_table()
        hdulist.append(gti_hdu)
        
        return hdulist

    def _build_headers(self, trigtime, tstart, tstop, num_chans):

        headers = self.headers.copy()
        time_obj = Time(trigtime, format='cgro')

        trig_day, trig_secs = (None, None)
        if trigtime is not None:
            trig_day, trig_secs = to_day_time(time_obj)
            headers['PRIMARY']['TRIG-DAY'] = trig_day
            headers['PRIMARY']['TRIG-TIM'] = trig_secs
            tstart_obj = from_day_time(trig_day, tstart + trig_secs)
            tstop_obj = from_day_time(trig_day, tstop + trig_secs)
        else:
            tstart_obj = Time(tstart, format='cgro')
            tstop_obj = Time(tstop, format='cgro')
        
        start_day, start_secs = to_day_time(tstart_obj)
        stop_day, stop_secs = to_day_time(tstop_obj)

        headers['PRIMARY']['STRT-DAY'] = start_day
        headers['PRIMARY']['STRT-TIM'] = start_secs
        headers['PRIMARY']['END-DAY'] = stop_day
        headers['PRIMARY']['END-TIM'] = stop_secs
        
        headers['BATSE PHOTON LIST']['LO_CHAN'] = 0
        headers['BATSE PHOTON LIST']['UP_CHAN'] = num_chans-1
        
        return headers
    
    def _ecalib_table(self):
        raise NotImplementedError
        num_det = self.ecalib.num_det
        cal_det_col = fits.Column(name='CAL_DET', format='{}I'.format(num_det),
                                  array=self.ecalib.det)
        cal_strt_col = fits.Column(name='CAL_STRT', 
                                   format='{}D'.format(num_det), unit='TJD',
                                   array=self.ecalib.cal_start)
        cal_stop_col = fits.Column(name='CAL_STOP', 
                                   format='{}D'.format(num_det), unit='TJD', 
                                   array=self.ecalib.cal_start)
        
        e_edges = np.append(self.ebounds.low_edges(), self.ebounds.range[1])
        
        e_edges_col = fits.Column(name='E_EDGES', unit='keV',
                                  format='{}E'.format(e_edges.size),
                                 array=e_edges.reshape(self.ecalib.num_det, -1))
        width64_col = fits.Column(name='WIDTH64', format='{}I'.format(num_det), 
                                  array=self.ecalib.width64)
        line_nrg_col = fits.Column(name='LINE_NRG', format='4E', unit='keV',
                                   array=self.ecalib.line_energy)
        line_chan_col = fits.Column(name='LINECHAN', format='4E',
                                    array=self.ecalib.line_chan)
        det_s_zn_col = fits.Column(name='DET_S_ZN',
                                   format='{}E'.format(num_det), unit='deg',
                                   array=self.ecalib.det_s_zn)
        det_e_zn_col = fits.Column(name='DET_E_ZN', 
                                   format='{}E'.format(num_det), unit='deg',
                                   array=self.ecalib.det_e_zn)
        cal_name_col = fits.Column(name='CAL_NAME', format='16A',
                                   array=self.ecalib.cal_name)

        hdu = fits.BinTableHDU.from_columns([cal_det_col, cal_strt_col, 
                                             cal_stop_col, e_edges_col, 
                                             width64_col, line_nrg_col, 
                                             line_chan_col, det_s_zn_col,
                                             det_e_zn_col, cal_name_col], 
                                           header=self.headers['BATSE_E_CALIB'])
        for key, val in self.headers['BATSE_E_CALIB'].items():
            hdu.header[key] = val
        hdu.header.comments['TTYPE1'] = 'Detector number: use to index cal. data'
        hdu.header.comments['TTYPE2'] = 'Start time of the calibration record'
        hdu.header.comments['TUNIT2'] = 'Truncated Julian days'
        hdu.header.comments['TTYPE3'] = 'Stop time of the calibration record'
        hdu.header.comments['TUNIT3'] = 'Truncated Julian days'
        hdu.header.comments['TTYPE4'] = 'Energy edges for each selected detector'
        hdu.header.comments['TTYPE5'] = 'Integer value of Width64 (SDs only)'
        hdu.header.comments['TTYPE6'] = 'Centroid energy of 4 calibration lines'
        hdu.header.comments['TTYPE7'] = 'Centroid channel of 4 calibration lines'
        hdu.header.comments['TTYPE8'] = 'Zenith of the source in detector coords'
        hdu.header.comments['TTYPE9'] = 'Zenith of the Earth in detector coords'
        hdu.header.comments['TTYPE10'] = 'Name of the channel-to-energy scheme used'
        return hdu

    def _spectrum_table(self):
        raise NotImplementedError
        times = np.copy(self.data.times)
        times_col = fits.Column(name='TIMES', format='2E', unit='s',
                                array=times)
        rates_col = fits.Column(name='RATES', unit='count /s',
                                format='{}E'.format(self.num_chans),
                                array=self.data.rates)
        errors_col = fits.Column(name='ERRORS', unit='count /s',
                                 format='{}E'.format(self.num_chans),
                                 array=self.data.rate_uncertainty)        
        
        hdu = fits.BinTableHDU.from_columns([times_col, rates_col, errors_col], 
                                     header=self.headers['BATSE BURST SPECTRA'])

        for key, val in self.headers['BATSE BURST SPECTRA'].items():
            hdu.header[key] = val
        hdu.header.comments['TTYPE1'] = 'Array of rate start and stop times'
        hdu.header.comments['TUNIT1'] = 'Seconds since BSTST'
        hdu.header.comments['TTYPE2'] = 'N_Channel X N_Times array of rates'
        hdu.header.comments['TTYPE3'] = 'N_Channel X N_Times array of errors'
        return hdu


class BatseTteMulti(FitsFileContextManager):
    """BATSE data containing TTE from multiple detectors.
    """
    def __init__(self):
        super().__init__()
        self._data = []
        self._headers = []
        self._ecalib = None
        self._tstart = None
        self._tstop = None
        self._trigtime = None
        self._det_mask = None

    @property
    def detectors(self):
        """(list): The detectors in the file"""
        return self._ecalib.detectors

    @property
    def num_dets(self):
        """(int): Number of detectors in the file"""
        return self._ecalib.num_dets

    def get_detector(self, det_var):
        """Retrieve the Tte object for the given detector.
        
        Args:
            det_var (str, int, or :class:`BatseDetectors`)
        
        Returns:
            (:class:`BatseTteTrigger``)
        """
        if isinstance(det_var, BatseDetectors):
            num = det_var.number
        elif isinstance(det_var, str):
            num = BatseDetectors.from_str(det_var).number
        elif isinstance(det_var, int):
            num = det_var
        else:
            raise TypeError('det_var must be a str, int, or BatseDetectors ' \
                            'object')

        ecalib_det = self._ecalib.get_detector(num)
        e_edges = ecalib_det.edges_over_timespan(num, self._tstart.cgro, 
                                                 self._tstop.cgro)
        ebounds = Ebounds.from_bounds(e_edges[:-1], e_edges[1:])
        
        times = self._data['TIMES'][num]
        channels = self._data['CHANNELs'][num]
        if (times.size != self._data['N_PHOTON'][num]):
            raise RuntimeError('Incorrect number of expected photons.' \
                               'File may be corrupted.')
        
        channels = np.copy(channels) - self._headers['BATSE PHOTON LIST']['LO_CHAN']
        
        ev = EventList(times=times, channels=channels, ebounds=ebounds)
        ev.sort_time()
        
        gti = self._create_gti(num)
        
        fname_type, _, fname_id = self.filename.split('_')
        fname = f'{fname_type}_list_{num}_{fname_id}'
        
        return BatseTteTrigger.from_data(ev, gti=gti, headers=self._headers, 
                                         ecalib=ecalib_det, filename=fname, 
                                         trigger_time=self._trigtime.cgro,
                                         detector=BatseDetectors.from_num(num))
    
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a BATSE file containing TTE time series from multiple detectors.
        
        Args:
            file_path (str): The file path
        
        Returns:
            (:class:`BatseTteMulti`)
        """
        obj = super().open(file_path, **kwargs)
        
        hdrs = [hdu.header for hdu in obj.hdulist]
        try:
            headers = TteTriggerHeaders.from_headers(hdrs)
        except:
            raise RuntimeError('Unsupported filetype or not a TTE file.')
        
        obj._ecalib = BatseEnergyCalib.from_hdu(obj.hdulist[1].data)
        obj._data = obj.hdulist[2].data
        obj._headers = headers
                
        obj._tstart = from_day_time(headers[0]['STRT-DAY'], headers[0]['STRT-TIM'])
        obj._tstop = from_day_time(headers[0]['END-DAY'], headers[0]['END-TIM'])
        obj._trigtime = from_day_time(headers[0]['TRIG-DAY'], headers[0]['TRIG-TIM'])
        
        obj.close()
        return obj

    def sum_detectors(self, det_var_list=None):
        """Sum data over multiple detectors and return a Tte object.
        
        Note::
          The energy edges are taken to be the geometric mean.
        
        Args:
            det_var_list (list of str, int, or :class:`BatseDetectors`, optional)
                If not set, will sum all available detectors.
        
        Returns:
            (:class:`BatseTteTrigger``)
        """
        if det_var_list is None:
            det_var_list = self.detectors
        ttes = [self.get_detector(det_var) for det_var in det_var_list]
        num_ttes = len(ttes)
        
        times = ttes[0].data.times
        channels = ttes[0].data.channels
        gti = ttes[0].gti
        for i in range(1, num_ttes):
            times = np.concatenate([times, ttes[i].data.times])
            channels = np.concatenate([channels, ttes[i].data.channels])
            gti = Gti.merge(gti, ttes[i].gti)
                
        ecalibs = [tte.ecalib for tte in ttes]
        ecalib_sum = BatseEnergyCalib.combine_detectors(ecalibs)
        e_edges = ecalib_sum.edges_over_timespan(0, self._tstart.cgro, 
                                                    self._tstop.cgro)
        ebounds = Ebounds.from_bounds(e_edges[:-1], e_edges[1:])
        
        ev = EventList(times=times, channels=channels, ebounds=ebounds)
                
        fname_type, _, fname_id = self.filename.split('_')
        fname = f"{fname_type}_list_{fname_id}"
        
        dets = [tte.detector for tte in ttes]

        obj = BatseTteTrigger.from_data(ev, gti=gti, headers=ttes[0].headers,
                                        ecalib=ecalib_sum, filename=fname,
                                        trigger_time=self._trigtime.cgro,
                                        detector=dets)
                    
        return obj

    def _create_gti(self, det_num):
        """Create GTI for the given detector"""
        tstart = self._data['T_START'][det_num]
        tstart_mask = (tstart > -1e10)
        tstart = tstart[tstart_mask]
        
        tstop = self._data['T_STOP'][det_num]
        tstop_mask = (tstop > -1e10)
        tstop = tstop[tstop_mask]
        
        return Gti.from_bounds(tstart, tstop)
        
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.num_dets} detectors>'
        

class BatseTteTrigger(BatseTte):
    """Class representing trigger BATSE PHAII data.
    """    
    @classmethod
    def open(cls, file_path, **kwargs):
        raise NotImplementedError
