import socket
import numpy as np
#import matplotlib.pyplot as plt


class WirelessMpu6050:
    def __init__(self):
        self.g_ax = 0
        self.g_ay = 0
        self.last_value = [0, 0] #initial values for numerical integration
    
    def received_data_to_nparray(self, received_data):
        return np.fromstring(received_data, dtype=float, sep=" ");
    
    def angle_from_accel(self, nparray_accel):
        return [180*(np.arctan(nparray_accel[2]/nparray_accel[0])) / np.pi, 
                180*(np.arctan(nparray_accel[2]/nparray_accel[1])) / np.pi]

    def angle_from_gyro(self, nparray_gyro, integration_timestep):
        current_value = nparray_gyro
        self.g_ax += (current_value[3] + self.last_value[0])*integration_timestep/2
        self.g_ay += (current_value[3] + self.last_value[1])*integration_timestep/2
        self.last_value[0] = current_value[3]
        self.last_value[1] = current_value[4]
        return [self.g_ax, self.g_ay]


tcp_ip = '10.3.141.1'
tcp_port = 5005
mpu6050 = WirelessMpu6050()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((tcp_ip, tcp_port))
        sock.listen()
        print('Listening...')
        conn, addr = sock.accept()
        with conn:
            print('Connected to ', addr)
            while True:
                data = conn.recv(1024).decode()
                received_nparray = mpu6050.received_data_to_nparray(data)
                #tilt_angle = mpu6050.angle_from_accel(received_nparray);
                tilt_angle = mpu6050.angle_from_gyro(received_nparray, 0.5);
                #print(received_nparray)
                print(tilt_angle)
                if not data: break
            
