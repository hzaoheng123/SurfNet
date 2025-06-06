"""
Preprocessing of the input cortical surfaces and brain MRI volumes.
The goal is to establish correspondence between the input surfaces and volumes.

To reduce the GPU memory cost, we clip the input MRI volume and
translate the surfaces accordingly.

For a new dataset, if the MRI is aligned to MNI-152 space 
and the ground truth is generated by FreeSurfer,
we recommend to set data_name='adni' with slight modification on the image clipping.

Note: it is tedious to tune the transformation of the surface to match the volume
for a new dataset, but the matching is important to make everything work.
"""


import numpy as np


def process_volume(x, data_name='hcp'):

    if data_name == 'hcp':
        x = x.transpose(1,2,0)
        x = x[::-1,:,:]
        x = x[:,:,::-1]
        return x[None, 32:-32, 16:-16, 32:-32].copy()
    elif data_name == 'adni':
        x = x.transpose(1,2,0)
        x = x[::-1,:,:]
        x = x[:,:,::-1]
        return x[None, ::].copy()
    elif data_name == 'dhcp':
        x = np.pad(x, ((2,2),(0,0),(0,0)), 'constant', constant_values=0)
        return x[None].copy()
    else:
        raise ValueError("data_name should be in ['hcp','adni','dhcp']")


def process_surface(v, f, data_name='hcp'):
    f = f.astype(np.float32)
    
    if data_name == 'hcp':
        v = v[:,[0,2,1]].copy()
        # clip the surface according to the volume
        v[:,0] = v[:,0] - 32
        v[:,1] = - v[:,1] - 15
        v[:,2] = v[:,2] - 32
        # normalize to [-1, 1]
        v = v + 128
        v = (v - [96, 112, 96]) / 112
    elif data_name == 'adni':       
        v=v/96

    elif data_name == 'dhcp':
        v = v[:,[2,1,0]].copy()
        f = f[:,[2,1,0]].copy()
        # normalize to [-1, 1]
        v = (v - [104, 104, 78]) / 104
    else:
        raise ValueError("data_name should be in ['hcp','adni','dhcp']")

    return v, f


def process_surface_inverse(v, f, data_name='hcp'):
    """
    inversed preprocessing to transform the surface to its original space
    """
    
    if data_name == 'hcp':
        v = v * 112 + [96, 112, 96]
        v = v - 128
        v[:,2] = v[:,2] + 32
        v[:,1] = v[:,1] + 15
        v[:,1] = - v[:,1]
        v[:,0] = v[:,0] + 32
        v = v[:,[0,2,1]].copy()

    elif data_name == 'adni':
        v = v *104 + [88, 104, 88]
        v = v - 128
        v[:,0] = v[:,0] + 40
        v[:,1] = v[:,1] + 24
        v[:,2] = v[:,2] + 40
        
    elif data_name == 'dhcp':
        v = v * 104 + [104, 104, 78]
        v = v[:,[2,1,0]].copy()
        f = f[:,[2,1,0]].copy()        
    else:
        raise ValueError("data_name should be in ['hcp','adni','dhcp']")

    return v, f

