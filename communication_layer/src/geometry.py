import numpy as np

from .utils import get_3d



class GeometryEstimator:



    def compute(self,detection,point_cloud):


        x1,y1,x2,y2=detection["box"]

        stem_x,stem_y=detection["stem"]



        cx=(x1+x2)/2
        cy=(y1+y2)/2



        dx=cx-stem_x
        dy=cy-stem_y


        distance=np.hypot(dx,dy)


        if distance==0:
            return None



        ux=dx/distance
        uy=dy/distance



        radius=min(
            x2-x1,
            y2-y1
        )/2



        center_x=stem_x+ux*radius
        center_y=stem_y+uy*radius



        stem3d=get_3d(
            point_cloud,
            stem_x,
            stem_y
        )


        center3d=get_3d(
            point_cloud,
            center_x,
            center_y
        )


        sphere3d=get_3d(
            point_cloud,
            cx,
            cy
        )


        if None in [
            stem3d,
            center3d,
            sphere3d
        ]:
            return None



        return {

            "stem3d":stem3d,
            "direction3d":center3d,
            "center3d":sphere3d,

            "diameter":radius*2,

            "stem2d":(
                int(stem_x),
                int(stem_y)
            ),

            "center2d":(
                int(center_x),
                int(center_y)
            )

        }