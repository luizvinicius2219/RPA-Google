#!/usr/bin/env python
# coding: utf-8

import time
import schedule
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from sqlalchemy import create_engine
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import datetime

# Função para pesquisar e coletar as notas de avaliação das lojas
def pesquisar_e_coletar_notas(navegador, termos_pesquisa):
    print("Iniciando pesquisa e coleta de notas das lojas...")
    
    # Lista para armazenar os dados coletados
    dados = []
    
    # Iterar sobre os termos de pesquisa
    for marca in termos_pesquisa:
        print("Pesquisando:", marca)
        
        # Pesquisar no Google
        campo_pesquisa = navegador.find_element(By.NAME, 'q')
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(marca)
        campo_pesquisa.submit()
        
        # Aguardar um período de tempo para os resultados carregarem
        time.sleep(5)  
        
        # Coletar as notas de avaliação das lojas
        resultados_pesquisa = navegador.find_elements(By.CSS_SELECTOR, 'span.Aq14fc')
        for resultado in resultados_pesquisa:
            nota = resultado.text
            dados.append({'Marca': marca, 'Nota': nota})
    
    return dados

# Função para configurar e rodar o navegador e salvar os dados no banco de dados
def agendar_pesquisa():
    print("Configurando o driver do Chrome...")
    servico = Service(ChromeDriverManager().install())
    print("Configuração concluída. Inicializando o navegador...")
    navegador = webdriver.Chrome(service=servico)

    # Lista de marcas para pesquisa
    marcas = [
        "AUTO PARVI CENTER", "Land Rover Way - João Pessoa", "Land Rover Way - MANAUS", 
        "Land Rover Way - RECIFE", "Land Rover Way - SALVADOR", "Land Rover Way - SAO LUIS", 
        "Bremen Volkswagen Aeroporto - São Luís MA", "BREMEN - AFOGADOS", "Audi Recife: Carros Audi", 
        "BREMEN - BEQUIMAO", "BREMEN - BOA VIAGEM", "BREMEN - BONGI", "BREMEN - CARUARU", 
        "Bremen Volkswagen - Feira de Santana BA", "BREMEN - HOLANDESES", "BREMEN - IMBIRIBEIRA", 
        "BREMEN - OLINDA", "Bremen Volkswagen Retiro Salvador BA", "BREMEN - SALVADOR SHOPPING", 
        "BYD - AFOGADOS", "BYD - BOA VISTA RR", "BYD - CARUARU", "BYD - IMBIRIBEIRA", "BYD - JOÃO PESSOA", 
        "Parvi BYD - MANAUS", "BYD - PATAMARES", "BYD - RECIFE", "BYD - RETIRO Salvador", 
        "FIORI - AFOGADOS", "FIORI - BONGI", "FIORI - CAMPINA GRANDE", "FIORI - JOAO PESSOA", 
        "FIORI - OLINDA", "FIORI - PARALELA", "Fiori Fiat Retiro - Salvador BA", "FIORI - SALVADOR SHOPPING", 
        "FIORI JEEP - AFOGADOS (PE)", "FIORI JEEP - BALSAS (MA)", "FIORI JEEP - BOA VISTA (RR)", 
        "FIORI JEEP - CAMPINA GRANDE", "FIORI JEEP - FEIRA DE SANTANA", "FIORI JEEP - IMPERATRIZ MA", 
        "FIORI JEEP - LAURO FREITAS(BA)", "FIORI JEEP - MANAUS (AM)", "FIORI JEEP - MARABA (PA)", 
        "FIORI JEEP - PARALELA (BA)", "FIORI JEEP - PARAUAPEBAS (PA)", "FIORI JEEP - RETIRO (BA)", 
        "FIORI JEEP - RUI BARBOSA (PE)", "MARDISA - ARACAJU", "Mardisa Manaus - AM Chapada", "MARDISA - RECIFE", 
        "MARDISA - SAO LUIS MA Holandeses", "MARDISA AGRO - FENDT BALSAS", "MARDISA AGRO - FENDT URUCUI", 
        "MARDISA AGRO - VALTRA BALSAS", "MARDISA AGRO -FENDT IMPERATRIZ MA Maranhão Novo, Imperatriz - MA,", 
        "MARDISA AGRO MASSEY - BALSAS", "Fendt - Mardisa Agro Rodovia BR 010, Km 1,5, s/n - Maranhão Novo, Imperatriz - MA, 65903-140", 
        "MARDISA AGRO MASSEY - SAO LUIS", "MARDISA AGRO MASSEY - SERGIPE", "MARDISA AGRO MASSEY - TERESINA", 
        "MARDISA AGRO MASSEY -BOA VISTA Nossa Sra. do Socorro - SE", "MARDISA AGRO VALTRA IMPERATRIZ", 
        "MARDISA VEICULOS - BOA VISTA", "MARDISA VEICULOS - BRASILIA", "MARDISA VEICULOS - CAMPOS dos Goytacazes", 
        "MARDISA VEICULOS - FLORIANO", "MARDISA VEICULOS - ITABAIANA", "MARDISA VEICULOS - ITAQUI Maranhão são luis", 
        "MARDISA VEICULOS - LUZIANIA", "MARDISA VEICULOS - MANAUS Da Paz, Manaus", "MARDISA VEICULOS - PALMARES", 
        "MARDISA VEICULOS - PETROPOLIS", "MARDISA VEICULOS - SAO GONCALO", "MARDISA VEICULOS - SAO LUIS Tirirical, São Luís - MA", 
        "MARDISA VEICULOS - SERGIPE R. Sessenta Nove Palestina, Nossa Sra. do Socorro - SE", "MARDISA VEICULOS - TANGUA", 
        "MARDISA VEICULOS - TERESINA", "MARDISA VEICULOS - TERESOPOLIS", "MARDISA VEICULOS - URUCUI", 
        "Auto Parvi Aeroporto sao luis", "Auto PARVI - AFOGADOS", "Auto AUTO PARVI - CAMPINA GRANDE", "AUTO PARVI - CENTER", 
        "AUTO PARVI - FEIRA DE SANTANA BA", "AUTO PARVI - AFOGADOS", "AUTO PARVI - JOAO PESSOA", "AUTO PARVI - MANAUS AM CHAPADA", 
        "AUTO PARVI - OLINDA", "AUTO PARVI - PARALELA BAHIA", "AUTO PARVI Shopping SSA - Salvador BA", "AUTO PARVI - PETROLINA", 
        "AUTO PARVI - RUI BARBOSA", "AUTO PARVI - SAO LUIS Holandeses", "AUTO PARVI - WAY", "Parvi Logística: Empilhadeiras, Peças, Manutenção", 
        "PATEO BEQUIMAO - MA", "PATEO BONGI - PE", "PATEO FEIRA - BA", "PATEO HOLANDESES - MA", "PATEO ILHA DO RETIRO - PE", 
        "PATEO JOAO PESSOA - PB", "PATEO MANAUS - AM manaus", "Hyundai HMB Pateo Olinda: Concessionária, Carros Novos", 
        "PATEO PIEDADE - PE", "PATEO RETIRO - BA", "TOYOLEX TIRIRICAL", "TOYOLEX AFOGADOS", "TOYOLEX AFOGADOS (BAIXADA)", 
        "TOYOLEX ARACAJU", "TOYOLEX BOA VISTA", "TOYOLEX CAICO", "TOYOLEX CARPINA SEMINOVOS", "TOYOLEX CARUARU", 
        "TOYOLEX GARANHUNS", "TOYOLEX IMBIRIBEIRA", "TOYOLEX MANAUS", "TOYOLEX MOSSORO", "TOYOLEX NATAL", "TOYOLEX OLINDA", 
        "TOYOLEX PETROLINA", "TOYOLEX RUI BARBOSA", "TOYOLEX SAO LUIS CALHAU", "TOYOLEX SERRA TALHADA", "TOYOLEX VEICULOS - LEXUS imbiribeira"
    ]

    # Acessar o Google
    navegador.get("https://www.google.com/")
    navegador.implicitly_wait(10)

    # Coletar as notas de avaliação das lojas
    dados_lojas = pesquisar_e_coletar_notas(navegador, marcas)

    # Fechar o navegador
    print("Fechando o navegador")
    navegador.quit()
    print("Navegador fechado com sucesso")

    # Criar DataFrame com os dados coletados e salvar em um arquivo Excel
    df = pd.DataFrame(dados_lojas)

    # Importando a biblioteca necessária para conectar ao banco de dados
    engine = create_engine('mssql+pymssql://sa:Vinilu@2219@N81PVYURY\\SQLEXPRESS:1433/Stage')

    # Inserindo os dados no banco de dados
    df.to_sql(
        name='GoogleAvaliacao',
        con=engine,
        if_exists='replace',
        index=False
    )

    # Fechar a conexão com o banco de dados
    engine.dispose()
    print("Fechando conexão com o Banco...")

# Função para verificar se é dia 13 e executar a automação
def verificar_e_agendar_pesquisa():
    if datetime.now().day == 13:
        agendar_pesquisa()

# Agendamento com schedule
schedule.every().day.at("09:23").do(verificar_e_agendar_pesquisa)

print("Agendador configurado. Aguardando execução...")

while True:
    schedule.run_pending()
    time.sleep(1)  