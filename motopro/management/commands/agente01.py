from openmanus.agents import ManusAgent

agent = ManusAgent(
    name="AssistenteMotoPro",
    instructions="Ajude a responder perguntas dos usuários sobre funcionamento de vagas, avaliações e entregas no MotoPro.",
    model="gpt-4"
)

resposta = agent.chat("Como posso aceitar uma vaga no MotoPro?")
print(resposta)
