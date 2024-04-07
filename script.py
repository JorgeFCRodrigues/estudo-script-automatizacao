import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Definindo a variável principal junto a leitura da planilha e definindo quais
# colunas ler e qual linha começar
planilha = 'Consulta_CPF_Base.xlsx'
url_CPF = 'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp'
df_planilha = pd.read_excel(
    planilha,
    header=3)

# Mudando o tipo de dado da planilha e colocando os ZEROS no CPF
df_planilha['CPF'] = df_planilha['CPF'].astype('string')
df_planilha['CPF'] = df_planilha['CPF'].str.zfill(11)
df_planilha['SITUAÇÃO'] = df_planilha['SITUAÇÃO'].astype('string')
df_planilha['Dt_NASC'] = pd.to_datetime(df_planilha['Dt_NASC'])
df_planilha['Dt_NASC'] = df_planilha['Dt_NASC'].dt.strftime('%d/%m/%Y')
df_planilha['Dt_NASC'] = df_planilha['Dt_NASC'].astype('string')

for index, row in df_planilha.iterrows():
    print('Index: ' + str(index) + 'O CPF é ' + row['CPF'])
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    chrome = webdriver.Chrome()

    chrome.get(url_CPF)

    time.sleep(3)

    elemento_CPF = chrome.find_element(
        By.XPATH, '//*[@id="txtCPF"]')
    elemento_Dt_Nasc = chrome.find_element(
        By.XPATH, '//*[@id="txtDataNascimento"]')

    elemento_CPF.send_keys(row['CPF'])
    elemento_Dt_Nasc.send_keys(row['Dt_NASC'])
    # chrome.find_element(By.XPATH, '//*[@id="id_submit"]').click()


chrome.quit
