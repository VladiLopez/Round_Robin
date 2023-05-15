# Actividad 10 - Programa 5 - Round Robin
# Alumnos: López Reynoso Javier Vladimir
#          López Ríos Ian Daniel
                                    
import os
import time
import random
from pynput import keyboard as kb
from proceso import Proceso

tecla2 = ''

procesos = []                       # [Op, Res, TME, ID, TT, TTBAct, TTBGeneral]
proceso_null = ['','',8,0,0,0,0]

tiempoProcesos = []                 # [Op, Res, TME, ID, TLlegada, T que entra en Ejecucion, TFin, TRet, TResp, TServ, TEsp]

cont_null = 0

lista_nuevos = []
lista_listos = []       #   \
lista_ejecucion = []    # --- Entre los 3 estados debe haber maximo 4 procesos en memoria
lista_bloqueados = []   #   /

proc_terminados = []                # [[id, op, res, TME, TT]]

listaAux = []
id_usados = []

operador = ['+','-','*','/','%']

contador_global = 0
contadorTiempoTrascurrido = 0
contadorTiempoBloqueado = 0
contador_procesos = 0

id_operacion = 1

#----------Tiempos de los procesos------------
tiempoLlegada = 0
tiempoFinalizacion = 0
tiempoRetorno = 0

tiempoEntradaEjecucion = 0
tiempoRespuesta = 0

tiempoEspera = 0
tiempoServicio = 0

quantum_cont = 0

def funcionOperacion(operador):
    proceso.numero1 = random.randint(-100, 100)
    proceso.numero2 = random.randint(-100, 100)
    proceso.cadena_operacion = '{} {} {}'.format(proceso.numero1, operador, proceso.numero2)
    procesos.append(proceso.cadena_operacion)
    listaAux.append(proceso.cadena_operacion)   

#-----------Tabla de procesos------------
""" def imprimirTablaProcesos():

    for j in range(0, len(tiempoProcesos)):

        tiempoRetorno = tiempoProcesos[j][6] - tiempoProcesos[j][4]     # Tiempo Retorno = Fin - Llegada
        tiempoProcesos[j].append(tiempoRetorno)

        tiempoRespuesta = tiempoProcesos[j][5] - tiempoProcesos[j][4]   # Tiempo Respuesta = 1ra Llegada a Ejecución - Llegada
        tiempoProcesos[j].append(tiempoRespuesta)

        #Tiempo de servicio, agregar TT y TME en proc_terminados para hacer comparacion
        for k in range(0, len(proc_terminados)):

            if tiempoProcesos[j][3] == proc_terminados[k][0]: #Comparar Indices para asignar el TS al proceso correcto

                if proc_terminados[k][3] == proc_terminados[k][4]: # Si el proceso terminó de forma correcta, TS = TME
                    tiempoServicio = proc_terminados[k][3]
                elif proc_terminados[k][3] > proc_terminados[k][4]: # Si el proceso no terminó de manera correcta, TS = TT
                    tiempoServicio = proc_terminados[k][4]
                
                tiempoProcesos[j].append(tiempoServicio)
            
        tiempoEspera =  tiempoProcesos[j][7] - tiempoProcesos[j][9] #TRet - TS     
        tiempoProcesos[j].append(tiempoEspera)

    os.system("cls")

    print('\t\tTABLA DE PROCESOS\n')

    for i in range(0, len(tiempoProcesos)):
        print(f'\n-------------Proceso {tiempoProcesos[i][3]}-------------\n')

        for k in range(0, len(proc_terminados)):

            if tiempoProcesos[i][3] == proc_terminados[k][0]:
                
                if proc_terminados[k][2] == 'ERROR!':
                    print('Tipo finalizacion: Erronea\n') 
                    print(f'Operacion: {tiempoProcesos[i][0]} = ERROR!')
                else:
                    print('Tipo finalizacion: Normal\n') 
                    print(f'Operacion: {tiempoProcesos[i][0]} = {tiempoProcesos[i][1]}')

        print(f'TME: {tiempoProcesos[i][2]}')
        print(f'Tiempo de Llegada:      {tiempoProcesos[i][4]}')
        print(f'Tiempo de Finalizacion: {tiempoProcesos[i][6]}')
        print(f'Tiempo de Retorno:      {tiempoProcesos[i][7]}')
        print(f'Tiempo de Respuesta:    {tiempoProcesos[i][8]}')
        print(f'Tiempo de Espera:       {tiempoProcesos[i][10]}')
        print(f'Tiempo de Servicio:     {tiempoProcesos[i][9]}') """
        
def imprimirTablaProcesos():

    os.system("cls")

    print('\t\tBLOQUE DE CONTROL DE PROCESOS\n')

    if len(lista_nuevos) > 0:

        print('********************** PROCESOS NUEVOS **********************\n')

        for i in range(0, len(tiempoProcesos)):

            for k in range(0, len(lista_nuevos)):

                if tiempoProcesos[i][3] == lista_nuevos[k][3]: # Comparar ID

                    print(f'\n-------------Proceso {tiempoProcesos[i][3]}-------------\n')
                    print(f'Operacion:              {tiempoProcesos[k][0]}')
                    print(f'TME:                    {tiempoProcesos[k][2]}')
                    print(f'Tiempo de Llegada:      NULL')
                    print(f'Tiempo de Finalizacion: NULL')
                    print(f'Tiempo de Retorno:      NULL')
                    print(f'Tiempo de Respuesta:    NULL')
                    print(f'Tiempo de Espera:       NULL')
                    print(f'Tiempo de Servicio:     NULL')

    if len(lista_bloqueados) > 0:

        print('\n********************** PROCESOS BLOQUEADOS **********************\n')

        for i in range(0, len(tiempoProcesos)):
            
            k = 0

            while k < len(lista_bloqueados):

                if tiempoProcesos[i][3] == lista_bloqueados[k][3]: # Comparar ID

                    print(f'\n-------------Proceso {tiempoProcesos[i][3]}-------------\n')
                    print(f'Operacion:              {tiempoProcesos[k][0]}')
                    print(f'TME:                    {tiempoProcesos[k][2]}')
                    print(f'Tiempo de Llegada:      {tiempoProcesos[k][4]}')
                    print(f'Tiempo de Finalizacion: NULL')
                    print(f'Tiempo de Retorno:      NULL')
                    print(f'Tiempo de Respuesta:    {tiempoProcesos[i][5] - tiempoProcesos[i][4]}') # Primera vez en Ejecucion - LLegada
                    print(f'Tiempo de Espera:       {tiempoProcesos[i][5] - tiempoProcesos[i][4] + lista_bloqueados[k][5]}') # Primera vez en Ejecucion - LLegada + Tiempo que lleva en Bloqueado
                    print(f'Tiempo de Servicio:     {lista_bloqueados[k][4]}') #Posicion de tiempo transurrido (TT)
                    print(f'Tiempo Restante en Bloqueado: {8 - lista_bloqueados[k][5]}') # 8 - TT
                
                k += 1 


    if len(proc_terminados) > 0:
        
        print('\n********************** PROCESOS TERMINADOS **********************\n')

        for j in range(0, len(tiempoProcesos)):

            for k in range(0, len(proc_terminados)): # Recorre la lista de terminados

                if tiempoProcesos[j][3] == proc_terminados[k][0]:

                    tiempoRetorno = tiempoProcesos[j][6] - tiempoProcesos[j][4]     # Tiempo Retorno = Fin - Llegada
                    tiempoProcesos[j].append(tiempoRetorno)

                    tiempoRespuesta = tiempoProcesos[j][5] - tiempoProcesos[j][4]   # Tiempo Respuesta = 1ra Llegada a Ejecución - Llegada
                    tiempoProcesos[j].append(tiempoRespuesta)

                    #Tiempo de servicio, agregar TT y TME en proc_terminados para hacer comparacion

                    if proc_terminados[k][3] == proc_terminados[k][4]: # Si el proceso terminó de forma correcta, TS = TME
                        tiempoServicio = proc_terminados[k][3]
                    elif proc_terminados[k][3] > proc_terminados[k][4]: # Si el proceso no terminó de manera correcta, TS = TT
                        tiempoServicio = proc_terminados[k][4]
                    
                    tiempoProcesos[j].append(tiempoServicio)
                
                    tiempoEspera =  tiempoProcesos[j][7] - tiempoProcesos[j][9] #TRet - TS     
                    tiempoProcesos[j].append(tiempoEspera)


        for i in range(0, len(tiempoProcesos)):

            for k in range(0, len(proc_terminados)):

                if tiempoProcesos[i][3] == proc_terminados[k][0]:
                    
                    print(f'\n-------------Proceso {tiempoProcesos[i][3]}-------------\n')
                    
                    if proc_terminados[k][2] == 'ERROR!':
                        print('Tipo finalizacion:      Erronea\n') 
                        print(f'Operacion:              {tiempoProcesos[i][0]} = ERROR!')
                    else:
                        print('Tipo finalizacion:      Normal\n') 
                        print(f'Operacion:              {tiempoProcesos[i][0]} = {tiempoProcesos[i][1]}')

                    print(f'TME:                    {tiempoProcesos[i][2]}')
                    print(f'Tiempo de Llegada:      {tiempoProcesos[i][4]}')
                    print(f'Tiempo de Finalizacion: {tiempoProcesos[i][6]}')
                    print(f'Tiempo de Retorno:      {tiempoProcesos[i][7]}')
                    print(f'Tiempo de Respuesta:    {tiempoProcesos[i][8]}')
                    print(f'Tiempo de Espera:       {tiempoProcesos[i][10]}')
                    print(f'Tiempo de Servicio:     {tiempoProcesos[i][9]}')

    os.system("pause")

#------PULSASIONES DEL TECLADO-----------

def pulsa2(letra):
    if letra == kb.KeyCode.from_char('c'):
        return False

def pulsa(tecla):
    global tecla2
    tecla2 = ''
    tecla2 = tecla
    return tecla2

        
cantidad = int(input("Ingrese la cantidad de procesos a realizar: "))
quantum = int(input('Ingresa en valor del quantum: '))

while(contador_procesos < cantidad):

    proceso = Proceso()

    #?Validacion de la operacion        
    while True:
        proceso.operacion = random.choice(operador)
        
        if proceso.operacion == "+":
            funcionOperacion('+')
            proceso.resultado_operacion = proceso.numero1 + proceso.numero2
            procesos.append(proceso.resultado_operacion)
            listaAux.append(proceso.resultado_operacion) 
            break

        elif proceso.operacion == "-":
            funcionOperacion('-')
            proceso.resultado_operacion = proceso.numero1 - proceso.numero2
            procesos.append(proceso.resultado_operacion)
            listaAux.append(proceso.resultado_operacion) 
            break

        elif proceso.operacion == "*":
            funcionOperacion('*')
            proceso.resultado_operacion = proceso.numero1 * proceso.numero2
            procesos.append(proceso.resultado_operacion)
            listaAux.append(proceso.resultado_operacion) 
            break

        elif proceso.operacion == "/":
            proceso.numero1 = random.randint(-100, 100)
            proceso.numero2 = random.randint(-100, 100)
            
            while True:
                if proceso.numero2 == 0:
                    proceso.numero2 = random.randint(-100, 100)
                else:
                    break

            proceso.cadena_operacion = '{} / {}'.format(proceso.numero1, proceso.numero2)
            proceso.resultado_operacion = proceso.numero1 / proceso.numero2
            procesos.append(proceso.cadena_operacion)
            procesos.append(proceso.resultado_operacion)

            listaAux.append(proceso.cadena_operacion) 
            listaAux.append(proceso.resultado_operacion) 
            break

        elif proceso.operacion == "%":
            proceso.numero1 = random.randint(-100, 100)
            proceso.numero2 = random.randint(-100, 100)
            
            while True:
                if proceso.numero2 == 0:
                    proceso.numero2 = random.randint(-100, 100)
                else:
                    break
            
            proceso.cadena_operacion = '{} % {}'.format(proceso.numero1, proceso.numero2)
            proceso.resultado_operacion = proceso.numero1 / proceso.numero2
            procesos.append(proceso.cadena_operacion)
            procesos.append(proceso.resultado_operacion)
            
            listaAux.append(proceso.cadena_operacion) 
            listaAux.append(proceso.resultado_operacion) 
            break

    #?TIEMPO MAXIMO ESTIMADO
    proceso.tiempo_maximo = random.randint(5, 16)
    procesos.append(proceso.tiempo_maximo)
    listaAux.append(proceso.tiempo_maximo)

    #?INGRESO DEL ID
    proceso.id_programa = id_operacion
    procesos.append(proceso.id_programa)
    listaAux.append(proceso.id_programa)
    id_operacion = id_operacion + 1

    #?TIEMPO TRANSCURRIDO
    tiempo_transcurrido = 0
    procesos.append(tiempo_transcurrido)

    #?TIEMPO TRANSCURRIDO BLOQUEADO (Actual)
    tiempoBloqueado = 0
    procesos.append(tiempoBloqueado)

    #?TIEMPO TRANSCURRIDO BLOQUEADO (General) -> En caso de que se vaya mas de 1 vez a bloqueados funciona como acumulador
    procesos.append(tiempoBloqueado)

    lista_nuevos.append(procesos) # Se agrega el proceso a 'lista_nuevos'
    tiempoProcesos.append(listaAux) 

    procesos = [] # Se vacía la lista de procesos para empezar uno nuevo
    listaAux = []
    contador_procesos += 1

# Pasan 4 procesos a memoria
if len(lista_nuevos) >= 4:

    longitudLista = len(lista_nuevos)    # Cuantos procesos hay en total

    for proc in range(4):
        lista_listos.append(lista_nuevos[proc])
        
        tiempoLlegada = contador_global
        tiempoProcesos[proc].append(contador_global) #Los primeros 4 procesos tienen 0 en tiempo de llegada
    
    del lista_nuevos[0:4]
    
    
elif len(lista_nuevos) < 4:

    longitudLista = len(lista_nuevos)

    for proc in range(len(lista_nuevos)):
        lista_listos.append(lista_nuevos[proc]) # En caso de que sean menos de 4 procesos, pasan solamente esos procesos

        tiempoLlegada = contador_global
        tiempoProcesos[proc].append(contador_global) #Los primeros  procesos tienen 0 en tiempo de llegada

    del lista_nuevos[0:len(lista_nuevos)]
    

os.system("pause")

#Impresion de datos
i = 0

while i < longitudLista: 
        
    contadorTiempoTrascurrido = 0
    tiempoRestante = 1
    quantum_cont = 0 #Reiniciar el quantum
        
    #if len(lista_listos) + len(lista_ejecucion) + len(lista_bloqueados) <= 4:    # Si hay 4 procesos en la memoria
     
    while tiempoRestante >= 0:

        tiempoRestante = lista_listos[0][2] - lista_listos[0][4]   # Tiempo restante del proceso -> TME - TT = TR
        contadorTiempoTrascurrido = lista_listos[0][4]


        os.system("cls")      

        print('----------Contador Global----------')
        print(contador_global)

        print('-----Procesos en estado Nuevo------')
        print(len(lista_nuevos))

        print('--------------Quantum--------------')
        print(quantum_cont)

        print('------------Cola de Listos------------')
        
        if len(lista_listos) == 0:
            pass
        else:
            for j in range(1, len(lista_listos)):    #Recorrer los procesos de listos
                print(f'ID: {lista_listos[j][3]} TME: {lista_listos[j][2]} TT: {lista_listos[j][4]}', end=' |')   

            if len(lista_ejecucion) == 0:
                lista_ejecucion.append(lista_listos[0])

                for j in range(0, len(tiempoProcesos)): #Recorrer la lista donde se guardan los tiempos

                    if tiempoProcesos[j][3] == lista_ejecucion[0][3]:   # Comparar indices para saber si es el mismo proceso 

                        if lista_ejecucion[0][4] == 0: #Si el tiempo transcurrido es 0 (Es la primera vez en Ejecucion)

                            tiempoEntradaEjecucion = contador_global
                            tiempoProcesos[j].append(tiempoEntradaEjecucion)

                        else:
                            pass
            else:
                lista_ejecucion[0] = lista_listos[0] # Pasa proceso de listos a ejecucion

                for j in range(0, len(tiempoProcesos)): #Recorrer la lista donde se guardan los tiempos

                    if tiempoProcesos[j][3] == lista_ejecucion[0][3]:   # Comparar indices para saber si es el mismo proceso 

                        if lista_ejecucion[0][4] == 0: #Si el tiempo transcurrido es 0 (Es la primera vez en Ejecucion)

                            tiempoEntradaEjecucion = contador_global
                            tiempoProcesos[j].append(tiempoEntradaEjecucion)
                        else:
                            pass
                
        print('\n-------Proceso en Ejecucion----------')

        if lista_ejecucion[0][3] == 0:
            pass

        else:
            print("Operacion: {} \nTME: {} \nId: {} \nTiempo trascurrido: {} \nTiempo restante: {}".format(lista_ejecucion[0][0], lista_ejecucion[0][2], 
                                                                                                           lista_ejecucion[0][3], contadorTiempoTrascurrido, tiempoRestante))

        print('-----------Cola de Bloqueados-----------')
       
        if len(lista_bloqueados) > 0:

            for proc in lista_bloqueados:

                print(f'ID: {proc[3]} TT en Bloqueado: {proc[5]}')
                proc[5] += 1

                if proc[5] == 9: 
                    lista_listos.append(proc)
                    del lista_bloqueados[0]
                    proc[6] += proc[5]       # El contador actual se suma al acumulador (Sirve para tiempo de espera)
                    proc[5] = 0
                
        
        print('--------Procesos Terminados--------')            
        if len(proc_terminados) >= 0:
        
            for proc in range(len(proc_terminados)):
                if proc_terminados[proc][0] >= 1:
                    print("Id: {} \tOperacion: {} \tResultado: {} \t".format(proc_terminados[proc][0],proc_terminados[proc][1], proc_terminados[proc][2])) 
                    
        if tiempoRestante == 0:

            if len(lista_nuevos) == 0:

                if len(lista_listos)-1 == 0 and len(lista_bloqueados) > 0:
                    proceso_null[4] = lista_bloqueados[0][5]                # Iguala el tiempo
                    lista_listos.append(proceso_null)                       # Agrega el proceso null
                    longitudLista += 1
                else:
                    pass

            else:
                if lista_ejecucion[0][3] == 0:          # proceso_null
                    pass
                else:
                    lista_listos.append(lista_nuevos[0]) # Pasa proceso de listos a ejecucion

                    if lista_ejecucion[0][3] == 0:
                        pass
                    else:
                        for j in range(0, len(tiempoProcesos)):
                            if tiempoProcesos[j][3] == lista_listos[len(lista_listos)-1][3]:
                                tiempoLlegada = contador_global
                                tiempoProcesos[j].append(tiempoLlegada) # Tiempo de llegada a partir del proceso 5

                    del lista_nuevos[0]

            del lista_listos[0]

            listaAux = []           
            listaAux.extend([lista_ejecucion[0][3],lista_ejecucion[0][0],lista_ejecucion[0][1], lista_ejecucion[0][2], lista_ejecucion[0][4]])   #Se agregan los datos a listaAux
            proc_terminados.append(listaAux)
            print("Id: {} \tOperacion: {} \tResultado: {} \t".format(listaAux[0],listaAux[1],listaAux[2]))
            tiempoRestante -= 1
            quantum_cont = 0

            for j in range(0, len(tiempoProcesos)):
                if tiempoProcesos[j][3] == proc_terminados[len(proc_terminados)-1][0]:    
                    tiempoFinalizacion = contador_global
                    tiempoProcesos[j].append(tiempoFinalizacion) #Tiempo de finalizacion


        else:  
            tiempoRestante -= 1
            contadorTiempoTrascurrido += 1
            lista_listos[0][4] = contadorTiempoTrascurrido        # Actualizar el TR
         

        contador_global += 1
        quantum_cont += 1
        
        if quantum_cont == quantum+1:
            # pasar al final de la cola de listos
            lista_listos.append(lista_listos[0])
            lista_listos[0][4] = contadorTiempoTrascurrido-1      # Se guarda el tiempo transcurrido
            del lista_listos[0]
            quantum_cont = 0

        time.sleep(0.8) #* Velocidad del tiempo

    #?----------------------------------LISTENER----------------------------------

        escuchador = kb.Listener(pulsa)
        escuchador.start()

        if tecla2 == kb.KeyCode.from_char('i'):

            if lista_ejecucion[0][3] == 0:  # En caso de que el proceso sea proceso_null que no haga nada
                pass
            else:
                procesoActual = lista_listos[0]                     # Se guarda el proceso actual
                procesoActual[4] = contadorTiempoTrascurrido-1      # Se guarda el tiempo transcurrido
                del lista_listos[0]                                 # Se elimina de la lista
               
                if len(lista_listos) == 0:                      # Si no hay nada en lista_listos
                    proceso_null[4] = lista_bloqueados[0][5]    # Iguala el tiempo
                    lista_listos.append(proceso_null)           # Agrega el proceso null
                    longitudLista += 1

                lista_bloqueados.append(procesoActual)
            
            quantum_cont = 0

        if tecla2 == kb.KeyCode.from_char('e'): 

            listaAux = []           
            listaAux.extend([lista_ejecucion[0][3],lista_ejecucion[0][0],'ERROR!', lista_ejecucion[0][2], lista_ejecucion[0][4]])   # Se agregan los datos a listaAux 
            proc_terminados.append(listaAux)

            for j in range(0, len(tiempoProcesos)):

                if tiempoProcesos[j][3] == proc_terminados[len(proc_terminados)-1][0]:    
                    tiempoFinalizacion = contador_global
                    tiempoProcesos[j].append(tiempoFinalizacion) #Tiempo de finalizacion

            if len(lista_nuevos) == 0:

                if i == longitudLista-1:     #En caso de que sea el ultimo proceso 
                                    
                    print("Id: {} \tOperacion: {} \tResultado: {} \t".format(lista_listos[0][3],lista_listos[0][0],'ERROR!'))    
                    break
                else:                           # No es el ultimo
                    
                    if len(lista_listos)-1 == 0 and len(lista_bloqueados) > 0:
                        proceso_null[4] = lista_bloqueados[0][5]                # Iguala el tiempo
                        lista_listos.append(proceso_null)                       # Agrega el proceso null
                        longitudLista += 1
                    else:
                        pass
                    
                    del lista_listos[0]
                    break   
            else:                               # En caso de que aún queden en nuevos
                lista_listos.append(lista_nuevos[0])
                del lista_nuevos[0]
                del lista_listos[0]

                for j in range(0, len(tiempoProcesos)):
                    if tiempoProcesos[j][3] == lista_listos[len(lista_listos)-1][3]:
                        tiempoLlegada = contador_global
                        tiempoProcesos[j].append(tiempoLlegada) # Tiempo de llegada del que entra cuando se aprieta e

                break 
            
        if tecla2 == kb.KeyCode.from_char('p'):
            
            print("\n\tTeclea 'c' para continuar...")

            with kb.Listener(pulsa2) as escucha:
                escucha.join()

        if tecla2 == kb.KeyCode.from_char('n'):
            cont_n = 0 
            cantidad_n = 1

            while(cont_n < cantidad_n):

                proceso = Proceso()

                #?Validacion de la operacion        
                while True:
                    proceso.operacion = random.choice(operador)
                    
                    if proceso.operacion == "+":
                        funcionOperacion('+')
                        proceso.resultado_operacion = proceso.numero1 + proceso.numero2
                        procesos.append(proceso.resultado_operacion)
                        listaAux.append(proceso.resultado_operacion) 
                        break

                    elif proceso.operacion == "-":
                        funcionOperacion('-')
                        proceso.resultado_operacion = proceso.numero1 - proceso.numero2
                        procesos.append(proceso.resultado_operacion)
                        listaAux.append(proceso.resultado_operacion) 
                        break

                    elif proceso.operacion == "*":
                        funcionOperacion('*')
                        proceso.resultado_operacion = proceso.numero1 * proceso.numero2
                        procesos.append(proceso.resultado_operacion)
                        listaAux.append(proceso.resultado_operacion) 
                        break

                    elif proceso.operacion == "/":
                        proceso.numero1 = random.randint(-100, 100)
                        proceso.numero2 = random.randint(-100, 100)
                        
                        while True:
                            if proceso.numero2 == 0:
                                proceso.numero2 = random.randint(-100, 100)
                            else:
                                break

                        proceso.cadena_operacion = '{} / {}'.format(proceso.numero1, proceso.numero2)
                        proceso.resultado_operacion = proceso.numero1 / proceso.numero2
                        procesos.append(proceso.cadena_operacion)
                        procesos.append(proceso.resultado_operacion)

                        listaAux.append(proceso.cadena_operacion) 
                        listaAux.append(proceso.resultado_operacion) 
                        break

                    elif proceso.operacion == "%":
                        proceso.numero1 = random.randint(-100, 100)
                        proceso.numero2 = random.randint(-100, 100)
                        
                        while True:
                            if proceso.numero2 == 0:
                                proceso.numero2 = random.randint(-100, 100)
                            else:
                                break
                        
                        proceso.cadena_operacion = '{} % {}'.format(proceso.numero1, proceso.numero2)
                        proceso.resultado_operacion = proceso.numero1 / proceso.numero2
                        procesos.append(proceso.cadena_operacion)
                        procesos.append(proceso.resultado_operacion)
                        
                        listaAux.append(proceso.cadena_operacion) 
                        listaAux.append(proceso.resultado_operacion) 
                        break

                #?TIEMPO MAXIMO ESTIMADO
                proceso.tiempo_maximo = random.randint(5, 16)
                procesos.append(proceso.tiempo_maximo)
                listaAux.append(proceso.tiempo_maximo)

                #?INGRESO DEL ID
                proceso.id_programa = id_operacion
                procesos.append(proceso.id_programa)
                listaAux.append(proceso.id_programa)
                id_operacion = id_operacion + 1

                #?TIEMPO TRANSCURRIDO
                tiempo_transcurrido = 0
                procesos.append(tiempo_transcurrido)

                #?TIEMPO TRANSCURRIDO BLOQUEADO (Actual)
                tiempoBloqueado = 0
                procesos.append(tiempoBloqueado)

                #?TIEMPO TRANSCURRIDO BLOQUEADO (General) -> En caso de que se vaya mas de 1 vez a bloqueados funciona como acumulador
                procesos.append(tiempoBloqueado)

                lista_nuevos.append(procesos) # Se agrega el proceso a 'lista_nuevos'
                tiempoProcesos.append(listaAux) 

                procesos = [] # Se vacía la lista de procesos para empezar uno nuevo
                listaAux = []
                cont_n += 1
            
            longitudLista += cantidad_n

        if tecla2 == kb.KeyCode.from_char('t'):
            imprimirTablaProcesos()

            print("\n\tTeclea 'c' para continuar...")

            with kb.Listener(pulsa2) as escucha:
                escucha.join()


        tecla2 = ''
        letra = ''
    
    tecla2 = ''

    i += 1

os.system("pause")


imprimirTablaProcesos() 