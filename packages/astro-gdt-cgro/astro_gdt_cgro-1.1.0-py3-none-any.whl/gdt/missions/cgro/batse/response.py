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
from gdt.core.data_primitives import Ebounds, ResponseMatrix
from gdt.core.file import FitsFileContextManager
from .detectors import BatseDetectors
from .headers import RspHeaders, RspHeadersAlt
from ..time import *

__all__ = ['BatseRsp', 'BatseRspMulti']

class BatseRsp(Rsp):
    """Class for BATSE single-DRM response files
    """
    @classmethod
    def open(cls, file_path, **kwargs):
        """Read a single-DRM response file from disk.

        Args:
            file_path (str): The file path

        Returns:
            (:class:`BatseRsp`)
        """
        obj = super().open(file_path, **kwargs)
        
        hdrs = [hdu.header for hdu in obj.hdulist]
        try:
            headers = RspHeaders.from_headers(hdrs)
        except:
            headers = RspHeadersAlt.from_headers(hdrs)
        
        # check the detector number and make sure this is a single-detector file
        det_num = obj.column(1, 'DET_NUM')
        if det_num.size == 1:
            det_num = det_num[0]
        else:
            raise RuntimeError('This is a multi-detector response file. ' \
                               'Use BatseRspMulti to open this file, and then ' \
                               'select the detector you wish to use.')
        det = BatseDetectors.from_full_name(headers[0]['DET_MODE']+str(det_num))            
        
        
        tstart = from_day_time(hdrs[0]['STRT-DAY'], hdrs[0]['STRT-TIM']).cgro
        tstop = from_day_time(hdrs[0]['END-DAY'], hdrs[0]['END-TIM']).cgro
        try:
            trigtime = from_day_time(hdrs[0]['TRIG-DAY'], 
                                     hdrs[0]['TRIG-TIM']).cgro
        except:
            trigtime = None
                
        # ebounds
        eedges = obj.column(1, 'E_EDGES')[0]
        ebounds = Ebounds.from_bounds(eedges[:-1], eedges[1:])
        
        drm = obj._decompress(obj.hdulist[1].data, 0)
        
        obj.close()
        obj = cls.from_data(drm, filename=obj.filename, start_time=tstart, 
                            stop_time=tstop, trigger_time=trigtime, 
                            headers=headers, detector=det.name)
                
        return obj
    
    @staticmethod
    def _decompress(drm_data, index):
        """Decompresses a BATSE DRM.
        """
        mat_type = drm_data['MAT_TYPE']
        mat_type = mat_type[index]
        if mat_type == 1:
            matrix = drm_data['DRM_DIR'][index]
        elif mat_type == 2:
            matrix = drm_data['DRM_SCT'][index]
        elif mat_type == 3:
            matrix = drm_data['DRM_SUM'][index]
        
        n_zeros = drm_data['N_ZEROS'][index]
        num_ebins = drm_data['NUMEBINS'][index]
        num_chans = drm_data['NUMCHAN'][index]
        num_zeros = drm_data['NUMZERO'][index]
        
        sidx = 0
        drm = np.zeros((num_ebins-1, num_zeros))
        for ichan in range(num_zeros):
            eidx = sidx + (num_ebins-n_zeros[ichan])
            drm[n_zeros[ichan]-1:,ichan] = matrix[sidx:eidx]
            sidx = eidx

        chan_edges = drm_data['E_EDGES'][index]
        phot_edges = drm_data['PHT_EDGE'][index]
        matrix = ResponseMatrix(drm, phot_edges[:-1], phot_edges[1:],
                                chan_edges[:-1], chan_edges[1:])
        return matrix
        

class BatseRspMulti(FitsFileContextManager):
    """BATSE response file for multiple detectors.  This is typically DISCSC, 
    MER, STTE or TTE data.
    """
    def __init__(self):
        self._data = None
        self._headers = None
        self._dets = None
        self._tstart = None
        self._tstop = None
        self._trigtime = None
    
    @property
    def detectors(self):
        """(list): The detectors in the file"""
        return self._dets
        
    @property
    def num_dets(self):
        """(int): Number of detectors in the file"""
        return len(self._dets)
        
    def get_detector(self, det_var):
        """Retrieve the response object for the given detector.
        
        Args:
            det_var (str, int, or :class:`BatseDetectors`)
        
        Returns:
            (:class:`BatseRsp``)
        """
        if isinstance(det_var, BatseDetectors):
            name = det_var.name
        elif isinstance(det_var, str):
            name = det_var
        elif isinstance(det_var, int):
            name = BatseDetectors.from_num(det_var).name
        else:
            raise TypeError('det_var must be a str, int, or BatseDetectors ' \
                            'object')
        
        # index number of the detector into the DRM arrays
        try:
            idx = self.detectors.index(name)
        except ValueError:
            raise ValueError(f'The DRM for {det_var} is not contained in this file.')
        
        # ebounds
        eedges = self._data['E_EDGES'][idx]
        ebounds = Ebounds.from_bounds(eedges[:-1], eedges[1:])
        drm = BatseRsp._decompress(self._data, idx)
        
        # update the filename for the extracted response
        det_num = BatseDetectors.from_str(name).number
        fname = self.filename.split('_')
        fname = '_'.join(fname[:-1]) + f'_{det_num}_' + fname[-1]
        
        obj = BatseRsp.from_data(drm, start_time=self._tstart, filename=fname,
                                 stop_time=self._tstop, 
                                 trigger_time=self._trigtime, 
                                 headers=self._headers, detector=name)
                
        return obj
        
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a response file containing DRMs from multiple detectors.
        
        Args:
            file_path (str): The file path
        
        Returns:
            (:class:`BatseDrmMulti`)
        """
        obj = super().open(file_path, **kwargs)
        hdrs = [hdu.header for hdu in obj.hdulist]
        try:
            headers = RspHeaders.from_headers(hdrs)
        except:
            headers = RspHeadersAlt.from_headers(hdrs)
        
        det_mode = headers[0]['DET_MODE']
        obj._dets = [det_mode + str(num) for num in obj.column(1, 'DET_NUM')]
        obj._headers = headers
        
        obj._tstart = from_day_time(hdrs[0]['STRT-DAY'], hdrs[0]['STRT-TIM']).cgro
        obj._tstop = from_day_time(hdrs[0]['END-DAY'], hdrs[0]['END-TIM']).cgro
        try:
            obj._trigtime = from_day_time(hdrs[0]['TRIG-DAY'], 
                                          hdrs[0]['TRIG-TIM']).cgro
        except:
            pass

        obj._data = obj.hdulist[1].data
        obj.close()
        
        return obj

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.num_dets} detectors>'