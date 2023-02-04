import re
import requests

def extract_urls(text):
    urls = re.findall(r'https?://\S+', text)
    return urls

def get_redirected_urls(urls):
    redirected_urls = []
    for url in urls:
        res = requests.head(url, allow_redirects=True)
        redirected_urls.append(res.url)
    return redirected_urls

text = """I rated Don't Say a Word 7/10 #IMDb https://t.co/pNWBRj7iou
I rated Severance: Defiant Jazz (S1.E7) 10/10 #IMDb https://t.co/FeqiXSsBPX
I rated The Last of Us: Long, Long Time (S1.E3) 10/10 #IMDb That is one of the best hours of TV ever. Wow just wow! https://t.co/CIdAPmxabb
I rated You People (2023) 8/10 #IMDb https://t.co/nBxMhRMtPI"""

urls = extract_urls(text)
redirected_urls = get_redirected_urls(urls)
print(redirected_urls)
