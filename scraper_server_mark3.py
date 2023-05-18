from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep, time
import random
from bs4 import BeautifulSoup as bs
import csv
import json
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(di, df, es, mei):

    port = 465  # For SSL
    sender_email = "exemplo@email.com"
    receiver_email = "exemplo@email.com"
    subject = "Extracao de dados"
    body = f"Numeros de celular das empresas abertas entre {di[-2]}{di[-1]}/{di[-5]}{di[-4]}/{di[-10]}{di[-9]}{di[-8]}{di[-7]} e {df[-2]}{df[-1]}/{df[-5]}{df[-4]}/{df[-10]}{df[-9]}{df[-8]}{df[-7]} no estado de {es}, Opçao Excluir MEI: {mei}"

    password ="ycmoccqyxggsrivv" #"meuemail12"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    filename = f"{di} -- {df} {es}.txt"



    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    part.add_header(
      "Content-Disposition",
      f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()


    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:

        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    print(f'\n\nArquivo "{filename}" enviado com sucesso\n\nEmail utilizado para o envio: {sender_email}\n\nEmail que recebeu o arquivo: {receiver_email}')

    return 0



def fazer_txt(lista_nums, data_ini, data_final, abre_estado):
    arq = open(f"{data_ini} -- {data_final} {abre_estado}.txt", "w")
    for r in lista_nums:
        arq.write(f"{r}\n")
    arq.close()
    print('\nArquivo TXT criado com sucesso')
    return 0


def fazer_csv(nome, header, dados):





    with open(f'{nome}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(dados)

    print('\nArquivo CSV criado com sucesso')

    return 0



def scrap_nome(html):

    b_element = html.find('b')
    socio = scrap_socio(b_element)

    if socio != None:
        return socio

    elif socio == None:
        p_list = html.find_all('p')
        razao = scrap_razao(p_list)

        if razao == None:
            return None
        
        else:
            return razao



def scrap_razao(p_list):
    
    for x in p_list:
        texto = x.text
        
        if "Social" in texto:
            
            y = x.next_sibling
           
            z = y.next_sibling
            
            txtz = z.text
            
            return str(txtz)

    return None

def scrap_socio(b_element):


    if b_element != None:

        socio = b_element.text
        print(socio)
    
        return str(socio)
        


    else:
        
        return None





def scrap_email(a_list):
    for i in a_list:
        href = i.get('href')

        try:
            if "mailto:" in href:
                print(href[7:])
                return href[7:]
            

        

        except Exception as e:
            print(f"Erro: {e}")
            
            pass
            #pass

    return None



def scrap_num(driver, a_list, nums_list):
    

    for i in a_list:
        href = i.get('href')

        try:
            if "tel:" in href and  "000" not in href and len(href.replace(" ", "")) > 10 and "9999" not in href:
                hrefsplited = href.split(" ")
                hrefsplited[1] = "9" + hrefsplited[1]
                hrefatt = " ".join(hrefsplited)
                
                if hrefatt[4:] not in nums_list:
                    if hrefatt[4:6] == "55":
                        return hrefatt[6:]
                        
                    else: 
                        
                        return hrefatt[4:]
            

        

        except Exception as e:
            print(f"Erro: {e}")
            pass
            

    return None

def processar_cnae(atividade_princi_cnae):
    if atividade_princi_cnae == "":
        print("cnae vazio")
        return ""
    else:
        string_temp = '\\", \\"'.join(atividade_princi_cnae)
        string_final = '\\"'+string_temp+'\\"'

        return string_final



def scrap_info(driver, urls_list, somente_nums):
    try:
        count_email_invalido = 0
        count_nome_invalido = 0
        count_tel_invalido = 0

        info_list = []
        count = 0
        for url in urls_list:

            count=count+1
            
            try:
                busi_page_html = driver.execute_script('return fetch("'+url+r'''", {
              "headers": {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "sec-fetch-user": "?0"
              },
              "referrer": "https://casadosdados.com.br/solucao/cnpj/pesquisa-avancada",
              "referrerPolicy": "strict-origin-when-cross-origin",
              "body": null,
              "method": "GET",
              "mode": "cors"
            }).then((response) => response.text())''')

                #inter = round(random.uniform(0.1,0.45), 2)
                #print(inter)
                #sleep(inter)
                html = bs(busi_page_html, "html.parser")

                a_list = html.find_all('a')

                if somente_nums == True:


                    num = scrap_num(driver, a_list, info_list)
                
                    if num != None:

                        info_list.append(num)

                    print(count)

                if somente_nums == False:

                    num = scrap_num(driver, a_list, info_list)

                    



                    email = scrap_email(a_list)
                    
                    nome = scrap_nome(html)

                    if " " not in nome or nome == None:

                        count_nome_invalido = count_nome_invalido + 1

                        continue


                    
                    nome_completo = nome.split(" ")
                    fn = nome_completo[0]
                    ln = nome_completo[-1]



                    if num == None:

                        count_tel_invalido = count_tel_invalido + 1
                        continue


                    if email == None:

                        count_email_invalido = count_email_invalido+1
                        continue
                    


                    num2 = "55"+num
                    num2 = num2.replace(" ",  "")

                    

                    temp_list = [str(fn), str(ln), str(num2), str(email)]

                    info_list.append(temp_list)

                    print(count)

            except Exception as e:
                print(f"Erro: {e}")
                continue

            


        # nums => ["871238", "41387983", "918430"]
        # todas infos => [["maria dos santos", "61998431", "oi@gmail.com"], ]
            

        return [info_list, count_nome_invalido, count_email_invalido, count_tel_invalido]
    except Exception as e:
        print(f"Erro: {e}")
        return [info_list, count_nome_invalido, count_email_invalido, count_tel_invalido]
    except KeyboardInterrupt:
        return [info_list, count_nome_invalido, count_email_invalido, count_tel_invalido]


        


    # nums => ["871238", "41387983", "918430"]
    # todas infos => [["maria dos santos", "61998431", "oi@gmail.com"], ]
        

    

def scrap_urls(driver, data_ini, data_final, cidade, abre_estado, mei_url_string, atividade_princi_cnae_string, com_email_url_string, salvar_json=False):


    names_and_cnpjs_list = []
    urls_list = []

    if abre_estado == "NH":
        abre_estado_url_string = ""

    else:
        abre_estado_url_string = f'\\"{abre_estado}\\"'

    
    for page in range(1, 50):

        page_str = str(page)

        data = '{\\"query\\":{\\"termo\\":[],\\"atividade_principal\\":['+atividade_princi_cnae_string+'],\\"natureza_juridica\\":[],\\"uf\\":['+abre_estado_url_string+'],\\"municipio\\":['+cidade+'],\\"situacao_cadastral\\":\\"ATIVA\\",\\"cep\\":[],\\"ddd\\":[]},\\"range_query\\":{\\"data_abertura\\":{\\"lte\\":\\"'+data_final+'\\",\\"gte\\":\\"'+data_ini+'\\"},\\"capital_social\\":{\\"lte\\":null,\\"gte\\":null}},\\"extras\\":{\\"somente_mei\\":false,\\"excluir_mei\\":'+str(mei_url_string)+',\\"com_email\\":'+str(com_email_url_string)+',\\"incluir_atividade_secundaria\\":false,\\"com_contato_telefonico\\":false,\\"somente_fixo\\":false,\\"somente_celular\\":true,\\"somente_matriz\\":false,\\"somente_filial\\":false},\\"page\\":'+page_str+'}'

        cnpjs_and_names_dict = driver.execute_script(f'''return fetch("https://api.casadosdados.com.br/v2/public/cnpj/search", {{
        "headers": {{
          "accept": "application/json, text/plain, */*",
          "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
          "cache-control": "no-cache",
          "content-type": "application/json;charset=UTF-8",
          "pragma": "no-cache",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-site"
        }},
        "referrer": "https://casadosdados.com.br/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": "{data}",
        "method": "POST",
        "mode": "cors"
      }}).then((response) => response.json()).catch((response)=> response.text())''')

        try:

            cnpjs = cnpjs_and_names_dict['data']['cnpj']

            for y in cnpjs:
                nome = y['razao_social']
                cnpj = y['cnpj']
                names_and_cnpjs_list.append([nome, cnpj])
      
        except:
            break

        #inter = round(random.uniform(0.1,0.8), 2)
      
        #sleep(inter)

    for name_and_cnpj_pair in names_and_cnpjs_list:

        name = (name_and_cnpj_pair[0].replace(" ", "-")).lower()

        url = "https://casadosdados.com.br/solucao/cnpj/"+name+"-"+str(name_and_cnpj_pair[1])

        urls_list.append(url)

    if salvar_json:

        with open("salvar_urls5.json", "w") as f:

            json.dump(urls_list, f)

    return urls_list



def start_selenium(disable_security = True, headless = True):

    print('\nFuncao do driver iniciada\n')
    chromedriver = "./chromedriver105"
    options = webdriver.ChromeOptions()
    # options.binary_location = 'Chrome-bin/chrome.exe'


 
#   ua = UserAgent()
#   a = ua.random
#   user_agent = ua.random
    user_agent="Mozilla/5.0 (X11; CrOS x86_64 14388.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.91 Safari/537.36"
    s=Service(chromedriver)
    options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
    
    if disable_security == True:

        options.add_argument("--disable-web-security")
    
    options.add_argument("--disable-gpu")
    
    if headless == True:

        options.add_argument('--headless')
    
    options.add_argument('--no-sandbox')
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument('--log-level=3')
                                                                                                            
    driver = webdriver.Chrome(service=s, options=options)

    print("\nFuncao do driver finalizada: driver inicializado com sucesso\n")
    
    return driver

def main(data_ini_func, data_final_func, abre_estado_func, mei_func, somente_nums, csv_ou_txt, com_email_func="desativado", atividade_princi_cnae_func="", cidade_func="", enviar_por_email=False):

    cidade=cidade_func

    #input cnae = lista com os cnaes, elementos tem que ser strings

    atividade_princi_cnae = atividade_princi_cnae_func



    # processar_cnae retorna string pra por na query dos cnaes

    atividade_princi_cnae_string = processar_cnae(atividade_princi_cnae)

    data_ini=data_ini_func

    data_final=data_final_func

    abre_estado=abre_estado_func.strip()

    abre_estado=abre_estado.upper()

    mei_url_string = ""
    
    mei = mei_func.strip()

    mei = mei.lower()

    com_email_url_string = ""
    
    com_email = com_email_func.strip()

    com_email = com_email.lower()

    if com_email == "ativado":
        com_email_url_string = "true"

    elif com_email == "desativado":
        com_email_url_string = "false"

    if mei == "ativado":
        mei_url_string = "true"

    elif mei == "desativado":
        mei_url_string = "false"

    else:
        return 0


    print(f"\n\nIniciado: \nData Inicial: {data_ini}\nData Final: {data_final}\nEstado: {abre_estado}\nApenas MEI: {mei}\nApenas MEI (STRING): {mei_url_string}")


    #if abre_estado not in ["SP", "RJ", "MG", "GO", "SC", "DF", "NH"]:
    #    return 0


    estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
    #estados = ["AC","AL","AP", "CE", "DF"]

    driver = start_selenium()

    if abre_estado == "TD":

        urls_list_final = []
        
        for est in estados:

            urls_list = scrap_urls(driver, data_ini, data_final, cidade, est, mei_url_string, atividade_princi_cnae_string, com_email_url_string)
            
            urls_list_final.extend(urls_list)

    elif abre_estado in estados or abre_estado == "NH": 


        #scrap_urls(driver, data_ini, data_final, cidade, abre_estado, mei_url_string, atividade_princi_cnae)
        #scrap_urls - retorna lista com as urls das paginas

        

        urls_list_final = scrap_urls(driver, data_ini, data_final, cidade, abre_estado, mei_url_string, atividade_princi_cnae_string, com_email_url_string, True)

    else:
        driver.quit()
        return 0

    #print(urls_list_final)
    
    scrap_return = scrap_info(driver, urls_list_final, somente_nums)

    info_list = scrap_return[0]

        


    print(len(info_list))

    print(f"\nNumero de Razoes None: {scrap_return[1]}")

    if csv_ou_txt == "csv":

        fazer_csv("novo23", ['fn', 'ln', 'phone', 'email'], info_list)

    elif csv_ou_txt == "txt":

        fazer_txt(info_list, data_ini, data_final, abre_estado)

    else:

        print("Missing or invalid file type for saving info")
        driver.quit()

        return 0

    if enviar_por_email == True:
        send_email(data_ini, data_final, abre_estado, mei_func)


    print(f"\n\nFinalizado:\n\nData Inicial: {data_ini}\n\nData Final: {data_final}\n\nEstado: {abre_estado}\n\nApenas MEI: {mei}\n\nApenas MEI (STRING): {mei_url_string}")
    print(f"\nFormato de arquivo: {csv_ou_txt}\n\nNumero de razoes/socios invalidos: {scrap_return[1]}\n\nNumero de emails invalidos: {scrap_return[2]}\n\nNumero de tels invalidos: {scrap_return[3]}")
    print(f"\nTamanho da lista de URLs: {len(urls_list_final)}\n\nTamanho da lista de dados ou da lista de telefones: {len(info_list)}")
    driver.quit()



    return 0




#main("2022-03-02", "2022-03-03", "AC", "Ativado", com_email_func="Desativado", somente_nums=True, csv_ou_txt="txt",enviar_por_email=True)

