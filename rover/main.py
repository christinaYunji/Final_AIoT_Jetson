import sys
project_path = "/home/jetson/MyWorkspace/jetson_final"
sys.path.append(project_path)
import mqtt.Publisher_camera as pc

if __name__ == "__main__":

    publiser_camera = pc.Publisher_camera("192.168.3.105", 1883, "/camera")
    print("cam publisher created")
    publiser_camera.connect()
    while True:
        pass
