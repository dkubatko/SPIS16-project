"drawing the percentage match visual"
from PIL import Image, ImageOps
import time
from random import randrange
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
def percentvisual(percent,width,height, colors):
    im = Image.new("RGBA", (width,height), (250,250,250,0))
    limit = (width) * percent
    count = 0
    incrR = 0
    incrG = 0
    incrB = 0
    print limit
    if limit != 0:
        incrR = 0.8*colors[0]/limit
        incrG = 0.8*colors[1]/limit
        incrB = 0.8*colors[2]/limit
    
    #print incrR, incrG, incrB 
    for x in range(height):
        r = int(colors[0]*0.2)
            
        g = int(colors[1]*0.2)
           
        b = int(colors[2]*0.2)
           
        count=0
        #print r, g, b
        for y in range(width):
            if count <= limit:
                im.putpixel((y, x), (int(r),int(g),int(b),1))
                if r <= colors[0]:
                    r = r + incrR
                if g <=colors[1]:
                    g = g + incrG
                if b <= colors[2]:
                    b = b + incrB
                count = count + 1
                #if x == 1:
                    #print r, g, b
                

    
    
    im_with_border = ImageOps.expand(im,border=2,fill='black')
    randint = randrange(9999999)
    im_with_border.save('static/images/' + 'tmp' + str(randint) + ".jpeg",'JPEG')
    return 'images/' + 'tmp'  + str(randint) + ".jpeg"


def set_default_pic(path):
    img = Image.new("RGB", (300, 300), (250,250,250))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("segoeuisl.ttf", 35)
    draw.text((60, 125),"No image :(",(0,0,0),font=font)
    img.save(path)

def captcha(digit):
    
    os.chdir('static/captchas')
    filelist = [ f for f in os.listdir(".") if f.endswith(".jpg") ]
    for f in filelist:
        os.remove(f)
    os.chdir('../../')
    
    img = Image.new("RGB", (90, 30), (250,250,250))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("segoeuisl.ttf", 25)
    draw.text((5, -3),str(digit),(0,0,0),font=font)
    img.save("static/captchas/captcha" + str(digit) + ".jpg")
    return "captchas/captcha" + str(digit) + ".jpg"
    


