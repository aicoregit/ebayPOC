def common_member(a, b):
     
    a_set = set(a)
    b_set = set(b)
     
    # check length 
    if len(a_set.intersection(b_set)) > 0:
        return(list(a_set.intersection(b_set)))  
    else:
        return("no common elements")
        
        
def remove_bg(file_path,label):
    import numpy as np
    import cv2
    import matplotlib
    matplotlib.use('agg',warn=False, force=True)
    from matplotlib import pyplot as plt
    print ("Switched to:",matplotlib.get_backend())
    
    import darknet as dn
    
    #file_path="/home/ec2-user/darknet/data/fridge3.jpg"
    
    img = cv2.imread(file_path)
    mask = np.zeros(img.shape[:2],np.uint8)
    
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    r = dn.give_boxes(file_path)
    print (r)
    
    listoflabels= list(set([item[0] for item in r]))
    print ("!!!!! listoflabels: ", listoflabels)
    if ("tvmonitor" in listoflabels):
        listoflabels[listoflabels.index("tvmonitor")]="tv"
        
    print("@@@  listoflabels",listoflabels)
    
    #hyponym calculation
    if (label in str(listoflabels)):
        if (label == "tv"):
            labelex="tvmonitor"
        else:
            labelex=label
    else:
        from nltk.corpus import wordnet as wn
        from itertools import chain
        listofHyponyms=[]
        for i,j in enumerate(wn.synsets(label)):
            if (i==0):
                listofHyponyms=list(chain(*[l.lemma_names() for l in j.hyponyms()]))
                listofHyponyms.append(label)
                break;
                
        print("listoflabels",listoflabels)
        listoflabelsHyponyms=[]
        listoflabelsHyponymstest=[]
        for k in listoflabels:
            for i,j in enumerate(wn.synsets(k.decode())):
                if (i==0):
                    listoflabelsHyponyms.extend(list(chain(*[l.lemma_names() for l in j.hyponyms()])))
                    listoflabelsHyponymstest.append(list(chain(*[l.lemma_names() for l in j.hyponyms()])))
                    break;
                    
        print ( "listoflabelsHyponyms before flatten",listoflabelsHyponyms) 
        print ( "listoflabelsHyponymstest ",listoflabelsHyponymstest)          
        listoflabelsHyponyms.extend(listoflabels)
        #listoflabelsHyponyms=[item for sublist in listoflabelsHyponyms for item in sublist]
        print("listofHyponyms",listofHyponyms)
        print("listoflabelsHyponyms after flatten",listoflabelsHyponyms)
        finallabel=common_member(listoflabelsHyponyms,listofHyponyms)
        print("finallabel",finallabel)
        for i in listoflabelsHyponymstest:
            if (finallabel[0] in i):
                labelex=listoflabels[listoflabelsHyponymstest.index(i)].decode()
                break;
                
        print ("labelex",labelex)
        if (finallabel=="no common elements"):
            listofSynonyms=[]
            synonyms = []
            for syn in wn.synsets(label):
                for l in syn.lemmas():
                    synonyms.append(l.name())
                    
            listofSynonyms = list(set(synonyms))
            listofSynonyms.append(label)
            print ('listofSynonyms',listofSynonyms)
            finallabel=common_member(listoflabels,listofSynonyms)
            print("finallabel again",finallabel)
            labelex= finallabel[0].decode()
    
    print("????????",labelex)
    print("MMMMMMMMMMMMMMMMMMMM",[item[-1] for item in r if item[0].decode() == labelex])
    t1=[item[-1] for item in r if item[0].decode() == labelex][0]
    
    
    width =  t1[2]
    height = t1[3]
    center_x = t1[0]
    center_y = t1[1]
    
    bottomLeft_x = center_x - (width / 2)
    bottomLeft_y = center_y - (height / 2)
    
    #rect = objects[0][-1]
    rect=(int(bottomLeft_x),int(bottomLeft_y),int(width),int(height))
    print (rect)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    out_loc="/home/ubuntu/ebayPOC/static/"
    out_filename=file_path.split("/")[-1]
    cv2.imwrite((out_loc+str(label)+'_'+out_filename),img)
    return (str(label)+'_'+out_filename)
    
    #plt.imshow(img),plt.colorbar(),plt.show()
