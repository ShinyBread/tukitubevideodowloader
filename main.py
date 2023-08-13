from urlNavegador import obtener_url_youtube
from obtenciones import obtener_ruta_guardado, obtener_video
from utilidades_video import procesar_video

def main():
    link_video = obtener_url_youtube()
    video = obtener_video(link_video)

    if video:
        ruta_guardado = obtener_ruta_guardado()
        procesar_video(video, ruta_guardado)

if __name__ == "__main__":
    main()
