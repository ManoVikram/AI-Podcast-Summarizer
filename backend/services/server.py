from concurrent.futures import ThreadPoolExecutor
import os

import grpc
from dotenv import load_dotenv
from proto import service_pb2, service_pb2_grpc


class PodcastSummarizerService(service_pb2_grpc.PodcastSummarizerServiceServicer):
    def __init__(self):
        super().__init__()

    def ProcessPodcast(self, request, context):
        pass

def serve():
     load_dotenv()
     assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY is not set in environment variables."

     server = grpc.server(thread_pool=ThreadPoolExecutor(max_workers=10))
     service_pb2_grpc.add_PodcastSummarizerServiceServicer_to_server(PodcastSummarizerService(), server)

     server.add_insecure_port("[::]:50051")
     server.start()
     print("gRPC server is running on port 50051...")
     server.wait_for_termination()

if __name__ == "__main__":
    serve()