from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

#MongoDB için gerekli kütüphaneler
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://emirhanbal:{password}@graduation.r68pz0b.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

#MONGODB ile kodumu ilişkilendirme adımı. burada database'imi bağlıyorum.
db = client["ilanlar"]
collection = db["arac_detay_arabamcom"]
dataFromDatabase = list(collection.find())

dataFromDatabase = list(collection.find())
# Convert entire collection to Pandas dataframe
import pandas as pd
_df = pd.DataFrame(dataFromDatabase)
# verilerimin içerisinde 10binden küçük veya 15milyondan büyük fiyatlı olanları kontrol ediyorum.
_df[(_df.Fiyat<10000) | (_df.Fiyat>15000000) | (_df.Kilometre>1000000)]
# ve bunları verilerim arasından çıkarıyorum
_df.drop(_df[(_df.Fiyat < 10000) | (_df.Fiyat > 15000000) | (_df.Kilometre>1000000)].index, inplace=True)
# boya değişen olanları 'Var' olarak değiştiriyorum
_df.Boya_degisen[(_df.Boya_degisen!='Tamamı orjinal') & (_df.Boya_degisen!='Belirtilmemiş')] = 'Var'
columns_to_keep = ['Fiyat', 'Marka', 'Seri', 'Yil', 'Kilometre', 'Vites_Tipi', 'Yakit_Tipi', 'Boya_degisen'] #'Model', 'Seri',
_df = _df[columns_to_keep]

from sklearn.impute import KNNImputer

for column in _df.columns:
    if _df[column].dtype == 'object':
        most_frequent_value = _df[column].mode().values[0]
        _df[column].fillna(most_frequent_value, inplace=True)
    else:
        imputer = KNNImputer(n_neighbors=5)
        column_data = _df[column].values.reshape(-1, 1)
        _df[column] = imputer.fit_transform(column_data)
_df['Yil'] = _df['Yil'].astype(int)
_df['Fiyat'] = _df['Fiyat'].astype(int)
_df['Kilometre'] = _df['Kilometre'].astype(int)
import pandas as pd

# One-Hot Encoding işlemi
yakit_Tipi_encoded = pd.get_dummies(_df['Yakit_Tipi'], prefix='Yakit_Tipi')
vites_Tipi_encoded = pd.get_dummies(_df['Vites_Tipi'], prefix='Vites_Tipi')
boya_degisen_encoded = pd.get_dummies(_df['Boya_degisen'], prefix='Boya_degisen')

from sklearn.preprocessing import LabelEncoder

# Marka sütununu seçme
Marka = _df['Marka']
Seri = _df['Seri']

from sklearn.preprocessing import LabelEncoder

# Marka sütununu seçme
Marka = _df['Marka']
# Seri sütununu seçme
Seri = _df['Seri']

# LabelEncoder nesnesini oluşturma ve dönüşümü yapma
label_encoder = LabelEncoder()

# Marka sütununu dönüştürme
marka_encoded = label_encoder.fit_transform(Marka)
# Dönüştürülen değerleri _df'e ekleme
_df['Marka_Encoded'] = marka_encoded
# Her bir sayısal değerin karşılık gelen markasını elde etme
marka_degerleri = label_encoder.classes_
# Her bir sayısal değerin ve karşılık gelen markanın ekrana yazdırılması
marka_sozlugu = {sayisal_deger: marka for sayisal_deger, marka in enumerate(marka_degerleri)}

# Seri sütununu dönüştürme
seri_encoded = label_encoder.fit_transform(Seri)
# Dönüştürülen değerleri _df'e ekleme
_df['Seri_Encoded'] = seri_encoded
# Her bir sayısal değerin karşılık gelen serisini elde etme
seri_degerleri = label_encoder.classes_
# Her bir sayısal değerin ve karşılık gelen serinin ekrana yazdırılması
seri_sozlugu = {sayisal_deger: seri for sayisal_deger, seri in enumerate(seri_degerleri)}


_df.drop(['Seri'],axis=1,inplace=True)
_df.drop(['Marka'],axis=1,inplace=True)
# Yeni sütunları ekleme
_df = pd.concat([_df, yakit_Tipi_encoded, vites_Tipi_encoded, boya_degisen_encoded], axis=1)
_df = _df.drop(['Yakit_Tipi', 'Vites_Tipi', 'Boya_degisen'], axis=1)

yakit_tipi_sozlugu = {
    'Benzin': [1, 0, 0, 0, 0],
    'Dizel': [0, 1, 0, 0, 0],
    'Elektrik': [0, 0, 1, 0, 0],
    'Hibrit': [0, 0, 0, 1, 0],
    'LPG & Benzin': [0, 0, 0, 0, 1]
}

vites_tipi_sozlugu = {
    'Düz': [1, 0, 0],
    'Otomatik': [0, 1, 0],
    'Yarı Otomatik': [0, 0, 1]
}

boya_degisen_sozlugu = {
    'Belirtilmemiş': [1, 0, 0],
    'Tamamı orjinal': [0, 1, 0],
    'Var': [0, 0, 1]
}

from sklearn.model_selection import train_test_split

# Bağımsız değişkenler (X) ve hedef değişken (y) olarak ayırma
X = _df.drop('Fiyat', axis=1)  # Hedef sütunu çıkararak bağımsız değişkenleri alıyoruz
y = _df['Fiyat']  # Hedef sütunu olarak ayarlanmış olan sütunu alıyoruz

# Veri kümesini eğitim ve test kümelerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Eğitim ve test kümelerinin boyutlarını kontrol etmek
print("Eğitim kümesi boyutu:", X_train.shape)
print("Test kümesi boyutu:", X_test.shape)

#Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
regressor=RandomForestRegressor(n_estimators=200,min_samples_split=2,min_samples_leaf=2,max_features='sqrt', max_depth=80, bootstrap=True)
regressor.fit(X_train,y_train)
y_pred_randf=regressor.predict(X_test)

from flask import Flask, request, jsonify , render_template

app = Flask(__name__)
def predict_price(regressor, input_data):
    # Girdi verilerini modele uygula ve çıktıyı al
    predicted_price = regressor.predict(input_data)

    # Tahmin edilen fiyatı döndür
    return predicted_price
# HTML formunu görüntülemek için GET isteği
@app.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # Process the form data and predict
        yil = int(request.form['yil'])
        kilometre = int(request.form['kilometre'])
        yakit_tipi = request.form['yakit_tipi']
        vites_tipi = request.form['vites_tipi']
        boya_degisen = request.form['boya_degisen']
        marka = request.form['marka']
        seri = request.form['seri']
        # ... rest of the processing and prediction code...
        # Prediction part stays the same
        yakit_tipi_kod = yakit_tipi_sozlugu.get(yakit_tipi, [0] * len(yakit_tipi_sozlugu))
        vites_tipi_kod = vites_tipi_sozlugu.get(vites_tipi, [0] * len(vites_tipi_sozlugu))
        boya_degisen_kod = boya_degisen_sozlugu.get(boya_degisen, [0] * len(boya_degisen_sozlugu))

        # Marka and Series encoding remains the same
        marka_kod = marka_sozlugu.get(marka, -1)
        seri_kod = seri_sozlugu.get(seri, -1)

        input_data = [[yil, kilometre] + yakit_tipi_kod + vites_tipi_kod + boya_degisen_kod + [marka_kod, seri_kod]]

        predicted_price = predict_price(regressor, input_data)
        return render_template('index.html', predicted_price=predicted_price)
    else:
        return render_template('index.html')
    
#return render_template('index.html')
    
    # You should extract the required features from the data received
    # You should sanitize your data here


    # Process your data here
if __name__ == '__main__':
    app.run()
