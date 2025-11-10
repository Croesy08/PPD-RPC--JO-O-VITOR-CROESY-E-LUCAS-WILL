import grpc
import hashlib
import threading
import grpcMiner_pb2
import grpcMiner_pb2_grpc

clientID = 1  # pode mudar para simular vários clientes

def mine_solution(difficulty):
    """Procura uma string cujo hash SHA1 começa com N zeros."""
    zeros = "0" * difficulty
    i = 0
    while True:
        text = f"client{clientID}-{i}"
        h = hashlib.sha1(text.encode()).hexdigest()
        if h.startswith(zeros):
            return text
        i += 1

def run():
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = grpcMiner_pb2_grpc.MineradorStub(channel)

        while True:
            print("\n--- MENU MINERADOR ---")
            print("1. getTransactionID")
            print("2. getChallenge")
            print("3. getTransactionStatus")
            print("4. getWinner")
            print("5. getSolution")
            print("6. Mine (minerar)")
            print("0. Sair")

            op = input("Escolha uma opção: ")

            if op == "0":
                break

            elif op == "1":
                res = stub.getTransactionID(grpcMiner_pb2.Empty())
                print("Transação atual:", res.id)

            elif op == "2":
                txid = int(input("TransactionID: "))
                res = stub.getChallenge(grpcMiner_pb2.TransactionID(id=txid))
                print("Desafio (dificuldade):", res.difficulty)

            elif op == "3":
                txid = int(input("TransactionID: "))
                res = stub.getTransactionStatus(grpcMiner_pb2.TransactionID(id=txid))
                print("Status:", res.status)

            elif op == "4":
                txid = int(input("TransactionID: "))
                res = stub.getWinner(grpcMiner_pb2.TransactionID(id=txid))
                print("Winner:", res.clientID)

            elif op == "5":
                txid = int(input("TransactionID: "))
                res = stub.getSolution(grpcMiner_pb2.TransactionID(id=txid))
                print(res)

            elif op == "6":
                txid = stub.getTransactionID(grpcMiner_pb2.Empty()).id
                challenge = stub.getChallenge(grpcMiner_pb2.TransactionID(id=txid)).difficulty
                print(f"Iniciando mineração para transação {txid} (dificuldade {challenge})...")

                def mine():
                    sol = mine_solution(challenge)
                    print(f"Solução encontrada: {sol}")
                    resp = stub.submitChallenge(
                        grpcMiner_pb2.SubmitRequest(transactionID=txid, clientID=clientID, solution=sol)
                    )
                    print("Resposta do servidor:", resp.code)

                threading.Thread(target=mine).start()

if __name__ == "__main__":
    run()
