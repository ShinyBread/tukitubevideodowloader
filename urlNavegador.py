import os
import sqlite3
from shutil import copyfile

def obtener_url_youtube():
    app_data_path = os.environ['LOCALAPPDATA']
    edge_history_db = os.path.join(app_data_path, r'Microsoft\Edge\User Data\Default\History')
    temp_history_db = os.path.join(os.path.dirname(__file__), 'temp_history.db')
    copyfile(edge_history_db, temp_history_db)

    conn = sqlite3.connect(temp_history_db)
    cursor = conn.cursor()

    # Modificamos la consulta para obtener solo las URL de YouTube
    cursor.execute("SELECT url FROM urls WHERE url LIKE '%www.youtube.com%' "
                   "ORDER BY last_visit_time DESC LIMIT 1")
    url = cursor.fetchone()[0]

    conn.close()
    os.remove(temp_history_db)
    return url

url = obtener_url_youtube()
print(url)
