# Kata Pengantar
Setiap negara yang berdaulat tentunya mempunyai mata uang dan singkatan untuk mempermudah pengucapan. Dalam membuat alat atau program tentunya memerlukan data yang akurat dan tidak salah jika mencoba pustaka ini. Pustaka pycurrency terlengkap perihal data nama negara, nama mata uangnya serta singkatannya dan sangat dipermudah karena setiap datanya disimpan dalam format berkas json.

## Cara Instalasi
Cukup mudah, hanya dengan tempel dan rekatkan di terminal
```bash
pip install pycurrencyid
```

## Cara mengunakan dan contoh program
Dalam menggunakan pustaka ini pertama -tama pahami dulu program berikut.
```python
from pycurrencyid import mataUang
import pprint


# ada dua fungsi utama pada kelas mataUang, semua dan cari
data = mataUang()

# untuk menampilkan semua data yang ada di pustaka ini
pprint.pprint(data.semua, sort_dicts=False)

# untuk mencari nama negara berdasarkan singkatan mata uangnya
pprint.pprint(data.cari("idr"), sort_dicts=False)
```

## Kata Penutup
Semoga bermanfaat dan jika tertarik dengan program ini dan lainnya, silahkan follow akun sosial media aku lainnya.
