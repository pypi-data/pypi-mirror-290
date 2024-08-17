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
from math import floor
from gdt.core.heasarc import BaseFinder
from ..time import *

__all__ = ['BatseTriggerFinder', 'BatseContinuousFinder']

class BatseFinder(BaseFinder):
    """Subclassing FtpFinder to enable _file_filter() to take a list of
    BATSE detectors.
    """    
    def _file_filter(self, file_list, filetype, extension, dets=None):
        """Filters the directory for the requested filetype, extension, and 
        detectors
        
        Args:
            filetype (str): The type of file, e.g. 'cont'
            extension (str): The file extension, e.g. '.fit'
            dets (list, optional): The detectors. If omitted, then files for 
                                   all detectors are returned

        Returns:
            (list): The filtered file list
        """
        files = super()._file_filter(file_list, filetype, extension)

        if dets is not None:
            if not isinstance(dets, (list, tuple)):
                dets = [dets]
            files = [f for f in files if
                     any(f'_{det}_' in f for det in dets) or 
                     any(f'_{det}.' in f for det in dets)]

        return files
    

class BatseTriggerFinder(BatseFinder):
    """A class that interfaces with the HEASARC FTP trigger directories.
    An instance of this class will represent the available files associated
    with a single trigger.
    
    An instance can be created without a trigger number, however a trigger
    number will need to be set by :meth:`cd(tnum) <cd>` to query and download files.
    An instance can also be changed from one trigger number to another without
    having to create a new instance.  If multiple instances are created and
    exist simultaneously, they will all use a single FTP connection.
    
    Parameters:
        tnum (str, optional): A valid trigger number
    
    Attributes:
        num_files (int): Number of files in the current directory
        files (list of str): The list of files in the current directory
    """
    _root = '/compton/data/batse/trigger'
    
    def _validate(self, tnum):
        tnum = '{:05d}'.format(int(tnum))
        return super()._validate(tnum)

    def get_cont(self, download_dir, dets=None, **kwargs):
        """Download the CONT files for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'cont_bfits', 'fits.gz', dets=dets)
        return self.get(download_dir, files, **kwargs)
    
    def get_discsc(self, download_dir, dets=None, **kwargs):
        """Download the combined LAD discriminator data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'discsc_bfits', 'fits.gz', 
                                  dets=dets)
        return self.get(download_dir, files, **kwargs)

    def get_discsp(self, download_dir, dets=None, **kwargs):
        """Download the spectroscopy detector discriminator data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'discsp_bfits', 'fits.gz', 
                                  dets=dets)
        return self.get(download_dir, files, **kwargs)
    
    def get_dsherb(self, download_dir, dets=None, **kwargs):
        """Download the spectroscopy high energy resolution data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'dsherb_bfits', 'fits.gz', 
                                  dets=dets)
        return self.get(download_dir, files, **kwargs)

    def get_drm(self, download_dir, drm_type='all', dets=None, **kwargs):
        """Download the detector response matrices for different data types.
        The valid data types, to be passed via `drm_type` are:
        
          'cont', 'discsc', 'discsp', 'dsherb', 'her', 'herb', 'mer', 'sher',
          'sherb', 'stte', 'tte'
        
        Args:
            download_dir (str): The download directory
            drm_type (str or list of str): The type(s) of DRMs to download. 
                                           Default is 'all', which downloads
                                           all DRMs.
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        _types = ['cont', 'discsc', 'discsp', 'dsherb', 'her', 'herb', 'mer',
                  'sher', 'sherb', 'stte_list', 'tte']
        
        if drm_type =='all':
            files = self._file_filter(self.files, '_drm', 'fits.gz', dets=dets)
        else:
            if isinstance(drm_type, str):
                drm_types = [drm_type]
            else:
                drm_types = drm_type
            files = []
            for drm_type in drm_types:
                if drm_type not in _types:
                    raise ValueError('{} is an invalid type.'.format(drm_type))
                f = self._file_filter(self.files, drm_type+'_drm', 'fits.gz', 
                                      dets=dets)
                if drm_type == 'her':
                    f = [i for i in f if i.startswith('h')]
                elif drm_type == 'herb':
                    f = [i for i in f if i.startswith('h')]
                elif drm_type == 'sherb':
                    f = [i for i in f if i.startswith('s')]
                else:
                    pass
                
                files.extend(f)
        
        return self.get(download_dir, files, **kwargs)

    def get_her(self, download_dir, dets=None, **kwargs):
        """Download the high energy resolution LAD data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'her_bfits', 'fits.gz', dets=dets)
        files = [file for file in files if file.startswith('h')]
        return self.get(download_dir, files, **kwargs)

    def get_herb(self, download_dir, dets=None, **kwargs):
        """Download the high energy resolution LAD data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'herb_bfits', 'fits.gz', dets=dets)
        files = [file for file in files if file.startswith('h')]
        return self.get(download_dir, files, **kwargs)

    def get_ibdb(self, download_dir, ibdb_type='all', **kwargs):
        """Download the IBDB (Individual Burst DataBase) files for different 
        data types. The valid data types, to be passed via `ibdb_type` are:
        
          'continuous', 'discla', 'discsc', 'discsp', 'her_cor', 'her', 'herb', 
          'info*', 'mer', 'preb', 'sher_cor', 'sher', 'sherb', 'stte', 'tte', 
          'tts'
        
        Args:
            download_dir (str): The download directory
            ibdb_type (str or list of str): The type(s) of IBDBs to download. 
                                            Default is 'all', which downloads
                                            all IBDBs for the trigger.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        _types = ['continuous', 'discla', 'discsc', 'discsp', 'her_cor', 'her', 
                  'herb', 'info', 'mer', 'preb', 'sher_cor', 'sher', 'sherb', 
                  'stte', 'tte', 'tts']
        
        if ibdb_type =='all':
            files = self._file_filter(self.files, '_ibdb', 'fits.gz')
        else:
            if isinstance(ibdb_type, str):
                ibdb_types = [ibdb_type]
            else:
                ibdb_types = ibdb_type
            files = []
            for ibdb_type in ibdb_types:
                if ibdb_type not in _types:
                    raise ValueError('{} is an invalid type.'.format(ibdb_type))
                if ibdb_type == 'info':
                    f = [f for f in \
                         self._file_filter(self.files, ibdb_type, 'fits.gz') \
                         if 'ibdb' in f]
                else:
                    f = self._file_filter(self.files, ibdb_type+'_ibdb', 
                                          'fits.gz')

                if ibdb_type == 'her':
                    f = [i for i in f if i.startswith('h')]
                elif ibdb_type == 'herb':
                    f = [i for i in f if i.startswith('h')]
                elif ibdb_type == 'sherb':
                    f = [i for i in f if i.startswith('s')]
                elif ibdb_type == 'tte':
                    f = [i for i in f if i.startswith('t')]
                else:
                    pass

                files.extend(f)
        
        return self.get(download_dir, files, **kwargs)

    def get_lightcurves(self, download_dir, **kwargs):
        """Download the lightcurve image files.
        
        Args:
            download_dir (str): The download directory
             verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, '', 'gif')
        return self.get(download_dir, files, **kwargs)
    
    def get_mer(self, download_dir, **kwargs):
        """Download the medium energy resolution data for the trigger.
        
        Args:
            download_dir (str): The download directory
             verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'mer_bfits', 'fits.gz')
        return self.get(download_dir, files, **kwargs)

    def get_sdisc(self, download_dir, dets=None, **kwargs):
        """Download the spectroscopy detector discriminator data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'sdisc_bfits', 'fits.gz', 
                                  dets=dets)
        return self.get(download_dir, files, **kwargs)

    def get_sher(self, download_dir, dets=None, **kwargs):
        """Download the high energy resolution SD data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'sher_bfits', 'fits.gz', dets=dets)
        return self.get(download_dir, files, **kwargs)

    def get_sherb(self, download_dir, dets=None, **kwargs):
        """Download the high energy resolution SD burst data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'sherb_bfits', 'fits.gz', dets=dets)
        files = [file for file in files if file.startswith('s')]
        return self.get(download_dir, files, **kwargs)

    def get_tte(self, download_dir, **kwargs):
        """Download the time-tagged event data for the trigger.
        
        Args:
            download_dir (str): The download directory
             verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'tte_bfits', 'fits.gz')
        return self.get(download_dir, files, **kwargs)

    def get_tts(self, download_dir, dets=None, **kwargs):
        """Download the time-to-spill data for the trigger.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'tts_bfits', 'fits.gz', dets=dets)
        return self.get(download_dir, files, **kwargs)

    def ls_cont(self):
        """List the continuous data for the trigger. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'cont_bfits', 'fits.gz')

    def ls_discsc(self):
        """List the combined LAD discriminator data for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'discsc_bfits', 'fits.gz')

    def ls_discsp(self):
        """List the spectroscopy detector discriminator data for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'discsp_bfits', 'fits.gz')

    def ls_dsherb(self):
        """List the spectroscopy high energy resolution data for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'dsherb_bfits', 'fits.gz')

    def ls_drm(self):
        """List the TTS data for the trigger. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '_drm', 'fits.gz')
    
    def ls_her(self):
        """List the high energy resolution LAD data for the trigger. 

        Returns:
            (list of str)
        """
        files = self._file_filter(self.files, 'her_bfits', 'fits.gz')
        return [file for file in files if file.startswith('h')]

    def ls_herb(self):
        """List the high energy resolution LAD data for the trigger.  

        Returns:
            (list of str)
        """
        files = self._file_filter(self.files, 'herb_bfits', 'fits.gz')
        return [file for file in files if file.startswith('h')]

    def ls_ibdb(self):
        """List the IBDB (Individual Burst DataBase) files for the trigger. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '_ibdb', 'fits.gz')
    
    def ls_lightcurve(self):
        """List all lightcurve plots for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '', 'gif')

    def ls_mer(self):
        """List the medium energy resolution data for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'mer_bfits', 'fits.gz')

    def ls_sdisc(self):
        """List the spectroscopy detector discriminator data for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'sdisc_bfits', 'fits.gz')

    def ls_sher(self):
        """List the high energy resolution SD data for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'sher_bfits', 'fits.gz')

    def ls_sherb(self):
        """List the SHERB data for the trigger.

        Returns:
            (list of str)
        """
        files = self._file_filter(self.files, 'sherb_bfits', 'fits.gz')
        return [f for f in files if f.startswith('s')]

    def ls_tte(self):
        """List the time-tagged event data for the trigger.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'tte_bfits', 'fits.gz')

    def ls_tts(self):
        """List the time-to-spill data for the trigger. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'tts_bfits', 'fits.gz')

    def _construct_path(self, str_trigger_num):
        """Constructs the FTP path for a trigger
        
        Args:
            str_trigger_num (str): The trigger number

        Returns:
            str: The path of the FTP directory for the trigger
        """
        # BATSE trigger numbers are separated into directories spanning 200
        # trigger numbers with 5 digit padding (e.g. 00001_00200; 00201_00400)
        beg = ( floor(float(str_trigger_num)/200.0) * 200 ) + 1
        end = beg + 199
        subdir = '{0:05d}_{1:05d}'.format(beg, end)
        
        path = os.path.join(self._root, subdir)
        try:
            trigger_dirs = self._protocol.ls(path, fullpath=True)
        except:
            raise FileExistsError
        
        the_path = ''
        for trigger_dir in trigger_dirs:
            if os.path.basename(trigger_dir).startswith(str_trigger_num):
                the_path = trigger_dir
                break
        
        if the_path == '':
            raise FileExistsError
                
        return the_path


class BatseContinuousFinder(BatseFinder):
    """A class that interfaces with the HEASARC FTP continuous daily data
    directories. An instance of this class will represent the available files 
    associated with a single day.
    
    An instance can be created without a time, however a time will need to be 
    set by :meth:`cd(time) <cd>` to query and download files. An instance can 
    also be changed from one time to another without having to create a new 
    instance.  If multiple instances are created and exist simultaneously, 
    they will all use a single FTP connection.
    
    Parameters:
        time (astropy.time.Time, optional): The time object
    """
    _root = '/compton/data/batse/daily'

    def cd(self, time):
        """Set the time. If the object was previously associated with a 
        different time, this will effectively change the working directory to 
        that of the new time. If the time is invalid, an exception will be 
        raised, and no directory change will be made.
        
        Args:
            time (astropy.time.Time, optional): The time object
        """
        super().cd(time)

    def get_cont(self, download_dir, **kwargs):
        """Download the LAD continuous data files.
        
        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self.ls_cont()
        return self.get(download_dir, files, **kwargs)

    def get_discla(self, download_dir, **kwargs):
        """Download the LAD discriminator files.
        
        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self.ls_discla()
        return self.get(download_dir, files, **kwargs)

    def get_her(self, download_dir, dets=None, **kwargs):
        """Download the LAD high energy resolution data.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'her', 'fits.gz', dets=dets)
        files = [f for f in files if f.startswith('h')]
        return self.get(download_dir, files, **kwargs)

    def get_sher(self, download_dir, dets=None, **kwargs):
        """Download the SD high energy resolution data.
        
        Args:
            download_dir (str): The download directory
            dets (list, optional): The detectors' data to download. 
                                   If omitted, will download all.
            verbose (bool, optional): If True, will output the download status. 
                                      Default is True.
        
        Returns:
            (list): The filenames of the downloaded files
        """
        files = self._file_filter(self.files, 'sher', 'fits.gz', dets=dets)
        return self.get(download_dir, files, **kwargs)

    def ls_cont(self):
        """List the LAD continuous data files.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'cont', 'fits.gz')

    def ls_discla(self):
        """List the  the LAD discriminator files.

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'discla', 'fits.gz')

    def ls_her(self):
        """List the LAD high energy resolution data. 

        Returns:
            (list of str)
        """
        files = self._file_filter(self.files, 'her', 'fits.gz')
        return [f for f in files if f.startswith('her')]

    def ls_sher(self):
        """List the SD high energy resolution data. 

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'sher', 'fits.gz')

    def _construct_path(self, met_obj):
        """Constructs the FTP path for a time.
        
        Args:
            met_obj (astropy.time.Time): The time object

        Returns:
            (str): The path of the FTP directory for the time
        """
        # BATSE daily data are separated into super directories spanning 1000 
        # units of TJD. Each super directory is then separated into 
        # directories spanning 100 units of TJD.  Each of those directories are
        # then divided into subdirectories, one for each TJD. 
        beg = ( floor(met_obj.cgro/1000.0) * 1000.0 ) + 1
        end = beg + 999
        subdir = '{0:05d}_{1:05d}'.format(int(beg), int(end))
        
        beg = ( floor(met_obj.cgro/100.0) * 100.0 ) + 1
        end = beg + 99
        # the first directory begins at 8361
        if beg < 8361:
            beg = 8361
        subsubdir = '{0:05d}_{1:05d}'.format(int(beg), int(end))
        
        daydir = 'dds{:05d}'.format(int(floor(met_obj.cgro)))
        
        path = os.path.join(self._root, subdir, subsubdir, daydir)
        
        return path
