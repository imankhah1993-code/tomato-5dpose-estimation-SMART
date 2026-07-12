import numpy as np
import pyzed.sl as sl



def get_3d(pc,x,y):

    err,point=pc.get_value(
        int(x),
        int(y)
    )


    if err != sl.ERROR_CODE.SUCCESS:
        return None


    xyz=point[:3]


    if np.isnan(xyz).any():
        return None


    if np.isinf(xyz).any():
        return None


    return np.array(xyz)