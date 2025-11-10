import grpc
from concurrent import futures
import hashlib
import random
import grpcMiner_pb2
import grpcMiner_pb2_grpc

# ------------------------------
# DADOS EM MEMÓRIA (simulação)
# ------------------------------
transactions = {}
current_id = 0

def generate_challenge():
    """Gera desafio simples (1 a 20)."""
    return random.randint(1, 20)

def new_transaction():
    global current_id
    challenge = generate_challenge()
    transactions[current_id] = {
        "challenge": challenge,
        "solution": None,
        "winner": -1,
    }
    current_id += 1

# Inicializa com uma transação
new_transaction()

# ------------------------------
# IMPLEMENTAÇÃO DO SERVIDOR RPC
# ------------------------------
class MineradorServicer(grpcMiner_pb2_grpc.MineradorServicer):
    def getTransactionID(self, request, context):
        return grpcMiner_pb2.TransactionID(id=current_id - 1)

    def getChallenge(self, request, context):
        tx = transactions.get(request.id)
        if not tx:
            return grpcMiner_pb2.Challenge(transactionID=-1, difficulty=-1)
        return grpcMiner_pb2.Challenge(transactionID=request.id, difficulty=tx["challenge"])

    def getTransactionStatus(self, request, context):
        tx = transactions.get(request.id)
        if not tx:
            return grpcMiner_pb2.Status(transactionID=-1, status=-1)
        status = 0 if tx["winner"] != -1 else 1
        return grpcMiner_pb2.Status(transactionID=request.id, status=status)

    def getWinner(self, request, context):
        tx = transactions.get(request.id)
        if not tx:
            return grpcMiner_pb2.Winner(transactionID=-1, clientID=-1)
        return grpcMiner_pb2.Winner(transactionID=request.id, clientID=tx["winner"])

    def getSolution(self, request, context):
        tx = transactions.get(request.id)
        if not tx:
            return grpcMiner_pb2.SolutionInfo(transactionID=-1, challenge=-1, solution="", winner=-1)
        return grpcMiner_pb2.SolutionInfo(
            transactionID=request.id,
            challenge=tx["challenge"],
            solution=tx["solution"] or "",
            winner=tx["winner"]
        )

    def submitChallenge(self, request, context):
        tx = transactions.get(request.transactionID)
        if not tx:
            return grpcMiner_pb2.SubmitResponse(code=-1)
        if tx["winner"] != -1:
            return grpcMiner_pb2.SubmitResponse(code=2)

        # Validação: se hash começa com N zeros (desafio)
        h = hashlib.sha1(request.solution.encode()).hexdigest()
        prefix = "0" * tx["challenge"]
        if h.startswith(prefix):
            tx["solution"] = request.solution
            tx["winner"] = request.clientID
            new_transaction()  # cria nova transação
            return grpcMiner_pb2.SubmitResponse(code=1)
        else:
            return grpcMiner_pb2.SubmitResponse(code=0)

# ------------------------------
# EXECUÇÃO DO SERVIDOR
# ------------------------------
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcMiner_pb2_grpc.add_MineradorServicer_to_server(MineradorServicer(), server)
    server.add_insecure_port("[::]:50052")
    print("🚀 Servidor gRPC Minerador ativo na porta 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
