import sys
import instaloader
from datetime import datetime
import time
import json
import random

def get_user_data(loader, username):
    """Obtiene la información de un usuario y sus últimos 10 posts."""
    result = {
        "status": "success",
        "data": None,
        "error": None
    }
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        user_data = {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "post_count": profile.mediacount,
            "posts": []
        }
        for post in profile.get_posts()[:10]:  # Usamos slicing para limitar los posts
            post_data = {
                "date": post.date.strftime('%Y-%m-%d %H:%M:%S'),
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption if post.caption else "",
                "url": post.url,
                "location": post.location if post.location else None
            }
            user_data["posts"].append(post_data)
            time.sleep(random.uniform(1, 3))
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

def get_user_posts(usernames):
    """Obtiene la información de múltiples usuarios."""
    if isinstance(usernames, str):
        usernames = [usernames]

    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )

    results = []
    for username in usernames:
        result = get_user_data(L, username)
        results.append(result)
        if len(usernames) > 1:
            time.sleep(random.uniform(2, 5))
    return results

def main():
    if len(sys.argv) < 2:
        print("Uso: python instagramInfo.py <nombre_de_usuario1> [nombre_de_usuario2 ...]\n")
        print("Ejemplos:")
        print("  Un usuario:    python instagramInfo.py elonmusk")
        print("  Varios usuarios: python instagramInfo.py elonmusk billgates markzuckerberg")
        sys.exit(1)

    usernames = sys.argv[1:]

    start_time = datetime.now()
    print(f"Inicio del script: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    results = get_user_posts(usernames)

    output_file = 'instagram_data.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    end_time = datetime.now()
    print(f"\nDatos guardados en el archivo: {output_file}")
    print(f"Finalización del script: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    time_difference = end_time - start_time
    print(f"Tiempo total transcurrido: {time_difference}")

if __name__ == '__main__':
    main()