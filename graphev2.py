import numpy as np
import random as r

"""
    Modélisation d'un graphe : classe graphe
    Le graphe sera modélisé sous la forme d'un double-dictionnaire 
    arc[S1 : sommet origine][S2 : sommet but ] = vecteur 
    Si le vecteur existe, alors il y a un arc entre S1 et S2
    Le vecteur sera de taille 1+R et représentera le vecteur cout et ressources de l'arc
    vecteur[0] = cout de l'arc
    vecteur[i] = Consommation ressource i sur l'arc ou i = [| 1 ; R |]
    
"""
class Graphe:
    nb_graph=0

    #res = nom des ressources à considérer
    def __init__(self,res=None):
        self.arc={} #double dictionnaire 
        self.noeud=[] #noeud
        if(type(res) is not list):
          res=[res]
        self.ressource=res # nom des ressources
        #Nombre de ressource
        if(res==[None]):
          self.nb_ressources = 0
        else:  
          self.nb_ressources = len(res) 
        Graphe.nb_graph+=1
    
    #Fonction permettant d'ajouter une/des ressources
    def ajout_ressource(self,nom_ress):
      if (type(nom_ress) is not list):
        nom_ress=[nom_ress]
      for nom in nom_ress:
        if(self.ressource==[None]):
          self.ressource=[nom]
        else: 
          self.ressource.append(nom)
        self.nb_ressources+=1
        for source in self.arc.keys():
          for cible in self.arc[source].keys():
            self.arc[source][cible].append(0)
        
    #Fonction permettant l'ajout d'un/des sommet au graphe
    def ajoutNoeud(self,sommet):
      if (type(sommet) is not list):
        sommet=[sommet]
      for som in sommet:
        if (som in self.noeud):
          print('Le sommet ',som,' est déjà présent dans votre graph')
        else:
          self.noeud.append(som)
    
    #Fonction permettant l'ajout d'un/des arc entre 2 sommets
    def ajoutArc(self,origin,dest,conso):
        #conso = Cout de l'emprunt de l'arc et consommation des ressources
        if(type(origin) is not list):
          origin=[origin]
        if(type(dest) is not list):
          dest=[dest]
        if (type(conso) is not list):
          conso=[conso]
        if(type(conso[0]) is not list):
          conso=[conso]
        for i in range(len(origin)):
          if(len(conso[i])==self.nb_ressources+1):
            if(origin[i] not in self.noeud):
                self.ajoutNoeud(origin[i])
            if(origin[i] not in self.arc.keys()):
                self.arc[origin[i]]={}
            if (dest[i] not in self.noeud):
              self.ajoutNoeud(dest[i])
            self.arc[origin[i]][dest[i]]=conso[i]
          else:
            print("Le vecteur conso de l'arc (",origin[i],dest[i],") n'a pas la bonne dimention. L'arc n'a donc pas été ajouté") 
        
    #Fonction retournant les predecesseurs d'un sommet sous forme de liste    
    def predecesseurs(self,sommet):
        liste_pred = []
        for key in self.arc.keys():
            if(sommet in self.arc[key].keys()):
                liste_pred.append(key)  
        return(liste_pred)
        
    #Fonction retournant les successeurs d'un sommet sous forme de liste
    def successeurs(self,sommet):
        liste_suc = []
        for key in self.arc[sommet].keys():
            liste_suc.append(key)
        return(liste_suc)
    
    #Fonction affichant le graphe sous forme
    # Sommet(nombre de successeurs) : [{successeur_i : vecteur conso }, ... ]
    def affiche(self):
        for key in self.arc.keys():
            print(key+"("+str(len(self.arc[key]))+"): [ ",end="")
            for cle in self.arc[key].keys():
                print("{"+cle+" : "+str(self.arc[key][cle])+" } ,",end="")
            print("]")
    
""" Création d'une fonction ordre_Pareto qui prend comme paramètre 2 arcs et 
    renvoie l'arc qui domine au sens de Pareto, ou les 2 arcs si pas 
    de dommination. Un vecteur domine si il minimise la consommation de ressources    """
    
def ordre_Pareto(arc1,arc2):
    arc = arc1 - arc2
    retour = None
    if np.all(arc>=0)==True:
        retour =np.array([arc2])
    elif np.all(arc<0)==True:
        retour = np.array([arc1.tolist()])
    else:
        retour = np.array([arc1,arc2])
    return(retour)

""" Fonction de Pareto retournant les étiquettes non dominées
    d'un ensemble d'étiquettes"""
    
def Pareto(E):
   #enleve les valeurs dupliques
   resu=np.unique(E,axis=0)
   #Conserve uniquement les element non dominés
   for element1 in resu:
     for element2 in resu:
         if(np.any(element1!=element2)):
             test=ordre_Pareto(element1,element2)
             if(len(test)==1):
                 if np.all(element1==test[0]):
                     resu=resu[np.array([np.any(resu[i]!=element2) for i in range(len(resu))])]
                 else:
                     resu=resu[np.array([np.any(resu[i]!=element2) for i in range(len(resu))])] 
     return(resu)
     

""" Code de l'algorithme à correction d'étiquettes """
#s1 est le sommet source, s2 le sommet puit
#b est une liste de taille R contenant la consommation maximale pour chaque ressources
def PCCC_correction(G,b,s1,s2):
    #Recupération des prédecesseurs pour avoir le chemin optimal
    pred ={}
    #Etiquettes vides à l'initialisation pour chaque sommet
    ETIQ={}
    for e in G.noeud:
        ETIQ[e] = [np.array([0]*(G.nb_ressources+1))]
    #Liste des sommets "non traités", contient s1 au départ
    LIST=[s1]
    nb=0
    #Traitement des étiquettes, on trouve celles qui sont dominées
    while(len(LIST)!=0):
        sommet = LIST[0];LIST.remove(sommet)
        nb+=1
        #On vérifie si le sommet a des successeurs
        if(sommet in G.arc.keys()):
            for successeur in G.successeurs(sommet):
                for etiq in ETIQ[sommet]:
                    if(all(etiq[i+1] + G.arc[sommet][successeur][i+1] <=b[i] for i in range(G.nb_ressources))):
                        etiq_ = etiq + G.arc[sommet][successeur]
                        #On vérifie si on modifie une étiquette pour la 1ere fois
                        condition = True
                        for liste in ETIQ[successeur]:
                            condition = all(liste==0)
                        if(condition):
                            ETIQ[successeur]=np.array([etiq_])
                        else:
                            ETIQ[successeur] = Pareto(np.vstack((ETIQ[successeur],etiq_)))
                        #Si nouvelle etiquette, on ajoute le successeur dans la liste
                        if(((etiq_-ETIQ[successeur])==0).any() ):
                            LIST.append(successeur)
                            #On recupère le prédecesseur associé à l'étiquette
                            if(successeur in pred.keys()):
                                if(sommet in pred[successeur].keys()):
                                    val = etiq_
                                    if(((val!=pred[successeur][sommet]).all())):
                                        pred[successeur][sommet].append(etiq_)
                                else:
                                    d1 = {sommet : [etiq_]}
                                    pred[successeur].update(d1)
                            else:
                                pred[successeur]={ sommet : [etiq_]}


    #On vérifie si une solution a été trouvée
    resultat = 0 #La variable de retour, elle est à 0 par défaut
    if(s2 not in pred.keys()):
        print("Il n'y a pas de solutions au problème")
        resultat = -1
    #si une solution a été trouvée, on cherche le chemin correspondant au cout minimal
    else:
        chemin=[s2] #chemin optimal
        e=s2
        costs=[]
        while(s1 not in chemin):
            #On retrouve l'étiquette en s2 ayant le plus petit cout 
            #pareil pour ses prédecesseurs 
            for etiq in ETIQ[e]:
                costs.append(etiq[0])
            min_cost = min(costs)
            #Etiquette correspondant à un cout minimal pour sommet e
            opt=[]
            for etiq in ETIQ[e]:
                if(etiq[0]==min_cost):
                    if(e==s2):
                        etiquette_s2 =etiq 
                    opt=etiq
                    break
    
            cle = "e" #Clé correspondant à l'étiquette de cout minimal
            for key in pred[e].keys():
                for l in pred[e][key]:
                    if(np.all(l==opt)):
                        cle=key
            e=cle
            chemin.append(e)
            #resultat : tuple("Chemin", etiquette en s2 )
            resultat = chemin[::-1],etiquette_s2
    return(resultat)
       
if __name__ == "__main__":
    Paul = Graphe()
    Paul.ajout_ressource(["nb_colab","distance","energie"])
    Paul.ajoutNoeud(["Debut","Meetings","Conferences","Financement","Corruption","Demagogie","Election","Decheance"])
    Paul.ajoutArc(["Debut","Debut","Debut","Financement","Conferences","Conferences","Meetings","Corruption","Corruption","Demagogie","Election"],
              ["Meetings","Conferences","Financement","Conferences","Corruption","Demagogie","Corruption","Election","Decheance","Election","Decheance"],
              [[15,1,3,4],[10,1,4,5],[8,2,6,5],[4,5,6,2],[20,2,0,1],[2,3,9,1],[10,3,0,4],[1,6,2,8],[2,6,6,4],[4,3,2,2],[4,5,6,4]])
    """Vecteur consommation max de ressources 
    1 - Pas plus de 12  collaborateurs
    2-  Pas plus de 20 unités d'energie
    3-  Une distance inférieure à 15 unités"""
    conso = np.array([12,20,15])
    parcours = PCCC_correction(Paul,conso,"Debut","Decheance")
    print(parcours)
    
    g=Graphe()
    g.ajout_ressource("prix")
    g.ajoutNoeud(["France","Allemagne","Belgique","Turquie","Chine","Russie","Japon"])
    g.ajoutArc(["France","France","Allemagne","Turquie","Chine","Belgique","Russie"],
           ["Allemagne","Belgique","Turquie","Chine","Japon","Russie","Japon"],
           [[3,107],[4,146],[2,65],[9,160],[2,98],[2,48],[6,300]])

    resultat = PCCC_correction(g,np.array([550]),"France","Japon")
    print(resultat)
            
        
        
    

    