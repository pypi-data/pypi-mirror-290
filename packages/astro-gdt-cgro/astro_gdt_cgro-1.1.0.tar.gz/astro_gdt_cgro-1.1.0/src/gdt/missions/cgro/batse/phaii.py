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
import numpy as np
import astropy.io.fits as fits
from astropy.coordinates import SkyCoord
import astropy.coordinates.representation as r

from gdt.core.coords import SpacecraftAxes
from gdt.core.coords.spacecraft import SpacecraftFrameModelMixin
from gdt.core.file import FitsFileContextManager
from gdt.core.phaii import Phaii
from gdt.core.data_primitives import Ebounds, Gti, TimeEnergyBins, TimeBins
from ..frame import *
from ..time import Time, from_day_time, to_day_time
from .detectors import BatseDetectors
from .headers import *


__all__ = ['BatsePhaii', 'BatsePhaiiMulti', 'BatsePhaiiCont', 
           'BatsePhaiiDiscla', 'BatsePhaiiTrigger', 'BatseEnergyCalib']

class BatseTimeEnergyBins(TimeEnergyBins):
    """Sub-class from gdt-core to add a tolerance in the calculating segments.
    Eventually this should be addressed in gdt-core.
    """
    def integrate_energy(self, emin=None, emax=None):
        temp = super().integrate_energy(emin=emin, emax=emax)
        return BatseTimeBins(temp.counts, temp.lo_edges, temp.hi_edges, 
                             temp.exposure)
        
    def _calculate_good_segments(self, lo_edges, hi_edges, tol=1e-4):
        """Calculates the ranges of data that are contiguous segments
        
        Args:
            lo_edges (np.array): The lower bin edges
            hi_edges (np.array): The upper bin edges
            tol (float, optional): A tolerance on matching bin edges. 
                                   Default is 1e-4 (0.1 ms)
        
        Returns:           
            ([(float, float), ...])
        """
        mask = np.abs(lo_edges[1:] - hi_edges[:-1]) > tol
        if mask.sum() == 0:
            return [(lo_edges[0], hi_edges[-1])]
        edges = np.concatenate(([lo_edges[0]], hi_edges[:-1][mask],
                                lo_edges[1:][mask], [hi_edges[-1]]))
        edges.sort()
        return edges.reshape(-1, 2).tolist()


class BatseTimeBins(TimeBins):
    """Sub-class from gdt-core to add a tolerance in the calculating segments.
    Eventually this should be addressed in gdt-core.
    """    
    def _calculate_good_segments(self, tol=1e-4):
        """Calculates the ranges of data that are contiguous segments
        
        Args:
            tol (float, optional): A tolerance on matching bin edges. Default is
                                   1e-4 (0.1 ms).

        Returns:
            ([(float, float), ...])
        """
        mask = np.abs(self.lo_edges[1:] - self.hi_edges[:-1]) > tol
        if mask.sum() == 0:
            return [self.range]
        times = np.concatenate(([self.lo_edges[0]], self.hi_edges[:-1][mask],
                                self.lo_edges[1:][mask], [self.hi_edges[-1]]))
        times.sort()
        return times.reshape(-1, 2).tolist()


class BatsePhaii(Phaii):
    """Class representing BATSE PHAII data.  This class reads either trigger
    files and returns a :class:`BatsePhaiiTrigger` object or a continuous
    data file containing data from multiple detectors and returns a 
    :class:`BatsePhaiiMulti` object.
    """
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
                  headers=None, ecalib=None, detector=None):
        """Create a BATSE PHAII object from data.
        
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
            detector (:class:`BatseDetectors` or list): The BATSE detector(s)
                 
        Returns:
            (:class:`BatsePhaii`)
        """
        obj = super().from_data(data, gti=gti, trigger_time=trigger_time, 
                                filename=filename, headers=headers)
        obj._ecalib = ecalib
        obj._detector = detector
        return obj

    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a BATSE PHAII FITS file and return either a 
        :class:`BatsePhaiiTrigger` or :class:`BatsePhaiiMulti` object depending
        on the type of file.
        
        Args:
            file_path (str): The file path of the FITS file
        
        Returns:        
            (:class:`BatsePhaiiTrigger` or :class:`BatsePhaiiMulti`)
        """
        fname = os.path.basename(file_path)
        if 'bfits' in fname:
            return BatsePhaiiTrigger.open(file_path, **kwargs)
        else:
            return BatsePhaiiMulti.open(file_path, **kwargs)

    def rebin_energy(self, method, *args, energy_range=(None, None)):
        """Rebin the PHAII in energy given a rebinning method. 
        Produces a new PHAII object.

        Args:
            method (<function>): The rebinning function
            *args: Arguments to be passed to the rebinning function
            energy_range ((float, float), optional): 
                The starting and ending energy to rebin.  If omitted, uses the 
                full range of data.  Setting start or end to ``None`` will use 
                the data from the beginning or end of the data, respectively.
        Returns        
            (:class:`BatsePhaii`)
        """
        return super().rebin_energy(method, *args, energy_range=energy_range, 
                                    ecalib=self.ecalib, detector=self.detector)

    def rebin_time(self, method, *args, time_range=(None, None)):
        """Rebin the PHAII in time given a rebinning method. 
        Produces a new PHAII object.
        
        Args:
            method (<function>): The rebinning function
            *args: Arguments to be passed to the rebinning function
            time_range ((float, float), optional): 
                The starting and ending time to rebin.  If omitted, uses the 
                full range of data.  Setting start or end to ``None`` will use 
                the data from the beginning or end of the data, respectively.
        Returns        
            (:class:`BatsePhaii`)
        """
        return super().rebin_time(method, *args, time_range=time_range, 
                                  ecalib=self.ecalib, detector=self.detector)

    def slice_energy(self, energy_ranges):
        """Slice the PHAII by one or more energy range. Produces a new 
        PHAII object.

        Args:
            energy_ranges ([(float, float), ...]): 
                The energy ranges to slice the data to.
        
        Returns:        
            (:class:`BatsePhaii`)
        """
        return super().slice_energy(energy_ranges=energy_ranges, 
                                  ecalib=self.ecalib, detector=self.detector)

    def slice_time(self, time_ranges):
        """Slice the PHAII by one or more time range. Produces a new 
        PHAII object. The GTI will be automatically update to match the new
        time range(s).

        Args:
            time_ranges ([(float, float), ...]): 
                The time ranges to slice the data to.
        
        Returns:        
            (:class:`BatsePhaii`)
        """
        return super().slice_time(time_ranges=time_ranges, ecalib=self.ecalib, 
                                  detector=self.detector)

    def _build_headers(self, trigtime, tstart, tstop, num_chans):
        
        headers = self.headers.copy()
        
        trig_day, trig_secs = (None, None)
        if trigtime is not None:
            time_obj = Time(trigtime, format='cgro')
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
        
        try:
            headers['BATSE BURST SPECTRA']['LO_CHAN'] = 0
            headers['BATSE BURST SPECTRA']['UP_CHAN'] = num_chans-1
        except:
            pass
                   
        return headers

    def _build_hdulist(self):
        raise NotImplementedError
        
        # create FITS and primary header
        hdulist = fits.HDUList()
        primary_hdu = fits.PrimaryHDU(header=self.headers['PRIMARY'])
        for key, val in self.headers['PRIMARY'].items():
            primary_hdu.header[key] = val
        hdulist.append(primary_hdu)
        
        # the ecalib extension
        ecalib_hdu = self._ecalib_table()
        hdulist.append(ecalib_hdu)
        
        # the spectrum extension
        spectrum_hdu = self._spectrum_table()
        hdulist.append(spectrum_hdu)        
        
        return hdulist
        
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

        tstart = np.copy(self.data.tstart)
        tstop = np.copy(self.data.tstop)
        times = np.vstack((tstart, tstop)).T
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


class BatsePhaiiMulti(FitsFileContextManager, SpacecraftFrameModelMixin):
    """BATSE data containing PHAII from multiple detectors.  This is typically
    either CONT or DISCLA data.  In addition to the PHAII data, these files
    also contain spacecraft orbit and attitude information.
    """
    def __init__(self):
        super().__init__()
        self._data = []
        self._headers = []
        self._filetype = None
        self._ecalib = None
        self._tstart = None
        self._tstop = None
        self._exposure = None
        self._frame = None

    @property
    def detectors(self):
        """(list): The detectors in the file"""
        return self._ecalib.detectors

    @property
    def num_dets(self):
        """(int): Number of detectors in the file"""
        return self._ecalib.num_dets
    
    def get_detector(self, det_var):
        """Retrieve the Phaii object for the given detector.
        
        Args:
            det_var (str, int, or :class:`BatseDetectors`)
        
        Returns:
            (:class:`BatsePhaii``)
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
        e_edges = ecalib_det.edges_over_timespan(num, self._tstart[0], 
                                                 self._tstop[-1])
        
        if self._filetype == 'cont':
        
            teb = BatseTimeEnergyBins(self._data['COUNTS'][:,:,num], 
                                      self._tstart, self._tstop, 
                                      self._exposure[:,num], 
                                      e_edges[:-1], e_edges[1:])

            return BatsePhaiiCont.from_data(teb, headers=self._headers, 
                                            ecalib=ecalib_det, 
                                            detector=BatseDetectors.from_num(num))
        
        elif self._filetype == 'discla':
            
            # in DISCLA, the first 4 channels are the discriminator channels,
            # channel 5 is the uncoincidenced total LAD rate (counts?), and the 
            # channel 6 is the total CPD rate (counts?)
            teb = BatseTimeEnergyBins(self._data['COUNTS'][:,:4,num], 
                                      self._tstart, self._tstop, 
                                      self._exposure[:,num], 
                                      e_edges[:-1], e_edges[1:])

            lad_lc = BatseTimeBins(self._data['COUNTS'][:,4,num], self._tstart, 
                                   self._tstop, self._exposure[:,num])
            
            cpd_lc = BatseTimeBins(self._data['COUNTS'][:,5,num], self._tstart, 
                                   self._tstop, self._exposure[:,num])
                    
            return BatsePhaiiDiscla.from_data(teb, headers=self._headers, 
                                              ecalib=ecalib_det, 
                                              detector=BatseDetectors.from_num(num),
                                              data_lad_tot=lad_lc, 
                                              data_cpd_tot=cpd_lc)
    
    def get_spacecraft_frame(self):
        """Retrieves the spacecraft frame(s) from the file.
        
        Returns:
            (:class:`CgroFrame`)
        """
        x_axis = SkyCoord(self._data['X_RA'], self._data['X_DEC'], unit='deg')
        z_axis = SkyCoord(self._data['Z_RA'], self._data['Z_DEC'], unit='deg')
        axes = SpacecraftAxes(x_pointing=x_axis, z_pointing=z_axis)
        sc_frame = CgroFrame(obstime=Time(self._data['MID_TIME'], format='cgro'),
                             obsgeoloc = r.CartesianRepresentation(
                                             x=self._data['X_POS'], 
                                             y=self._data['Y_POS'],
                                             z=self._data['Z_POS'], unit='km'),
                            axes=axes, detectors=BatseDetectors)
        return sc_frame

    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a BATSE file containing PHA time series from multiple detectors.
        
        Args:
            file_path (str): The file path
        
        Returns:
            (:class:`BatsePhaiiMulti`)
        """
        obj = super().open(file_path, **kwargs)
        
        hdrs = [hdu.header for hdu in obj.hdulist]
        if 'cont_' in obj.filename:
            try:
                headers = PhaiiContHeaders.from_headers(hdrs)
            except:
                try:
                    headers = PhaiiContHeadersAlt1.from_headers(hdrs)
                except:
                    headers = PhaiiContHeadersAlt2.from_headers(hdrs)
            filetype = 'cont'
        elif 'discla_' in obj.filename:
            try:
                headers = PhaiiDisclaHeaders.from_headers(hdrs)
            except:
                try:
                    headers = PhaiiDisclaHeadersAlt1.from_headers(hdrs)
                except:
                    headers = PhaiiDisclaHeadersAlt2.from_headers(hdrs)
            filetype = 'discla'
        else:
            raise RuntimeError('Unsupported filetype or not a PHAII file.')
        
        obj._ecalib = BatseEnergyCalib.from_hdu(obj.hdulist[1].data)
        obj._data = obj.hdulist[2].data
        obj._headers = headers
        obj._filetype = filetype

        if filetype == 'cont':
            obj._tstart = obj._data['MID_TIME'] - (1.024/86400.0)
            obj._tstop = obj._data['MID_TIME'] + (1.024/86400.0)
            obj._exposure = 2.048 - obj._data['DEADTIME']
        elif filetype == 'discla':
            obj._tstart = obj._data['MID_TIME'] - (0.512/86400.0)
            obj._tstop = obj._data['MID_TIME'] + (0.512/86400.0)
            obj._exposure = 1.024 - obj._data['DEADTIME']
        
        
        obj.close()
        return obj
        
    def sum_detectors(self, det_var_list=None):
        """Sum data over multiple detectors and return a Phaii object.
        
        Note::
          The exposures are averaged between multiple detectors and the 
          energy edges are taken to be the geometric mean.
        
        Args:
            det_var_list (list of str, int, or :class:`BatseDetectors`, optional)
                If not set, will sum all available detectors.
        
        Returns:
            (:class:`BatsePhaii``)
        """
        if det_var_list is None:
            det_var_list = self.detectors
        phaiis = [self.get_detector(det_var) for det_var in det_var_list]
        num_phaiis = len(phaiis)
        
        counts = np.copy(phaiis[0].data.counts)
        exposure = np.copy(phaiis[0].data.exposure)
        
        for i in range(1, num_phaiis):
            counts += phaiis[i].data.counts
            exposure += phaiis[i].data.exposure
        exposure /= num_phaiis

        ecalibs = [phaii.ecalib for phaii in phaiis]
        ecalib_sum = BatseEnergyCalib.combine_detectors(ecalibs)
        e_edges = ecalib_sum.edges_over_timespan(0, self._tstart[0], 
                                                    self._tstop[-1])
        
        data = BatseTimeEnergyBins(counts, phaiis[0].data.tstart, 
                                   phaiis[0].data.tstop, exposure, e_edges[:-1],
                                   e_edges[1:])
        
        dets = [phaii.detector for phaii in phaiis]
        
        if self._filetype == 'cont':
            obj = BatsePhaiiCont.from_data(data, headers=phaiis[0].headers,
                                           ecalib=ecalib_sum, detector=dets)
        elif self._filetype == 'discla':
            lad_lc = BatseTimeBins.sum([phaii.lad_lightcurve for phaii in phaiis])
            cpd_lc = BatseTimeBins.sum([phaii.cpd_lightcurve for phaii in phaiis])
            obj = BatsePhaiiDiscla.from_data(data, headers=phaiis[0].headers,
                                             ecalib=ecalib_sum, 
                                             detector=dets,
                                             data_lad_tot=lad_lc,
                                             data_cpd_tot=cpd_lc)
            
        return obj
    
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.num_dets} detectors>'
 

class BatsePhaiiCont(BatsePhaii):
    """The continuous CONT data."""
    pass


class BatsePhaiiDiscla(BatsePhaii):
    """The continuous LAD discriminator data."""
    
    def __init__(self):
        super().__init__()
        self._data_lad_tot = None
        self._data_cpd_tot = None
    
    @property
    def cpd_lightcurve(self):
        """(:class:`TimeBins`): The total charged particle detector lightcurve"""
        return self._data_cpd_tot
    
    @property
    def lad_lightcurve(self):
        """(:class:`TimeBins`): The total uncoincidenced lightcurve"""
        return self._data_lad_tot
    
    @classmethod
    def from_data(cls, data, gti=None, trigger_time=None, filename=None, 
                  headers=None, ecalib=None, detector=None, data_lad_tot=None, 
                  data_cpd_tot=None):
        """Create a PHAII object from data.
        
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
            detector (:class:`BatseDetectors` or list): The BATSE detector(s)
            ecalib (:class:`BatseEnergyCalib`): The detector calibration
            data_lad_tot (:class:`TimeBins`): The total uncoincidenced lightcurve
            data_cpd_tot (:class:`TimeBins`): The total charged particle detector
                                              lightcurve
                 
        Returns:
            (:class:`BatsePhaiiDiscla`)
        """
        obj = super().from_data(data, gti=gti, filename=filename, ecalib=ecalib,
                                headers=headers, detector=detector)
        obj._data_lad_tot = data_lad_tot
        obj._data_cpd_tot = data_cpd_tot
        return obj

    def rebin_energy(self, method, *args, energy_range=(None, None)):
        """Rebin the DISCLA in energy given a rebinning method. 
        Produces a new DISCLA object.

        Args:
            method (<function>): The rebinning function
            *args: Arguments to be passed to the rebinning function
            energy_range ((float, float), optional): 
                The starting and ending energy to rebin.  If omitted, uses the 
                full range of data.  Setting start or end to ``None`` will use 
                the data from the beginning or end of the data, respectively.
        Returns        
            (:class:`BatsePhaiiDiscla`)
        """
        obj = super().rebin_energy(method, *args, energy_range=energy_range)
        obj._data_lad_tot = self.lad_lightcurve
        obj._data_cpd_tot = self.cpd_lightcurve
        return obj

    def rebin_time(self, method, *args, time_range=(None, None)):
        """Rebin the DISCLA in time given a rebinning method. 
        Produces a new DISCLA object. This also rebins the associated 
        LAD and CPD lightcurve objects.
        
        Args:
            method (<function>): The rebinning function
            *args: Arguments to be passed to the rebinning function
            time_range ((float, float), optional): 
                The starting and ending time to rebin.  If omitted, uses the 
                full range of data.  Setting start or end to ``None`` will use 
                the data from the beginning or end of the data, respectively.
        Returns        
            (:class:`BatsePhaiiDiscla`)
        """
        obj = super().rebin_time(method, *args, time_range=time_range)
        
        cpd_lc = self.cpd_lightcurve.rebin(method, *args, tstart=time_range[0],
                                           tstop=time_range[1])
        obj._data_cpd_tot = cpd_lc
        lad_lc = self.lad_lightcurve.rebin(method, *args, tstart=time_range[0],
                                           tstop=time_range[1])
        obj._data_lad_tot = lad_lc
        
        return obj  

    def slice_energy(self, energy_ranges):
        """Slice the DISCLA by one or more energy range. Produces a new 
        DISCLA object.

        Args:
            energy_ranges ([(float, float), ...]): 
                The energy ranges to slice the data to.
        
        Returns:        
            (:class:`BatsePhaiiDiscla`)
        """
        obj = super().slice_energy(energy_ranges=energy_ranges)
        obj._data_lad_tot = self.lad_lightcurve
        obj._data_cpd_tot = self.cpd_lightcurve
        return obj

    def slice_time(self, time_ranges):
        """Slice the DISCLA by one or more time range. Produces a new 
        DISCLA object. The GTI will be automatically update to match the new
        time range(s). This also slices the associated LAD and CPD lightcurve 
        objects.

        Args:
            time_ranges ([(float, float), ...]): 
                The time ranges to slice the data to.
        
        Returns:        
            (:class:`BatsePhaiiDiscla`)
        """
        obj = super().slice_time(time_ranges=time_ranges)
        
        time_ranges = self._assert_range_list(time_ranges)
        
        cpd_lc = BatseTimeBins.merge([self.cpd_lightcurve.slice(*trange) \
                                      for trange in time_ranges])
        obj._data_cpd_tot = cpd_lc

        lad_lc = BatseTimeBins.merge([self.lad_lightcurve.slice(*trange) \
                                      for trange in time_ranges])
        obj._data_lad_tot = lad_lc
        
        return obj
        

class BatsePhaiiTrigger(BatsePhaii):
    """Class representing trigger BATSE PHAII data.
    """    
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a trigger BATSE PHAII FITS file.
        
        Args:
            file_path (str): The file path of the FITS file
        
        Returns:        
            (:class:`BatsePhaiiTrigger`)
        """
        obj = Phaii.open(file_path, **kwargs)
        hdrs = [hdu.header for hdu in obj.hdulist]
        if 'tts_bfits' in str(file_path):
            headers = PhaiiTriggerTtsHeaders.from_headers(hdrs)
        else:
            headers = PhaiiTriggerHeaders.from_headers(hdrs)
        
        trigtime = from_day_time(hdrs[0]['TRIG-DAY'], hdrs[0]['TRIG-TIM'])

        ecalib = BatseEnergyCalib.from_hdu(obj.hdulist[1].data)
        
        tstart, tstop = obj.column(2, 'TIMES').astype(np.float64).T
        tstart = tstart.astype(float)
        tstop = tstop.astype(float)
        rates = obj.column(2, 'RATES').astype(float)
        e_edges = ecalib.edges_over_timespan(ecalib.detectors[0], tstart[0],
                                             tstop[-1])
                
        #mark: FIXME exposures are not stored, so assume binwidths
        exposure = tstop - tstart
        if rates.ndim == 2:
            counts = rates * exposure[:,np.newaxis]
        else:
            counts = (rates * exposure).reshape(-1,1)
        
        teb = BatseTimeEnergyBins(counts, tstart, tstop, exposure, 
                                  e_edges[:-1], e_edges[1:])
        
        det = BatseDetectors.from_num(ecalib.detectors[0])
        obj.close()
        return cls.from_data(teb, trigger_time=trigtime.cgro, ecalib=ecalib,
                             headers=headers, filename=obj.filename, 
                             detector=det)
                

class BatseEnergyCalib():
    """BATSE Energy Calibration data, which is stored in PHAII and event list
    files.  There may be multiple detectors in the energy calibration, and there
    may be multiple calibrations with associated time ranges.
    
    This class is not intended to be instantiated by the user, but is rather 
    instantiated when reading a data file.
    """
    def __init__(self):
        self._data = None
    
    @property
    def detectors(self):
        """(list): The detectors in the calibration"""
        return [int(d) for d in list(set(self._data['CAL_DET']))]
    
    @property
    def num_dets(self):
        """(int): Number of detectors in the calibration"""
        return len(self.detectors)
    
    @property
    def num_times(self):
        """(int): Number of calibration times"""
        return int(self._data['CAL_DET'].size / self.num_dets)
    
    @classmethod
    def combine_detectors(cls, calib_list):
        """Combines the calibrations from different detectors.  This assumes the
        number of calibrations are the same and made at the same times between
        all of the detectors.  The output is a calibration with edges that are
        the geometric mean of the edges from the input detectors.
        
        Args:
            calib_list (list): List of :class:`BatseEnergyCalib`
        
        Returns:
            (:class:`BatseEnergyCalib`)
        """
        new_calib = np.copy(calib_list[0]._data)
        for calib in calib_list[1:]:
            new_calib['E_EDGES'] *= calib._data['E_EDGES']
        new_calib['E_EDGES'] = new_calib['E_EDGES'] ** (1.0/len(calib_list))
        
        return cls.from_hdu(new_calib)
    
    def edges_at_time(self, det, time):
        """The energy edges for a given detector at a given time.
        
        Args:
            det (int): The detector number
            time (float): The CGRO MET
        
        Returns:
            (np.array)
        """
        # find the closest time interval that has a calibration
        tidx = self._time_index(det, time)
        
        # mask the array for the detector
        mask = self._data['CAL_DET'] == det
        
        # retrieve the calibrated energy edges for detector and time
        e_edges = self._data['E_EDGES'][mask,:][tidx,:]
        return e_edges

    def edges_over_timespan(self, det, t0, t1):
        """The energy edges for a given detector covering a timespan.
        The timespan may cover multiple energy calibrations, so the energy
        calibrations are weighted by the amount of time spanned until the next
        calibration.
        
        Args:
            det (int): The detector number
            tstart (float): The start time in CGRO MET
            tstop (float): The stop time in CGRO MET
        
        Returns:
            (np.array)
        """
        tidx0 = self._time_index(det, t0)
        tidx1 = self._time_index(det, t1)
        tidx = np.arange(tidx0, tidx1+1)
        
        time_edges = self._time_edges(det)
        time_edges = time_edges[:,tidx]
        # if t0 is before the first calibration tstop, then extend/truncate
        if t0 <= time_edges[0,0]:
            time_edges[0,0] = t0
        # if t0 is after the first calibration
        else:
            time_edges[:,0] = [min(time_edges[1,0], t0), max(time_edges[1,0], t0)]
        # if t1 is after the last calibration tstart, then extend/truncate
        if t1 >= time_edges[1,-1]:
            time_edges[1,-1] = t1
        # if t1 is before the last calibration
        else:
            if tidx.size == 1:
                time_edges[1,0] = t1
            else:
                time_edges[:,-1] = [min(t1, time_edges[0,1]), max(t1, time_edges[0,1])]
        
        dt = time_edges[1,:] - time_edges[0,:]
        weights = dt / dt.sum()

        # mask the array for the detector
        mask = self._data['CAL_DET'] == det
        
        e_edges = np.zeros_like(self._data['E_EDGES'][0,:])
        for i in range(len(tidx)):
            e_edges += self._data['E_EDGES'][mask,:][tidx[i],:] * weights[i]
            
        return e_edges
    
    @classmethod
    def from_hdu(cls, hdu_data):
        """Create a :class:`BatseEnergyCalib` object from a FITS HDU data table
        
        Args:
            hdu_data (astropy.io.FITS_rec) The FITS data table
        
        Returns:
            (:class:`BatseEnergyCalib`)
        """
        obj = cls()
        obj._data = hdu_data
        return obj        

    def get_detector(self, det):
        """Return a new :class:`BatseEnergyCalib` containing only the requested
        detector calibration.
        
        Args:
            det (int): Detector number
        
        Returns:
            (:class:`BatseEnergyCalib`)
        """
        mask = self._data['CAL_DET'] == det
        return self.from_hdu(self._data[mask])
    
    def _time_edges(self, det):
        """Return the calibration time edges for a detector
        """
        # mask the array for the detector
        mask = self._data['CAL_DET'] == det
        time_edges = np.vstack([self._data['CAL_STRT'][mask],
                                self._data['CAL_STOP'][mask]])

        return time_edges
    
    def _time_index(self, det, time):
        """Retrieve the index into the calibration of the closest time interval.
        """
        time_edges = self._time_edges(det)
        
        # find the closest time interval that has a calibration
        idx0, idx1 = np.abs(time_edges - time).argmin(axis=1)
        if idx0 != idx1:
            idx_test = np.argmin([np.abs(time_edges[0,idx0] - time), 
                                  np.abs(time_edges[1,idx1] - time)])
            tidx = [idx0, idx1][idx_test]
        else:
            tidx = idx0
        
        return tidx   
    
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.num_times} calibrations>'
  
