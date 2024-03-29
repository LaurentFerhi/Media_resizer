########################################################
# Script to resize images and videos v1.2              #
# By Laurent Ferhi                                     #
# Need to have ffmpeg installed and added to the PATH  #
########################################################

import PIL
from PIL import Image
import os
from zipfile import ZipFile, ZIP_DEFLATED
import datetime

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

def create_folder(name_f):
	if name_f not in os.listdir():
		os.mkdir(name_f)
		os.chdir(initial_path) # return to initial path

def resize_pictures(basewidth,folder):
	# for all files in directory with image extension
	supported_files_img = ['jpg','JPG','jpeg','JPEG']
	for name in [file for file in os.listdir() if file[-3:] in supported_files_img]:
		# load image
		img = Image.open(name)
		# New dimensions
		wpercent = (basewidth / float(img.size[0]))
		hsize = int((float(img.size[1]) * float(wpercent)))
		# Antialiasing to avoid grain effect
		img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
		print('{} redimensionnée avec succès'.format(name))
		img.save('{}\\resized_{}'.format(folder,name))

def resize_video(ratio,folder):
	# for all files in directory with video extension
	supported_files_vid = ['mp4','MP4','avi','AVI','mpeg','MPEG']
	for name in [file for file in os.listdir() if file[-3:] in supported_files_vid]:
		os.system('ffmpeg -i {} -vf "scale=iw/{}:ih/{}" {}\\resized_{}'.format(
            name,ratio,ratio,folder,name
            ))

if __name__ == '__main__':

	basewidth_pictures = 900 
	ratio_video = 6
	initial_path = os.path.abspath(os.getcwd())
    
	# Create folders
	folder_name = str(datetime.datetime.now().strftime('%y%m%d'))
	create_folder(folder_name)

	# process pictures and videos
	resize_pictures(basewidth_pictures,folder_name)
	resize_video(ratio_video,folder_name)

	# zip all data in media folders
	process_folder(folder_name)
