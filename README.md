# autentica
Autenticação dos produtos **GlbHash**

Para configurar e rodar o ambiente, siga os passos abaixo:

```bash
- python -m venv .venv
- .venv\Scripts\activate  
- railway --version  
- pip freeze > requirements.txt
- pip install -r requirements.txt
- npm i -g @railway/cli
- railway login
- railway link -p 50594409-8ec3-4211-9cf7-6f4ef2f9afc8
- railway up
- python manage.py makemigrations  
- python manage.py migrate
- python manage.py createsuperuser

 - python manage.py escanear_portas --host 127.0.0.1 --inicio 31400 --fim 31409

https://autentica-desenvolvimento.up.railway.app/


## 🏢 Persona: Estabelecimento

### 🧾 Nome: **Hamburgueria Sabor de Rua**

- **Localização:** Avenida Principal, 1234 – Centro, Porto Alegre, RS  
- **Responsável:** Carlos Menezes – Gerente Operacional  
- **Contato:**  
  - 📞 (51) 99999-1234  
  - 📧 carlos@saborderua.com.br  

---

### 🔧 Características Operacionais

- **Tipo de negócio:** Alimentação (hamburgueria artesanal)  
- **Horários de entrega:**
  - Segunda a Quinta: 18h às 23h
  - Sexta e Sábado: 18h à 1h
  - Domingo: 17h às 22h
- **Turnos configurados:** 
  - Noite (18h às 23h)
  - Madrugada (23h à 1h)
- **Frequência de vagas:** 2 a 3 motoboys por dia
- **Contrato padrão:** Contrato fixo por turno com adicional por entrega extra

---

### 🧠 Comportamento e Expectativas

- Valoriza **pontualidade** e **comunicação rápida** com os motoboys.
- Gosta de **visualizar status das vagas e alocações em tempo real**.
- Costuma **reutilizar motoboys de confiança**, mas está aberto a novos.
- Reclama de **cancelamentos em cima da hora** ou **mudança de turno inesperada**.

---

### 💡 Objetivos com a Plataforma

- Ter um **painel simples para abrir vagas**, inclusive de última hora.
- Acompanhar o **histórico de motoboys alocados**.
- **Avaliar e receber avaliações** dos motoboys.
- Automatizar a **reposição de vagas abertas**.

---

### 🔐 Regras Personalizadas

- Motoboy só pode ser alocado se **não estiver "alocado" em outro turno** no mesmo horário.
- Vaga muda para **"preenchida" apenas após confirmação do motoboy**.
- Cancelamentos devem **gerar notificação imediata por e-mail ou WhatsApp**.


## 👨‍💼 Persona: Supervisor

### 🧾 Nome: **Luciana Ribeiro**

- **Função:** Supervisora Regional de Logística  
- **Área de Atuação:** Região Metropolitana de Porto Alegre – RS  
- **Contato:**  
  - 📞 (51) 98888-4567  
  - 📧 luciana.ribeiro@logsuper.com.br  

---

### 🧠 Perfil Profissional

- Mais de 6 anos atuando com **logística urbana e gestão de entregadores**.  
- Experiência com **aplicativos de gestão de motoboys**, mas prefere interfaces objetivas e com **filtros rápidos**.  
- Coordena cerca de **25 motoboys distribuídos em 6 estabelecimentos**.  
- Acompanha diariamente os **turnos, entregas e feedbacks** dos entregadores.

---

### 🔧 Atividades Frequentes

- Gerencia a **disponibilidade de motoboys** por turno e região.  
- **Intermedia conflitos** entre entregadores e estabelecimentos.  
- Atualiza os **status dos motoboys** (livre, alocado, indisponível) conforme realocações.  
- Monitora **cancelamentos frequentes** para avaliar a performance.  
- Aprova ou reprova **pedidos de troca de turno**.

---

### 💡 Objetivos com a Plataforma

- Ter uma **visão geral por data e turno** com filtros por estabelecimento.  
- **Ver e editar** status dos motoboys de forma rápida.  
- Receber **alertas em tempo real** de problemas com entregadores.  
- Exportar **relatórios semanais** de alocação e desempenho.

---

### 🔐 Regras Personalizadas

- Um motoboy não pode ser alocado em **dois estabelecimentos no mesmo turno**.  
- Após 3 cancelamentos em uma semana, o motoboy deve ser **sinalizado com alerta**.  
- Preferência por **motoboys com histórico de avaliação acima de 4.5 estrelas**.


## 🏍️ Persona: Motoboy Insatisfeito

### 🧾 Nome: **Carlos "Carlão" dos Santos**

- **Função:** Motoboy parceiro  
- **Tempo de parceria:** 1 ano e 3 meses  
- **Região de Atuação:** Zona Norte – Porto Alegre, RS  
- **Contato:**  
  - 📞 (51) 98777-1234  
  - 📧 carlao.entregas@gmail.com  

---

### 🧠 Perfil

- Profissional dedicado, com foco em **pontualidade e organização de rota**.  
- Sempre buscou manter **boa relação com os estabelecimentos**, mas sente-se **desvalorizado nos últimos meses**.  
- Já foi considerado "exemplo de conduta" por um dos supervisores antigos.  

---

### 😤 Situação Atual

- Está **insatisfeito com a falta de comunicação**: raramente é avisado com antecedência sobre mudanças de turno.  
- Teve **duas vagas canceladas de última hora** sem justificativa.  
- Observou que **motoboys menos experientes** estão sendo alocados com mais frequência.  
- Deseja **entendimento direto com um supervisor**, pois não sente que suas mensagens estão sendo lidas na plataforma.

---

### 💬 Comentários Recentes

> "Tô na rua todo dia. Quando precisam, tô sempre pronto. Mas agora parece que ninguém se importa se a gente fica sem vaga."

> "Só queria ser ouvido. Tô tentando resolver dentro do sistema, mas ninguém responde."

---

### 🎯 Objetivo com a Plataforma

- Quer um **canal direto com o supervisor** responsável pelo estabelecimento que mais atende.  
- Deseja **transparência nas escolhas de alocação** de motoboys.  
- Sugere uma **área de feedback e histórico de cancelamentos** acessível ao entregador.  
- Acredita que um **sistema de avaliação mútua** (motoboy ↔ estabelecimento) pode melhorar o respeito entre as partes.

---

### 🔧 Propostas de Melhoria

- Criar um botão "**Quero falar com o supervisor**" nas vagas recusadas.  
- Notificação automática ao motoboy quando for **removido de uma vaga**, com motivo.  
- Implantar uma **pontuação de confiabilidade** visível, com base em entregas realizadas, atrasos e feedback dos estabelecimentos.


## 🏍️ Persona: Motoboy Satisfeito

### 🧾 Nome: **André Oliveira**

- **Função:** Motoboy parceiro  
- **Tempo de parceria:** 2 anos e 7 meses  
- **Região de Atuação:** Centro-Sul – Belo Horizonte, MG  
- **Contato:**  
  - 📞 (31) 98888-4466  
  - 📧 andre.rider@gmail.com  

---

### 🧠 Perfil

- Profissional experiente e proativo, conhecido por seu **excelente relacionamento com os estabelecimentos**.  
- Organiza sua rotina com antecedência, utilizando todos os recursos da plataforma.  
- Gosta de dar **feedback construtivo** sobre as rotas, horários e experiência geral.

---

### 😄 Situação Atual

- Está **muito satisfeito com o funcionamento da plataforma**, principalmente com a agilidade na liberação de novas vagas.  
- **Valoriza a transparência** nas alocações e sente-se respeitado como parceiro.  
- Costuma ser **alocado com frequência** por um mesmo supervisor, o que facilita sua rotina.

---

### 💬 Comentários Recentes

> "Nunca tive dor de cabeça. As vagas vêm certinho, os horários são claros e o suporte é rápido quando preciso."

> "Gosto de trabalhar com quem respeita o motoboy. Quando a gente se sente parte do time, trabalha melhor."

---

### 🎯 Objetivo com a Plataforma

- Continuar mantendo um **bom índice de aceitação e pontualidade**.  
- Ajudar a **melhorar a experiência dos novos motoboys**, compartilhando dicas e sugestões.  
- Deseja que a plataforma **reconheça motoboys com boas médias de desempenho**, como forma de incentivo.

---

### 🏆 Reconhecimentos

- 5 estrelas em mais de **300 entregas consecutivas**  
- Destaque no relatório mensal da supervisão (Março/2025)  
- Um dos primeiros a testar o sistema de **avaliação automática de rotas**  

---

### 🔧 Sugestões para o Futuro

- Criar um **ranking semanal com bonificação simbólica** para os motoboys mais bem avaliados.  
- Disponibilizar **relatórios de desempenho por período** no perfil do entregador.  
- Implantar um **canal de boas práticas** com dicas de outros motoboys.



## 📌 Sub Supervisor Local: Desafio Operacional e Solução de Conflito

### 🎯 O Problema

Para garantir presença física nos estabelecimentos, mesmo quando o supervisor principal gerencia múltiplos locais, é necessária a criação da figura de um **sub supervisor local**.

Este perfil precisa:
- Atuar presencialmente como elo de gestão no local.
- Ter mais responsabilidades do que um motoboy comum.
- Ser remunerado de forma diferenciada.

**Conflito:** De onde virá a verba para remunerar esse novo papel?
- Do estabelecimento?
- Do supervisor principal?
- Da empresa prestadora?
- Ou de um modelo híbrido?

---

## ✅ Soluções Propostas

### 🔸 1. Modelo de Coparticipação (Híbrido)

- **Funcionamento:** Custo dividido entre o estabelecimento e a empresa prestadora ou o supervisor.
- **Exemplo:** Sub supervisor recebe R$ 100 mensais → Estabelecimento paga R$ 60 e a empresa ou supervisor R$ 40.
- **Vantagem:** Responsabilidade compartilhada e impacto financeiro reduzido.
- **Dica:** Registrar esse custo como “Taxa de Supervisão Presencial”.

---

### 🔸 2. Sistema de Bônus por Desempenho

- **Funcionamento:** Sub supervisor recebe bônus com base em metas específicas (ex: pontualidade, redução de cancelamentos, feedbacks positivos).
- **Origem dos recursos:** Margem da empresa, parte do supervisor ou contratos variáveis.
- **Vantagem:** Custo variável, atrelado à performance. Ideal para etapas iniciais de validação.

---

### 🔸 3. Plano Interno de Carreira

- **Funcionamento:** Motoboys com bom desempenho são promovidos a sub supervisores com:
  - Pequeno aumento simbólico inicial.
  - Prioridade de acesso a vagas.
  - Bonificações por indicação ou suporte a novos motoboys.
- **Vantagem:** Cria engajamento interno, reduz rotatividade e custos fixos.

---

### 🔸 4. Inclusão no Plano de Contrato com o Estabelecimento

- **Funcionamento:** Negociar com os estabelecimentos um plano que já inclua esse serviço como diferencial da plataforma.
- **Exemplo:** Valor fixo adicional por mês para garantir presença local e resposta rápida.
- **Vantagem:** Sustentável e escalável, com argumento comercial forte.

---

## 📊 Quadro Comparativo: Modelos de Remuneração do Sub Supervisor

| Modelo                            | Custo para Estabelecimento | Custo para Empresa | Vantagem Principal                       | Risco / Desvantagem                    |
|-----------------------------------|-----------------------------|--------------------|------------------------------------------|----------------------------------------|
| Coparticipação (Híbrido)          | Médio                       | Médio              | Divisão de responsabilidades             | Requer negociação e consenso           |
| Bônus por Desempenho              | Variável                    | Variável           | Custo proporcional ao resultado          | Pode haver inconsistência de receita   |
| Plano Interno de Carreira         | Baixo                       | Baixo              | Engajamento interno, baixo custo fixo    | Menor atratividade sem incentivo direto|
| Inclusão no Contrato Comercial    | Alto (direto)               | Nenhum             | Sustentável e justificado no serviço     | Requer habilidade de venda             |

---

## 🧭 Recomendação Estratégica

> **Comece com o Modelo Híbrido + Indicadores de Desempenho**, estruturando também:
> - Funções claras e escaláveis para o sub supervisor.
> - Reconhecimento interno com plano de carreira.
> - Formalização contratual com os estabelecimentos.

---

## ⚖️ Riscos Trabalhistas Envolvendo o Sub Supervisor Local

Ao criar uma nova função com mais responsabilidades (e possível remuneração diferenciada), é necessário estar atento a aspectos legais e previdenciários. A seguir, listamos os principais riscos e implicações para cada uma das partes envolvidas:

---

### 🏢 Estabelecimento

| Risco | Descrição |
|-------|-----------|
| **Vínculo Empregatício** | Se o sub supervisor for escolhido, gerido e remunerado diretamente pelo estabelecimento, pode-se caracterizar vínculo empregatício. |
| **Solidariedade em Ações Trabalhistas** | Caso a empresa prestadora não cumpra obrigações legais, o estabelecimento pode ser responsabilizado solidariamente. |
| **Descaracterização de Terceirização** | Envolvimento direto na gestão de pessoal (ex: dar ordens, controlar horários) pode descaracterizar terceirização lícita. |

---

### 🏢 Empresa Prestadora de Serviços (EPS) / Supervisor

| Risco | Descrição |
|-------|-----------|
| **Acúmulo de Função** | Se o sub supervisor exerce funções administrativas além das operacionais sem formalização, pode pleitear adicional de função. |
| **Desvio de Função** | Caso o contrato com o motoboy não preveja as novas atribuições, há risco de alegação de desvio. |
| **Reconhecimento de Vínculo** | Mesmo com PJ, MEI ou autônomo, se houver subordinação, habitualidade, pessoalidade e onerosidade, pode haver reconhecimento de vínculo empregatício. |
| **Carga Horária Oculta** | Se o sub supervisor “ajuda” fora do horário da sua vaga normal, pode alegar horas extras ou dupla jornada. |

---

## 📌 Recomendações Legais

1. **Contrato Formalizado com Cláusula de Função Adicional**  
   > Inclua no contrato de prestação de serviço a descrição clara da função de sub supervisor, atribuições e contrapartida.

2. **Modelo de Remuneração por Tarefa ou Bônus**  
   > Em vez de fixar salário adicional, use bonificações por performance ou metas mensuráveis.

3. **Treinamento e Termo de Ciência**  
   > Apresente um termo assinado de ciência das responsabilidades da função, com treinamento registrado.

4. **Evitar Subordinação Direta ao Estabelecimento**  
   > Toda a comunicação e controle deve ocorrer via supervisor ou app, nunca diretamente pelo estabelecimento.

5. **Consultar um Especialista Trabalhista**  
   > Antes de formalizar o modelo, é recomendado revisar os contratos com apoio de um advogado ou consultoria jurídica.

---

## ✅ Conclusão

> A criação da figura do sub supervisor local é uma excelente solução de gestão operacional, **desde que implementada com segurança jurídica**. O segredo está em documentar tudo, evitar subordinação direta ao cliente (estabelecimento) e adotar modelos de remuneração claros e transparentes.

