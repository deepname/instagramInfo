import sys
import instaloader
from datetime import datetime
import time
import json

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
    
    result = {
        "status": "success",
        "data": None,
        "error": None
    }
    
    try:
        # Obtener el perfil
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Preparar la información del usuario
        user_data = {
            "username": username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "post_count": profile.mediacount,
            "posts": []
        }
        
        # Obtener los posts
        count = 0
        for post in profile.get_posts():
            post_data = {
                "date": post.date.strftime('%Y-%m-%d %H:%M:%S'),
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption if post.caption else "",
                "url": post.url,
                "location": post.location if post.location else None
            }
            user_data["posts"].append(post_data)
            
            count += 1
            if count >= 10:  # Limitar a 10 posts
                break
            # Pequeña pausa para evitar límites de tasa
            time.sleep(1)
        
        result["data"] = user_data
                
    except instaloader.exceptions.ProfileNotExistsException:
        result["status"] = "error"
        result["error"] = f"El usuario '{username}' no existe"
    except instaloader.exceptions.LoginRequiredException:
        result["status"] = "error"
        result["error"] = "Se requiere iniciar sesión para ver esta información"
    except instaloader.exceptions.ConnectionException:
        result["status"] = "error"
        result["error"] = "Problema de conexión con Instagram. Intente más tarde"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    
    return result

def main():
    if len(sys.argv) != 2:
        print("Uso: python instagramInfo.py <nombre_de_usuario>")
        print("Ejemplo: python instagramInfo.py elonmusk")
        sys.exit(1)
    
    username = sys.argv[1]
    result = get_user_posts(username)
    
    # Imprimir el resultado en formato JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()