import requests
from bs4 import BeautifulSoup


def ekstraksi_data():
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')

        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        koordinat = None
        lokasi = None
        dirasakan = None

        i = 0
        for res in result:
            #print(i, res)
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal
        hasil['waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = koordinat
        hasil['lokasi'] = lokasi
        hasil['keterangan'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(hasil):
    if hasil is None:
        print("Can't find the latest earthquake data")
        return
    print("Latest Earthquake in Indonesia")
    print(f"tanggal : {hasil['tanggal']}")
    print(f"waktu : {hasil['waktu']}")
    print(f"magnitudo : {hasil['magnitudo']}")
    print(f"kedalaman : {hasil['kedalaman']}")
    print(f"koordinat : {hasil['koordinat']}")
    print(f"lokasi : {hasil['lokasi']}")
    print(f"keterangan : {hasil['keterangan']}")


if __name__ == "__main__":
    result = ekstraksi_data()
    tampilkan_data(result)
