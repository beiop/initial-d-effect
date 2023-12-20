#written by beiop
#with the help of a lot of google searches
#and ranting to many discord users


#to do
#[ ] figure out what the opacity does
#[ ] add in the soft blending half
#[ ] fix the effect
#[ ] question what np even does
#[ ] make it faster, don't ask me how
#[ ] figure out how to comment out sections and not have to start each line with #
#[ ] learn python...
#[ ] get some sleep
#[ ] fold laundry


import os
import cv2
import numpy as np
from blend_modes import lighten_only
from blend_modes import soft_light

# Set the opacity for blending - honestly no clue what this does, needs testing
opacity = 1
soft_opacity = .7

B = 25
S = 0
E = 600

#os.system("cd #")

#os.system("cd /home/beiopi/Desktop/d_effect/")
#Turn video_in.mp4 into images:

#spice = input("Splice video? y/n")
spice = "n"

if spice == "y":
	os.system ("rm pngs -r ")
	os.system ("mkdir pngs")
	#b = input("seconds (0-59)")
	b = 20
	a = 0
	os.system(f"ffmpeg -i video_in.mp4 -ss 00:00:{str(a).zfill(2)} -t 00:00:{str(b).zfill(2)} -vf format=rgba pngs/frame%04d.png")


#Magic effect:       

os.system ("rm pngs_out -r ")
os.system ("mkdir pngs_out")
for j in range(B,E):
	#do the first one
	print(f'pngs/frame{str((j-B)+1).zfill(4)}.png')
	sanity_float_1 = cv2.imread(f'pngs/frame{str((j-B)+1).zfill(4)}.png', -1).astype(float)
	sanity_float_2 = cv2.imread(f'pngs/frame{str(j-(B-1)+1).zfill(4)}.png', -1).astype(float)
	blended_img_float = lighten_only(
		sanity_float_1,
		sanity_float_2,
		opacity)
	for i in range(0,B-3):
		sanity_float_3 = cv2.imread(f'pngs/frame{str((j+i-B)+3).zfill(4)}.png', -1).astype(float)
		blended_img_float = lighten_only(sanity_float_3,blended_img_float,opacity)
	#Convert the final blended image to OpenCV native display format
	blended_img_uint8 = blended_img_float.astype(np.uint8)
	cv2.imwrite(f'pngs_out/frame{str(j).zfill(4)}.png', blended_img_uint8)
	print(j)

#soft thingy
if True:
	for k in range(1,E):
		sanity_float_1 = cv2.imread(f'pngs_out/frame{str(k).zfill(4)}.png', -1).astype(float)
		sanity_float_2 = cv2.imread(f'pngs/frame{str(k).zfill(4)}.png', -1).astype(float)
		blended_img_float = soft_light(
		sanity_float_1,
		sanity_float_2,
		opacity)
		blended_img_uint8 = blended_img_float.astype(np.uint8)
		cv2.imwrite(f'pngs_out/frame{str(k).zfill(4)}.png', blended_img_uint8)
		print("soft left: " + str(k))




#Turn images into vvideo_out.mp4
print("Hasn't crashed?!?")
print("Now exporting as mp4")
os.system(f"ffmpeg -r 60 -f image2 start_number {B} -i pngs_out/frame%04d.png -vcodec libx264  -pix_fmt yuv420p video_out.mp4")