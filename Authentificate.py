import crypt
import os
import spwd
import subprocess

class Authentication :
    def __init__(self,username : str, password : str) -> None:
        self.username = username
        self.password = password

    def AuthenticateUser(self) -> bool:
        try:
            user = spwd.getspnam(self.username)
            hashedmdp, salt = user.sp_pwdp, user.sp_pwdp
            hashed = crypt.crypt(self.password, hashedmdp)
            if self.username in os.listdir("/home") and hashed == hashedmdp:
                print("x")
                return True
            else:
                print("Le nom d'utilisateur ou le mot de passe est incorrect.")
        except KeyError:
            print("L'utilisateur n'existe pas.")
        except Exception as e:
            print(f"Une erreur s'est produite: {e}")
        return False
    
    def authentification(self) -> bool:
        try :
            return self.AuthenticateUser()
        except : 
            return False

class Account : 
    
    def __init__(self) -> None:
        pass
    #Ajouter un utilisateur
    def addAccount(self,username,password) -> bool:
        if username in os.listdir("/home"):
            return False
        try :
            cmd = f"sudo adduser {username} --gecos '' --disabled-password"
            subprocess.run(cmd.split(), check=True)
            cmd = f"echo '{username}:{password}' | sudo chpasswd"
            subprocess.run(cmd, shell=True, check=True)
        except :
            return False
        return True

if __name__ == "__main__":
    a = Account()