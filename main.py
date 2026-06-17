import customtkinter as ctk
import tkinter as tk ##Librería para la interfaz que se abre en otra ventana
from tkinter import messagebox ##Muestra pequeñas ventanas de alerta o error
from tkinter import filedialog
from dotenv import load_dotenv ##Busca el archivo y las variables escritas en el
from openai import OpenAI
from pypdf import PdfReader
import os ##Permite leer variables del sistema o entorno

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

load_dotenv() ##Carga las variables del .env para no escribir la API Key directamente en el código
api_key = os.getenv("OPENAI_API_KEY") #Recupera la API Key de las variables de entorno

if api_key is None or api_key == "":
    messagebox.showerror(
        "Error",
        "No se encontro la API Key. Revisa el archivo .env"
    )
cliente = OpenAI(api_key=api_key) #Se conecta la App con el API de OpenAI 

# Crear la ventana principal
ventana = ctk.CTk() ##Abre ventana principal
ventana.title("⚡️JD Spark - Asistente de Estudio IA")
ventana.geometry("730x710")
ventana.configure(fg_color="#1e1e1e")

contenedor = ctk.CTkFrame(
    ventana,
    fg_color="#242424",
    corner_radius=18
)
contenedor.pack(padx=25, pady=25, fill="both", expand=True)

# Titulo de la app

titulo = ctk.CTkLabel(
    contenedor,
    text="⚡️JD Spark",
    font=("Arial", 30, "bold"),
    text_color="#FFFFFF"
) ## Contiene la etiqueta que esta en la ventana (titulo)
titulo.pack(pady=(20, 5)) ## el pack acomoda el texto 

subtitulo = ctk.CTkLabel(
    contenedor,
    text="Carga apuntes, resume contenido y genera preguntas con IA",
    font=("Arial", 13),
    text_color="#A3A3A3"
)
subtitulo.pack(pady=(0, 10))

# Texto de instruccion
#instruccion = ctk.CTkLabel(
  #  contenedor,
   # text="Escribe texto o carga un PDF para empezar:",
   # font=("Arial", 14),
   # text_color="#CFCFCF"
#)
#instruccion.pack(pady=(0, 10))


# Cuadro donde el usuario escribe
entrada_texto = ctk.CTkTextbox(
    contenedor,
    height=135,
    width=540,
    fg_color="#2B2B2B",
    text_color="#FFFFFF",
    corner_radius=12,
    border_width=1,
    border_color="#3A3A3A"
)
entrada_texto.pack(pady=10) #Muestra el cuadro en la ventana 

placeholder_entrada = "Escribe texto o carga un PDF para empezar:"

entrada_texto.insert("1.0", placeholder_entrada)
entrada_texto.configure(text_color="#9CA3AF")

# Cuadro donde despues aparecera la respuesta
salida_texto = ctk.CTkTextbox(
    contenedor,
    height=165,
    width=540,
    fg_color="#2B2B2B",
    text_color="#FFFFFF",
    corner_radius=12,
    border_width=1,
    border_color="#3A3A3A"
)
salida_texto.pack(pady=10)

#Inicio de las funciones principales

def consultar_ia(instruccion): ##La funcion contiene el texto que enviamos al AI
    try: # Intenta ejecutar el codigo que podría fallar
        respuesta = cliente.responses.create( #Envía soli a OpenAI
            model="gpt-4o-mini",
            input=instruccion
        )

        return respuesta.output_text # Devuelve el texto generado por AI

    except Exception as error:
        print("ERROR REAL:", error)

        messagebox.showerror(
            "Error",
            "Ocurrio un problema al consultar la IA. Revisa la terminal para ver el detalle."
        )
        return "Error: no se pudo obtener respuesta de la IA."

def resumir_texto():
    texto_usuario = entrada_texto.get("1.0", tk.END).strip()

    if texto_usuario == "" or texto_usuario == placeholder_entrada:
        messagebox.showwarning(
            "Advertencia",
            "Primero escribe o pega un texto para resumir."
        )
        return

    instruccion = "Resume el siguiente texto de forma clara y breve:\n\n" + texto_usuario

    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, "Generando resumen...")
    estado_label.configure(text="Consultando IA...", text_color="#FACC15")
    ventana.update()

    respuesta = consultar_ia(instruccion)

    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, respuesta)
    estado_label.configure(text="Resumen generado correctamente", text_color="#22C55E")


def explicar_concepto():
    texto_usuario = entrada_texto.get("1.0", tk.END).strip()

    if texto_usuario == "" or texto_usuario == placeholder_entrada:
        messagebox.showwarning(
            "Advertencia",
            "Primero escribe un concepto, tema o texto para explicar."
        )
        return

    instruccion = (
        "Explica el siguiente tema de forma sencilla, clara y como si fueras "
        "un tutor academico para un estudiante de primer año:\n\n"
        + texto_usuario
    )

    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, "Generando explicacion...")
    estado_label.configure(text="Consultando IA...", text_color="#FACC15")
    ventana.update()

    respuesta = consultar_ia(instruccion)

    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, respuesta)
    estado_label.configure(text="Explicacion generada correctamente", text_color="#22C55E")


def generar_preguntas():
    texto_usuario = entrada_texto.get("1.0", tk.END).strip()

    if texto_usuario == "" or texto_usuario == placeholder_entrada:
        messagebox.showwarning(
            "Advertencia",
            "Primero escribe un tema, texto o carga un PDF para generar preguntas."
        )
        return

    instruccion = (
        "Crea 5 preguntas de practica basadas en el siguiente contenido. "
        "Incluye tambien una respuesta breve para cada pregunta:\n\n"
        + texto_usuario
    )

    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, "Generando preguntas...")
    estado_label.configure(text="Consultando IA...", text_color="#FACC15")
    ventana.update()

    respuesta = consultar_ia(instruccion)

    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, respuesta)
    estado_label.configure(text="Preguntas generadas correctamente", text_color="#22C55E")


def limpiar_campos():
    entrada_texto.delete("1.0", tk.END)
    salida_texto.delete("1.0", tk.END)

    entrada_texto.insert("1.0", placeholder_entrada)
    entrada_texto.configure(text_color="#9CA3AF")

    estado_label.configure(text="Listo para estudiar",
                           text_color="#9CA3AF")

def borrar_placeholder_entrada(event):
    texto_actual = entrada_texto.get("1.0", tk.END).strip() ##Obtiene el texto actual del cuadro, () lee todo el contenido y strip quit espacios y saltos de linea

    if texto_actual == placeholder_entrada: 
        entrada_texto.delete("1.0", tk.END)
        entrada_texto.configure(text_color="#FFFFFF")

def cargar_pdf(): 
    ruta_pdf = filedialog.askopenfilename( #Selecciona el archivo en otra ventana
        title="Selecciona un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")] #Hace que la ventana muestre en especifico archivos .pdf
    )

    if ruta_pdf == "":
        return

    try:
        lector_pdf = PdfReader(ruta_pdf) #Abre el PDF usando PdfReader
        texto_pdf = "" ##Crea variable vacía para ser acumuladora del texto

        for pagina in lector_pdf.pages:
            texto_pagina = pagina.extract_text()

            if texto_pagina: #Revisa si la pagina tiene texto
                texto_pdf += texto_pagina + "\n" #Agrega el texto de la pagina a la var del text_pdf

        if texto_pdf.strip() == "":
            messagebox.showwarning(
                "Advertencia",
                "No se pudo extraer texto del PDF. Puede ser un PDF escaneado."
            )
            return

        entrada_texto.delete("1.0", tk.END)
        entrada_texto.configure(text_color="#FFFFFF")
        entrada_texto.insert(tk.END, texto_pdf)
        estado_label.configure(text="PDF cargado correctamente",
                               text_color="#22C55E")

    except Exception as error:
        print("ERROR AL LEER PDF:", error)

        messagebox.showerror(
            "Error",
            "Ocurrio un problema al leer el PDF."
        )

def copiar_respuesta():
    respuesta = salida_texto.get("1.0", tk.END).strip()

    if respuesta == "":
        messagebox.showwarning(
            "Advertencia",
            "No hay respuesta para copiar."
        )
        return

    ventana.clipboard_clear() ##Limpia el portapapeles antes de copiar
    ventana.clipboard_append(respuesta) ##Agrega el texto al portapapeles para que se pueda pegar en otro lado

    estado_label.configure(text="Respuesta copiada al portapapeles")

entrada_texto.bind("<Key>", borrar_placeholder_entrada) ##Conecta el cuadro de texto con la funcion

# Inicio de configuracion visual de botones
frame_botones = ctk.CTkFrame(
    contenedor,
    fg_color="transparent"
)
frame_botones.pack(pady=20)

boton_pdf = ctk.CTkButton(
    frame_botones,
    text="📄 Cargar PDF",
    width=180,
    height=38,
    corner_radius=12,
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    text_color="#FFFFFF",
    command=cargar_pdf
)
boton_pdf.grid(row=0, column=0, padx=8, pady=6)

boton_resumir = ctk.CTkButton(
    frame_botones,
    text="📝 Resumir",
    width=180,
    height=38,
    corner_radius=12,
    fg_color="#7C3AED",
    hover_color="#6D28D9",
    text_color="#FFFFFF",
    command=resumir_texto
)
boton_resumir.grid(row=0, column=1, padx=8, pady=6)

boton_explicar = ctk.CTkButton(
    frame_botones,
    text="💡 Explicar",
    width=180,
    height=38,
    corner_radius=12,
    fg_color="#0891B2",
    hover_color="#0E7490",
    text_color="#FFFFFF",
    command=explicar_concepto
)
boton_explicar.grid(row=1, column=0, padx=8, pady=6)

boton_preguntas = ctk.CTkButton(
    frame_botones,
    text="❓ Generar preguntas",
    width=180,
    height=38,
    corner_radius=12,
    fg_color="#9333EA",
    hover_color="#7E22CE",
    text_color="#FFFFFF",
    command=generar_preguntas
)
boton_preguntas.grid(row=1, column=1, padx=8, pady=6)

boton_copiar = ctk.CTkButton(
    frame_botones,
    text="📋 Copiar respuesta",
    width=180,
    height=38,
    corner_radius=12,
    fg_color="#16A34A",
    hover_color="#15803D",
    text_color="#FFFFFF",
    command=copiar_respuesta
)
boton_copiar.grid(row=2, column=0, padx=8, pady=6)

boton_limpiar = ctk.CTkButton(
    frame_botones,
    text="🧹 Limpiar",
    width=180,
    height=38,
    corner_radius=12,
    fg_color="#4B5563",
    hover_color="#374151",
    text_color="#FFFFFF",
    command=limpiar_campos
)
boton_limpiar.grid(row=2, column=1, padx=8, pady=6)

estado_label = ctk.CTkLabel(
    contenedor,
    text="Listo para estudiar",
    font=("Arial", 12),
    text_color="#9CA3AF"
)
estado_label.pack(pady=(5, 0))

# Mantener la ventana abierta
ventana.mainloop()