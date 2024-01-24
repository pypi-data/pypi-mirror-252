# Kata Pengantar
Setiap negara yang berdaulat tentunya mempunyai mata uang dan singkatan untuk mempermudah pengucapan. Dalam membuat alat atau program tentunya memerlukan data yang akurat dan tidak salah jika mencoba pustaka ini. Pustaka pycurrency terlengkap perihal data nama negara, nama mata uangnya serta singkatannya dan sangat dipermudah karena setiap datanya disimpan dalam format berkas json.

## Cara Instalasi
Cukup mudah, hanya dengan tempel dan rekatkan di terminal
```bash
pip install pycurrencyid
```

## Cara mengunakan dan contoh program
```python
from pycurrencyid import IsoNegara


# ada dua fungsi utama pada kelas mataUang, semua dan cari
uang = IsoNegara()

print(uang.data_asia)
print(uang.data_eropa)
print(uang.data_afrika)
print(uang.data_australia)
print(uang.data_amerika_utara)
print(uang.data_amerika_selatan)
```
