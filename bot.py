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
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Bot tespitini engelleyen JS enjeksiyonu
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        print("X giriş sayfasına gidiliyor...")
        page.goto("https://x.com/i/flow/login", timeout=60000)
        time.sleep(5)

        # Kullanıcı Adı
        print("Kullanıcı adı giriliyor...")
        username_input = page.wait_for_selector('input[autocomplete="username"], input[name="text"]', timeout=30000)
        username_input.type(USERNAME, delay=100)
        page.keyboard.press("Enter")
        time.sleep(4)

        # Ekstra Güvenlik Sorusu (Email / Telefon)
        extra_input = page.query_selector('input[data-testid="ocfEnterTextTextInput"]')
        if extra_input and extra_input.is_visible():
            print("Ekstra doğrulama istendi, e-posta giriliyor...")
            extra_input.type(EMAIL, delay=100)
            page.keyboard.press("Enter")
            time.sleep(4)

        # Şifre
        print("Şifre giriliyor...")
        password_input = page.wait_for_selector('input[name="password"]', timeout=30000)
        password_input.type(PASSWORD, delay=100)
        page.keyboard.press("Enter")
        time.sleep(6)

        # Tweet Gönderme Ekranı
        print("Tweet ekranına geçiliyor...")
        page.goto("https://x.com/compose/post", timeout=60000)
        time.sleep(4)

        editor = page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=30000)
        editor.click()
        editor.type(tweet_text, delay=30)
        time.sleep(2)

        post_button = page.wait_for_selector('button[data-testid="tweetButton"]', timeout=15000)
        post_button.click()
        print("Tweet gönder butonuna basıldı!")
        
        time.sleep(6)
        browser.close()
        print("İşlem başarıyla tamamlandı.")

if __name__ == "__main__":
    post_tweet()
