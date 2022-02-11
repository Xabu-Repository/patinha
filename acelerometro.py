from machine import I2C, Pin
from time import sleep_ms

MPU6050_ADDR = 0x68

MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_ACCEL_XOUT_L = 0x3C
MPU6050_ACCEL_YOUT_H = 0x3D
MPU6050_ACCEL_YOUT_L = 0x3E
MPU6050_ACCEL_ZOUT_H = 0x3F
MPU6050_ACCEL_ZOUT_L = 0x40
MPU6050_GYRO_XOUT_H = 0x43
MPU6050_GYRO_XOUT_L = 0x44
MPU6050_GYRO_YOUT_H = 0x45
MPU6050_GYRO_YOUT_L = 0x46
MPU6050_GYRO_ZOUT_H = 0x47
MPU6050_GYRO_ZOUT_L = 0x48
MPU6050_PWR_MGMT_1 = 0x6B

MPU6050_LSBG = 16384.0
MPU6050_LSBDS = 131.0


def mpu6050_init(i2c):
    i2c.writeto_mem(MPU6050_ADDR, MPU6050_PWR_MGMT_1, bytes([0]))


def combine_register_values(h, l):
    if not h[0] & 0x80:
        return h[0] << 8 | l[0]
    return -((h[0] ^ 255) << 8) |  (l[0] ^ 255) + 1


def mpu6050_get_accel(i2c):
    accel_x_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_XOUT_H, 1)
    accel_x_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_XOUT_L, 1)
    accel_y_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_YOUT_H, 1)
    accel_y_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_YOUT_L, 1)
    accel_z_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_ZOUT_H, 1)
    accel_z_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_ZOUT_L, 1)
    
    return [9.81*combine_register_values(accel_x_h, accel_x_l) / MPU6050_LSBG,
            9.81*combine_register_values(accel_y_h, accel_y_l) / MPU6050_LSBG,
            9.81*combine_register_values(accel_z_h, accel_z_l) / MPU6050_LSBG]


def mpu6050_get_gyro(i2c):
    gyro_x_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_XOUT_H, 1)
    gyro_x_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_XOUT_L, 1)
    gyro_y_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_YOUT_H, 1)
    gyro_y_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_YOUT_L, 1)
    gyro_z_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_ZOUT_H, 1)
    gyro_z_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_ZOUT_L, 1)
    
    return [combine_register_values(gyro_x_h, gyro_x_l) / MPU6050_LSBDS,
            combine_register_values(gyro_y_h, gyro_y_l) / MPU6050_LSBDS,
            combine_register_values(gyro_z_h, gyro_z_l) / MPU6050_LSBDS]


if __name__ == "__main__":
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    mpu6050_init(i2c)
    
    while True:
        print("Accelerometer:\t", mpu6050_get_accel(i2c), "g")
        print("Gyroscope:\t", mpu6050_get_gyro(i2c), "deg/s")
        sleep_ms(2000)





