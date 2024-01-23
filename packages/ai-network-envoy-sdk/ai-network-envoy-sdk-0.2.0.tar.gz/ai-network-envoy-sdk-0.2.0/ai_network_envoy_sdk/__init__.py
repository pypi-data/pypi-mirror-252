# ai_network_envoy_sdk/__init__.py
from os.path import dirname
from sys import path

path.insert( 0 , dirname( __file__ ) );
from .internal import AINetworkEnvoyClient
from .instruction_parser import InstructionParser, ParsedInstruction
import ai_network_envoy_pb2


class AINetworkEnvoySDK:
    def __init__(self, server_address):
        self.client = AINetworkEnvoyClient(server_address)
        pass

    def add_file(self, filename):
        return self.client.add_file_internal(filename)
    
    def get_file(self, cid, filename):
        return self.client.get_file_internal(cid, filename)
    
    def add(self, cid, message=None, data=None, filename=None, children=None):
        if message:
            content_type = ai_network_envoy_pb2.ContentType.MESSAGE
        elif data:
            content_type = ai_network_envoy_pb2.ContentType.DATA
        elif children:
            content_type = ai_network_envoy_pb2.ContentType.PARENT

        content = ai_network_envoy_pb2.Content(
            cid=cid,
            type=content_type,
            message=message if message else "",
            data=data if data else b"",
            filename=filename if filename else "",
            children=children if children else []
        )
        return self.client.add_internal(content)

    def get(self, cid):
        return self.client.get_internal(cid)
    
    def publish(self, topic, instruction, node_pk, destination_topic=None):
        publication = ai_network_envoy_pb2.Publication(
            topic=topic,
            instruction=instruction,
            node_pk=node_pk,
            destination_topic=destination_topic if destination_topic else ""
        )
        return self.client.publish_internal(publication)

    def subscribe(self, topic, node_pk, callback):
        subscription = ai_network_envoy_pb2.Subscription(
            topic=topic,
            node_pk=node_pk
        )
        return self.client.subscribe_internal(subscription, callback)
    
    def parse(self, instruction):
        parser = InstructionParser(instruction)
        return parser.parse()

