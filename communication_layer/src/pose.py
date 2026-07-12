import math


class PoseEstimator:


    def compute(self,geometry):


        vector=(
            geometry["direction3d"]
            -
            geometry["stem3d"]
        )


        X,Y,Z=geometry["center3d"]



        yaw=math.degrees(
            math.atan2(
                vector[0],
                vector[2]
            )
        )


        pitch=math.degrees(
            math.atan2(
                -vector[1],
                math.sqrt(
                    vector[0]**2+
                    vector[2]**2
                )
            )
        )



        return {

            "x":X,
            "y":Y,
            "z":Z,

            "yaw":yaw,
            "pitch":pitch,

            "diameter":
                geometry["diameter"]

        }