Relatório Técnico – Laboratório II – RPC/gRPC

Disciplina: Programação Paralela e Distribuída
Professor: Breno Krohling
Período: 2025/2
Aluno: João Vitor Croesy Pereira e Lucas Will
Turma: [coloque o código da sua turma aqui]

1. Introdução

O objetivo deste trabalho foi desenvolver aplicações cliente/servidor utilizando o conceito de Chamada de Procedimento Remoto (RPC).
Primeiro foi implementada uma calculadora distribuída utilizando Python e gRPC, e posteriormente um sistema de mineração de criptomoedas que simula o funcionamento de um minerador em um ambiente distribuído.

O gRPC foi escolhido por ser uma implementação moderna e de alto desempenho de RPC, com suporte a múltiplas linguagens e comunicação baseada em HTTP/2 e Protobuf, facilitando a serialização dos dados transmitidos entre cliente e servidor.

⚙️ 2. Metodologia

O desenvolvimento foi dividido em duas etapas principais, conforme as atividades propostas.

2.1 Atividade 1 – Calculadora RPC

A primeira atividade consistiu em criar um sistema Cliente/Servidor que executasse as quatro operações básicas (soma, subtração, multiplicação e divisão) de forma remota.
O servidor era responsável pelos cálculos, enquanto o cliente enviava os números e recebia o resultado.

Estrutura de arquivos:
grpcCalc.proto
grpcCalc_pb2.py
grpcCalc_pb2_grpc.py
grpcCalc_server.py
grpcCalc_client.py

Funcionamento:

O arquivo grpcCalc.proto define a interface RPC e as mensagens trocadas.

O comando grpc_tools.protoc gera automaticamente os stubs cliente e servidor.

O servidor (grpcCalc_server.py) implementa as funções de cálculo e aguarda conexões.

O cliente (grpcCalc_client.py) apresenta um menu interativo ao usuário e se comunica com o servidor através das funções gRPC.

Durante os testes, o servidor foi executado primeiro e o cliente pôde realizar as operações com sucesso, mostrando o resultado processado remotamente.

2.2 Atividade 2 – Minerador de Criptomoedas

Na segunda atividade foi implementado um protótipo de minerador de criptomoedas baseado em RPC, também usando Python/gRPC.
A aplicação simula um ambiente onde o servidor cria desafios criptográficos e vários clientes tentam resolvê-los (minerar) usando hashing SHA-1.

Estrutura de arquivos:
grpcMiner.proto
grpcMiner_pb2.py
grpcMiner_pb2_grpc.py
grpcMiner_server.py
grpcMiner_client.py

Funcionamento geral:

O servidor mantém uma tabela de transações contendo:

TransactionID

Challenge (nível de dificuldade)

Solution

Winner

O cliente se conecta ao servidor, consulta o desafio atual e tenta encontrar uma solução válida.

A solução consiste em encontrar uma string cujo hash SHA-1 comece com uma quantidade específica de zeros (definida pela dificuldade).

Quando uma solução é encontrada, o cliente envia o resultado via submitChallenge(), e o servidor valida o hash e atualiza o vencedor.

A implementação utilizou threads para permitir que o cliente pudesse minerar de forma independente, sem travar o menu principal.

3. Testes e Resultados

Foram realizados testes locais com o servidor e cliente rodando em terminais separados.
O servidor foi iniciado primeiro e ficou escutando na porta 50052, enquanto o cliente se conectou ao endereço localhost.

Durante os testes:

O cliente conseguiu obter o TransactionID e o nível de dificuldade do desafio.

A mineração foi executada com sucesso, encontrando uma solução que satisfazia a condição do hash.

Após o envio da solução, o servidor marcou o cliente como vencedor e criou automaticamente uma nova transação.

Exemplo de saída:

Iniciando mineração para transação 0 (dificuldade 3)...
Solução encontrada: client1-9923
Resposta do servidor: 1


Esse resultado demonstra que o sistema conseguiu simular corretamente o processo de mineração e comunicação distribuída via gRPC.

4. Conclusão

O laboratório permitiu compreender de forma prática o funcionamento de sistemas distribuídos baseados em RPC, bem como o uso do gRPC e Protobuf para criar aplicações escaláveis e eficientes.

Através da implementação da calculadora e do minerador, foi possível observar a importância dos stubs, da serialização de mensagens e da comunicação bidirecional entre cliente e servidor.

Além disso, o uso do Python simplificou a implementação e possibilitou rápida prototipagem, sendo uma ferramenta adequada para estudos de RPC e gRPC.
