import time
import random
from models.instagram_user import InstagramUser

class InstagramController:
    def __init__(self):
        self.model = InstagramUser()

    def get_users_data(self, usernames):
        """Obtiene la información de múltiples usuarios."""
        if isinstance(usernames, str):
            usernames = [usernames]

        results = []
        for username in usernames:
            result = self.model.get_user_data(username)
            results.append(result)
            if len(usernames) > 1:
                time.sleep(random.uniform(2, 5))
        return results
