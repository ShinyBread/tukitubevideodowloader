from obtenciones import obtener_url, obtener_ruta_guardado, obtener_video
from utilidades_video import seleccionar_opcion_formato, descargar_video, procesar_video

def main():
    url = obtener_url()
    video = obtener_video(url)

    if video:
        ruta_guardado = obtener_ruta_guardado()
        procesar_video(video, ruta_guardado)

if __name__ == "__main__":
    main()
