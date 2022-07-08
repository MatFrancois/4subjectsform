import json
import numpy as np
from tqdm import tqdm
# script to filter our data on id list created before

def read_data():
    with open('users_with_cluster.json', 'r') as f:
        return json.load(f)

def main():
    id_list = np.loadtxt('id_list.txt', dtype=str)
    users_with_cluster = read_data()
    new_json = {}
    for user, user_att in tqdm(users_with_cluster.items()):
        filtered_id = list(filter(
            lambda x: str(x) in id_list,
            user_att.get('id')
        ))
        new_json[user] = {
                "id": filtered_id,
                "score": {
                    "db": user_att.get('score').get('db'),
                    "da": user_att.get('score').get('da'),
                },
                "desc": user_att.get('desc'),
                "profil_image_url": user_att.get('profil_image_url')
        }
    with open('filtered_users_on_embed.json', 'w') as f:
        json.dump(new_json, f)
        
if __name__ == "__main__":
    main()
