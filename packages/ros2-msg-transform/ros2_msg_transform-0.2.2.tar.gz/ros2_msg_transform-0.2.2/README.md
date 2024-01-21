# ros2_msg_conversions
Implements ros2 message conversion operations.


## Methods

### Convert ROS2 structures to OrderedDict

Can be used to convert any type of ROS2 communication structure
(Topic Message, Service, Action).

```python
def ros2_msg_to_dict(msg: Any) -> OrderedDict:
    """ros2_msg_to_dict.
    Converts a ROS2 communication message to an OrderedDict.

    Args:
        msg: ROS2 Message to transform. Can be one of type:
            - Topic Message (Message)
            - Service Request Message (Service.Request)
            - Service Response Message (Service.Response)
            - Action Goal Message (Action.Goal)
            - Action Cancel Message (Action.Cancel)
            - Action Result Message (Action.Result)
            - Action Status Message (Action.Status)
            - Action Feedback Message (Action.Feedback)
    """
```

Below are two examples, one for converting a ROS2 msg and one for converting
a ROS2 srv into an OrderedDict.

```python
from sensor_msgs.msg import Range

msg = Range()
_dict = ros2_msg_to_dict(msg)
```

```python
from std_srvs.srv import SetBool

req = SetBool.Request()
_dict = ros2_msg_to_dict(req)
```


### Convert an OrderedDict to a ROS2 communication structure

Can be used to convert into any type of ROS2 communication structure
(Topic Message, Service, Action).

```python
def dict_to_ros2_msg(py_dict: OrderedDict, msg_cls: Any) -> Any:
    """dict_to_ros2_msg.
    Converts a dict/OrderedDict into a ROS2 message, given the message cls
        as input.

    Args:
        py_dict (OrderedDict): Dict/OrderedDict to convert to ROS2 message.
        msg_cls (Any): ROS2 Message class.
            - Topic Message (Message)
            - Service Request Message (Service.Request)
            - Service Response Message (Service.Response)
            - Action Goal Message (Action.Goal)
            - Action Cancel Message (Action.Cancel)
            - Action Result Message (Action.Result)
            - Action Status Message (Action.Status)
            - Action Feedback Message (Action.Feedback)
    """
```

Below are two examples, one for converting a ROS2 msg and one for converting
a ROS2 srv into an OrderedDict.

```python
from sensor_msgs.msg import Range

_dict = {
    'range': 10.0,
    'min_range': 0.2,
    'max_range': 240.0,
    'field_of_view': 60.0,
    'radiation_type': 0,
}
_msg = dict_to_ros2_msg(_dict, Range)
```

```python
from std_srvs.srv import SetBool

...

_req = dict_to_ros2_msg(_dict, SetBool.Request)
_resp = dict_to_ros2_msg(_dict, SetBool.Response)
```

You can also construct from and to ROS2 message structures without the need
to import them. This is achieved via passing a string that includes the
namespace of the message.

```
_msg = dict_to_ros2_msg_from_ns(_dict, 'sensor_msgs/Range')
```

```
_msg = dict_to_ros2_srv_from_ns(_dict, 'std_srvs/SetBool.Request')
```
