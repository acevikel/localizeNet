# localizeNet

A deep learning model to give better estimation than global localization service
of the AMCL(adaptive monte carlo localization) in feature-rich environments.

## Problem

In robots using AMCL, stability is dependent on robust localization of the vehicle.
There are several effects that may effect robot localization such as slippage or hardware error.
One possible strategy is to use global localization service which disperses
random particles, and teleoperate robot for localization. Another strategy
would be to give manual pose estimates. Both methods are not capable of
localizing the vehicle autonomously.

## Methodology

The main methodology which will be applied in this repository to solve this
problem is to train a neural network to give a pose estimation. This model is
meant to work offline, and assumes that there is a set of rosbag files
which has the localization data. There are several modules.

1-) Rosbag parser:
  - Parses rosbag files to extract path, scan and tf data
  - Matches scans with corresponding tf

2-) Localization evaluator:
  - Evaluates matched scan-tf pairs considering path, and filters out pairs that are not localized well

3-) Train
  - Trains the module using localization data

4-) Localizer
  - Uses the pre-trained model to localize the robot.

## Notes:

This repository is currently just a rough idea. I will start implementation as I have time.
Please feel free to suggest improvements to methodology.
