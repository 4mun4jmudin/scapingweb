import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

# 1. Load Data Terlabeli (Pastikan file ini sudah ada di folder Anda)
df = pd.read_excel("data_twitter_terlabeli.xlsx")

X = df["cleaned_text"].astype(str)
y = df["label"]

# 2. Split Data (80% Training, 20% Testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Ekstraksi Fitur menggunakan TF-IDF
# PERHATIKAN: Di sini variabel 'tfidf' didefinisikan
tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# 4. Pelatihan Model NAIVE BAYES
# PERHATIKAN: Di sini variabel 'nb_model' didefinisikan
print("\n--- MENJALANKAN NAIVE BAYES ---")
nb_model = MultinomialNB()
nb_model.fit(X_train_tfidf, y_train)

y_pred_nb = nb_model.predict(X_test_tfidf)
print(f"Akurasi Naive Bayes: {accuracy_score(y_test, y_pred_nb):.2%}")

# 5. Pelatihan Model SVM
# PERHATIKAN: Di sini variabel 'svm_model' didefinisikan
print("\n--- MENJALANKAN SVM ---")
svm_model = SVC(kernel="linear")
svm_model.fit(X_train_tfidf, y_train)

y_pred_svm = svm_model.predict(X_test_tfidf)
print(f"Akurasi SVM: {accuracy_score(y_test, y_pred_svm):.2%}")


# 6. MENYIMPAN MODEL KE PICKLE (.pkl)
# Baris ini sekarang aman karena variabel di atas sudah dibuat semua
print("\n--- MENYIMPAN MODEL ---")
with open("nb_model.pkl", "wb") as f:
    pickle.dump(nb_model, f)

with open("svm_model.pkl", "wb") as f:
    pickle.dump(svm_model, f)

with open("tfidf.pkl", "wb") as f:
    pickle.dump(tfidf, f)

print("Semua file model (.pkl) sukses dibuat!")