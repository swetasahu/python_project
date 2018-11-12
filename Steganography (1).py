# Python program implementing Image Steganography

from PIL import Image
import binascii
import optparse
import tkinter as tk
import tkinter.messagebox as ms


# Convert encoding data into 8-bit binary 
# form using ASCII value of characters 
def genData(data): 
		  
		# list of binary codes 
		# of given data 
		newd = []  
		  
		for i in data: 
			newd.append(format(ord(i), '08b')) 
		return newd 


# Pixels are modified according to the 
# 8-bit binary data and finally returned 
def modPix(pix, data): 
	  
	datalist = genData(data) 
	lendata = len(datalist) 
	imdata = iter(pix) 
  
	for i in range(lendata): 
		  
		# Extracting 3 pixels at a time 
		pix = [value for value in imdata.__next__()[:3] +
								  imdata.__next__()[:3] +
								  imdata.__next__()[:3]] 
									  
		# Pixel value should be made  
		# odd for 1 and even for 0 
		for j in range(0, 8): 
			if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
				  
				if (pix[j]% 2 != 0): 
					pix[j] -= 1
					  
			elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
				pix[j] -= 1
				  
		# Eigh^th pixel of every set tells  
		# whether to stop ot read further. 
		# 0 means keep reading; 1 means the 
		# message is over. 
		if (i == lendata - 1): 
			if (pix[-1] % 2 == 0): 
				pix[-1] -= 1
		else: 
			if (pix[-1] % 2 != 0): 
				pix[-1] -= 1
  
		pix = tuple(pix) 
		yield pix[0:3] 
		yield pix[3:6] 
		yield pix[6:9] 


def encode_enc(newimg, data): 
	w = newimg.size[0] 
	(x, y) = (0, 0) 
	  
	for pixel in modPix(newimg.getdata(), data): 
		  
		# Putting modified pixels in the new image 
		newimg.putpixel((x, y), pixel) 
		if (x == w - 1): 
			x = 0
			y += 1
		else: 
			x += 1


# Encode data into image 
def encode(): 
	img = filename.get() 
	image = Image.open(img, 'r') 
	  
	data = msg.get("1.0", tk.END) 
	if (len(data) == 0): 
		raise ValueError('Data is empty') 
		  
	newimg = image.copy() 
	encode_enc(newimg, data)

	new_img_name = filename.get()

	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

	return ("Successfully Encoded in file " + img)


# Decode the data in the image 
def decode(): 
	img = filename.get() 
	image = Image.open(img, 'r') 
	
	data = '' 
	imgdata = iter(image.getdata())

	while (True): 
		pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]] 
		# string of binary data 
		binstr = '' 
		  
		for i in pixels[:8]: 
			if (i % 2 == 0): 
				binstr += '0'
			else: 
				binstr += '1'
				  
		data += chr(int(binstr, 2)) 
		if (pixels[-1] % 2 != 0): 
			return data


def enc_action():
	ms.showinfo("Completed!", encode())


def dec_action():
	msg.delete("1.0", tk.END)
	msg.insert(tk.END, decode())
	ms.showinfo("Extracted!", "Extraction was successful!")


# Setting up the GUI
root = tk.Tk()

# Title of the Window
root.title("Image Encode/Decode")

# Make the Window non-resizable
root.resizable(False, False)

# Label for Image Filename
label_one = tk.Label(root, text="Filename")
label_one.grid(row=0, column=0, sticky=tk.E)

# Image Name input
filename = tk.Entry(root, width=20)
filename.grid(row=0, column=1)

# Label for Message
label_two = tk.Label(root, text="Message")
label_two.grid(row=1, column=0)

# Message Multiline Input
msg = tk.Text(root, width=15, height=4)
msg.grid(row=1, column=1)

# Button to encode the message in the image
enc = tk.Button(root, text="Encode", command=enc_action, width=7)
enc.grid(row=2, column=0)

# Button to decode the message from the image
dec = tk.Button(root, text="Decode", command=dec_action, width=16)
dec.grid(row=2, column=1)

root.mainloop()

# End