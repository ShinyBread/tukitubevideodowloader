from moviepy.editor import VideoFileClip, AudioFileClip
import os
import time

def seleccionar_opcion_formato(streams):
    print("Seleccione el formato para descargar:")

    for idx, stream in enumerate(streams, start=1):
        print(f"{idx}. {stream.resolution} - {stream.mime_type}")

    opcion = int(input("Ingresa el formato: "))
    return opcion

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

def combinar_video_y_audio(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, codec="libx264")

def eliminar_archivo(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def procesar_video(video, ruta_guardado):
    streams = video.streams.filter(adaptive=True, file_extension="mp4")
    opcion_formato = seleccionar_opcion_formato(streams)

    if 1 <= opcion_formato <= len(streams):
        formato_elegido = streams[opcion_formato - 1]
        descargar_video(formato_elegido, ruta_guardado)

        audio_stream = video.streams.filter(only_audio=True, file_extension="mp4").first()
        if audio_stream:
            nombre_archivo_audio = f"{video.title}_audio.mp4"
            descargar_video(audio_stream, ruta_guardado, nombre_archivo=nombre_archivo_audio)

            video_path = os.path.join(ruta_guardado, formato_elegido.default_filename)
            audio_path = os.path.join(ruta_guardado, nombre_archivo_audio)

            esperar_archivos(video_path, audio_path)

            output_path = os.path.join(ruta_guardado, f"{video.title}_combinado.mp4")
            combinar_video_y_audio(video_path, audio_path, output_path)

            eliminar_archivo(video_path)
            eliminar_archivo(audio_path)

            print("Archivos combinados y guardados como:", output_path)
        else:
            print("No se pudo encontrar un formato de audio compatible.")
    else:
        print("Opcion no valida!!.")

def esperar_archivos(*file_paths):
    for file_path in file_paths:
        while not os.path.exists(file_path):
            time.sleep(1)
