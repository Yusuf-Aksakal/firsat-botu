import os
import requests
import tweepy

# GitHub Secrets'tan anahtarları çekiyoruz
API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

def send_tweet():
    # GamerPower API'den güncel oyun fırsatını al
    url = "https://www.gamerpower.com/api/giveaways"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Fırsatlar API'den çekilemedi.")
        return

    deals = response.json()
    if not deals:
        print("Aktif fırsat bulunamadı.")
        return

    # En güncel fırsatı al
    latest_deal = deals[0]
    title = latest_deal.get("title")
    giveaway_url = latest_deal.get("open_giveaway_url")
    platforms = latest_deal.get("platforms")

    # Tweet metnini oluştur
    tweet_text = f"🔥 Ücretsiz Oyun Fırsatı!\n\n🎮 {title}\n🕹️ Platform: {platforms}\n\n🔗 Hemen Al: {giveaway_url}\n\n#ÜcretsizOyun #OyunFırsatı #Gaming"

    # X API v2 Bağlantısı
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

    try:
        res = client.create_tweet(text=tweet_text)
        print(f"Tweet başarıyla paylaşıldı! ID: {res.data['id']}")
    except Exception as e:
        print(f"Tweet atılırken hata oluştu: {e}")

if __name__ == "__main__":
    send_tweet()
