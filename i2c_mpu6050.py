import smbus
from time import sleep
from math import atan2, degrees


#registros do mpu6050 (nomes e enderecos)
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0X1B
ACCEL_CONFIG = 0x1C
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_init():
	#escreve no sample rate register / configura periodo de amostragem
	bus.write_byte_data(mpu6050_address, SMPLRT_DIV, 7)
	
	#escreve no power management register
	bus.write_byte_data(mpu6050_address, PWR_MGMT_1, 1)
	
	#escreve no registro de configuracao
	bus.write_byte_data(mpu6050_address, CONFIG, 0)
	
	#escreve no resgistro de configuracao do giroscopio (2000deg/s p cada 131LSB)
	bus.write_byte_data(mpu6050_address, GYRO_CONFIG, 24)
	
	#escreve no interrupt enable register
	bus.write_byte_data(mpu6050_address, INT_ENABLE, 1)
	
	#escreve no registro de sensibilidade do acelerometro (2g/LSB)
	bus.write_byte_data(mpu6050_address, ACCEL_CONFIG, 0)

	
def read_raw_data(dev_addr, reg_addr):
        high = bus.read_byte_data(dev_addr, reg_addr)
        low = bus.read_byte_data(dev_addr, reg_addr+1)
    
        #concatena valores mais significativos e menos significativos
        value = ((high << 8) | low)
        
        #valor com sinal
        if(value > 32768):
                value = value - 65536
        return value

	
def accel_2_degrees(a, b):
    angle = degrees(atan2(b, a))
    if angle < 0:
        angle += 360
    return angle


def get_inclination(ax, ay, az):
    x, y, z = ax, ay, az
    return accel_2_degrees(x, z), accel_2_degrees(y, z)


bus = smbus.SMBus(1)
mpu6050_address = 0x68
MPU_init()

print("Leituras do acelerometro e giroscopio")

while True:
	acc_x = read_raw_data(mpu6050_address, ACCEL_XOUT_H)
	acc_y = read_raw_data(mpu6050_address, ACCEL_YOUT_H)
	acc_z = read_raw_data(mpu6050_address, ACCEL_ZOUT_H)
	Ax = 9.80665*acc_x/16384.0
	Ay = 9.80665*acc_y/16384.0
	Az = 9.80665*acc_z/16384.0
	
	gyro_x = read_raw_data(mpu6050_address, GYRO_XOUT_H)
	gyro_y = read_raw_data(mpu6050_address, GYRO_YOUT_H)
	gyro_z = read_raw_data(mpu6050_address, GYRO_ZOUT_H)
	#Gx = gyro_x/131.0
	#Gy = gyro_y/131.0
	#Gz = gyro_z/131.0
	
	angle_xz, angle_yz = get_inclination(Ax, Ay, Az)
	
	print(Ax, Ay, Az)
	#print(Gx, Gy, Gz)
	print("XZ_angle = %.2f degrees" %angle_xz + "    YZ_angle = %.2f degrees" %angle_yz)
	
	sleep(1)
	
	