# ai_network_envoy_sdk/__init__.py
from .internal import add_internal, get_internal, publish_internal, subscribe_internal
from .instruction_parser import InstructionParser, ParsedInstruction
from .ai_network_envoy_pb2 import ai_network_envoy_pb2
from .ai_network_envoy_pb2_grpc import ai_network_envoy_pb2_grpc
# from os.path import dirname
# from sys import path

# path.insert( 0 , dirname( __file__ ) );

class AINetworkEnvoySDK:
    def __init__(self):
        # 초기화 코드 (필요한 경우)
        pass

    def add(self, cid, message=None, data=None, filename=None, children=None):
        if (message):
            content_type = ai_network_envoy_pb2.ContentType.Me
        content = ai_network_envoy_pb2.Content(
            cid=cid,
            type=content_type,
            message=message if message else "",
            data=data if data else b"",
            filename=filename if filename else "",
            children=children if children else []
        )
        return add_internal(content)
    

    def get(self, cid):
        return get_internal(cid)
    
    def publish(self, topic, instruction, node_pk, destination_topic=None):
        publication = ai_network_envoy_pb2.Publication(
            topic=topic,
            instruction=instruction,
            node_pk=node_pk,
            destination_topic=destination_topic if destination_topic else ""
        )
        return publish_internal(publication)

    def subscribe(self, topic, node_pk):
        subscription = ai_network_envoy_pb2.Subscription(
            topic=topic,
            node_pk=node_pk
        )
        return subscribe_internal(subscription)
    
    def parse(instruction):
        parser = InstructionParser(instruction)
        return parser.parse()

