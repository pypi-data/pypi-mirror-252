# ai_network_sdk/internal.py

import grpc
import requests
from ai_network_envoy_pb2_grpc import AINetworkMerkleDAGStub
from ai_network_envoy_pb2 import Content, ContentType, ContentRequest, Publication
import threading


class AINetworkEnvoyClient:
    def __init__(self, server_address='localhost:50051'):
        self.server_address = server_address

    def add_internal(self, content):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = AINetworkMerkleDAGStub(channel)
            return stub.add(content).cid

    def get_internal(self, cid):
        content_request = ContentRequest(cid=cid)
        with grpc.insecure_channel(self.server_address) as channel:
            stub = AINetworkMerkleDAGStub(channel)
            content = stub.get(content_request)
            return content

    def publish_internal(self, publication):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = AINetworkMerkleDAGStub(channel)
            return stub.publish(publication)

    def subscribe_internal(self, subscription, callback):
        def listen_to_sse(sse_url):
            try:
                response = requests.get(sse_url, stream=True)
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        callback(decoded_line)
            except Exception as e:
                print(f"Error listening to SSE: {e}")

        with grpc.insecure_channel(self.server_address) as channel:
            stub = AINetworkMerkleDAGStub(channel)
            response = stub.subscribe(subscription)
            if response.success:
                threading.Thread(target=listen_to_sse, args=(response.sse_url,)).start()
            return response

    # 파일을 1MB 청크로 분할하는 함수
    def split_file_into_chunks(self, filename, chunk_size=1024*1024): # 1MB
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def add_file_internal(self, filename):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = AINetworkMerkleDAGStub(channel)
            chunk_cids = []
            for chunk in self.split_file_into_chunks(filename):
                response = stub.add(Content(type=ContentType.DATA, data=chunk, filename=filename))
                chunk_cids.append(response.cid)
                # print(f"Uploaded chunk for {filename}, CID: {response.cid}")
            parent_content = Content(type=ContentType.PARENT, children=chunk_cids, filename=filename)
            parent_response = stub.add(parent_content)
            print(f"Parent CID: {parent_response.cid}")

    def get_file_internal(self, cid, file_path):
        content = self.get_internal(cid)
        if content.type == ContentType.DATA:
            with open(file_path, 'wb') as file:
                for child_cid in content.children:
                    child_content = self.get(child_cid)
                    file.write(child_content.data)
                file.close()
        elif content.type == ContentType.PARENT:
            self.merge_child_contents(content.children, file_path)
        return content

    def merge_child_contents(self, children, file_path):
        with open(file_path, 'wb') as file:
            for child_cid in children:
                child_content = self.get_internal(child_cid)
                file.write(child_content.data)
            file.close()

if __name__ == "__main__":
    print("hi")
    # content = get_internal("dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f")
    # print(content.message)
    # 기본 서버 주소를 사용하여 클라이언트 인스턴스 생성
    client = AINetworkEnvoyClient()
    client.add_file_internal("test_file_64mb")