# localizeNet

A deep learning model to give better estimation than global localization service
of the AMCL(adaptive monte carlo localization) in feature-rich environments.

# Status

Currently the rosbag parser and train script are implemented. After 5 minutes of training data
from turtlebot, the model gives 97% accuracy on test data, with 98% accuracy on train data. 
I have also tested with a relatively large dataset from a real robot, the
model is consistently giving 99% accuracy on both test and train data.

## Problem

In robots using AMCL, stability is dependent on robust localization of the vehicle.
There are several effects that may effect robot localization such as slippage or hardware error.
One possible strategy is to use global localization service which disperses
random particles, and teleoperate robot for localization. Another strategy
would be to give manual pose estimates. Both methods are not capable of
localizing the vehicle autonomously.

## Methodology

The laser scans are converted to X vector by normalizing over max_range.
Position data has been converted to three-hot encoded vector. 

Current Model: Dense -> ReLu -> Dense -> ReLu -> Dense -> Sigmoid

A note on regularization: I didn't add any regularization on purpose. 
This model is not about learning but for memorizing environment. It is not
expected to generalize to any other robot or map. 
 
The main methodology which will be applied in this repository to solve this
problem is to train a neural network to give a pose estimation. This model 
is trained offline, and assumes that there is a set of rosbag files
which has the localization data. There are several modules.

1-) Rosbag parser(Implemented):
  - Parses rosbag files to extract scan and tf data
  - Matches scans with corresponding tf

3-) Train(Implemented)
  - Trains the module using localization data

4-) Localizer
  - Uses the pre-trained model to localize the robot.

5-) tb3_simulator(Implemented)
  - This package is for recording bag data by using a gazebo world with turtlebot 3.
  - Turtlebot scan range has been increased to increase features. 

## TODO:
- [ ] Localizer 
- [ ] Try convnet by converting scan to occupancy grid
- [ ] Try with pointcloud
- [ ] Collect more data, try new models 
- [ ] Try integrating Y vector with particle-filter
- [ ] Train with huge dataset from actual robot
- [ ] Try regularization

## Notes:

This repository is mainly built for practice purposes. Does not rely on any academic work
and just my idea for solving localization problem. Please feel free to suggest improvements.

