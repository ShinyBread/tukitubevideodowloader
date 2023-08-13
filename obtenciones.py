from pytube import YouTube

def obtener_ruta_guardado():
    ruta_guardado = input("Donde lo vas a guardar?: ")
    return ruta_guardado

def obtener_video(url):
    try:
        video = YouTube(url)
        return video
    except Exception as e:
        print("<<< Error al obtener el video >>>:", str(e))
        return None