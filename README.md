# MQTT Bridge

## Description

Fowards ros topic messages to MQTT Topics in recursive manner.
 

Example, geometry_msgs/Twist type, /cmd_vel topic

there will be 6 topics created in the MQTT network.

```
/cmd_vel/linear/x
/cmd_vel/linear/y
/cmd_vel/linear/z
/cmd_vel/angular/x
/cmd_vel/angular/y
/cmd_vel/angular/z
```

Therefore MQTT Dasboard applications can be used directly, instead of deserializing the message etc.


Works in only one way, ros -> mqtt.


## Installation

- Install mosquitto



## License

MIT


## Author 

Sencer Yazici, [senceryazici@gmail.com](mailto:senceryazici@gmail.com)


