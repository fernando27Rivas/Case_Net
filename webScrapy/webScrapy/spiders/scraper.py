# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from webScrapy.items import WebscrapyItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime,timedelta
import csv
from selenium.webdriver.support.ui import Select
from .. import settings
from selenium.common.exceptions import NoSuchElementException

class ScraperSpider(CrawlSpider):
    name = 'scraper'
    allowed_domains = ['courts.mo.gov']
    search_url = 'https://www.courts.mo.gov/casenet/cases/calendarSearch.do'
    start_urls = ['https://www.courts.mo.gov/casenet/cases/calendarSearch.do']


    def parse(self, response):
        url = "https://www.courts.mo.gov/casenet/cases/calendarSearch.do"
        first_name = ""
        last_name = ""
        addres_petitioner = ""
        city_petitioner = ""
        state_petitioner = ""
        zip_petitioner = ""
        city_descendent = ""
        addres_descendent = ""
        state_descendent = ""
        zip_descendent = ""
        save_csv=None


        choice = settings.SELECT
        choice2 = settings.Judge

        choice3=settings.SELECT2
        choice4=settings.Judge2



        browser = webdriver.Chrome("C:/chromedriver.exe")
        #browser = webdriver.Chrome("/usr/local/bin/chromedriver")
        browser.get(url)
        time.sleep(4)
        
        select_box = Select(browser.find_element_by_id("courtId"))
        select_box.select_by_visible_text(choice)
        time.sleep(4)
        select2_box = Select(browser.find_element_by_id("JudgeId"))
        select2_box.select_by_visible_text(choice2)
        browser.find_element_by_css_selector("input#sevenDayRadio").click()
        browser.find_element_by_css_selector("input#judgeSortByPet").click()
        time.sleep(10)
        browser.find_element_by_id("findButton").click()
        time.sleep(3)


        try:
             time.sleep(8)
             pagination = browser.find_element_by_xpath("//tr[3]/td/table/tbody/tr[2]/td/form/table/tbody/tr").text
        except:
            pass
            print("Error en obtener la cantidad de paginas")


        pagination=pagination.split(" ")

        if(len(pagination)>10):
            for x in pagination:
                print("Numero de Pagina"+ str(x))


            hasNext=pagination[-4]
            print(hasNext)
            if (hasNext == "[Next"):
                last_page=pagination[-1]
                try:
                 last_page=last_page.split("]")[0]
                 print("Cantidad de Paginas mayor a 10")
                except:
                    pass
                    print("Cantidad de paginas menor a 10")
                    #last_page=pagination[-1]
        else:
            last_page = pagination[-1]





        print("LA ULTIMA PAGINA ES: "+str(last_page))


        try:
             initial_page=browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td/span").text
        except NoSuchElementException:
              pass
              time.sleep(2)
              initial_page = browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td/span").text

        initial_page=int(initial_page)



        while(initial_page<=int(last_page)):
          print("Inicio de Pagina:" + str(initial_page))

          if(initial_page!=1):
              try:
                 if(initial_page>11):
                     initial_page=3
                     print("Estamos en la pagina:" + str(initial_page + 9))
                 else:
                     print("Estamos en la pagina:" + str(initial_page ))
                 try:
                    browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td["+str(initial_page)+"]/a").click()
                 except NoSuchElementException:
                     pass
                     time.sleep(2)
                     browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td[" + str(initial_page) + "]/a").click()




              except NoSuchElementException:
                  pass
                  print("Error en la paginacion")

          #time.sleep(10)

          i=3
        #search=false
          while(i<16):
            try :
                 time.sleep(6)
                 rest=browser.find_element_by_xpath("//tr["+str(i)+"]//td[contains(@class, 'td')][2]").text
            except NoSuchElementException:
                         pass
                         print("Error en la Busqueda de Elementos")
                         try:
                            time.sleep(4)
                            rest = browser.find_element_by_xpath(
                                "//tr[" + str(i) + "]//td[contains(@class, 'td')][2]").text

                         except NoSuchElementException:
                                print("'SALTO DE TABLA!!")
                                pass
                                i=i+2
                                try:
                                    time.sleep(6)
                                    rest = browser.find_element_by_xpath( "//tr[" + str(i) + "]//td[contains(@class, 'td')][2]").text
                                except NoSuchElementException:
                                    pass
                                    time.sleep(5)
                                    print("Final del Scraper")


            if(rest is not None):

               print(rest)
               result= rest.split(',')
               print(result)

               for x in result:
                   if(x == " DECEASED "):
                       try:
                          time.sleep(3)
                          browser.find_element_by_xpath("//tr["+str(i)+"]//td[contains(@class, 'td')][1]/a").click()
                       except NoSuchElementException:
                          pass
                          browser.find_element_by_xpath("//tr[" + str(i) + "]//td[contains(@class, 'td')][1]/a").click()
                          print("Error in search DECEASED")
                       time.sleep(3)
                       try:
                            browser.find_element_by_xpath("//tr/td/a/img[contains(@name,'parties')]").click()
                       except NoSuchElementException:
                           pass
                           print("Error in select a parties")
                           time.sleep(5)
                           browser.find_element_by_xpath("//tr/td/a/img[contains(@name,'parties')]").click()
                       #time.sleep(2)
                       p=1
                       s=0
                       while(p<10):
                        try:
                            time.sleep(3)
                            result_path=browser.find_element_by_xpath("//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr["+str(p)+"]/td[contains(@class, 'detailSeperator')][2]").text
                        except NoSuchElementException:
                            pass
                            print("Error en Iteracion de variables P")

                            try:
                                time.sleep(3)
                                print("Segundo Error en la Iteracion de Varble P")
                                result_path = browser.find_element_by_xpath(
                                    "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                        p) + "]/td[contains(@class, 'detailSeperator')][2]").text
                            except NoSuchElementException:
                                pass
                                print("Tercer error de Iteracion en P")
                                time.sleep(4)
                                result_path = browser.find_element_by_xpath(
                                    "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                        p) + "]/td[contains(@class, 'detailSeperator')][2]").text
                        p=p+2
                        s=s+2
                        print( "El resultado de la path es:"+ str(result_path))
                        res_petitioner=result_path.split(',')
                        first_name= res_petitioner[0]
                        last_name = res_petitioner[1]

                        print(res_petitioner)
                        for x in res_petitioner:
                            temp=x.rstrip()
                            temp=temp.lstrip()
                            if(temp == "Petitioner" or temp== "Applicant" or temp == "Personal Representative"or temp== "Respondent" ):
                                 print(temp)
                                 try:
                                    time.sleep(5)
                                    petitioner_info=browser.find_element_by_xpath("//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr["+ str(s)+"]/td[contains(@class, 'detailData')][2]").text
                                 except NoSuchElementException:
                                     pass
                                     print("Error en obtener el Pettitioner")
                                 petitioner_split=petitioner_info.split(',')
                                 if( len(petitioner_info)>1):
                                     p=10
                                     var_city=1
                                     var_temp = 1
                                     save_csv=True
                                     for x in petitioner_split:
                                         temp2=x.rstrip()
                                         temp2=temp2.lstrip()
                                         print("Data de Responsable en Iteracion:"+ str(var_city))
                                         print(temp2)
                                         if(var_city==1):
                                            temp3=temp2.split(sep="\n")
                                            print("Valor de var_city: " +str(var_city))
                                            for y in temp3:
                                                print("Valor de Y en iteracion:" + str(var_temp))
                                                if(var_temp==1):
                                                    print(y)
                                                    addres_petitioner=y
                                                else:
                                                    if(var_temp==2):
                                                        print(y)
                                                        city_petitioner=y
                                                var_temp=var_temp+1
                                         else:
                                             if(var_city==2):
                                                 temp3 = temp2.split(sep="\n")
                                                 temp4=list(filter(None, temp3))
                                                 var_temp3=1
                                                 if(var_temp3==1):
                                                    for z in temp4:
                                                        print("Iteracion Numero :"+ str(var_temp3))
                                                        print("Valor temp4 separado "+ str(z))
                                                        if(var_temp3==1):
                                                            var_temp3=var_temp3+1
                                                            print("Primer valor de temp4: "+ str(z))
                                                            code=str(z)
                                                            code=code.split()
                                                            print("Valor de Code Separado:")
                                                            print(code)
                                                            value_q=1
                                                            for q in code:
                                                                 if(value_q==1):
                                                                    print("Primer valor de Code:"+ str(q))
                                                                    state_petitioner=q
                                                                    print("Estado del Petitioner: "+ str(state_petitioner))
                                                                 else:
                                                                    if(value_q==2):
                                                                      print("Segundo valor de Code:" + str(q))
                                                                      zip_petitioner=q
                                                                      print("Codigo Postal del Petitioner: " + str(zip_petitioner))
                                                                 value_q=value_q+1
                                                                 print("Afuera de los if else el valor de Code es :" + str(q))

                                                 print("Valor de var_city en la Segunda Iteracion: " + str(var_city))
                                         var_city=var_city+1
                                 else:
                                     save_csv=False

                                 t=1
                                 r=0
                                 while (t < 10):
                                     try:
                                         decendent = browser.find_element_by_xpath(
                                             "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                 t) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                     except NoSuchElementException:
                                         pass
                                         print("Error en Iteracion de variables T")
                                         try:
                                             time.sleep(4)
                                             decendent = browser.find_element_by_xpath(
                                                 "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                     t) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                         except NoSuchElementException:
                                             pass
                                             print("Segundo error de Iteracion en T")
                                             time.sleep(5)
                                             decendent = browser.find_element_by_xpath(
                                                 "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                     t) + "]/td[contains(@class, 'detailSeperator')][2]").text

                                     t = t + 2
                                     r = r + 2
                                     print(decendent)
                                     res_decendent = decendent.split(',')
                                     print(res_decendent)
                                     for x in res_decendent:
                                         temp = x.rstrip()
                                         temp = temp.lstrip()
                                         decendent_second=""
                                         if (temp == "Decedent"):
                                             print(temp)
                                             try:
                                               time.sleep(3)
                                               print("Primer error de Iteracion en T Para verificar Segundo Deceaced")
                                               decendent_second = browser.find_element_by_xpath(
                                                 "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                     t) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                             except NoSuchElementException:
                                                 pass
                                                 print("Segundo error de Iteracion en T Para verificar Segundo Deceaced")
                                                 time.sleep(5)
                                                 decendent_second = browser.find_element_by_xpath(
                                                     "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                         t) + "]/td[contains(@class, 'detailSeperator')][2]").text


                                             print(decendent_second)
                                             res_second= decendent_second.split(',')
                                             print(res_second)
                                             for u in res_second:
                                                 temp_second = u.rstrip()
                                                 temp_second = temp_second.lstrip()
                                                 if(temp_second=="Decedent"):
                                                     print("Data Correcta de Descendent ERA esta!!")
                                                     r=r+2
                                                     t=10
                                             t=10

                                             try:
                                                 time.sleep(5)
                                                 decendet_info = browser.find_element_by_xpath(
                                                     "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                         r) + "]/td[contains(@class, 'detailData')][2]").text
                                             except NoSuchElementException:
                                                 pass
                                                 print("Error en obtener el Descendent")
                                                 time.sleep(5)
                                                 decendet_info = browser.find_element_by_xpath(
                                                     "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                         r) + "]/td[contains(@class, 'detailData')][2]").text

                                             decendent_split = decendet_info.split(",")
                                             decendent_split_len=decendet_info.split(sep="\n")
                                             print("El dato dividido inicial de Deceaced es :")
                                             print(decendent_split_len)
                                             var_decision=len(decendent_split_len)
                                             print("El tamañao de la informacion de decendent es: "+ str(var_decision))
                                             for M in decendent_split_len:
                                                 if("Date of Death" in M):
                                                     var_decision= var_decision - 1
                                                     print("Se encontro un Date of death")
                                                 else:
                                                     if("Year of Birth" in M):
                                                         var_decision = var_decision - 1
                                                         print("Se encontro un Year of Birth")
                                                     else:
                                                         if("Party End Reason" in M):
                                                             var_decision = var_decision - 1
                                                             print("Se encontro un Party")



                                             print("Valor final del tamaño de Datos del Decedent" + str(var_decision))
                                             if(var_decision>2):
                                                 t = 10
                                                 var_descent = 1
                                                 var_temp_des = 1
                                                 save_csv=True
                                                 for x in decendent_split:
                                                     temp2 = x.rstrip()
                                                     temp2 = temp2.lstrip()
                                                     print("Data de Descendent")
                                                     print(temp2)
                                                     if (var_descent == 1):
                                                         temp4 = temp2.split(sep="\n")
                                                         print("Valor de var_descent: " + str(var_descent))
                                                         for F in temp4:
                                                             print("Valor de F en iteracion:" + str(var_temp_des))
                                                             if (var_temp_des == 1):
                                                                 print(F)
                                                                 addres_descendent = F
                                                                 print("ADRRES de DECENDENT: "+ str(addres_descendent))
                                                             else:
                                                                 if (var_temp_des == 2):
                                                                     print(F)
                                                                     city_descendent = F
                                                                     print("CITY de DECENDENT: " + str(city_descendent))
                                                             var_temp_des = var_temp_des + 1

                                                     else:
                                                         if (var_descent == 2):
                                                             temp4 = temp2.split(sep="\n")
                                                             temp9 = list(filter(None, temp4))
                                                             var_temp4 = 1
                                                             if (var_temp4 == 1):
                                                                 for z in temp4:
                                                                     print(
                                                                         "Iteracion de DECENDENT Numero :" + str(var_temp4))
                                                                     print("Valor DECENDENT temp4 separado " + str(z))

                                                                     if (var_temp4 == 1):
                                                                         var_temp4 = var_temp4 + 1
                                                                         print("Primer valor de temp4 DECENDENT: " + str(z))
                                                                         code_desc = str(z)
                                                                         code_desc = code_desc.split()
                                                                         print("Valor de Code DECENDENT Separado:")
                                                                         print(code_desc)
                                                                         value_q = 1
                                                                         for q in code_desc:
                                                                             if (value_q == 1):
                                                                                 print(
                                                                                     "Primer valor de DECENDENT code_desc:" + str(
                                                                                         q))
                                                                                 state_descendent = q
                                                                                 print("Estado del DECENDENT: " + str(
                                                                                     state_descendent))
                                                                             else:
                                                                                 if (value_q == 2):
                                                                                     print(
                                                                                         "Segundo valor de DECENDENT Codigo Postal:" + str(
                                                                                             q))
                                                                                     zip_descendent = q
                                                                                     print(
                                                                                         "Codigo Postal del DECENDENT: " + str(
                                                                                             zip_descendent))
                                                                             value_q = value_q + 1
                                                             print("Valor de var_descent en la Segunda Iteracion: " + str(
                                                                 var_descent))
                                                     var_descent=var_descent+1
                                             else:
                                                 print("El tamaño de la infor de decesead es Menor a 1  ")
                                                 save_csv=False




                       browser.back()
                       time.sleep(5)
                       try:
                          case=browser.find_element_by_xpath("//table[contains(@class,'detailRecordTable')]/tbody/tr[2]/td[4]").text
                          print("El tipo de caso es:" + str(case))
                       except:
                           pass
                           print("Error in type case")

                       if(save_csv):
                           with open('data.csv', 'a') as csvFile:
                               data_writer = csv.writer(csvFile)
                               data_writer.writerow( [ first_name,last_name ,addres_petitioner,city_petitioner,
                                                       state_petitioner,zip_petitioner,addres_descendent,city_descendent,state_descendent,zip_descendent,case  ] )
                       else:
                           print("El elemento no se agrego Ya que no posee Suficientes datos.")
                       browser.back()

               i=i+2   

            else:
               i=i+2

          print("LLEGANDO A FIN DE LA PAGINA")
          initial_page=initial_page+1

          if(initial_page>11):
              print("LA SIGUIENTE  PAGINA ES : " + str(initial_page+9))
          else:
             print("LA SIGUIENTE  PAGINA ES : " + str(initial_page))




                       



        
        browser.close()


