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

import astropy.units as u
from gdt.core.detector import Detectors

__all__ = ['BatseDetectors']

class BatseDetectors(Detectors):
    """The BATSE detector name and orientation definitions.    

    .. rubric:: Attributes Summary
    .. autosummary::

      azimuth
      elevation
      full_name
      number
      zenith

    .. rubric:: Methods Summary

    .. autosummary::
      
      from_full_name
      from_num
      from_str
      is_lad
      is_sd
      lad
      pointing
      sd
      skycoord
  
    .. rubric:: Attributes Documentation

    .. autoattribute:: azimuth
    .. autoattribute:: elevation
    .. autoattribute:: full_name
    .. autoattribute:: number
    .. autoattribute:: zenith

    .. rubric:: Methods Documentation

    .. automethod:: from_full_name
    .. automethod:: from_num
    .. automethod:: from_str
    .. automethod:: is_lad
    .. automethod:: is_sd
    .. automethod:: lad
    .. automethod:: pointing
    .. automethod:: sd
    .. automethod:: skycoord
    """
    LAD0 = ('LAD0', 0,  45.0 * u.deg, 35.26 * u.deg)
    LAD1 = ('LAD1', 1, 135.0 * u.deg, 35.26 * u.deg)
    LAD2 = ('LAD2', 2, 225.0 * u.deg, 35.26 * u.deg)
    LAD3 = ('LAD3', 3, 315.0 * u.deg, 35.26 * u.deg)
    LAD4 = ('LAD4', 4,  45.0 * u.deg, 144.73 * u.deg)
    LAD5 = ('LAD5', 5, 135.0 * u.deg, 144.73 * u.deg)
    LAD6 = ('LAD6', 6, 225.0 * u.deg, 144.73 * u.deg)
    LAD7 = ('LAD7', 7, 315.0 * u.deg, 144.73 * u.deg)
    
    # SD detectors are shifted toward the X-Y plane by 19 degrees relative to
    # the LAD detectors
    SD0 = ('SD0',  8,  45.0 * u.deg, 54.26 * u.deg)
    SD1 = ('SD1',  9, 135.0 * u.deg, 54.26 * u.deg)
    SD2 = ('SD2', 10, 225.0 * u.deg, 54.26 * u.deg)
    SD3 = ('SD3', 11, 315.0 * u.deg, 54.26 * u.deg)
    SD4 = ('SD4', 12,  45.0 * u.deg, 125.73 * u.deg)
    SD5 = ('SD5', 13, 135.0 * u.deg, 125.73 * u.deg)
    SD6 = ('SD6', 14, 225.0 * u.deg, 125.73 * u.deg)
    SD7 = ('SD7', 15, 315.0 * u.deg, 125.73 * u.deg)

    @classmethod
    def all_lads(cls):
        """Get all detectors that are Large Area Detectors (LADs).
        
        Returns:
            (list of :class:`Detector`): The LAD detectors
        """
        return [x for x in cls if x.is_lad()]

    @classmethod
    def all_sds(cls):
        """Get all detectors that are Spectroscopy Detectors (SDs).
    
        Returns:
            (list of :class:`Detector`): The SD detectors
        """
        return [x for x in cls if x.is_sd()]

    def is_lad(self):
        """Check if detector is a LAD.
    
        Returns:
            (bool): True if detector is LAD, False otherwise.
        """
        return self.name[0] == 'L'

    def is_sd(self):
        """Check if detector is a SD.
    
        Returns:
            (bool): True if detector is SD, False otherwise.
        """
        return self.name[0] == 'S'

