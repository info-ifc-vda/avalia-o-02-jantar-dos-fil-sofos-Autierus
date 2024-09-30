[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/-Z5ovbbf)

Para resolver o problema de Deadlock; foi implementada uma política de ordem diferenciada para pegar os garfos:

Filósofos com IDs pares pegam primeiro o garfo à esquerda e depois o garfo à direita.
Filósofos com IDs ímpares pegam primeiro o garfo à direita e depois o garfo à esquerda.
Essa alternância evita a situação onde todos os filósofos pegam o mesmo garfo primeiro, criando uma sequência circular em que sempre um filósofo consegue pegar os dois garfos, liberar os recursos e permitir que outros prossigam. Com essa abordagem, a simulação garante que os filósofos não fiquem travados indefinidamente em uma espera mútua.


Para resolver o problema de Starvation;
Uma thread de monitoramento verifica periodicamente o tempo que cada filósofo está sem comer. Se algum filósofo ficar sem comerpor mais tempo do que o valor máximo definido (no caso, 10 segundos), esse filósofo entra em fome crítica. Quando um filósofo está em fome crítica, ele ganha prioridade para pegar os garfos. Isso significa que, se algum filósofo estiver muito tempo sem comer, ele terá prioridade sobre os outros, garantindo que ele possa pegar os garfos e comer antes de voltar à concorrência normal.
