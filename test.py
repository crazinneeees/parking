import requests

def get_location_by_ip(ip=''):
    try:
        # Если ip пустой — запрос будет к твоему IP (серверу)
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data.get('country'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'isp': data.get('isp')
            }
        else:
            return None
    except Exception as e:
        print("Ошибка:", e)
        return None

# Пример использования:
print(get_location_by_ip(''))  # по IP сервера
