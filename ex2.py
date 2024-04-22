import threading
import time
import random

# Variável compartilhada que representa o recurso
recurso_compartilhado = 0

# Semáforos para controlar o acesso ao recurso
mutex = threading.Semaphore(1)  # para exclusão mútua entre leitores e escritores
escrita = threading.Semaphore(1)  # para garantir que apenas um escritor escreva de cada vez
leitores = threading.Semaphore(0)  # para controlar o número de leitores lendo simultaneamente

# Função que simula o comportamento de um leitor
def leitor(leitor_id):
    while True:
        time.sleep(random.uniform(1, 3))  # Simula o tempo entre leituras
        print(f'Leitor {leitor_id} está tentando ler o recurso...')
        
        mutex.acquire()  # Garante exclusão mútua entre leitores e escritores
        leitores.release()  # Indica que um leitor está lendo
        if leitores._value == 1:
            escrita.acquire()  # Se este é o primeiro leitor, bloqueia a escrita
        mutex.release()
        
        # Lendo o recurso compartilhado
        print(f'Leitor {leitor_id} está lendo o recurso: {recurso_compartilhado}')
        
        mutex.acquire()  # Garante exclusão mútua entre leitores e escritores
        leitores.acquire()  # Indica que um leitor terminou de ler
        if leitores._value == 0:
            escrita.release()  # Se não há mais leitores, libera a escrita
        mutex.release()

# Função que simula o comportamento de um escritor
def escritor(escritor_id):
    while True:
        time.sleep(random.uniform(1, 3))  # Simula o tempo entre escritas
        print(f'Escritor {escritor_id} está tentando escrever no recurso...')
        
        escrita.acquire()  # Bloqueia outros escritores
        print(f'Escritor {escritor_id} está escrevendo no recurso...')
        global recurso_compartilhado
        recurso_compartilhado += 1  # Escreve no recurso compartilhado
        print(f'Escritor {escritor_id} terminou de escrever. Recurso atual: {recurso_compartilhado}')
        escrita.release()  # Libera a escrita

# Criando threads para os leitores
threads_leitores = []
for i in range(3):  # Criando 3 leitores
    thread = threading.Thread(target=leitor, args=(i,))
    thread.start()
    threads_leitores.append(thread)

# Criando threads para os escritores
threads_escritores = []
for i in range(2):  # Criando 2 escritores
    thread = threading.Thread(target=escritor, args=(i,))
    thread.start()
    threads_escritores.append(thread)

# Aguardando as threads terminarem
for thread in threads_leitores:
    thread.join()

for thread in threads_escritores:
    thread.join()
