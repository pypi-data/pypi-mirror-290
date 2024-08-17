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

from astropy.time.formats import TimeFromEpoch, Time
import datetime

__all__ = ['TimeCgroSec', 'Time', 'from_day_time', 'to_day_time']

class TimeCgroSec(TimeFromEpoch):
    """Truncated Julian Date + fraction of a day."""

    name = 'cgro'
    unit = 1.0  # day
    epoch_val = '1968-05-24 00:00:00'
    epoch_val2 = None
    epoch_scale = 'utc'  # Scale for epoch_val class attribute
    epoch_format = 'iso'  # Format for epoch_val class attribute


def from_day_time(yyyy_ddd, day_secs):
    """Create from day-of-year and seconds-of-day. This is a format
    often used in the BATSE FITS files.
    
    Args:
        yyyy_ddd (float): The day-of-year, where the integer part is the 
                          year, and the decimal part represents the day
                          of year.
        day_secs (float): Seconds of day
        
    Returns:
        (astropy.time.Time)
    """
    dt = datetime.datetime.strptime(str(yyyy_ddd), '%Y.%j')
    dt += datetime.timedelta(seconds=day_secs)
    return Time(dt)


def to_day_time(time_obj):
    """Convert an astropy time object to day-of-year and seconds-of-day BATSE
    format.  The day-of-year is in the form yyyy.ddd, where the integer part is
    the year, and the decimal part is the day of year.
    
    Args:
        time_obj (astropy.Time): The time object
        
    Returns:
        (float, float): (day-of-year and seconds-of-day)
    """
    dt = time_obj.datetime
    doy = dt.year + (dt.timetuple().tm_yday) / 1000
    num_secs = dt - dt.replace(hour=0, minute=0, second=0, microsecond=0)
    num_secs = num_secs.seconds + (num_secs.microseconds / 1e6)
    return (doy, num_secs)