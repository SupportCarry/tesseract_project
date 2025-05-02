# AINDA NÃO TESTADO, TENHO QUE PREPARAR OS BOLETOS
# BIBLIOTECAS USADAS
from PyPDF2 import PdfMerger
from pdf2image import convert_from_path
import os
from fpdf import FPDF
from PIL import Image
import re
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR" + r"\tesseract.exe"


# TODAS AS VARIÁVEIS
pasta_imagens = r"C:\Users\GRUPO FE\Desktop\projeto 1\imagens"
pastaA = r"C:\Users\GRUPO FE\Desktop\out\comprovantes"
pastaB = r"C:\Users\GRUPO FE\Desktop\out\boletos"
pasta_saida = r"C:\Users\GRUPO FE\Desktop\out"
arquivo_sem_correspondente = os.path.join(
    pasta_saida, "sem_correspondente.txt")
y = 1
x = 1
contagem_y = [arquivo for arquivo in os.listdir(
    "C:\\Users\\GRUPO FE\\Desktop\\projeto 1\\bordero") if arquivo.lower().endswith('.pdf')]

# FUNÇÕES USADAS NO PROGRAMA:


def extrair_codigo_barras(texto):

    padrao = r'\b\d{11}-\d \d{11}-\d \d{11}-\d \d{11}-\d\b'
    resultado = re.search(padrao, texto)
    print(resultado)
    return resultado.group() if resultado else None


def renomear_imagem(caminho_imagem, codigo):
    pasta = os.path.dirname(caminho_imagem)
    novo_caminho = os.path.join(pasta, f"{codigo}.jpg")
    os.rename(caminho_imagem, novo_caminho)
    return novo_caminho


def processar_imagens(pasta):
    for nome_arquivo in os.listdir(pasta):
        caminho_imagem = os.path.join(pasta, nome_arquivo)

        if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):

            imagem = cv2.imread(caminho_imagem)

            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR" + r"\tesseract.exe"
            texto = pytesseract.image_to_string(imagem, lang='por')

            codigo = extrair_codigo_barras(texto)

            if codigo:
                print(
                    f"Código de barras encontrado em {nome_arquivo}: {codigo}")

                renomear_imagem(caminho_imagem, codigo)
            else:
                print(f"Nenhum código de barras encontrado em {nome_arquivo}.")


def colar_imagens(imagemA, imagemB):
    larguraA, alturaA = imagemA.size
    larguraB, alturaB = imagemB.size
    alturaA = alturaA
    colagem = Image.new('RGB', (larguraA, alturaA))
    colagem.paste(imagemA, (0, 0))
    colagem.paste(imagemB, (0, 1500))
    return colagem


def comparar_pastas(pastaA, pastaB, pasta_saida):
    sem_correspondente = []

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    for nome_arquivo in os.listdir(pastaA):
        if nome_arquivo.lower().endswith(('.jpg', '.jpeg')):
            caminho_imagemA = os.path.join(pastaA, nome_arquivo)
            caminho_imagemB = os.path.join(pastaB, nome_arquivo)

            if os.path.exists(caminho_imagemB):

                imagemA = Image.open(caminho_imagemA)
                imagemB = Image.open(caminho_imagemB)

                colagem = colar_imagens(imagemA, imagemB)

                caminho_pdf = os.path.join(
                    pasta_saida, f"{os.path.splitext(nome_arquivo)[0]}.pdf")
                colagem.save(caminho_pdf, "PDF", resolution=100.0)
                print(f"PDF gerado: {caminho_pdf}")
            else:

                sem_correspondente.append(nome_arquivo)
                print(f"Arquivo sem correspondente: {nome_arquivo}")

    with open(arquivo_sem_correspondente, "w") as f:
        for nome in sem_correspondente:
            f.write(f"{nome}\n")
    print(
        f"Lista de arquivos sem correspondente salva em: {arquivo_sem_correspondente}")


def unir_pdfs(pasta_origem, nome_saida):

    if not os.path.exists(pasta_origem):
        print(f"A pasta '{pasta_origem}' não existe!")
        return

    merger = PdfMerger()

    arquivos = os.listdir(pasta_origem)

    pdfs = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.pdf')]

    if not pdfs:
        print("Nenhum arquivo PDF encontrado na pasta!")
        return

    pdfs.sort()

    for pdf in pdfs:
        caminho_pdf = os.path.join(pasta_origem, pdf)
        try:
            merger.append(caminho_pdf)
            print(f"Adicionado: {pdf}")
        except Exception as e:
            print(f"Erro ao adicionar {pdf}: {e}")

    caminho_saida = os.path.join(pasta_origem, nome_saida)
    try:
        with open(caminho_saida, 'wb') as f:
            merger.write(f)
        print(f"\nPDFs unidos com sucesso em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao salvar o PDF unido: {e}")
    finally:
        merger.close()


def renomear_arquivos(pasta):

    if not os.path.exists(pasta):
        print(f"Erro: A pasta {pasta} não existe.")
        return

    regex = re.compile(r'\b(\d{11})-\d (\d{11})-\d (\d{11})-\d (\d{11})-\d\b')

    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.lower().endswith('.jpg'):
            caminho_arquivo = os.path.join(pasta, nome_arquivo)

            match = regex.search(nome_arquivo)
            if match:

                codigo_sem_verificadores = ''.join(match.groups())

                novo_nome = f"{codigo_sem_verificadores}.jpg"
                novo_caminho = os.path.join(pasta, novo_nome)

                os.rename(caminho_arquivo, novo_caminho)
                print(f"Arquivo renomeado: {nome_arquivo} -> {novo_nome}")
            else:
                print(
                    f"O arquivo {nome_arquivo} não corresponde ao padrão esperado.")

# AQUI COMEÇA A AÇÃO:


for i in range(len(contagem_y)):
    pdf = "C:\\Users\\GRUPO FE\\Desktop\\projeto 1\\bordero\\Bordero Cod de barras {}.pdf".format(
        y)
    pdfs = convert_from_path(
        pdf, fmt='jpg', poppler_path=r'C:\Users\GRUPO FE\Desktop\projeto 1\poppler-22.04.0\Library\bin')

    for img in pdfs:
        img.save(os.path.join(
            "C:\\Users\\GRUPO FE\\Desktop\\out\\comprovantes\\", 'b '+str(x)+".jpg"), "JPEG")
        x = x+1
    y = y+1

processar_imagens(pastaA)
renomear_arquivos(pastaA)
comparar_pastas(pastaA, pastaB, pasta_saida)
unir_pdfs(pasta_saida, "cota 3 merged.pdf")
