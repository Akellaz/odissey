import re
import requests
from bs4 import BeautifulSoup

def get_water_temperatures():
    """Получает температуру воды из корректных источников на seatemperature.ru"""
    
    urls = {
        'moskva': 'https://seatemperature.ru/current/russia/moscow-river-sea-temperature',
        'oka': 'https://seatemperature.ru/current/russia/serpuhov-russia-sea-temperature',
        'ugra': 'https://seatemperature.ru/current/russia/ugra-russia-sea-temperature'
    }
    
    temperatures = {}
    for key, url in urls.items():
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            page = requests.get(url, timeout=10, headers=headers)
            page.raise_for_status()
            soup = BeautifulSoup(page.text, "html.parser")
            
            # Ищем температуру в специфичном элементе
            temp_element = soup.find('div', id='temp1')
            if temp_element:
                # Ищем число с плавающей точкой
                temp_text = temp_element.get_text()
                match = re.search(r'(\d+(?:\.\d+)?)°C', temp_text)
                if match:
                    temperatures[f't_{key}'] = match.group(1)
                else:
                    # Альтернативный поиск во всем тексте
                    temp_text = soup.get_text()
                    match = re.search(r'(\d+(?:\.\d+)?)°C', temp_text)
                    temperatures[f't_{key}'] = match.group(1) if match else 'N/A'
            else:
                # Если не нашли специфичный элемент, ищем во всем тексте
                temp_text = soup.get_text()
                match = re.search(r'(\d+(?:\.\d+)?)°C', temp_text)
                temperatures[f't_{key}'] = match.group(1) if match else 'N/A'
                
        except Exception as e:
            print(f"Ошибка при получении температуры для {key}: {e}")
            temperatures[f't_{key}'] = 'N/A'
    
    return temperatures

# Использование
if __name__ == "__main__":
    temps = get_water_temperatures()
    print(temps)
