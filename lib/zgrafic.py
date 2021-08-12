from PIL import Image
 
def redimensionar(rutas,ancho=None,alto=None,nueva=False,sufijo=None,path=None):
    if type(rutas)==str:
        image_file = rutas
        #abrimos la imagen
        img = Image.open(image_file)
        width, height = img.size

        if ancho==None and alto!=None:
            prop=(alto*100)/float(width)
        elif ancho!=None and alto==None:
            prop=(ancho*100)/float(width)

        elif ancho!=None and alto!=None:
            prop=None
            width=ancho
            height=alto

        # cogemos la anchura y altura



        if prop!=None:
            width=int(width*prop/100)
            height=int(height*prop/100)
                  # use nearest neighbour
            
            im2 = img.resize((width, height), Image.ANTIALIAS)     # linear interpolation in a 2x2 environment
            
        else:
            im2 = img.resize((width,height),Image.ANTIALIAS)      # use nearest neighbour
        ext=rutas.split(".")[-1]



        if nueva:
            if sufijo==None:
                if path==None:
                    im2.save(rutas[:-len(ext)-1]+"_"+str(width)+"x"+str(height)+"_1."+ext)
                else:
                    if path[-1]!="/":
                        path+="/"
                    im2.save(path+rutas.split("/")[-1][:-len(ext)-1]+"_"+str(width)+"x"+str(height)+"_1."+ext)
                
                
            else:
                if path==None:
                    im2.save(rutas[:-len(ext)-1]+sufijo+"."+ext)
                else:
                    if path[-1]!="/":
                        path+="/"
                    im2.save(path+rutas.split("/")[-1][:-len(ext)-1]+sufijo+"."+ext)
        else:
            if path==None:
                im2.save(rutas)
            else:
                if path[-1]!="/":
                        path+="/"
                im2.save(path+rutas.split("/")[-1])
    elif type(rutas)==list:
        for ruta in rutas:
            image_file = ruta
            #abrimos la imagen
            img = Image.open(image_file)
            width, height = img.size
            if ancho==None and alto!=None:
                prop=(alto*100)/float(width)
            elif ancho!=None and alto==None:
                prop=(ancho*100)/float(width)
            elif ancho!=None and alto!=None:
                prop=None


            # cogemos la anchura y altura

            if prop!=None:
                width=int(width*prop/100)
                height=int(height*prop/100)
                im2 = img.resize((width, height),Image.ANTIALIAS)      # use nearest neighbour
            else:
                im2 = img.resize((width,height),Image.ANTIALIAS)      # use nearest neighbour
            ext=ruta.split(".")[-1]
            
            if nueva:
                if sufijo==None:
                    if path==None:
                        im2.save(ruta[:-len(ext)-1]+"_"+str(width)+"x"+str(height)+"."+ext)
                    else:
                        if path[-1]!="/":
                            path+="/"
                        im2.save(path+ruta.split("/")[-1][:-len(ext)-1]+"_"+str(width)+"x"+str(height)+"."+ext)
                    
                else:
                    if path==None:
                        im2.save(ruta[:-len(ext)-1]+sufijo+"."+ext)
                    else:
                        if path[-1]!="/":
                            path+="/"
                        im2.save(path+ruta.split("/")[-1][:-len(ext)-1]+sufijo+"."+ext)

                    
            else:
                if path==None:
                    im2.save(ruta)
                else:
                    if path[-1]!="/":
                        path+="/"
                    im2.save(path+ruta.split("/")[-1])
                

def cortar(ruta, x, y, width,height,nueva=False,sufijo=None,path=None):
    im = Image.open(ruta)
    region = im.crop((x,y,width,height))
    if nueva:
        if sufijo!=None:
            ext=ruta.split(".")[-1]
            
            if path==None:
                region.save(ruta[:-len(ext)]+sufijo+ext)
            else:
                if path[-1]!="/":
                    path+="/"
                region.save(path+ruta.split("/")[-1][:-len(ext)]+sufijo+ext)

    else:
        if path==None:
            region.save(ruta)
        else:
            if path[-1]!="/":
                path+="/"
            region.save(path+ruta.split("/")[-1])
            

def thumbails(rutas,sufijo="_540x540",ancho=540,alto=540,nueva=True,path=None):
    if type(rutas)==str:
        if path:
            image_file = path + rutas
        else:
            image_file = rutas

        #abrimos la imagen
        img = Image.open(image_file)
        width, height = img.size
        orientacion=width>=height#true es horizontal

        
        if orientacion:
            prop=(ancho*100)/float(height)
        else:
            prop=(ancho*100)/float(width)


        # cogemos la anchura y altura



        if prop!=None:
            width=int(width*prop/100)
            height=int(height*prop/100)

            # use nearest neighbour
            im2 = img.resize((width, height), Image.ANTIALIAS)     # linear interpolation in a 2x2 environment            
            width, height = im2.size
            if orientacion:
                dx=width/2-ancho/2
                im2=im2.crop((dx,0,width-dx,height))    
                
            else:
                dy=(height-ancho)/2
                im2=im2.crop((0,dy,width,height-dy))

            



        ext=rutas.split(".")[-1]



        if nueva:
            if sufijo==None:
                if path==None:
                    im2.save(rutas[:-len(ext)-1]+"_"+str(ancho)+"x"+str(im2.size[1])+"."+ext)
                else:
                    if path[-1]!="/":
                        path+="/"
                    im2.save(path+rutas[:-len(ext)-1].split("/")[-1]+"_"+str(ancho)+"x"+str(alto)+"."+ext)

                
                
            else:
                if path==None:
                    im2.save(rutas[:-len(ext)-1]+sufijo+"."+ext)
                else:
                    if path[-1]!="/":
                        path+="/"
                    im2.save(path+rutas[:-len(ext)-1].split("/")[-1]+sufijo+"."+ext)
        else:
            if path==None:
                im2.save(rutas)
            else:
                if path[-1]!="/":
                    path+="/"
                im2.save(path+rutas.split("/")[:-1])
    elif type(rutas)==list:
        for ruta in rutas:
            image_file = ruta
            #abrimos la imagen
            img = Image.open(image_file)
            width, height = img.size
            orientacion=width>=height#true es horizontal

        
            if orientacion:
                prop=(ancho*100)/float(height)
            else:
                prop=(ancho*100)/float(width)


            # cogemos la anchura y altura



            if prop!=None:

                width=int(width*prop/100)
                height=int(height*prop/100)
                im2 = img.resize((width, height),Image.ANTIALIAS)      # use nearest neighbour
                width, height = im2.size
                if orientacion:
                    dx=width/2-ancho/2
                    im2=im2.crop((dx,0,width-dx,height))    
                    
                else:
                    dy=(height-ancho)/2
                    im2=im2.crop((0,dy,width,height-dy))
            
            ext=ruta.split(".")[-1]
            
            if nueva:
                if sufijo==None:
                    if path==None:
                        im2.save(ruta[:-len(ext)-1]+"_"+str(ancho)+"x"+str(alto)+"."+ext)
                    else:
                        if path[-1]!="/":
                            path+="/"
                        im2.save(path+ruta[:-len(ext)-1]+"_"+str(ancho)+"x"+str(alto)+"."+ext)
                else:
                    
                    if path==None:
                        im2.save(ruta[:-len(ext)-1]+sufijo+"."+ext)
                    else:
                        if path[-1]!="/":
                            path+="/"
                        im2.save(path+ruta.split()[-1][:-len(ext)-1]+sufijo+"."+ext)

                        
            else:
                if path==None:
                    im2.save(ruta)    
                else:
                    if path[-1]!="/":
                        path+="/"
                    im2.save(path+ruta.split("/")[-1])
                    
def optimizar(ruta,calidad=80):
	from PIL import Image
	i = Image.open(ruta)
	i.save(ruta,quality=calidad)
	   

def postOptimizar(ruta,calidad=80):
	import sys , os, glob,shutil
	from PIL import Image
	cont =0

	for img in glob.glob(ruta+'*.jpg') + glob.glob(ruta+'*.png')+glob.glob(ruta+'*.gif')+glob.glob(ruta+'*.JPEG')+glob.glob(ruta+'*.JPG'):
	    try:
	        namefile =os.path.basename(img)
	        splitname =  os.path.splitext(namefile)
	        namefile = splitname[0]
	        extens = splitname[1]
	        i = Image.open(img)
	        width, height = i.size

	        if width>1000 or height>1000:
	        	if not img[:img.rfind(".")].endswith("__full"):
	        		shutil.copy2(img,img[:img.rfind(".")]+"__full"+img[img.rfind("."):])
	        	
	        	i.save(img,quality=calidad)

	    except ValueError:
	        print(ValueError)
	        cont=cont +1
	if cont >0:
	    print("Algunos archivos no se puedieron comprimir")
	else:
	    print("todos los ficheros fueron comprimidos con exito")

