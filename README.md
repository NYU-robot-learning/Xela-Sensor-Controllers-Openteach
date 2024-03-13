
# Xela-Sensor-Controllers-Openteach

This is the README for Xela-Sensor-Controllers used for Openteach. 
Clone this repository and install it in base [controller](https://github.com/NYU-robot-learning/OpenTeach-Controllers.git).

Setup the low level drivers following xela documentation.

Start the low level drivers using `cd /etc/xela && sudo ./xela_server -f xServ.ini`

Clone this repository. 
Start the ROS Xela drivers by: 
    1. `roslaunch xela_server service.launch`


### Citation
If you use this repo in your research, please consider citing the paper as follows:
```@misc{iyer2024open,
      title={OPEN TEACH: A Versatile Teleoperation System for Robotic Manipulation}, 
      author={Aadhithya Iyer and Zhuoran Peng and Yinlong Dai and Irmak Guzey and Siddhant Haldar and Soumith Chintala and Lerrel Pinto},
      year={2024},
      eprint={2403.07870},
      archivePrefix={arXiv},
      primaryClass={cs.RO}
}




