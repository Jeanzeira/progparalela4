import threading
import time
import random

# Número de cadeiras na barbearia
NUM_CADEIRAS = 5

# Semáforos para controlar o acesso às cadeiras e aos barbeiros
sem_cadeiras = threading.Semaphore(NUM_CADEIRAS)
sem_barbeiros = threading.Semaphore(0)

# Variável para indicar se a barbearia está aberta
barbearia_aberta = True

# Função que simula o atendimento de um cliente por um barbeiro
def atender_cliente(barbeiro_id):
    while True:
        sem_barbeiros.acquire()
        print(f'Barbeiro {barbeiro_id} está atendendo um cliente...')
        time.sleep(random.uniform(1, 3))  # Simulação do tempo de atendimento
        print(f'Barbeiro {barbeiro_id} terminou o atendimento.')

        # Liberando uma cadeira
        sem_cadeiras.release()

# Função que simula a chegada de um cliente à barbearia
def cliente_chega(cliente_id):
    global barbearia_aberta
    while barbearia_aberta:
        if sem_cadeiras.acquire(blocking=False):
            print(f'Cliente {cliente_id} chegou e encontrou uma cadeira livre.')
            sem_barbeiros.release()  # Chamando um barbeiro
            return
        else:
            print(f'Cliente {cliente_id} chegou, mas todas as cadeiras estão ocupadas. Ele vai embora.')
            return

# Função que simula o funcionamento da barbearia
def barbearia():
    global barbearia_aberta
    # Número de barbeiros
    num_barbeiros = 3
    barbeiros = []
    clientes = []

    # Criando threads para os barbeiros
    for i in range(num_barbeiros):
        barbeiro_thread = threading.Thread(target=atender_cliente, args=(i+1,))
        barbeiro_thread.start()
        barbeiros.append(barbeiro_thread)

    # Loop principal para a chegada dos clientes
    cliente_id = 1
    while barbearia_aberta:
        # Simula a chegada de clientes em intervalos aleatórios
        time.sleep(random.uniform(0.5, 2))
        cliente_thread = threading.Thread(target=cliente_chega, args=(cliente_id,))
        cliente_thread.start()
        clientes.append(cliente_thread)
        cliente_id += 1

    # Aguardando todas as threads dos clientes terminarem
    for cliente_thread in clientes:
        cliente_thread.join()

    # Aguardando todas as threads dos barbeiros terminarem
    for barbeiro_thread in barbeiros:
        barbeiro_thread.join()

# Iniciando o funcionamento da barbearia
barbearia_thread = threading.Thread(target=barbearia)
barbearia_thread.start()

# Simulando o funcionamento da barbearia por um tempo
time.sleep(15)

# Fechando a barbearia
barbearia_aberta = False
barbearia_thread.join()
print('Barbearia fechada.')
