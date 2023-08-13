from pytube import YouTube

def obtener_url():
    url = input("URL del video: ")
    return url

def obtener_ruta_guardado():
    ruta_guardado = input("Donde lo vas a guardar?: ")
    return ruta_guardado

def seleccionar_opcion_formato(streams):
    print("Seleccione el formato para descargar:")

    for idx, stream in enumerate(streams, start=1):
        print(f"{idx}. {stream.resolution} - {stream.mime_type}")

    opcion = int(input("Ingresa el formato: "))
    return opcion

def obtener_video(url):
    try:
        video = YouTube(url)
        return video
    except Exception as e:
        print("<<< Error al obtener el video >>>:", str(e))
        return None

def descargar_video(video_stream, ruta_guardado):
    try:
        print("Descargando...", video_stream.title)
        video_stream.download(output_path=ruta_guardado)
        print("Descarga completada!!!")
    except Exception as e:
        print("<<< Error >>>", str(e))

def procesar_video(video, ruta_guardado):
    streams = video.streams.filter(progressive=True, file_extension="mp4")
    opcion_formato = seleccionar_opcion_formato(streams)

    if 1 <= opcion_formato <= len(streams):
        formato_elegido = streams[opcion_formato - 1]
        descargar_video(formato_elegido, ruta_guardado)
    else:
        print("Opcion no valida!!.")

def main():
    url = obtener_url()
    video = obtener_video(url)

    if video:
        ruta_guardado = obtener_ruta_guardado()
        procesar_video(video, ruta_guardado)

if __name__ == "__main__":
    main()
