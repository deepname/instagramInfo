import sys
import instaloader
from datetime import datetime
import time

def get_user_posts(username):
    # Crear una instancia de Instaloader con algunas configuraciones para evitar bloqueos
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )
    
    try:
        print(f"Buscando información del usuario '{username}'...")
        # Obtener el perfil
        profile = instaloader.Profile.from_username(L.context, username)
        
        print(f"\nInformación encontrada para @{username}:")
        print(f"Nombre completo: {profile.full_name}")
        print(f"Biografía: {profile.biography}")
        print(f"Seguidores: {profile.followers}")
        print(f"Siguiendo: {profile.followees}")
        print(f"Número de posts: {profile.mediacount}")
        print("\nÚltimos posts:")
        
        # Obtener los posts
        count = 0
        for post in profile.get_posts():
            print(f"\nFecha: {post.date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Likes: {post.likes}")
            print(f"Comentarios: {post.comments}")
            print(f"Descripción: {post.caption if post.caption else 'Sin descripción'}")
            print("-" * 50)
            
            count += 1
            if count >= 10:  # Limitar a 10 posts
                break
            # Pequeña pausa para evitar límites de tasa
            time.sleep(1)
                
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: El usuario '{username}' no existe")
    except instaloader.exceptions.LoginRequiredException:
        print("Error: Se requiere iniciar sesión para ver esta información")
    except instaloader.exceptions.ConnectionException:
        print("Error: Problema de conexión con Instagram. Intente más tarde")
    except Exception as e:
        print(f"Error al obtener la información: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python instagramInfo.py <nombre_de_usuario>")
        print("Ejemplo: python instagramInfo.py elonmusk")
        sys.exit(1)
    
    username = sys.argv[1]
    get_user_posts(username)

if __name__ == '__main__':
    main()