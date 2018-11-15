from ScanPoseMatcher import ScanPoseMatcher
import numpy as np 
import os 

def make_directory_safe(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

root_dir = "/home/acevikel/localizenet/src/"


sm = ScanPoseMatcher(scan_topic="scan",tf_topic="tf",global_frame="odom",target_frame="base_footprint")

train_dir = root_dir+"train/"
test_dir = root_dir +"test/"


make_directory_safe(train_dir+"scan/")
make_directory_safe(train_dir+"label/")
ct=0
for filename in os.listdir(train_dir+"bags/"):
    if filename.endswith(".bag"):
        X,Y =sm.getPairs(os.path.join(train_dir+"bags/", filename))
        np.save(os.path.join(train_dir+"scan/", str(ct).zfill(6)),X)
        np.save(os.path.join(train_dir+"label/", str(ct).zfill(6)),Y)
        ct+=1

make_directory_safe(test_dir+"scan/")
make_directory_safe(test_dir+"label/")

for filename in os.listdir(test_dir+"bags/"):
    if filename.endswith(".bag"):
        X,Y =sm.getPairs(os.path.join(test_dir+"bags/", filename))
        np.save(os.path.join(test_dir+"scan/", str(ct).zfill(6)),X)
        np.save(os.path.join(test_dir+"label/", str(ct).zfill(6)),Y)
        ct+=1