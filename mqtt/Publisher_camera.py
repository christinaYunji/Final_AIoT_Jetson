import threading
import cv2
import base64
import paho.mqtt.client as mqtt
import sys

project_path = "/home/jetson/MyWorkspace/jetson_final"
sys.path.append(project_path)

#v = cv2.VideoCapture(0)
class Publisher_camera:
    def __init__(self, brokerIp, brokerPort, pubtopic):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.pubtopic = pubtopic

    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect= self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.__brokerIp, self.__brokerPort)
        self.client.loop_forever()

    def connect(self):
        print("Vconnect")
        thread = threading.Thread(target=self.read_camera,daemon=True)
        print("reading thread")
        thread.start()
        print("cam read")
        thread2 = threading.Thread(target=self.__run,daemon=True)
        print("running thread")
        thread2.start()
        print("cam run")

    def disconnect(self):
        self.client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        print("VImageMqttClient mqtt broker connected")

    def __on_disconnect(self, client, userdata, rc):
        print("VImageMqttClient mqtt broker disconnected")

    def sendBase64(self, frame):
        if self.client.is_connected() is False: # jpg -> cv2.imeconde ->  base64.b64encode
            return
        retval, bytes = cv2.imencode('.jpg', frame)
        if not retval:
            print("image encoding fail")
            return
        b64_bytes = base64.b64encode(bytes)
        self.client.publish(self.pubtopic , b64_bytes)

    def read_camera(self):
        print("reading start")
        video = cv2.VideoCapture(0)
        print("video capture object created")
        video.read()
        print("reading")

        video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        while True:
            if video.isOpened():
                retval, data = video.read()
                if not retval:
                    print("fail")
                    break
                self.sendBase64(data)
            else:
                break

        video.release()
        self.disconnect()
        print("Program exit")