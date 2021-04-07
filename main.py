from PIL import Image, ImageDraw
import numpy as np

res = 50
scale = 5

img = Image.open('img.png')
width, height = img.size
rw, rh = width/res, height/res
im = np.array(img)
im_average = np.average(im)

avgs = [np.average(np.array(c)) for c in img.split()]

out = Image.new("RGB", (width*scale, height*scale), (int(im_average), int(im_average), int(im_average)))

for y in range(res):
    for x in range(res):
        timg = list(img.split())
        cropped = img.crop((int(rw*x), int(rh*y), int(rw*(x+1)), int(rh*(y+1))))
        tsource = cropped.split()
        tavgs = [np.average(np.array(c)) for c in tsource]
        for i, s in enumerate(timg):
            timg[i] = s.point(lambda p: p * tavgs[i]/avgs[i])
        imgt = Image.merge(cropped.mode, timg).resize((int(rw*scale), int(rh*scale)))
        # try:
        #     imgt = img.point(lambda p: p * tavg/im_average).resize((int(rw*scale), int(rh*scale)))
        #     # imgt = Image.new('RGB', (int(rw*scale), int(rh*scale)), (int(tavg), int(tavg), int(tavg)))
        # except:
        #     imgt = img.resize((int(rw*scale), int(rh*scale)))
        #     # imgt = Image.new('RGB', (int(rw*scale), int(rh*scale)), (255, 0, 0))
        ix, iy = int(rw*x*scale), int(rh*y*scale)
        out.paste(imgt, (ix, iy))
    print(f"{y}/{res}", end='\r')

out.save("img2.png")