# Descargador de videos

Pequeña aplicación de escritorio en Python para descargar videos (o solo el audio) pegando la URL.
Usa [yt-dlp](https://github.com/yt-dlp/yt-dlp), que funciona con cientos de sitios.

## Características

- Ventana sencilla: pegás la URL y presionás **Descargar** (o Enter).
- Opción **Solo audio**.
- Elegís la carpeta donde se guarda.
- Barra de progreso con porcentaje.
- La ventana no se congela mientras descarga (la descarga corre en un hilo aparte).
- No necesita `ffmpeg`.

## Requisitos

- Python 3.8 o superior
- Tkinter (en Linux: `sudo apt install python3-tk`)

## Instalación

```bash
git clone https://github.com/ErickCr96/descagador_videos.py.git
cd descagador_videos.py
python3 -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
python descargador.py
```

1. Pegá la URL del video.
2. (Opcional) Elegí otra carpeta o marcá **Solo audio**.
3. Presioná **Descargar**.

## Mantenerlo funcionando

Los sitios de video cambian seguido. Si una descarga falla, actualizá yt-dlp:

```bash
pip install -U yt-dlp
```

## Aviso

Usá esta herramienta solo con contenido que tengás derecho a descargar y respetando
los términos de uso de cada sitio.

## Licencia

MIT. Mirá el archivo [LICENSE](LICENSE).
