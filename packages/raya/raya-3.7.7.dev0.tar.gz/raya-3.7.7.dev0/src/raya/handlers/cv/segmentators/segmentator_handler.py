import typing
from rclpy.node import Node
from raya.handlers.cv.model_handler import ModelHandler


class SegmentatorHandler(ModelHandler):

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        pass

    async def get_segmentations_once(self, as_dict=False, get_timestamp=False):
        return

    def get_current_segmentations(self, as_dict=False, get_timestamp=False):
        return

    def set_segmentations_callback(self,
                                   callback: typing.Callable = None,
                                   callback_async: typing.Callable = None,
                                   as_dict: bool = False,
                                   call_without_segmentations: bool = False):
        return

    def set_img_segmentations_callback(
            self,
            callback: typing.Callable = None,
            callback_async: typing.Callable = None,
            as_dict: bool = False,
            call_without_segmentations: bool = False,
            cameras_controller: typing.Callable = None):
        return
