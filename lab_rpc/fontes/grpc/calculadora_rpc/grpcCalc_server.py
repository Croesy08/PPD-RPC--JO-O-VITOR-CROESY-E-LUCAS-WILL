import grpc
from concurrent import futures
import grpcCalc_pb2
import grpcCalc_pb2_grpc

class CalculatorServicer(grpcCalc_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        return grpcCalc_pb2.Result(value=request.x + request.y)
    def Sub(self, request, context):
        return grpcCalc_pb2.Result(value=request.x - request.y)
    def Mul(self, request, context):
        return grpcCalc_pb2.Result(value=request.x * request.y)
    def Div(self, request, context):
        if request.y == 0:
            return grpcCalc_pb2.Result(value=float('inf'))
        return grpcCalc_pb2.Result(value=request.x / request.y)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcCalc_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("🚀 Servidor RPC ativo na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
