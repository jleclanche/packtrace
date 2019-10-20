import datetime

import requests

URL = "https://track.bpost.be/btr/api/items"
TRANSLATIONS_URL = "https://track.bpost.be/btr/api/translations"


def track(tracking_number: str):
	r = requests.get(URL, params={"itemIdentifier": tracking_number})
	data = r.json().get("items", [])

	ret = []

	for parcel in data:
		for event in parcel.get("events", []):
			date = datetime.date.fromisoformat(event["date"])
			time = datetime.time.fromisoformat(event["time"])

			ret.append((
				datetime.datetime.combine(date, time),
				event["key"],
				"Irregularity detected" if event["irregularity"] else "",
			))

	if ret:
		translations = get_translations()
		for i, (dt, key, extra) in enumerate(ret):
			ret[i] = (dt, translations["event"][key]["description"], extra)

	return ret


def get_translations(lang: str = "en"):
	return requests.get(TRANSLATIONS_URL, params={"lang": lang}).json()


if __name__ == "__main__":
	import sys
	from tabulate import tabulate

	ret = track(sys.argv[1])

	print(tabulate(ret))
