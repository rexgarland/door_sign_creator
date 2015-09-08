"""create_door_signs.py
This script imports from the Python Image Library (PIL), now unsupported but still working fine! A handbook can be found here:
http://effbot.org/imagingbook/pil-index.htm

See last few lines for an example.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pickle, sys, os

wBUF = 200

def get_text_size(draw, width, fontpath, size, text):
	"""Returns the largest size for the given text that can fit within the template image of width 'width'."""
	font = ImageFont.truetype(fontpath, size)
	w, h = draw.textsize(text, font)
	if w>width:
		return get_text_size(draw, width, fontpath, size-5, text)
	else:
		return size

def write_png(name, room, hometown, im, template_font):
	"""Creates an image object of the door sign. Saves the image as a png file in a folder corresponding to the door sign's floor."""
	# create image
	draw = ImageDraw.Draw(im)
	buf = 60
	W, H = im.size

	# draw name
	size = get_text_size(draw, int(W*4.2/7), template_font, 80, name)
	print "Creating sign for '%s', text size %s." % (name, str(size))
	font = ImageFont.truetype(template_font, size)
	w, h = draw.textsize(name, font)
	draw.text(((W-w)/2,(H-h)/2-buf), name, (0,0,0), font=font)

	# draw room number
	f = ImageFont.truetype(template_font, 30)
	txt = Image.new('L', (300,50))
	d = ImageDraw.Draw(txt)
	d.text( (0,0), room, font=f, fill=255)
	w=txt.rotate(6, expand=1)
	im.paste( ImageOps.colorize(w, (0,0,0), (0,0,0)), (125,55), w)

	# draw hometown
	size = get_text_size(draw, int(W*4.0/7), template_font, 40, name)
	font = ImageFont.truetype(template_font, size)
	w, h = draw.textsize(hometown, font)
	draw.text(((W-w)/2,(H-h)/2+buf), hometown, (0,0,0), font=font)

	# save file
	floor = room.split(' ')[-1][0]
	number = room.split(' ')[-1][1:]
	if not os.path.isdir('signs'):
		os.mkdir('./signs')
	if not os.path.isdir('signs/'+'floor'+floor):
		os.mkdir('./signs/'+'floor'+floor)
	filename = 'signs/'+'floor'+floor+'/'+number+'_'+name.split()[-1]+'_'+name.split()[0]+'.png'
	im.save(filename, 'PNG')

if __name__=='__main__':
	# example script
	resident = {'name':'Leland Stanford', 'room':'HooTow 100', 'hometown':'Stanford, CA'}
	im = Image.open('template.png')
	write_png(resident['name'], resident['room'], resident['hometown'], im, "/Library/Fonts/Bohemian Typewriter.ttf")
