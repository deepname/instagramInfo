import instaloader
from datetime import datetime
import time
import random

class InstagramUser:
    def __init__(self):
        self.loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )

    def get_user_data(self, username):
        """Obtiene la información de un usuario y sus últimos 10 posts."""
        result = {
            "status": "success",
            "data": None,
            "error": None
        }
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            user_data = {
                "username": profile.username,
                "full_name": profile.full_name,
                "biography": profile.biography,
                "followers": profile.followers,
                "following": profile.followees,
                "post_count": profile.mediacount,
                "posts": []
            }
            try:
                posts = list(profile.get_posts())
                for post in posts[:10]:
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
            except instaloader.exceptions.LoginRequiredException:
                # Si no podemos acceder a los posts pero tenemos la info del perfil
                result["status"] = "error"
                result["error"] = "Se requiere iniciar sesión para ver los posts de este usuario"
                result["data"] = user_data
                return result
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
