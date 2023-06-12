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
