'''
	Script to resize images and videos
	By Laurent Ferhi
	Need to have ffmpeg installed and added to the PATH
'''

import PIL
from PIL import Image
import os
from zipfile import ZipFile, ZIP_DEFLATED

def process_folder(folder_name):
	# Zip files in folder
	os.chdir(folder_name)
	with ZipFile(folder_name+'.zip','w') as z:
		for name in [file for file in os.listdir() if file[-3:] != 'zip']:
			z.write(name, compress_type=ZIP_DEFLATED)
	# Print size of new img folder
	zipped_size = os.path.getsize(folder_name+'.zip')
	print('\nTaille du dossier {}.zip: {} Mo'.format(folder_name,round(zipped_size/1E6,2)))
	os.chdir(initial_path)

if __name__ == '__main__':

	initial_path = os.path.abspath(os.getcwd())

	# Create new folder for resized images
	if 'resized_images' not in os.listdir():
		os.mkdir('resized_images')
		os.chdir(initial_path) # return to initial path

	# Create new folder for resized images
	if 'resized_videos' not in os.listdir():
		os.mkdir('resized_videos')
		os.chdir(initial_path) # return to initial path

	# base width for resized image and height for resized video in pixels
	basewidth = 900 #int(input('Images - Nombre de pixels en base (reco: 900) ?'))
	height = 320 #int(input('Videos - Nombre de pixels en hauteur (reco: 240) ?'))

	# for all files in directory with image extension
	supported_files_img = ['jpg','JPG']
	for name in [file for file in os.listdir() if file[-3:] in supported_files_img]:
		# load image
		img = Image.open(name)
		# New dimensions
		wpercent = (basewidth / float(img.size[0]))
		hsize = int((float(img.size[1]) * float(wpercent)))
		# Antialiasing to avoid grain effect
		img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
		print(name+' redimensionnée avec succès')
		img.save('resized_images\\resized_'+name)

	# for all files in directory with video extension
	supported_files_vid = ['mp4','MP4','avi','AVI']
	for name in [file for file in os.listdir() if file[-3:] in supported_files_vid]:
		os.system('ffmpeg -i '+str(name)+' -vf scale='+str(height)+':-1 resized_videos\\resized_'+str(name))

	# zip all data in media folders
	process_folder('resized_images')
	process_folder('resized_videos')
