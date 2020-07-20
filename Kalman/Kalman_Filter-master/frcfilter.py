
import numpy as np
import pandas as pd
from numpy.linalg import inv
import matplotlib.pyplot as plt




t = np.arange(0.0, 14.0, 0.01)

xt=2*t
yt=np.sin(t)

vx=[2]*1400
vx=np.asarray(vx)
vy=np.cos(t)

vf=np.sqrt((vx*vx+vy*vy))

theta=np.arctan(0.5*np.cos(0.5*t))

vfnoisy=vx+np.random.normal(0, 0.1, vx.shape)

thetanoisy=theta+np.random.normal(0, 0.1, theta.shape)





prv_time = 0
x = np.array([
        [xt[0]],
        [yt[0]],
        [vx[0]],
        [vy[0]]
        ])



#Initialize matrices P and A

#equation variances
P = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1000, 0],
        [0, 0, 0, 1000]
        ])
#equation creator
A = np.array([
        [1.0, 0, 1.0, 0],
        [0, 1.0, 0, 1.0],
        [0, 0, 1.0, 0],
        [0, 0, 0, 1.0]
        ])
#shaper
H = np.array([
        [1.0, 0, 0, 0],
        [0, 1.0, 0, 0]
        ])
I = np.identity(4)
z_lidar = np.zeros([2, 1])
#sensor variances
R = np.array([
        [0.0225, 0],
        [0, 0.0225]
        ])
noise_ax = 5
noise_ay = 5
Q = np.zeros([4, 4])

def predict():
    # Predict Step
    global x, P, Q
    x = np.matmul(A, x)
    #predicted sensor values
    At = np.transpose(A)
    #predicted value variances
    P = np.add(np.matmul(A, np.matmul(P, At)), Q)

def update(z):
    global x, P
    # Measurement update step
    Y = np.subtract(z_lidar, np.matmul(H, x))
    Ht = np.transpose(H)
    S = np.add(np.matmul(H, np.matmul(P, Ht)), R)
    K = np.matmul(P, Ht)
    Si = inv(S)
    K = np.matmul(K, Si)

    # New state
    #final predicted values
    x = np.add(x, np.matmul(K, Y))
    #final variances
    P = np.matmul(np.subtract(I ,np.matmul(K, H)), P)

def CalculateRMSE(estimations, ground_truth):
    rmse = np.zeros([4, 1])
    """
    if (sys.getsizeof(estimations) != sys.getsizeof(ground_truth) or sys.getsizeof(estimations) == 0):
        print ('Invalid estimation or ground_truth data')
        return rmse
    """
    rmse[0][0] =  np.sqrt(((estimations[0][0] - ground_truth[0][0]) ** 2).mean())
    rmse[1][0] =  np.sqrt(((estimations[1][0] - ground_truth[1][0]) ** 2).mean())
    rmse[2][0] =  np.sqrt(((estimations[2][0] - ground_truth[2][0]) ** 2).mean())
    rmse[3][0] =  np.sqrt(((estimations[3][0] - ground_truth[3][0]) ** 2).mean())
    print('rmse',rmse)
    return rmse

#**********************Iterate through main loop********************
#Begin iterating through sensor data
xList=[]
sensorList=[]
groundList=[]
tList=[]
for i in range (len(measurements)):
    new_measurement = measurements.iloc[i, :].values
    if new_measurement[0] == 'L':
        #Calculate Timestamp and its power variables
        cur_time = new_measurement[3]/1000000.0
        tList.append(cur_time)
        dt = cur_time - prv_time
        prv_time = cur_time
        dt_2 = dt * dt
        dt_3 = dt_2 * dt
        dt_4 = dt_3 * dt
        #Updating matrix A with dt value
        A[0][2] = dt
        A[1][3] = dt
        #Updating Q matrix
        Q[0][0] = dt_4/4*noise_ax
        Q[0][2] = dt_3/2*noise_ax
        Q[1][1] = dt_4/4*noise_ay
        Q[1][3] = dt_3/2*noise_ay
        Q[2][0] = dt_3/2*noise_ax
        Q[2][2] = dt_2*noise_ax
        Q[3][1] = dt_3/2*noise_ay
        Q[3][3] = dt_2*noise_ay
        #Updating sensor readings
        z_lidar[0][0] = new_measurement[1]
        z_lidar[1][0] = new_measurement[2]
        #Collecting ground truths
        ground_truth[0] = new_measurement[4]
        ground_truth[1] = new_measurement[5]
        ground_truth[2] = new_measurement[6]
        ground_truth[3] = new_measurement[7]
        #Call Kalman Filter Predict and Update functions.
        predict()
        update(z_lidar)
        sensorList.append(z_lidar[0][0])
        xList.append(x[0])
        groundList.append(ground_truth[1])


    rmse = CalculateRMSE(x, ground_truth)

    print('iteration', i, 'x: ', x)
