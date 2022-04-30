from PIL import Image


cerveau = Image.open("main.png").convert("RGB")

cerveau_contraste = cerveau.point(lambda i : (i-140)*255/(150-140))

#cerveau_contraste.show()

#lambda i : (i-MIN)/(MAX - MIN)*255 #MIN = 30

#effacer le bruit : 
def FiltrageMedian(cerveau_contraste, nbrFiltre):
    cerveau_contraste=cerveau_contraste.convert("RGB") #je veux reprendre l'image modifiée
    (l, h) = cerveau_contraste.size #CR2ER IMAGE BLANC

    nbr=0
    cerveau_contrasteFinale=Image.new('RGB' ,(l,h))
    #Création d'une seconde image de même taille que l'image de départ
    while nbr<nbrFiltre:
       
        for y in range(1,h-1):
            for x in range(1,l-1):
           
                matriceR= [] #TOUTES LES VALEURS DE ROUGE DES DIFF ¨PIXELS
                matriceV=[]
                matriceB=[]
                for ybis in range(y-1,y+2):
                   for xbis in range(x-1,x+2):
                     r,v,b=cerveau_contraste.getpixel((xbis,ybis))
                     matriceR.append(r)
                     matriceV.append(v)
                     matriceB.append(b)
                   
                matriceR.sort() #ORDRE CROISSANT
                matriceV.sort()
                matriceB.sort()

                cerveau_contrasteFinale.putpixel((x,y),(matriceR[4],matriceV[4],matriceB[4])) #pour effectuer la médiane
        cerveau_contraste=cerveau_contrasteFinale
        nbr+=1      

        cerveau_contrasteFinale.show()
FiltrageMedian(cerveau_contraste,1)