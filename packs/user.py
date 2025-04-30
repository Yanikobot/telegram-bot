import json
import math, os
import random


PROFILE_DATA_FILE = "data.json"


def load_profiles():
    if not os.path.exists(PROFILE_DATA_FILE):
        return {}

    with open(PROFILE_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profiles(profiles):
    with open(PROFILE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4)


def get_top_position(user_id):

    profiles = load_profiles()



    sorted_profiles = sorted(profiles.items(), key=lambda x: x[1]["balance"], reverse=True)
    
    # Ищем пользователя в отсортированном списке
    for index, (uid, profile) in enumerate(sorted_profiles, start=1):
        if uid == str(user_id):  # Сравниваем ID как строки для универсальности
            return index
    
    # Если пользователь не найден, возвращаем None
    return None


def create_or_update_profile(userr_id, name):
    profiles = load_profiles()
    user_id = str(userr_id) 

    if user_id not in profiles:
        profiles[user_id] = {
            "name": name,
            "balance": 0,
            "title": "новичок",
            "xp": 10,
            "last_farm_time": 0  
        }
    else:
        profiles[user_id]["name"] = name  

    save_profiles(profiles)
    return profiles[user_id]

def update_profile(userr_id):
    profiles = load_profiles()
    save_profiles(profiles)
    return profiles[userr_id]



def get_lvl(id):
    profil = update_profile(id)
    lvl = profil["xp"] / 10
    return str(lvl)

def farm_coins(idd, name):
    profil = create_or_update_profile(idd, name)
    coin = random.randint(1, profil["xp"])
