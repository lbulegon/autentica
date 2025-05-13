import os
from django.core.management.base import BaseCommand
from docling.document_converter import DocumentConverter

class Command(BaseCommand):
    help = "Extrai texto estruturado de um PDF usando o Docling"

    def add_arguments(self, parser):
        parser.add_argument('caminho_pdf', type=str, help='Caminho para o arquivo PDF')

    def handle(self, *args, **kwargs):
        caminho_pdf = kwargs['caminho_pdf']

        if not os.path.exists(caminho_pdf):
            self.stderr.write(self.style.ERROR(f"Arquivo não encontrado: {caminho_pdf}"))
            return

        try:
            converter = DocumentConverter()
            resultado = converter.convert(caminho_pdf)

            self.stdout.write(self.style.SUCCESS("📑 Texto extraído com sucesso!\n"))

            markdown = resultado.document.export_to_markdown()
            self.stdout.write(markdown)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao processar o arquivo: {e}"))
