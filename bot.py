import os
import time
import requests
from playwright.sync_api import sync_playwright

USERNAME = os.environ.get("X_USERNAME")
PASSWORD = os.environ.get("X_PASSWORD")
EMAIL = os.environ.get("X_EMAIL")

def get_deal():
    url = "https://www.gamerpower.com/api/giveaways"
    res = requests.get(url)
    if res.status_code == 200:
        deals = res.json()
        if deals:
            deal = deals[0]
            return f"🔥 Ücretsiz Oyun Fırsatı!\n\n🎮 {deal.get('title')}\n🕹️ Platform: {deal.get('platforms')}\n\n🔗 {deal.get('open_giveaway_url')}\n\n#ÜcretsizOyun #Gaming"
    return None

def post_tweet():
    tweet_text = get_deal()
    if not tweet_text:
        print("Paylaşılacak fırsat bulunamadı.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("X giriş sayfasına gidiliyor...")
        page.goto("https://x.com/i/flow/login")
        page.wait_for_timeout(4000)

        # Kullanıcı Adı Girişi
        print("Kullanıcı adı giriliyor...")
        page.fill('input[autocomplete="username"]', USERNAME)
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)

        # Şüpheli giriş kontrolü (Email veya telefon sorarsa)
        if page.locator('input[data-testid="ocfEnterTextTextInput"]').is_visible():
            print("Ekstra doğrulama istendi, e-posta giriliyor...")
            page.fill('input[data-testid="ocfEnterTextTextInput"]', EMAIL)
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)

        # Şifre Girişi
        print("Şifre giriliyor...")
        page.fill('input[name="password"]', PASSWORD)
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        # Tweet Gönderme
        print("Tweet hazırlanıyor...")
        page.goto("https://x.com/compose/tweet")
        page.wait_for_timeout(4000)

        editor = page.locator('div[data-testid="tweetTextarea_0"]')
        editor.click()
        editor.fill(tweet_text)
        page.wait_for_timeout(2000)

        post_button = page.locator('button[data-testid="tweetButton"]')
        post_button.click()
        print("Tweet gönder butonuna basıldı!")
        
        page.wait_for_timeout(5000)
        browser.close()
        print("İşlem başarıyla tamamlandı.")

if __name__ == "__main__":
    post_tweet()
