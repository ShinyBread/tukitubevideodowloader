from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

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

def descargar_video(video_stream, ruta_guardado, nombre_archivo=None):
    try:
        print("Descargando...", video_stream.title)
        if nombre_archivo:
            video_stream.download(output_path=ruta_guardado, filename=nombre_archivo)
        else:
            video_stream.download(output_path=ruta_guardado)
        print("Descarga completada!!!")
    except Exception as e:
        print("<<< Error >>>", str(e))

def procesar_video(video, ruta_guardado):
    streams = video.streams.filter(adaptive=True, file_extension="mp4")
    opcion_formato = seleccionar_opcion_formato(streams)

    if 1 <= opcion_formato <= len(streams):
        formato_elegido = streams[opcion_formato - 1]
        descargar_video(formato_elegido, ruta_guardado)

        # Descargar audio en formato mp4
        audio_stream = video.streams.filter(only_audio=True, file_extension="mp4").first()
        if audio_stream:
            nombre_archivo_audio = f"{video.title}_audio.mp4"
            descargar_video(audio_stream, ruta_guardado, nombre_archivo=nombre_archivo_audio)

            # Esperar a que ambas descargas estén completas
            while not os.path.exists(os.path.join(ruta_guardado, formato_elegido.default_filename)):
                pass
            while not os.path.exists(os.path.join(ruta_guardado, nombre_archivo_audio)):
                pass

            # Combinar video y audio
            video_path = os.path.join(ruta_guardado, formato_elegido.default_filename)
            audio_path = os.path.join(ruta_guardado, nombre_archivo_audio)
            output_path = os.path.join(ruta_guardado, f"{video.title}_combinado.mp4")

            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(output_path, codec="libx264")

            print("Archivos combinados y guardados como:", output_path)

            # Eliminar archivos originales
            os.remove(video_path)
            os.remove(audio_path)

        else:
            print("No se pudo encontrar un formato de audio compatible.")
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
