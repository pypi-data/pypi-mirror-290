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

from gdt.core import cache_path
from gdt.core.heasarc import BrowseCatalog

__all__ = ['BatseGrbCatalog', 'BatseGrb4bCatalog', 'BatseSpectralCatalog',
           'BatseBrightSpectralCatalog', 'BatseEarthOccultationCatalog',
           'BatsePulsarCatalog', 'BatseTriggerCatalog']

batse_cache_path = os.path.join(cache_path, 'batse')

class BatseGrbCatalog(BrowseCatalog):
    """The BATSE GRB trigger Catalog.
    """
    def __init__(self, cache_path=batse_cache_path, **kwargs):
        super().__init__(cache_path, table='batsegrb', **kwargs)

class BatseGrb4bCatalog(BrowseCatalog):
    """The BATSE 4B catalog of localizations and durations.
    """
    def __init__(self, cache_path=batse_cache_path, **kwargs):
        super().__init__(cache_path, table='batse4b', **kwargs)

class BatseSpectralCatalog(BrowseCatalog):
    """The BATSE 5B spectral catalog.
    """
    def __init__(self, cache_path=batse_cache_path, **kwargs):
        super().__init__(cache_path, table='bat5bgrbsp', **kwargs)

class BatseBrightSpectralCatalog(BrowseCatalog):
    """The BATSE time-resolved spectral catalog of bright GRBs.
    """
    def __init__(self, cache_path=batse_cache_path, **kwargs):
        super().__init__(cache_path, table='batsegrbsp', **kwargs)

class BatseEarthOccultationCatalog(BrowseCatalog):
    """The BATSE Earth Occultation Catalog of Low-Energy Gamma-ray Sources.
    """
    def __init__(self, cache_path=batse_cache_path, **kwargs):
        super().__init__(cache_path, table='batseeocat', **kwargs)

class BatsePulsarCatalog(BrowseCatalog):
    """The BATSE Pulsar Observations Catalog.
    """
    def __init__(self, cache_path=batse_cache_path, **kwargs):
        super().__init__(cache_path, table='batsepulsr', **kwargs)

class BatseTriggerCatalog(BrowseCatalog):
    """The BATSE Trigger Catalog.
    """
    def __init__(self, cache_path=batse_cache_path, **kwargs):
        super().__init__(cache_path, table='batsetrigs', **kwargs)

