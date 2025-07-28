import os
import json
from telegram import User, File, Location

DB_FILE = "database/data.json"


def get_all_users() -> list[dict]:
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "x"):
            pass
    
    with open(DB_FILE, 'r+') as f:
        content = f.read()
        if content == "":
            data = {"users": []}
            f.write(json.dumps(data, indent=4))
        else:
            data = json.loads(content)
    
    return data


def create_user(user: User) -> bool:
    data = get_all_users()

    if get_user(user) is None:
        data['users'].append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'gender': None,
                'photo': None,
                'location': None,
                'bio': None,
            })
    
        with open(DB_FILE, "w") as f:
            f.write(json.dumps(data, indent=4))
        
        return True

    else:
        return False


def get_user(user: User) -> dict:
    data = get_all_users()

    result = list(filter(
        lambda temp_user: temp_user['id'] == user.id,
        data['users']
    ))
    if result:
        return result[0]
    else:
        None


def update_user(
        user: User, 
        gender: str | None = None, 
        photo: File | None = None, 
        location: Location | None = None, 
        bio: str | None = None
    ) -> bool:
    data = get_all_users()

    for i, temp in enumerate(data['users']):
        if temp['id'] == user.id:
            if gender:
                temp.update({'gender': gender})
            if photo:
                temp.update({'photo': photo})
            if location:
                temp.update({'location': {
                    'latitude': location.latitude,
                    'longitude': location.longitude
                }})
            if bio:
                temp.update({'bio': bio})
                
            data['users'][i] = temp

    with open(DB_FILE, "w") as f:
        f.write(json.dumps(data, indent=4))


def delete_user(user: User) -> bool:
    data = get_all_users()

    for temp in data['users']:
        if temp['id'] == user.id:
            data['users'].remove(temp)
            break

    with open(DB_FILE, "w") as f:
        f.write(json.dumps(data, indent=4))
