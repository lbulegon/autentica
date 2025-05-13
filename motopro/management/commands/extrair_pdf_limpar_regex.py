import os
import re
import spacy
from django.core.management.base import BaseCommand
from docling.document_converter import DocumentConverter

# Carrega o modelo de linguagem do spaCy
nlp = spacy.load("pt_core_news_sm")  # Certifique-se de instalar com: python -m spacy download pt_core_news_sm

class Command(BaseCommand):
    help = "Extrai texto estruturado de um PDF usando o Docling e aplica limpeza + NLP"

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

            texto_bruto = resultado.document.export_to_markdown()

            self.stdout.write(self.style.SUCCESS("📑 Texto extraído com sucesso!\n"))
            self.stdout.write("-" * 60)

            # --- LIMPEZA VIA REGEX ---
            texto_limpo = self.limpar_texto_regex(texto_bruto)

            # --- NORMALIZAÇÃO / EXTRAÇÃO COM SPACY ---
            self.analisar_texto_spacy(texto_limpo)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao processar o arquivo: {e}"))

    def limpar_texto_regex(self, texto):
        # Remove múltiplos espaços
        texto = re.sub(r'[ \t]+', ' ', texto)

        # Remove hifenização de quebra de linha
        texto = re.sub(r'-\n', '', texto)

        # Junta quebras de linha desnecessárias
        texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)  # Mantém parágrafos

        # Remove cabeçalhos/rodapés fictícios (exemplo simples)
        texto = re.sub(r'Página \d+ de \d+', '', texto)

        self.stdout.write(self.style.WARNING("🧹 Texto após limpeza:\n"))
        self.stdout.write(texto[:500] + "\n...")  # Mostra os primeiros 500 caracteres
        return texto

    def analisar_texto_spacy(self, texto):
        doc = nlp(texto)
        self.stdout.write(self.style.NOTICE("🧠 Entidades reconhecidas (spaCy):\n"))
        for ent in doc.ents:
            self.stdout.write(f"- {ent.text} ({ent.label_})")
