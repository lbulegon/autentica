from django_cron import CronJobBase, Schedule
from django.utils.timezone import now
from motopro.management.commands.gerar_vagasSpot import Command as GerarVagasCommand

class GerarVagasSpotCron(CronJobBase):
    RUN_EVERY_MINS = 1440  # 1440 minutos = 1 vez por dia

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'vagas.gerar_vagas_spot'  # Código único para identificar essa cron job

    def do(self):
        # Executa o mesmo comando de management!
        command = GerarVagasCommand()
        command.handle(data=now().date())
