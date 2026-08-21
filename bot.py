import requests
import os

def get_free_games():
    url = "https://www.gamerpower.com/api/giveaways"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Toplam {len(data)} fırsat bulundu.")
        for item in data[:3]:  # En güncel 3 oyunu listeler
            print("---")
            print(f"Oyun: {item.get('title')}")
            print(f"Platform: {item.get('platforms')}")
            print(f"Link: {item.get('open_giveaway_url')}")
    else:
        print("Veri çekilemedi, hata kodu:", response.status_code)

if __name__ == "__main__":
    get_free_games()
