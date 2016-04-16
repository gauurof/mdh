import numpy as np
import cv2

fn = 'letter-recognition.data'
a = np.loadtxt(fn, np.float32, delimiter=',', converters={ 0 : lambda ch : ord(ch)-ord('A') })
samples, responses = a[:,1:], a[:,0]

model = cv2.KNearest()
retval = model.train(samples,responses)
retval, results, neigh_resp, dists = model.find_nearest(samples, k = 10)
print results.ravel()