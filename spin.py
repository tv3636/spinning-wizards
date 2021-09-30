import requests, zipfile, io, os, sys
from PIL import Image

if len(sys.argv) > 1:
	ADDRESS = sys.argv[1]

	CONTRACT = "0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42"
	OPENSEA_API = "https://api.opensea.io/api/v1/assets"
	PAGE_SIZE = 50

	print('Scouring the blockchain for wizards...')

	tokens = []
	response = {'assets': ['']}
	querystring = {
		"owner": ADDRESS,
		"asset_contract_address": CONTRACT,
		"order_direction": "desc",
		"offset": "0",
		"limit": PAGE_SIZE
	}

	while response['assets']:
		response = requests.request("GET", OPENSEA_API, params=querystring).json()
		for wizard in response['assets']:
			tokens.append(int(wizard['token_id']))

		querystring['offset'] = str(int(querystring['offset']) + PAGE_SIZE)

	print('Downloading turnarounds...')
	os.mkdir('./output')

	for token in tokens:
		try:
			r = requests.get("https://www.forgottenrunes.com/api/art/wizards/%d.zip" % token)
			z = zipfile.ZipFile(io.BytesIO(r.content))
			z.extractall("./downloads/%d" % token)

			images = []
			basePath = "./downloads/%d/1024/turnarounds" % token

			for png in sorted(os.listdir(basePath)):
				images.append(Image.open(basePath + '/' + png))

			images[0].save("./output/%d-spin.gif" % token, save_all=True, append_images=images[1:], optimize=False, duration=300, loop=0)
			print("GIF generated for Wizard %d!" % token)
		
		except Exception as e:
			print("Error downloading turnarounds for wizard", token, '-', e)

else:
	print("Please provide your wallet address. Usage: python spin.py [WALLET_ADDRESS]")