from collections import OrderedDict
from typing import Any

from rosidl_runtime_py.convert import message_to_ordereddict
from rosidl_runtime_py.import_message import import_message_from_namespaced_type
from rosidl_runtime_py.set_message import set_message_fields
from rosidl_parser.definition import NamespacedType


def ros2_msg_to_dict(msg: Any) -> OrderedDict:
    """ros2_msg_to_dict.
    Converts a ROS2 communication message to an OrderedDict.

    Args:
        msg: ROS2 Message to transform. Can be one of type:
            - Topic Message (Message)
            - RPC Request Message (Service.Request)
            - RPC Response Message (Service.Response)
            - Action Goal Message (Action.Goal)
            - Action Cancel Message (Action.Cancel)
            - Action Result Message (Action.Result)
            - Action Status Message (Action.Status)
            - Action Feedback Message (Action.Feedback)
    """
    _d = message_to_ordereddict(msg)
    return _d


def dict_to_ros2_msg(py_dict: OrderedDict, msg_cls: Any) -> Any:
    """dict_to_ros2_msg.
    Converts a dict/OrderedDict into a ROS2 message, given the message cls
        as input.

    Args:
        py_dict (OrderedDict): Dict/OrderedDict to convert to ROS2 message.
        msg_cls (Any): ROS2 Message class.
    """
    m = msg_cls()
    set_message_fields(m, py_dict)
    return m


def dict_to_ros2_msg_from_ns(py_dict: OrderedDict, msg_type: str) -> Any:
    """dict_to_ros2_msg_from_ns.
    Converts a dict/OrderedDict into a ROS message, given the message type
    in string representation (e.g. 'sensor_msgs/Range').

    Args:
        py_dict (OrderedDict): Dict/OrderedDict to convert to ROS2 message.
        msg_type (str): ROS2 Message type.
    """
    (pkg, name) = msg_type.split('/')
    msg_ns_type = NamespacedType([pkg, 'msg'], name)
    msg_cls = import_message_from_namespaced_type(msg_ns_type)
    print(msg_cls)
    return dict_to_ros2_msg(py_dict, msg_cls)


def dict_to_ros2_srv_req(py_dict: OrderedDict, srv_cls: Any) -> Any:
    """dict_to_ros2_srv_req.
    Converts a dict/OrderedDict into a ROS2 Service request,
        given the svc cls as input.

    Args:
        py_dict (OrderedDict): Dict/OrderedDict to convert to ROS2 message.
        srv_cls (Any): ROS2 Message class.
    """
    return dict_to_ros2_msg(py_dict, srv_cls.Request)


def dict_to_ros2_srv_resp(py_dict: OrderedDict, srv_cls: Any) -> Any:
    """dict_to_ros2_srv_resp.
    Converts a dict/OrderedDict into a ROS2 Service response,
        given the svc cls as input.

    Args:
        py_dict (OrderedDict): Dict/OrderedDict to convert to ROS2 message.
        srv_cls (Any): ROS2 Message class.
    """
    return dict_to_ros2_msg(py_dict, srv_cls.Response)


def dict_to_ros2_srv_from_ns(py_dict, srv_type) -> Any:
    """dict_to_ros2_srv_from_ns.
    Converts a dict/OrderedDict into a ROS message, given the message type
    in string representation (e.g. 'std_srvs/SetBool.Request').

    Args:
        py_dict (OrderedDict): Dict/OrderedDict to convert to ROS2 message.
        srv_type (str): ROS2 Message type.
    """
    if '.' not in srv_type:
        raise ValueError('Not a valid srv_type given.')
    (pkg, name) = srv_type.split('/')
    msg_ns_type = NamespacedType([pkg, 'srv'], name.split('.')[0])
    msg_cls = import_message_from_namespaced_type(msg_ns_type)
    if name.split('.')[1] == 'Request':
        return dict_to_ros2_msg(py_dict, msg_cls.Request)
    elif name.split('.')[1] == 'Response':
        return dict_to_ros2_msg(py_dict, msg_cls.Response)
