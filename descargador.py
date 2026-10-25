"""
Mini descargador de videos por URL.
Usa yt-dlp, que soporta cientos de sitios.
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk

import yt_dlp


class Descargador:
    def __init__(self, root):
        self.root = root
        root.title("Descargador de videos")
        root.geometry("560x260")
        root.resizable(False, False)

        self.carpeta = tk.StringVar(value=os.path.expanduser("~/Descargas"))
        self.solo_audio = tk.BooleanVar(value=False)

        marco = ttk.Frame(root, padding=16)
        marco.pack(fill="both", expand=True)

        # URL
        ttk.Label(marco, text="URL del video:").grid(row=0, column=0, sticky="w")
        self.entrada_url = ttk.Entry(marco, width=60)
        self.entrada_url.grid(row=1, column=0, columnspan=2, sticky="we", pady=(2, 10))
        self.entrada_url.focus()

        # Carpeta de destino
        ttk.Label(marco, text="Guardar en:").grid(row=2, column=0, sticky="w")
        ttk.Entry(marco, textvariable=self.carpeta, width=48).grid(
            row=3, column=0, sticky="we", pady=(2, 10)
        )
        ttk.Button(marco, text="Elegir...", command=self.elegir_carpeta).grid(
            row=3, column=1, padx=(8, 0), pady=(2, 10)
        )

        # Opciones y botón
        ttk.Checkbutton(marco, text="Solo audio", variable=self.solo_audio).grid(
            row=4, column=0, sticky="w"
        )
        self.boton = ttk.Button(marco, text="Descargar", command=self.iniciar)
        self.boton.grid(row=4, column=1, sticky="e")

        # Progreso
        self.barra = ttk.Progressbar(marco, length=520, mode="determinate")
        self.barra.grid(row=5, column=0, columnspan=2, sticky="we", pady=(14, 4))
        self.estado = ttk.Label(marco, text="Pega una URL y presiona Descargar.")
        self.estado.grid(row=6, column=0, columnspan=2, sticky="w")

        marco.columnconfigure(0, weight=1)
        root.bind("<Return>", lambda e: self.iniciar())

    def elegir_carpeta(self):
        ruta = filedialog.askdirectory(initialdir=self.carpeta.get())
        if ruta:
            self.carpeta.set(ruta)

    # Actualiza la interfaz de forma segura desde el hilo de descarga
    def mostrar(self, texto, porcentaje=None):
        def _actualizar():
            self.estado.config(text=texto)
            if porcentaje is not None:
                self.barra["value"] = porcentaje
        self.root.after(0, _actualizar)

    def iniciar(self):
        url = self.entrada_url.get().strip()
        if not url:
            self.mostrar("Primero pega una URL.")
            return
        os.makedirs(self.carpeta.get(), exist_ok=True)
        self.boton.config(state="disabled")
        self.barra["value"] = 0
        threading.Thread(target=self.descargar, args=(url,), daemon=True).start()

    def progreso(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            bajado = d.get("downloaded_bytes", 0)
            if total:
                pct = bajado / total * 100
                self.mostrar(f"Descargando... {pct:.0f}%", pct)
            else:
                self.mostrar(f"Descargando... {bajado / 1_048_576:.1f} MB")
        elif d["status"] == "finished":
            self.mostrar("Terminando...", 100)

    def descargar(self, url):
        # Formatos de un solo archivo: no requieren ffmpeg
        formato = "bestaudio[ext=m4a]/bestaudio" if self.solo_audio.get() else "best[ext=mp4]/best"
        opciones = {
            "format": formato,
            "outtmpl": os.path.join(self.carpeta.get(), "%(title).80B [%(id)s].%(ext)s"),
            "progress_hooks": [self.progreso],
            "noplaylist": True,
            "quiet": True,
            "restrictfilenames": False,
            "windowsfilenames": True,  # quita caracteres raros del nombre
        }
        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
            self.mostrar(f"Listo: {info.get('title', 'video')}", 100)
        except Exception as e:
            self.mostrar(f"Error: {str(e)[:80]}", 0)
        finally:
            self.root.after(0, lambda: self.boton.config(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    Descargador(root)
    root.mainloop()
