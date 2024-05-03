import http.client

conn = http.client.HTTPSConnection("tvjan-tvmaze-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "6b8ac29e2emsh6ab8ab839308489p1bc14ejsnd16b0a7410d3",
    'X-RapidAPI-Host': "tvjan-tvmaze-v1.p.rapidapi.com"
}

conn.request("GET", "/schedule?country=FR", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))