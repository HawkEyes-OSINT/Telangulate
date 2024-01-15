from telethon.tl import functions, types
from unittest import result


async def get_users(client, coordinates):
    output = []
    distances = []

    for coordinate in coordinates:
        try:
            result = await client(functions.contacts.GetLocatedRequest(
            geo_point=types.InputGeoPoint(
                    lat=coordinate[0],
                    long=coordinate[1],
                    accuracy_radius=42
                ),
                self_expires=42,
            ))


            # get distances for users
            for user in result.updates[0].peers:
                try:
                    if hasattr(user, 'distance') and hasattr(user, 'peer'):
                        distances.append({
                            'user_id': user.peer.user_id,
                            'distance': user.distance,
                        })
                except:
                    pass

            # get additional data for users
            for user in result.users:
                for distance_data in distances:
                    if user.id == distance_data['user_id']:
                        output.append({
                            'ALIAS': user.username,
                            'FIRST NAME': user.first_name,
                            'LAST NAME': user.last_name,
                            'PHONE': user.phone,
                            # ------
                        })

        except Exception as e:
            print(f'[-] Could not get users at {coordinate[0]}, {coordinate[1]}')
            print(e)
            return []
    
    return output

