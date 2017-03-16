with open("usuarios.csv", "r", encoding="utf8") as f:
	for line in f:
		line = line.strip()
		separados = line.split(",")
		print(separados)
	f.close()
