import glob
import os
import subprocess
import zipfile

class GsDirectory:
    def __init__(self) -> None:
        self.searchFIle = []

    def chemin(self,path):
        try:
            return [{'chemin': os.path.join(path, i), 'nom': i} for i in os.listdir(path) if i[0] != '.']
        except:
            return []
    
    def getUserDerictory(self, path : str) :
        try:
            return [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
        except:
            return []

    def getUserFiles(self, path : str) :
        try:
            return [os.path.basename(file) for file in glob.glob(f"{path}/*") if os.path.isfile(file)]
        except:
            return []
        
    def getnbrFichier(self, path : str) -> int :
        return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and not f.startswith('.')])

    def getnbrDirectory(self, path : str) -> int : 
        directories = glob.glob(path + '/*/')  
        return len(directories)
    
    def getsize(self, path : str) -> None :
        try:
            return sum(os.path.getsize(os.path.join(path, f)) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))
        except:
            return 0
        
    def rechercheFilesName(self,path:str,filename : str )  : 
        l = []
        try:
            for i in os.listdir(path) :
                if i[0] != '.':
                    if(i.count(filename)): 
                        l.append({
                            'chemin':path+"/"+i,
                            'nom' : i
                        })
        except:
            return []
        return l 
    
    def download(self,username) -> None :
        home_dir = os.path.expanduser('/home/'+username)
        zip_filename = "/home/"+username+"/"+username+".zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(home_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, home_dir))

if __name__ == "__main__" :
    a= GsDirectory()
    a.chemin("/home/omar")
    '''print(a.chemin("/home/omar"))'''
    print(str(a.getnbrFichier("/home")))
    '''print(a.gettaille("/home/omar"))
    a.telechercherHomeDerectory("user")'''
    #print(a.getUserFiles("/home/omar"))
    print(a.getnbrDirectory("/home/omar"))