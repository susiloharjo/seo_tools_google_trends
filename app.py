import time
import random
import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError

# Fungsi untuk menangani permintaan dengan pembatasan kecepatan
def fetch_trends_with_rate_limiting(pytrends, method, *args, **kwargs):
    while True:
        try:
            result = method(*args, **kwargs)
            return result
        except TooManyRequestsError:
            print("Terlalu banyak permintaan. Menunggu sebentar...")
            time.sleep(random.randint(60, 120))  # Tunggu 1-2 menit

# Koneksi ke Google
pytrends = TrendReq(hl='en-US', tz=360)

# Definisikan kata kunci
kw_list = ["AI", "Data Analyst", "LLM", "Machine Learning"]

# Bangun payload
pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='')

# Ambil kueri terkait
# Ambil kueri terkait dan simpan ke dalam satu DataFrame
all_related_queries_df = pd.DataFrame()

for kw in kw_list:
    related_queries = fetch_trends_with_rate_limiting(pytrends, pytrends.related_queries)
    if kw in related_queries and related_queries[kw]['top'] is not None:
        related_queries_df = pd.DataFrame(related_queries[kw]['top'])
        related_queries_df['keyword'] = kw  # Tambahkan kolom kata kunci
        all_related_queries_df = pd.concat([all_related_queries_df, related_queries_df], ignore_index=True)

# Simpan semua kueri terkait ke dalam satu file CSV
if not all_related_queries_df.empty:
    all_related_queries_df.to_csv('all_related_queries.csv', index=False)
    print("Semua kueri terkait disimpan ke 'all_related_queries.csv'")