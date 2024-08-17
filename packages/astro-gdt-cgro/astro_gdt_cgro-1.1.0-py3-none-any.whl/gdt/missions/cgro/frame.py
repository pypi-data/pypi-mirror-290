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

from astropy.coordinates import FunctionTransform, ICRS, frame_transform_graph
import numpy as np
from scipy.spatial.transform import Rotation
from gdt.core.coords import SpacecraftFrame, Quaternion
from gdt.core.coords.quaternion import QuaternionAttribute
from gdt.core.coords.spacecraft.axes import SpacecraftAxesAttribute
from gdt.core.coords.spacecraft.frame import spacecraft_to_icrs, icrs_to_spacecraft

__all__ = ['CgroFrame', 'cgro_to_icrs', 'icrs_to_cgro']

class CgroFrame(SpacecraftFrame):
    """
    The CGRO spacecraft frame in azimuth and elevation.
    
    The frame is defined by orientation of the CGRO X and Z axes in the J2000
    frame.  The axis directions are used to convert to a quaternion, which is
    used by SpacecraftFrame to do the frame transforms.
    
    Example usage::
    
      from astropy.coordinates import SkyCoord
      from gdt.core.coords import SpacecraftAxes
      x_pointing = SkyCoord(19.090958, 8.04433, unit='deg')
      z_pointing = SkyCoord(108.162994, -6.5431795, unit='deg')
      axes = SpacecraftAxes(x_pointing=x_pointing, z_pointing=z_pointing) 
      frame = CgroFrame(axes=axes)

    """
    axes=SpacecraftAxesAttribute(default=None)
    quaternion = QuaternionAttribute(default=None)
    def __init__(self, *args, axes=None, quaternion=None, **kwargs):
        if axes is not None:
            
            x_pv = axes.pointing_vector('x')
            z_pv = axes.pointing_vector('z')
                      
            if x_pv.ndim == 1:
                x_pv = x_pv.reshape(3, 1)
                z_pv = z_pv.reshape(3, 1)
            
            # rotation between equatorial frame X axis and CGRO X pointing
            q1 = Quaternion.from_vectors(axes.x_vector[np.newaxis,:], x_pv.T).unit
            q1_arr = np.array([q1.x, q1.y, q1.z, q1.w])
            
            # apply X-axis rotation to equatorial frame Z axis
            z_vector = Rotation.from_quat(q1_arr.T).apply(axes.z_vector)

            # rotation between equatorial frame Z axis and CGRO Z pointing
            q2 = Quaternion.from_vectors(z_vector, z_pv.T)
            
            quaternion = (q2 * q1).unit
            
        super().__init__(*args, quaternion=quaternion, **kwargs)


@frame_transform_graph.transform(FunctionTransform, CgroFrame, ICRS)
def cgro_to_icrs(cgro_frame, icrs_frame):
    """Convert from the CGRO frame to the ICRS frame.
    
    Args:
        cgro_frame (:class:`CgroFrame`): The CGRO frame
        icrs_frame (:class:`astropy.coordinates.ICRS`)
    
    Returns:
        (:class:`astropy.coordinates.ICRS`)
    """
    return spacecraft_to_icrs(cgro_frame, icrs_frame)


@frame_transform_graph.transform(FunctionTransform, ICRS, CgroFrame)
def icrs_to_cgro(icrs_frame, cgro_frame):
    """Convert from the ICRS frame to the CGRO frame.
    
    Args:
        icrs_frame (:class:`astropy.coordinates.ICRS`)
        cgro_frame (:class:`CgroFrame`): The CGRO frame
    
    Returns:
        (:class:`CgroFrame`)
    """
    return icrs_to_spacecraft(icrs_frame, cgro_frame)

