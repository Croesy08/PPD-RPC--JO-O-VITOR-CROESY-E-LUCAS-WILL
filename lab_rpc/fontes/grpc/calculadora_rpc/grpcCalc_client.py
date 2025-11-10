import grpc
import grpcCalc_pb2
import grpcCalc_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grpcCalc_pb2_grpc.CalculatorStub(channel)
        while True:
            print("\n--- MENU CALCULADORA ---")
            print("1. Soma")
            print("2. Subtração")
            print("3. Multiplicação")
            print("4. Divisão")
            print("0. Sair")
            opc = input("Escolha uma opção: ")

            if opc == "0":
                break

            x = float(input("Digite o primeiro número: "))
            y = float(input("Digite o segundo número: "))
            ops = grpcCalc_pb2.Operands(x=x, y=y)

            if opc == "1":
                res = stub.Add(ops)
            elif opc == "2":
                res = stub.Sub(ops)
            elif opc == "3":
                res = stub.Mul(ops)
            elif opc == "4":
                res = stub.Div(ops)
            else:
                print("Opção inválida.")
                continue

            print("Resultado:", res.value)

if __name__ == '__main__':
    run()
