import threading
import time
import random

# Definindo o número de filósofos (e garfos)
NUM_FILOSOFOS = 5
TEMPO_MAXIMO_FOME = 10  # Tempo máximo sem se alimentar em segundos

# Criando os semáforos para representar os garfos, para gerenciar o acesso aos recursos compartilhados
garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]

# Variável global para controlar a fome crítica dos filósofos, Essa lista será usada para rastrear se um filósofo está em "fome crítica"
filosofos_com_fome_critica = [False] * NUM_FILOSOFOS

# Classe para representar os filósofos
class Filosofo(threading.Thread):
    def __init__(self, id, tempo_comer):
        threading.Thread.__init__(self)
        self.id = id
        self.tempo_comer = tempo_comer  # Tempo necessário para o filósofo comer
        self.ultimo_jantar = time.time()  # Registra quando o filósofo comeu pela última vez
        self.fome_critica = False  # Inicialmente, não está em fome crítica

    def pensar(self): #
        print(f"Filósofo {self.id} está pensando.")
        time.sleep(random.uniform(1, 3))  # Tempo de pensamento aleatório

    def pegar_garfos(self):
        garfo_esquerdo = self.id
        garfo_direito = (self.id + 1) % NUM_FILOSOFOS

        # Evitando deadlock: filósofos famintos pegam prioridade
        while True:
            if filosofos_com_fome_critica[self.id]:
                print(f"Filósofo {self.id} está com fome crítica e tem prioridade para pegar os garfos.")
            
            if (not filosofos_com_fome_critica[self.id] and
                any(filosofos_com_fome_critica)):  # Prioridade para quem tem fome crítica
                time.sleep(0.1)  # Aguardar até que filósofos famintos peguem os garfos
                continue
            
            # Pegando os garfos
            if self.id % 2 == 0:  # Filósofos pares pegam primeiro o garfo esquerdo
                garfos[garfo_esquerdo].acquire()
                print(f"Filósofo {self.id} pegou o garfo esquerdo ({garfo_esquerdo}).")
                garfos[garfo_direito].acquire()
                print(f"Filósofo {self.id} pegou o garfo direito ({garfo_direito}).")
            else:  # Filósofos ímpares pegam primeiro o garfo direito
                garfos[garfo_direito].acquire()
                print(f"Filósofo {self.id} pegou o garfo direito ({garfo_direito}).")
                garfos[garfo_esquerdo].acquire()
                print(f"Filósofo {self.id} pegou o garfo esquerdo ({garfo_esquerdo}).")
            break

    def largar_garfos(self):
        garfo_esquerdo = self.id
        garfo_direito = (self.id + 1) % NUM_FILOSOFOS

        garfos[garfo_esquerdo].release() #Libera o semáforo, permitindo que outros filósofos possam pegar os garfos.
        garfos[garfo_direito].release()

        print(f"Filósofo {self.id} largou os garfos.")

    def comer(self):
        print(f"Filósofo {self.id} está comendo por {self.tempo_comer} segundos.")
        time.sleep(self.tempo_comer)
        self.ultimo_jantar = time.time()  # Atualiza o tempo do último jantar
        self.fome_critica = False  # Resetando a fome crítica após comer

    def run(self):
        while True:
            self.pensar()
            self.pegar_garfos()
            self.comer()
            self.largar_garfos()

# Criando e iniciando as threads (filósofos) com tempos de alimentação diferentes
filosofos = [Filosofo(i, random.uniform(1, 5)) for i in range(NUM_FILOSOFOS)] #Cria uma lista, e cada filósofo tem um ID único e um tempo de comer aleatório (entre 1 e 5 segundos).

for filosofo in filosofos:
    filosofo.start()

# Monitorando se algum filósofo está sem comer por muito tempo (evitando starvation)
def monitorar_filosofos():
    while True:
        for filosofo in filosofos:
            tempo_sem_comer = time.time() - filosofo.ultimo_jantar
            if tempo_sem_comer > TEMPO_MAXIMO_FOME:
                filosofos_com_fome_critica[filosofo.id] = True  # Ativar fome crítica
                print(f"ALERTA: Filósofo {filosofo.id} está em fome crítica, sem comer há {int(tempo_sem_comer)} segundos.")
            else:
                filosofos_com_fome_critica[filosofo.id] = False  # Desativar fome crítica
        time.sleep(1)  # Verificação a cada 1 segundo

monitor_thread = threading.Thread(target=monitorar_filosofos)
monitor_thread.daemon = True
monitor_thread.start()
