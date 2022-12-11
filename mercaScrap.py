#!/usr/bin/python3
# -*- coding: utf-8 -*-
#By: Zanderc0de

import os
import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore,init

init()

#PARA LIMPIAR LA PANTALLA TANTO EN LINUX COMO EN WINDOWS
clearConsole = lambda: os.system('cls' if os.name=='nt' else 'clear')


#COLORES
color_rojo = Fore.LIGHTRED_EX
color_azul = Fore.LIGHTBLUE_EX
color_blanco = Fore.LIGHTWHITE_EX
color_verde = Fore.LIGHTGREEN_EX


def banner():

    text = """
    • ▌ ▄ ·. ▄▄▄ .▄▄▄   ▄▄·  ▄▄▄· .▄▄ ·  ▄▄· ▄▄▄   ▄▄▄·  ▄▄▄·
    ·██ ▐███▪▀▄.▀·▀▄ █·▐█ ▌▪▐█ ▀█ ▐█ ▀. ▐█ ▌▪▀▄ █·▐█ ▀█ ▐█ ▄█
    ▐█ ▌▐▌▐█·▐▀▀▪▄▐▀▀▄ ██ ▄▄▄█▀▀█ ▄▀▀▀█▄██ ▄▄▐▀▀▄ ▄█▀▀█  ██▀·
    ██ ██▌▐█▌▐█▄▄▌▐█•█▌▐███▌▐█ ▪▐▌▐█▄▪▐█▐███▌▐█•█▌▐█ ▪▐▌▐█▪·•
    ▀▀  █▪▀▀▀ ▀▀▀ .▀  ▀·▀▀▀  ▀  ▀  ▀▀▀▀ ·▀▀▀ .▀  ▀ ▀  ▀ .▀   
    """

    text_colombia = f'{Fore.LIGHTYELLOW_EX}Colo{color_azul}mb{color_rojo}ia'

    print(Fore.LIGHTYELLOW_EX+text)
    print(f'\t\t\t{text_colombia}')

#ACORTAR LA URL DEL PRODUCTO A TRAVÈS DE ESTA FUNCION
def acortar_url(url):

    payload = {
    'url': url,
    'domain': 0
    }

    r = requests.post('https://cutt.ly/scripts/shortenUrl.php',data=payload)

    return r.text


#PARAMETROS ELEGIDOS POR EL USUARIO
def parametros():

    buscar_producto = input(color_verde+'\nNombre del producto: '+color_blanco).lower()

    #SEPARAR LAS PALABRAS CON GUIONES PARA LUEGO HACER LA PETICION
    buscar_producto = buscar_producto.replace(' ','-')

    #PEDIR EL NUMERO DE RESULTADOS AL USUARIO
    while True:
        
        try:
            limite_productos = int(input(color_verde+'\nNumero de resultados a mostrar: '+color_blanco))
            break
        except ValueError:
            print(color_rojo+'\nEl valor debe ser numerico')

    envios_gratis = False

    val_max = None
    val_min = None

    #FILTROS QUE EL USUARIO PUEDE APLICAR O SIMPLEMENTE OMITIR
    while True:
        clearConsole()
        banner()

        print(Fore.LIGHTMAGENTA_EX+'\n***Filtros opcionales***')
        print(color_azul+'1'+color_blanco+' - Solo Envios gratis')
        print(color_azul+'2'+color_blanco+' - Elegir rango de precios')
        print(color_azul+'3'+color_blanco+' - Todo listo / Omitir')

        try:
            opc = int(input(color_verde+'\n-> '+color_blanco))

            if opc == 1:
                if envios_gratis == False:
                    print(color_verde+'\nSE HA ACTIVADO EL FILTRO SOLO ENVIOS GRATIS\n')
                    envios_gratis = True
                    time.sleep(1.5)
                else:
                    print(color_rojo+'\nSE HA DESACTIVADO EL FILTRO SOLO ENVIOS GRATIS')
                    envios_gratis = False
                    time.sleep(1.5)

            elif opc == 2:
                clearConsole()
                while True:
                    while True:
                        try:
                            val_min = int(input(color_verde+'Ingresa el valor minimo (COP) -> '+color_blanco))
                            break
                        except ValueError:
                            print(color_rojo+'\nRECUERDA: debe ser valor numerico\n')
                    while True:
                        try:
                            val_max = int(input(color_verde+'Ingresa el valor maximo (COP) -> '+color_blanco))
                            break
                        except ValueError:
                            print(color_rojo+'\nRECUERDA: debe ser valor numerico\n')

                    print(color_verde+ f'SE HA APLICADO EL RANGO DE {val_min}-{val_max}')
                    time.sleep(1.5)
                    break

            elif opc == 3:
                break

        except ValueError:
            print(color_rojo+'\nError, elige una de las opciones disponibles\n')

    #INVOCAR A LA FUNCION DE SCRAPING PASANDOLE LOS DATOS Y GUSTOS DEL USUARIO
    scraping(buscar_producto,limite_productos,envios_gratis,val_max,val_min)
    

#SCRAPING Y ESTRUCTURACIÒN DE LOS DATOS
def scraping(nombre_producto,n_productos,envio,v_max,v_min):

    clearConsole()
    banner()

    #SI SE APLICÒ SOLO EL FITLRO DE ENVIOS
    if envio == True and v_max == None:
        print(color_verde+'\n\t[*] Haciendo busqueda con solo envios gratis')
        r = requests.get('https://listado.mercadolibre.com.co/'+nombre_producto+'_CostoEnvio_Gratis_NoIndex_True')

    #SI SE APLICARON TODOS LOS FITLROS
    elif envio == True and v_max != None:
        print(color_verde+'\n\t[*] Haciendo busqueda con envios gratis y rango de precios')
        url = 'https://listado.mercadolibre.com.co/'+nombre_producto+'_CostoEnvio_Gratis_PriceRange_'+str(v_min)+'-'+str(v_max)+'_NoIndex_True'
        r = requests.get(url)

    #SI SE ALICÒ SOLAMENTE RANGO DE PRECIOS
    elif envio == False and v_max != None:
        print(color_verde+'\n\t[*] Haciendo busqueda solamente con rango de precio')
        url = 'https://listado.mercadolibre.com.co/'+nombre_producto+'_PriceRange_'+str(v_min)+'-'+str(v_max)+'_NoIndex_True'
        r = requests.get(url)

    #SI NO SE APLICÒ NINGÙN FILTRO
    else:
        print(color_verde+'\n\t[*] Haciendo busqueda normal')
        r = requests.get('https://listado.mercadolibre.com.co/'+nombre_producto)

    #GUARDAR EL LIMITE DE RESULTADOS QUE SE MOSTRARÀN
    limite_productos = n_productos

    soup = BeautifulSoup(r.text,'html.parser')

    #DIVIDIR LOS PRODUCTOS EN SUS DIV PARA LUEGO DESMENUZARLOS (PRECIO , TITULO, ETC)
    productos_div = soup.find_all('div',{'class':'shops__cardStyles'})

    i = 0

    for producto in productos_div:

        i += 1

        #DETENERSE CUANDO SE LLEGA AL LIMITE DE RESULTADOS PEDIDOS POR EL USUARIO
        if i == limite_productos+1:
            break

        #DATOS PRINCIPALES DE LA PUBICACION
        titulo = producto.find('h2',{'class':'ui-search-item__title'})
        precio = producto.find('span',{'class':'price-tag-fraction'})

        #POSIBLE ERROR EN ALGUNAS CATEGORIAS O PUBLICACIONES
        try:
            envio = producto.find('p',{'class':'ui-search-item__shipping'})
            envio = envio.text
        except:
            envio = 'No se hacen envios'

        #posible error al obtener el link de la publicacion
        try:
            link = producto.find('a',{'class':'ui-search-item__group__element'})['href']
        except:
            link = producto.find('a',{'class':'ui-search-result__content'})['href']
        

        #COMPROBAR SI ES INMUEBLE O VEHICULO TAMBIEN
        try:
            localizacion = producto.find('span',{'class':'ui-search-item__location'})
        except:
            pass

        #ESTO ES PARA COMPROBAR SI ES UN INMUEBLE
        try:
            tipo_venta = producto.find('span',{'class':'ui-search-item__subtitle'})
        except:
            pass

        nose = str(titulo).lower()
        

        #SI ES UN INMUEBLE
        if localizacion and 'No se hacen' in envio and tipo_venta:

            datos = producto.find_all('li',{'class':'ui-search-card-attributes__attribute'})

            datos_basicos = ''

            for d in datos:
                datos_basicos = datos_basicos +' '+d.text
                
            print(f'''
            {color_azul}Titulo: {color_blanco}{titulo.text}
            {color_azul}Precio inmueble: {color_blanco}{precio.text}
            {color_azul}Localizacion Inmueble: {color_blanco}{localizacion.text}
            {color_azul}Datos Basicos Inmueble: {color_blanco}{datos_basicos}
            {color_azul}Tipo de inmueble: {color_blanco}{tipo_venta.text}
            {color_azul}Link Publicacion: {Fore.LIGHTCYAN_EX}{acortar_url(link)}
            
            ''')

        #SI ES UN TIPO DE VEHICULO
        elif localizacion and 'se hacen' in envio:
            datos_auto = producto.find_all('li',{'class':'ui-search-card-attributes__attribute'})

            datos_basicos = ''

            for d in datos_auto:
                datos_basicos = datos_basicos +' '+d.text

            print(f'''
            {color_azul}Titulo: {color_blanco}{titulo.text}
            {color_azul}Precio: {color_blanco}{precio.text}
            {color_azul}Ubicacion del vehiculo: {color_blanco}{localizacion.text}
            {color_azul}Año y kilometraje: {color_blanco}{datos_basicos}
            {color_azul}Link Publicacion: {Fore.LIGHTCYAN_EX}{acortar_url(link)}
            ''')

        #SI ES UN PRODUCTO NORMAL
        else:
            print(f'''
            {color_azul}Titulo: {color_blanco}{titulo.text}
            {color_azul}Precio: {color_blanco}{precio.text}
            {color_azul}Costo de Envio: {color_blanco}{envio}
            {color_azul}Link Publicacion: {color_blanco}{acortar_url(link)}
            ''')

#FUNCIÒN INICIAL
def main():

    clearConsole()

    #BANNER DEL PROGRAMA
    banner()

    #AQUI INICIA LA INTERVENCION DEL USUARIO
    parametros()

    #FIN
    print(color_verde+'\t[*]Fin de los resultados\n')


if __name__ == '__main__':

    #SI SE PULSA CTRL+C
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nSaliendo...\n')
