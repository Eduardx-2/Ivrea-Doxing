try:

  import requests, signal
  import json, base64
  import sys
  import random

except ImportError:
      print(ROJO +"USTED NO TIENE INSTALADO UN MODULO DEL SCRIPT")
ROJO = '\033[31m'
MG = '\033[35m'
AQUA = "\033[96;1m" 
VERDEL = "\033[32;1m" 
WHITEL = "\033[0;1m"  
AZUL = "\033[31;1m" 
CYANL = "\033[36;1m" 
YELLOW = "\033[33;1m"    
VERDE = "\033[32m"    
WHITE = "\033[0;1m"     
CYAN = "\033[36;1m"    


def trap_c(sig, frame):
    print(ROJO + "\nSALIENDO....")
    exit()
  
signal.signal(signal.SIGINT, trap_c)

class inicio():

    def __init__(self):      
        self.url_requests = "http://localhost:9080/eduardx-2/peru/api/data/dni="
        self.getJson = requests.session()
        self.url_judicial = "http://localhost:9080/eduardx-2/ecuador/judicial/api/cedula="
        self.user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                            'Mozilla/5.0 (X11; Linux i686; rv:107.0) Gecko/20100101 Firefox/107.0',
                            'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
                            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0',
                            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/107.0.5304.101 Mobile/15E148 Safari/604.1',
                            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                            'Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.105 Mobile Safari/537.36',
                            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36']
        

    def consultaPeru(self):
        numDni = int(input(f"{WHITEL}[{MG}+{WHITEL}] {VERDE}INGRESA EL DNI: {WHITE}"))
        if len(str(numDni)) == 8:
            requestUrl = self.getJson.get(self.url_requests + str(numDni))
            json = self.returnDataBaseBytes(requestUrl.json())['Contenido']['DatosAdicionales']

            if requestUrl.status_code == 200:
               try:

                 nombre = json['prenombres']
                 apePrimero = json['apPrimer']
                 apeSegundo = json['apSegundo']
                 restriccion = json['restriccion']
                 ubigeo = json['ubigeo']
                 direccion = json['direccion']
                 estado = json['estadoCivil']
                 fotoImg = json['foto']
                 decodeImg = open(f'{numDni}.jpg', 'wb')
                 decodeImg.write(base64.b64decode((fotoImg)))
                 decodeImg.close()
                 print(f"{VERDEL}NOMBRE: {WHITE}{nombre}\n{VERDEL}APELLIDO PATERNO: {WHITE}{apePrimero}\n{VERDEL}APELLIDO MATERNO: {WHITE}{apeSegundo}\n{VERDEL}RESTRICCIÓN: {WHITE}{restriccion}\n{VERDEL}ESTADO: {WHITE}{estado}\n{VERDEL}UBIGEO: {WHITE}{ubigeo}\n{VERDEL}DIRECCIÓN: {WHITE}{direccion}\n")
                 print(VERDE+"LA FOTO DEL DNI SE GUARDO EN LA RUTA ACTUAL")
               except KeyError:
                   print(f"{YELLOW}EL DNI {ROJO}{numDni} {YELLOW}ES DE UN MENOR")

            else:
                print(f"{ROJO}OCURRIO UN ERROR")
        else:
            print(f"{ROJO}EL DNI CONSULTADO NO ES VALIDO")

    def returnBaseFix(self, fotoJpg:bytes):
        return base64.b64encode(fotoJpg).decode('utf-8')

    def returnDataBaseBytes(self, dataBytes:dict):
        dataBytes['Contenido']['DatosAdicionales']['foto'] = self.returnBaseFix(bytes(dataBytes.get('Contenido')['DatosAdicionales']['foto']))
        return dataBytes
        
    
    def ecuadorRequests(self):
        nombre = str(input(f"{WHITE}[{MG}-{WHITE}] {VERDE}ESCRIBA EL NOMBRE: {WHITE}"))
        finalNombre = f"{nombre}".upper().split()
        url = f"https://srienlinea.sri.gob.ec/movil-servicios/api/v1.0/deudas/porDenominacion/{finalNombre[0]} {finalNombre[1]} {finalNombre[2]}/?tipoPersona=N&resultados=30&_=1665425573625"
        headers = {
           'User-Agent': random.choice(self.user_agents),
           'Content-Type': 'application/json'
        }
        r_request = requests.get(url, headers=headers)
        if r_request.status_code == 200:
            if len(r_request.json()) != 0:
                print(f'{WHITE}BUSCANDO => {AQUA}{" ".join(finalNombre)} {MG}-> {WHITE}{len(r_request.json())} RESULTADOS')
                for name in r_request.json():
                    print(f"{VERDEL}{name['identificacion']} {MG}-> {WHITE}{name['tipoIdentificacion']} {MG}-> {WHITE}{name['nombreComercial']} {MG}-> {WHITE}{name['clase']}")
            else:
                print(f"{ROJO}NO SE ENCONTRARON RESULTADOS DE {CYANL}{finalNombre}") 
        else:
            print("{}OCURRIO UN ERROR {}=> {}[{}]".format(ROJO, MG, WHITE, r_request.status_code))

    def requestJudicial(self):
        cedula = int(input(f"{WHITE}[{MG}-{WHITE}] {VERDE}INGRESA LA CEDULA: {WHITE}"))
        if len(str(cedula)) == 10:
            request_Session = requests.get(self.url_judicial + str(cedula))
            responseJson = request_Session.json()['respuesta']

            try:
              for e in responseJson:
                  nombre = e['nombre']
                  juicioID = e['idJuicio']
                  estadoActual = e['estadoActual']
                  delito = e['nombreDelito']
                  provincia = e['fechaProvidencia']
                  estado = e['nombreProvincia']
              print(f"\n{VERDEL}NOMBRE: {WHITE}{nombre}\n{VERDEL}ESTADO ACTUAL: {WHITE}{estadoActual}\n{VERDEL}ID-JUICIO: {WHITE}{juicioID}{MG}-> {VERDEL}DELITO: {WHITE}{delito}\n{VERDEL}FECHA: {WHITE}{provincia} {MG}-> {VERDEL}ESTADO: {WHITE}{estado}")
            except UnboundLocalError:
                print(f"LA CEDULA {cedula} NO TIENE PROBLEMAS JUDICIALES")

        else:
            print("LA CEDULA INGRESADA NO ES VALIDA")

    def ecuadorMatricula(self):
        sendPlaca = input(f"{WHITE}[{MG}-{WHITE}] {VERDEL}[PLACA] {ROJO}>>{WHITE}").upper()
        if len(sendPlaca) == 7:
            url_send = "http://localhost:9080/eduardx-2/ecuador/matricula/api/placa=%s" % (sendPlaca)   
            sessionPlaca = requests.get(url_send)
            
            responseTojson = sessionPlaca.json()

            try:
              placa = responseTojson['placa']
              marca = responseTojson['marca']
              modelo = responseTojson['modelo']
              timeModel = responseTojson['anioModelo']
              paisF = responseTojson['paisFabricacion']
              clase = responseTojson['clase']
              servicio = responseTojson['servicio']

              print(f"{VERDEL}PLACA {MG}=> {WHITE}{placa} {MG}=> {VERDEL}MARCA {WHITE}{marca} {MG}=> {VERDEL}MODELO {WHITE}{modelo} {MG}=> {VERDEL}AÑO {WHITE}{timeModel} {MG}=> {VERDEL}PAIS {WHITE}{paisF} {MG}=> {VERDEL}CLASE {MG}=> {WHITE}{clase} {MG}=> {VERDEL}SERVICIO {WHITE}{servicio}")

            except KeyError:
               print(f"{ROJO}LA PLACA {AZUL}{sendPlaca} {ROJO}NO EXISTE")
        else:
            print(f"{ROJO}LA PLACA {AZUL}{sendPlaca} {ROJO}NO ES VALIDA")
            
    def requestCedula(self):
        try:
           cedula = int(input(f"{WHITE}[{MG}-{WHITE}] {VERDE}INGRESA LA CEDULA: {WHITE}"))
        except:
            print(ROJO+"NO INGRESES LETRAS")
            exit()

        url_cedula = "http://localhost:8081/api/ecuador/v2.0/request/data/json/?cedula="
        r_send = requests.get(url_cedula + str(cedula))
        try:
          respuesta_json = r_send.json()['contribuyente']
          nombre = respuesta_json['nombreComercial']
          ide = respuesta_json['tipoIdentificacion']
          print(f"{VERDEL}NOMBRE {MG}=> {WHITE}{nombre} {MG}-> {VERDEL}TIPO IDENTIFICACION {MG}=> {WHITE}{ide}")
        except KeyError:
            print(ROJO+"LA CEDULA QUE INGRESASTE NO ES VALIDA")

    def requestRuc(self):
        try:
            ruc = int(input(f"{WHITE}[{MG}+{WHITE}] {VERDE}INGRESA EL RUC: {WHITE}"))
        except:
            pass
        if len(str(ruc)) == 11:
           urlRuc = "http://localhost:8081/peru/data/ruc/?ruc="
           sendRuc = requests.get(urlRuc + str(ruc))
           jsonRuc = sendRuc.json()['data']
           print(f"{VERDEL}NOMBRE: {WHITE}{jsonRuc['nombre_o_razon_social']}") 
        else:
            print(ROJO+"EL RUC INGRESADO NO ES VALIDO")

    def option_fn(self):
        try:
          options = int(input(f"\n{VERDEL}[OPCIONES] {CYAN}=>{WHITE} "))
        except NameError:
            print(ROJO+"NO INGRESES LETRAS")
        while True:
              if options == 1:
                 data.ecuadorRequests()
                 return data.option_fn()
              elif options == 2:
                 data.requestJudicial()
                 return data.option_fn()
              elif options == 3:
                 data.ecuadorMatricula()
                 return data.option_fn()
              elif options == 4:
                 data.requestCedula()
                 return data.option_fn()
              elif options == 5:
                 data.requestRuc()
                 return data.option_fn()
              elif options == 6:
                 data.consultaPeru()
                 return data.option_fn()
              else:
                 print(ROJO+"OPCION INVALIDA") 
                 sys.exit(1)
 ##   def grabify(self):
banner = f"""
{ROJO}
   ██╗██╗   ██╗██████╗ ███████╗ █████╗        ██████╗ ███████╗██╗███╗   ██╗████████╗
   ██║██║   ██║██╔══██╗██╔════╝██╔══██╗      ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
   ██║██║   ██║██████╔╝█████╗  ███████║█████╗██║   ██║███████╗██║██╔██╗ ██║   ██║   
   ██║╚██╗ ██╔╝██╔══██╗██╔══╝  ██╔══██║╚════╝██║   ██║╚════██║██║██║╚██╗██║   ██║   
   ██║ ╚████╔╝ ██║  ██║███████╗██║  ██║      ╚██████╔╝███████║██║██║ ╚████║   ██║EDUARDX
   ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝{ROJO}
                                                                                """
print(banner)
print(f"{WHITEL}[{CYANL}1{WHITEL}] - BUSQUEDA POR NOMBRE ECUADOR\n{WHITEL}[{CYANL}2{WHITEL}] - BUSQUEDA JUDICIAL ECUADOR")
print(f"{WHITEL}[{CYANL}3{WHITEL}] - BUSQUEDA DE PLACAS ECUADOR\n{WHITEL}[{CYANL}4{WHITEL}] - BUSQUEDA CEDULA ECUADOR\n{WHITEL}[{CYANL}5{WHITEL}] - BUSQUEDA RUC PERÚ\n{WHITEL}[{CYANL}6{WHITEL}] - BUSQUEDA DNI PERÚ +18")

 
data = inicio()
data.option_fn()

