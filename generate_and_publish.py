
import openai, requests, os, random
from datetime import datetime

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GUMROAD_KEY = os.getenv("GUMROAD_API_KEY")

business_types = [
    "AI-Powered Marketing Agency",
    "Ebook Publishing Business",
    "Dropshipping Side Hustle",
    "Freelance Graphic Design Service",
    "Personal Branding Coach",
    "Digital Course Creator Kit",
    "Social Media Management Agency",
    "AI Prompt Selling Business",
    "Affiliate Marketing Toolkit",
    "Copywriting Business Starter Pack"
]

def generate_bizkit(topic):
    prompt = f"""Create a complete 'Business in a Box' kit for '{topic}'.
    Include:
    - A brand name and logo idea
    - Website landing page copy
    - A 20-page marketing and business strategy guide
    - 30-day social media content plan
    - A small ebook (10 pages) for lead generation
    Make it professional, premium, and ready-to-use."""
    r = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}],
        max_tokens=7000
    )
    return r.choices[0].message["content"]

def save_bizkit(content, topic):
    filename = f"bizkits/{topic.replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    os.makedirs("bizkits", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def upload_to_gumroad(file_path, title, price):
    url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": GUMROAD_KEY,
        "name": title + " – Complete Business Kit",
        "price": price,
        "description": f"A premium done-for-you business kit for {title}. Includes a 20-page strategy guide, ebook, website copy, and social media plan. PayPal: fargnom14@gmail.com",
        "custom_permalink": title.lower().replace(" ", "-"),
        "tags": "business, startup kit, marketing, AI, side hustle",
        "published": True
    }
    files = {"file": open(file_path, "rb")}
    return requests.post(url, data=data, files=files).json()

if __name__ == "__main__":
    for _ in range(2):  # Upload 2 premium kits per run
        topic = random.choice(business_types)
        content = generate_bizkit(topic)
        file_path = save_bizkit(content, topic)
        gumroad_res = upload_to_gumroad(file_path, topic, random.choice([19900, 29900, 39900, 49900]))  # €199-499
        print("Uploaded business kit:", gumroad_res)
