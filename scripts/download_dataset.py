from roboflow import Roboflow

rf = Roboflow(api_key="Yc9P3iOmEuSts3mFZLd3")
PROJECT = rf.workspace().project("chess-4jvm8")
dataset = PROJECT.version(1).download("yolov8")