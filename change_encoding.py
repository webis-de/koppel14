import os



#path = '/Users/alexandersauer/Documents/Programmieren/Python/5114.male.25.indUnk.Scorpio.xml'
path = '/Users/alexandersauer/Desktop/blogs/' 

files = [f for f in os.listdir(path)]


for k in range(5): 
	for name in files:
		try: 
			print(name)
			file = open(path+name, 'r')

			text = ''
			for line in file:
				try: 
					text += line
				except UnicodeDecodeError:
					pass
	# 		for line in file:
	# 			text += line
	# 			
			text = text.translate({ord('&'): None})


			target = open(path + name, 'w')
			target.write(text)

			file.close()
			target.close()
		except UnicodeDecodeError:
					pass