from ultralytics import YOLO


class TomatoDetector:


    def __init__(self,model_path):

        self.model=YOLO(model_path)



    def detect(self,frame):

        result=self.model(
            frame,
            conf=0.4,
            imgsz=1280
        )[0]


        detections=[]


        if result.boxes is None:
            return detections,result.plot(labels=False)


        boxes=result.boxes.xyxy.cpu().numpy()
        kps=result.keypoints.xy.cpu().numpy()



        for box,kp in zip(boxes,kps):

            detections.append(
                {
                    "box":box,
                    "stem":kp[0]
                }
            )


        return detections,result.plot(labels=False)