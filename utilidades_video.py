import os
import time
from moviepy.editor import VideoFileClip, AudioFileClip

def seleccionar_opcion_formato(streams, formato):
    print(f"Seleccione el formato {formato} para descargar:")

    for idx, stream in enumerate(streams, start=1):
        print(f"{idx}. {stream.resolution} - {stream.mime_type}")

    opcion = int(input("Ingresa el formato: "))
    return opcion

def descargar_video_y_audio(stream, ruta_guardado, nombre_archivo=None):
    try:
        print("Descargando...", stream.title)
        if nombre_archivo:
            stream.download(output_path=ruta_guardado, filename=nombre_archivo)
        else:
            stream.download(output_path=ruta_guardado)
        print("Descarga completada!!!")
    except Exception as e:
        print("<<< Error >>>", str(e))

def combinar_video_y_audio(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, codec="libx264")

def eliminar_archivo(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def procesar_video(video, ruta_guardado):
    formato = input("Ingrese el formato deseado (1080p, 720p, 480p, audio): ").strip().lower()

    if formato in ["1080p", "720p", "480p", "audio"]:
        if formato == "audio":
            streams = video.streams.filter(only_audio=True)
            if streams:
                audio_stream = streams.get_highest_resolution()
                nombre_archivo_audio = f"{video.title}_audio.mp3"
                descargar_video_y_audio(audio_stream, ruta_guardado, nombre_archivo=nombre_archivo_audio)
                print("Archivo de audio descargado:", nombre_archivo_audio)
            else:
                print("No se pudo encontrar un formato de audio compatible.")
            return

        if formato == "1080p":
            video_stream = video.streams.filter(adaptive=True, resolution="1080p").first()
            audio_stream = video.streams.filter(only_audio=True).first()
        else:
            if formato == "720p":
                video_stream = video.streams.filter(progressive=True, resolution="720p").first()
            elif formato == "480p":
                video_stream = video.streams.filter(progressive=True, resolution="480p").first()

        if video_stream:
            nombre_archivo_video = f"{video.title}_{formato}.mp4"
            descargar_video_y_audio(video_stream, ruta_guardado, nombre_archivo=nombre_archivo_video)

            if formato == "1080p" and audio_stream:
                nombre_archivo_audio = f"{video.title}_audio.mp3"
                descargar_video_y_audio(audio_stream, ruta_guardado, nombre_archivo=nombre_archivo_audio)

                video_path = os.path.join(ruta_guardado, nombre_archivo_video)
                audio_path = os.path.join(ruta_guardado, nombre_archivo_audio)

                esperar_archivos(video_path, audio_path)

                output_path = os.path.join(ruta_guardado, f"{video.title}_combinado.mp4")
                combinar_video_y_audio(video_path, audio_path, output_path)

                eliminar_archivo(video_path)
                eliminar_archivo(audio_path)

                print("Archivos combinados y guardados como:", output_path)
        else:
            print("Opción no válida.")
    else:
        print("Formato no válido.")

def esperar_archivos(*file_paths):
    for file_path in file_paths:
        while not os.path.exists(file_path):
            time.sleep(1)
