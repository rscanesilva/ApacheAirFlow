**<s>Capacidade de cada ferramenta deve cobrir para startar uma malha ou um determinado batch:</s>**
1.	<s>Trigger do agendamento do schedule, via regras de calendário de data/hora</s>
2.	<s>Trigger do Arquivos salvos no bucket</s>
3.	<s>Trigger via API</s>
4.	<s>Trigger via fila JMS (Preferência de uso do Pub/Sub, mantido pela google)</s>
5.	<s>Trigger recursivas que executem dentro de espaços determinados de tempos</s>
6.	<s>Um batch específico dentro de uma malha pode possuir sua própria regra de schedule, sendo que só execute em dias específicos da semana, por exemplo.</s>
 
**Interação da área de sustentação com as malhas:**
1.	<s>Caso um batch específico dentro de uma malha dê erro, e seja orientado o skip do mesmo no momento da verificação do problema, como deve lidar?</s>
2.	Caso uma malha deva ser suspensa sua execução por determinado motivo
3.	<s>Antes da execução da malha poder inabilitar um batch específico por alguma necessidade</s>
 
**Interdependência entre as malhas:**
1.	Tendo duas malhas, A e  B:
	. <s>A malha B pode depender da finalização de um terminado batch da malha A, tendo dependência o status de sucesso ou não na finalização</s>

    . Existência do conceito de “Ponteiro externo”, sendo este, uma malha B ter um determinado step no qual depende de um step da malha A sem ter uma dependência física direta entre as mesmas.

    . <s>Dependência entre malhas do legado e malhas da cloud</s>
      Podem se comunicar por filas, um job em uma das dags (legado ou novo) inicializa a execução da outra via api ou posta uma mensagem na fila que irá tirggar a execução da segunda DAG

    . <s>Tratamento de status da dependência dentro de fluxo e subfluxo, podendo ser fortemente acoplado ou não. Ou seja, caso um subfluxo B execute a malha A pode depender ou não do resultado ou da finalização do fluxo B, para continuar seu processamento.</s>
 
**Compartilhamento de Arquivos entre ambientes:**
1.	<s>Simular um envio do ambiente on primese para a nuvem</s>
 
**Observabilidade:**
	Ferramenta de monitoração para tratar:
2.	Ter a capacidade de diferenciar problemas emergenciais e problemas comuns, diferenciando o SLA de cada um para notificação do suporte.
3.	Mapear como será a  tratativa do suporte, verificando log, do batch e da malha, recuperação dos dados do Pod que está executando o processo.

**Fluxo:**
1.	<s>Validar o batch solto, sem ter fluxo para o mesmo.</s>
2.	<s>Validar a execução do novo modelo desenhado para grid dentro da malha.</s>
3.	<s>Validar as execuções das batchs em containers.</s>
 
