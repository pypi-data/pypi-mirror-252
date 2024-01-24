from ..mata_uang import asia, eropa, australia, afrika, amerika

class ISO:
    def __init__(self):
        self.iso_benua_asia = asia.Asia().iso4217
        self.iso_benua_eropa = eropa.Eropa().iso4217
        self.iso_benua_australia = australia.Australia().iso4217
        self.iso_benua_afrika = afrika.Afrika().iso4217
        self.iso_benua_amerika_utara = amerika.amerika_utara.AmerikaUtara().iso4217
        self.iso_benua_amerika_selatan = amerika.amerika_selatan.AmerikaSelatan().iso4217 

class Negara:
    def __init__(self):
        self.negara_benua_asia = asia.Asia().negara
        self.negara_benua_eropa = eropa.Eropa().negara
        self.negara_benua_australia = australia.Australia().negara
        self.negara_benua_afrika = afrika.Afrika().negara
        self.negara_benua_amerika_utara = amerika.amerika_utara.AmerikaUtara().negara
        self.negara_benua_amerika_selatan = amerika.amerika_selatan.AmerikaSelatan().negara

class IsoNegara:
    def __init__(self):
        iso = ISO()
        negara = Negara()
        self.data_asia = dict(zip(negara.negara_benua_asia, iso.iso_benua_asia))
        self.data_eropa = dict(zip(negara.negara_benua_eropa, iso.iso_benua_eropa))
        self.data_afrika = dict(zip(negara.negara_benua_afrika, iso.iso_benua_afrika))
        self.data_australia = dict(zip(negara.negara_benua_australia, iso.iso_benua_australia))
        self.data_amerika_utara = dict(zip(negara.negara_benua_amerika_utara, iso.iso_benua_amerika_utara))
        self.data_amerika_selatan = dict(zip(negara.negara_benua_amerika_selatan, iso.iso_benua_amerika_selatan))
