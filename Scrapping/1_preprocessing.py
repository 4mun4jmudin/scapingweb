import re
import pandas as pd

# 1. Load Data
file_path = "dataTwitter_20000.xlsx"
df = pd.read_excel(file_path)

# Pastikan hanya mengambil kolom 'text'
df = df[["text"]].dropna()


# 2. Fungsi Pembersihan Data (Cleansing)
def clean_twitter_text(text):
    text = text.lower()  # Case folding
    text = re.sub(
        r"https?://\S+|www\.\S+", "", text
    )  # Hapus URL/Link (seperti t.co)
    text = re.sub(r"@\w+", "", text)  # Hapus Mention (@username)
    text = re.sub(r"#\w+", "", text)  # Hapus Hashtag (#qris)
    text = re.sub(r"[^\w\s]", "", text)  # Hapus Tanda Baca & Emoji
    text = re.sub(r"\d+", "", text)  # Hapus Angka
    text = re.sub(r"\s+", " ", text).strip()  # Hapus spasi berlebih
    return text


print("Sedang membersihkan teks...")
df["cleaned_text"] = df["text"].apply(clean_twitter_text)

# 3. Pelabelan Sederhana Berbasis Kamus Kata (Lexicon-based)
# Anda bisa memperluas daftar kata ini sesuai kebutuhan analisis QRIS Anda
positive_words = [
    "mudah",
    "cepat",
    "praktis",
    "gembira",
    "aman",
    "untung",
    "sukses",
    "bagus",
    "setuju",
    "mendukung",
    "bantu",
    "bonus",
    "diskon",
]
negative_words = [
    "error",
    "lambat",
    "gagal",
    "kendala",
    "maaf",
    "rugi",
    "susah",
    "ribet",
    "pending",
    "ditolak",
    "lelet",
    "biaya",
    "admin",
    "menyulitkan",
    "sulit",
    "buruk",
    "kecewa",
    "parah",
    "lemot",
    "potongan",
]


def rtp_labeling(text):
    score = 0
    words = text.split()
    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    # Mengubah skor menjadi label
    if score > 0:
        return "Positif"
    elif score < 0:
        return "Negatif"
    else:
        return "Netral"


print("Sedang melakukan pelabelan otomatis...")
df["label"] = df["cleaned_text"].apply(rtp_labeling)

# Hapus data netral agar fokus pada klasifikasi biner (Positif vs Negatif)
df_filtered = df[df["label"] != "Netral"]

# 4. Simpan ke file baru untuk tahap Machine Learning
df_filtered.to_excel("data_twitter_terlabeli.xlsx", index=False)
print("Selesai! Data siap digunakan untuk Machine Learning.")
print(df_filtered["label"].value_counts())