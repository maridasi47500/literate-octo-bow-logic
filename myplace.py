import subprocess
from fichier import Fichier
import geopy
from geopy.geocoders import Nominatim
 
# Création d'un objet géocodeur Nominatim

class Myplace:
    def __init__(self,lieu="lieu"):
        print("========================")
        self.lieu=lieu

    def trouver1(self):
        geolocator = Nominatim(user_agent="my_geocoder")
         
        # Géocodage d'une adresse
        location = geolocator.geocode(self.lieu)
        print(location.raw)
         
        # Affichage des informations de localisation
        print("Adresse:", location.address,"Latitude:", str(location.latitude), "Longitude:", location.longitude)
        code=location.address.split(", ")[-2]
        pays=location.address.split(", ")[-3]
        try:
          region=location.address.split(", ")[-4]
        except:
          region="ma region"
        city=location.address.split(", ")[0]
        return [city,code, region, pays, str(location.latitude), str(location.longitude)]
        return x
    def trouver(self):
        geolocator = Nominatim(user_agent="my_geocoder")
         
        # Géocodage d'une adresse
        location = geolocator.geocode(self.lieu)
        print(location.raw)
         
        # Affichage des informations de localisation
        print("Adresse:", location.address,"Latitude:", str(location.latitude), "Longitude:", location.longitude)
        code=location.address.split(", ")[-2]
        pays=location.address.split(", ")[-3]
        city=location.address.split(", ")[0]
        return [city,code, pays, str(location.latitude), str(location.longitude)]
        return x

