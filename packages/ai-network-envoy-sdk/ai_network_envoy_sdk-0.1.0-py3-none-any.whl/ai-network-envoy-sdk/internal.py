# ai_network_sdk/internal.py

import grpc
import requests
from .ai_network_envoy_pb2_grpc import AINetworkMerkleDAGStub
from .ai_network_envoy_pb2 import ContentRequest, Publication
import threading

def add_internal(content):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = AINetworkMerkleDAGStub(channel)
        return stub.add(content).cid

def get_internal(cid):
    content_request = ContentRequest(cid=cid)
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = AINetworkMerkleDAGStub(channel)
        content = stub.get(content_request)
        return content

def publish_internal(publication):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = AINetworkMerkleDAGStub(channel)
        return stub.publish(publication).success

def subscribe_internal(subscription, callback):
    def listen_to_sse(sse_url):
        try:
            response = requests.get(sse_url, stream=True)
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    callback(decoded_line)
        except Exception as e:
            print(f"Error listening to SSE: {e}")

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = AINetworkMerkleDAGStub(channel)
        response = stub.subscribe(subscription)
        if response.success:
            threading.Thread(target=listen_to_sse, args=(response.sse_url,)).start()


if __name__ == "__main__":
    print("hi")
    content = get_internal("dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f")
    print(content.message)