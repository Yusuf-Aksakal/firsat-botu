import os
import requests
import tweepy

API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

def send_tweet():
    url = "https://www.gamerpower.com/api/giveaways"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Fırsatlar API'den çekilemedi.")
        return

    deals = response.json()
    if not deals:
        print("Aktif fırsat bulunamadı.")
        return

    latest_deal = deals[0]
    title = latest_deal.get("title")
    giveaway_url = latest_deal.get("open_giveaway_url")
    platforms = latest_deal.get("platforms")

    tweet_text = f"🔥 Ücretsiz Oyun Fırsatı!\n\n🎮 {title}\n🕹️ Platform: {platforms}\n\n🔗 Hemen Al: {giveaway_url}\n\n#ÜcretsizOyun #OyunFırsatı #Gaming"

    # v1.1 API Bağlantısı (Pay Per Use sınırına takılmaz)
    auth = tweepy.OAuth1UserHandler(
        API_KEY, API_SECRET,
        ACCESS_TOKEN, ACCESS_SECRET
    )
    api = tweepy.API(auth)

    try:
        status = api.update_status(status=tweet_text)
        print(f"Tweet başarıyla paylaşıldı! ID: {status.id}")
    except Exception as e:
        print(f"Tweet atılırken hata oluştu: {e}")

if __name__ == "__main__":
    send_tweet()
