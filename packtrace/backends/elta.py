from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_datetime


URL = "https://www.elta.gr/en-us/personal/tracktrace.aspx"


def track(tracking_number: str):
	session = requests.Session()
	initial_response = session.get(URL).content
	soup = BeautifulSoup(initial_response, "html.parser")

	form = soup.find("form")
	fields = form.find_all("input")

	form_data = {field.get("name"): field.get("value") for field in fields}
	form_data["dnn$ctr1554$View$txtInputCode"] = tracking_number

	post_url = urljoin(URL, form["action"])
	track_response = session.post(post_url, data=form_data)

	response_soup = BeautifulSoup(track_response.text, "html.parser")
	container = response_soup.find("div", {"id": "printme"})
	table = container.find("table")

	ret = []

	cells = table.find_all("td")[3:]  # Skip first row (header)

	for datetime, location, status in zip(*[iter(cells)] * 3):
		ret.append((
			parse_datetime(datetime.text),
			location.text,
			status.text,
		))

	return ret
