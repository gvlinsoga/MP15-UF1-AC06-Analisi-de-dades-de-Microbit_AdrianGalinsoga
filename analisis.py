import matplotlib.pyplot as plt  # Para gráficos
import numpy as np  # Para operaciones numéricas
import pandas as pd  # Para manipulación de datos
import os  # Para manipulación de directorios y archivos

# Asegúrate de que el directorio 'graficos' exista
os.makedirs("graficos", exist_ok=True)  # Si no existe, lo crea

# Definición del menú para interacción con el usuario
def mostrar_menu():
    print("Selecciona qué gráficos quieres ver:")
    print("1. Todos los datos")
    print("2. Temperatura histórica")
    print("3. Nivel de luz")
    print("4. Nivel de sonido")
    print("5. Aceleración")
    print("6. Orientación de brújula")
    print("7. Mapa de correlaciones")
    print("8. Salir")
    try:
        # Devuelve la opción seleccionada por el usuario
        return int(input("Opción: "))
    except ValueError:
        # Si el usuario no introduce un número, vuelve a mostrar el menú
        print("Por favor, introduce un número.")
        return mostrar_menu()

# Leer datos del archivo CSV y crear intervalos
def obtener_datos() -> pd.core.groupby.DataFrameGroupBy:
    # Lee el archivo CSV y convierte a DataFrame
    df = pd.read_csv("microbit_sensor.csv")
    # Crear un identificador para cada intervalo basado en el reinicio de 'sample-id'
    df['intervalo'] = (df['sample-id'] == 0).cumsum()
    # Agrupar por intervalos
    return df.groupby("intervalo")

# Gráficos de todo el dataset
def todos_los_datos(intervalos: list):
    plt.style.use("ggplot")  # Estilo del gráfico
    for intervalo in intervalos:
        # El título incluye el número de intervalo
        plt.title(f'Intervalo {intervalo["intervalo"].iloc[0]}')
        # Trazar las columnas, excepto 'Time (seconds)' y 'sample-id'
        plt.plot(intervalo.loc[:, ~intervalo.columns.isin(["Time (seconds)", "sample-id"])])
        plt.xlabel("ID de muestra")
        plt.ylabel("Valores")
        # Leyenda basada en las columnas del DataFrame
        plt.legend(intervalo.loc[:, ~intervalo.columns.isin(["Time (seconds)", "sample-id"])].columns)
        # Guardar el gráfico
        plt.savefig(f"graficos/todos_{intervalo['intervalo'].iloc[0]}.png", dpi=200)
        # Mostrar el gráfico
        plt.show()

# Gráfico de temperatura histórica
def temperatura_historica(intervalos: list):
    plt.style.use("ggplot")  # Cambiar estilo del gráfico
    # Colores para los distintos intervalos
    colores = ["#ff9999", "#ffcc99", "#66b3ff"]
    for idx, intervalo in enumerate(intervalos):
        # Convertir el tiempo a minutos para el eje x
        tiempo_minutos = intervalo["Time (seconds)"] / 60
        # Graficar la temperatura
        plt.scatter(tiempo_minutos, intervalo["temp"], color=colores[idx], edgecolor="black")
    
    plt.xlabel("Tiempo (minutos)")
    plt.ylabel("Temperatura (ºC)")
    plt.title("Temperatura a lo largo del tiempo")
    plt.legend([f"Intervalo {i + 1}" for i in range(len(intervalos))])
    plt.grid(True)  # Añadir líneas de rejilla
    plt.savefig("graficos/temperatura.png", dpi=200, bbox_inches="tight")  # Guardar gráfico
    plt.show()  # Mostrar gráfico

# Gráfico de luz histórica
def luz_historica(intervalos: list):
    plt.style.use("ggplot")
    fig, axs = plt.subplots(len(intervalos), 1)  # Crear un subplot por intervalo
    etiquetas = ["Oscuro", "Luz"]  # Etiquetas para las barras
    colores = ["#800000", "#ffff00"]  # Colores para las barras

    for idx, intervalo in enumerate(intervalos):
        # Asignar niveles de luz a 'Oscuro' o 'Luz'
        binned = pd.cut(intervalo["light"], np.linspace(0, 300, 3), labels=etiquetas, right=False)
        cuentas = binned.value_counts()  # Contar cuántas veces cae en cada categoría
        axs[idx].barh(cuentas.index, cuentas, color=colores, edgecolor="black")  # Dibujar barras horizontales
        axs[idx].set_title(f'Intervalo {intervalo["intervalo"].iloc[0]}')  # Título del subplot

    axs[1].set_ylabel("Nivel de luz (lux)")
    plt.xlabel("Cantidad de mediciones")
    fig.suptitle("Nivel de luz por intervalo", fontsize=16)  # Título general
    plt.subplots_adjust(hspace=0.45)  # Espaciado entre subplots
    plt.savefig("graficos/luz.png", dpi=200, bbox_inches="tight")  # Guardar gráfico
    plt.show()  # Mostrar gráfico

# Gráfico de nivel de sonido histórica
def sonido_historico(intervalos: list):
    plt.style.use("ggplot")  # Cambiar estilo de gráfico
    fig, axs = plt.subplots(1, len(intervalos), sharex=True)  # Crear subplots

    for idx, intervalo in enumerate(intervalos):
        axs[idx].hist(intervalo["sound-level"], bins=20, color="#707070", edgecolor="black")  # Histograma
        axs[idx].axvline(x=70, color="red", label="Umbral")  # Línea roja para el umbral
        axs[idx].axvline(x=intervalo["sound-level"].mean(), color="orange", label="Promedio")  # Línea para la media
        axs[idx].set_xticks(np.arange(0, 220, 20))  # Definir ticks del eje x
        axs[idx].set_title(f'Intervalo {intervalo["intervalo"].iloc[0]}')  # Título del subplot
    
    plt.legend()  # Mostrar la leyenda
    axs[1].set_xlabel("Nivel de sonido (dB)")  # Etiqueta del eje x
    axs[0].set_ylabel("Cantidad de mediciones")  # Etiqueta del eje y
    fig.suptitle("Nivel de sonido", fontsize=16)  # Título general
    plt.subplots_adjust(wspace=0.45)  # Espaciado entre subplots
    plt.savefig("graficos/sonido.png", bbox_inches="tight", dpi=200)  # Guardar gráfico
    plt.show()  # Mostrar gráfico

# Gráfico de aceleración histórica
def aceleracion_historica(intervalos: list):
    plt.style.use("ggplot")  # Estilo del gráfico
    fig, axs = plt.subplots(len(intervalos), 1)  # Crear un subplot por intervalo
    colores = ["#cc0000", "#ff66ff", "#66cccc"]  # Nuevos colores para las líneas

    for idx, intervalo in enumerate(intervalos):
        # Graficar aceleración en los ejes x, y, y z
        axs[idx].plot(intervalo["sample-id"], intervalo["acc-x"], color=colores[0], label="X")
        axs[idx].plot(intervalo["sample-id"], intervalo["acc-y"], color=colores[1], label="Y")
        axs[idx].plot(intervalo["sample-id"], intervalo["acc-z"], color=colores[2], label="Z")
        axs[idx].set_yticks(np.arange(-2000, 2500, 500))  # Definir ticks del eje y
        axs[idx].set_title(f'Intervalo {intervalo["intervalo"].iloc[0]}')  # Título del subplot

    plt.legend()  # Mostrar leyenda
    axs[1].set_ylabel("Aceleración (mg)")  # Etiqueta del eje y
    plt.xlabel("Cantidad de mediciones")  # Etiqueta del eje x
    fig.suptitle("Aceleración y desaceleración", fontsize=16)  # Título general
    plt.subplots_adjust(hspace=0.55)  # Ajustar el espaciado entre subplots
    plt.savefig("graficos/aceleracion.png", dpi=200)  # Guardar gráfico
    plt.show()  # Mostrar gráfico

# Gráfico de orientación de brújula histórica
def orientacion_brujula(intervalos: list):
    fig, axs = plt.subplots(1, len(intervalos)) # Crear subplots
    etiquetas = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'] # Etiquetas para los sectores
    bins = np.linspace(-22.5, 360 - 22.5, 9) # Bins para los sectores
    
    for idx, intervalo in enumerate(intervalos): # Iterar sobre los intervalos
        binned = pd.cut(intervalo['compass-heading'], bins=bins, labels=etiquetas) # Asignar a sectores
        cuentas = binned.value_counts() # Contar cuántas veces cae en cada sector
        cuentas = cuentas[cuentas != 0] # Eliminar sectores sin datos
        
        axs[idx].pie(cuentas, labels=cuentas.index, autopct='%1.1f%%', pctdistance=0.8) # Gráfico de pastel
        axs[idx].set_title(f'Intervalo {intervalo["intervalo"].iloc[0]}') # Título del subplot
        centro = plt.Circle((0, 0), 0.65, fc='black') # Círculo negro en el centro
        axs[idx].add_artist(centro)
    
    fig.suptitle('Orientación de la brújula', fontsize=16)
    plt.savefig('graficos/orientacionBrujula.png', dpi=200)
    plt.show()

# Mapa de correlaciones
def correlaciones(intervalos: list):
    plt.style.use("ggplot")  # Cambiar estilo
    fig, axs = plt.subplots(1, len(intervalos), figsize=(8, 5))  # Crear subplots

    for idx, intervalo in enumerate(intervalos):
        matriz_corr = intervalo.corr().iloc[:-1, :-1]  # Excluir la última fila y columna
        im = axs[idx].matshow(matriz_corr, cmap="coolwarm")  # Mapa de correlaciones
        fig.colorbar(im, ax=axs[idx])  # Añadir barra de colores
        axs[idx].set_xticks(np.arange(len(matriz_corr.columns)), labels=matriz_corr.columns, rotation=45, ha="right")  # Rotar etiquetas
        axs[idx].set_yticks(np.arange(len(matriz_corr.columns)), labels=matriz_corr.columns)  # Etiquetas en eje y

    fig.suptitle("Mapa de correlaciones", fontsize=16)  # Título general
    plt.subplots_adjust(wspace=0.45)  # Ajustar espaciado entre subplots
    plt.savefig("graficos/correlacion.png", dpi=200)  # Guardar gráfico
    plt.show()  # Mostrar gráfico

# Menú para interacción del usuario
def menu():
    # Obtenemos los datos y generamos los intervalos
    datos_por_intervalo = obtener_datos()  
    intervalos = [datos_por_intervalo.get_group(i) for i in range(1, 4)]  # Obtener primeros tres intervalos
    
    while True:
        opcion = mostrar_menu()  # Mostrar menú y obtener opción
        if opcion == 1:
            todos_los_datos(intervalos)  # Todos los datos
        elif opcion == 2:
            temperatura_historica(intervalos)  # Gráfico de temperatura histórica
        elif opcion == 3:
            luz_historica(intervalos)  # Nivel de luz histórica
        elif opcion == 4:
            sonido_historico(intervalos)  # Nivel de sonido histórico
        elif opcion == 5:
            aceleracion_historica(intervalos)  # Aceleración histórica
        elif opcion == 6:
            orientacion_brujula(intervalos)  # Orientación de brújula
        elif opcion == 7:
            correlaciones(intervalos)  # Mapa de correlaciones
        elif opcion == 8:
            print("Saliendo...")  # Opción para salir
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# Ejecutar el menú 
menu()
