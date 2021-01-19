#from django.apps import AppConfig
from .lib.apps import AppConfig
import os,imp,json
class MainConfig(AppConfig):
    name = 'asenzor'
    ejecutado=False
    plugins=[]
    __version__="0.1.0"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.settings["webpack"]["entry"]["main"]="./asenzor/py/main.py"
        #self.webpack()
        #self.sass(self.name)
        self.load_plugins()
        

    def load_plugins(self):
        for plugin in os.listdir("asenzor/plugins/"):
            try:

                if plugin!="__pycache__" and plugin!="__init__.py" :
                    modulo=imp.load_source(plugin,os.path.abspath("asenzor/plugins/"+plugin))

                    self.plugins.append([modulo,None])#[modulo, instacia]
            except Exception as e:
                print(e)
    def get_plugins(self):
        return self.plugins
    def get_secret_key(self):
        with  open("asenzor/settings.json") as f:
            data=json.loads(f.read())
        return data["secret_key"]

    def encode(self,texto,clave):
        c=0
        code=""
        for ch in texto:
            
            n=ord(ch)+ord(clave[c])
            
            while  n >1114111:
                n-=1114111
            code+=chr(n)            
            if c+1<len(clave):
                c+=1
            else:
                c=0
        return code
            

    def decode(self,texto,clave):
        c=0
        code=""
        for ch in texto:
            n=ord(ch)-ord(clave[c])
            
            while  n >1114111:
                n-=1114111
            code+=chr(n)            
            if c+1<len(clave):
                c+=1
            else:
                c=0
        return code
    def send_mail(self,receiver_email,subject,message):
        from .models import Option
        import smtplib, ssl
        smtp_server = Option.get("smtp_server")#"smtp.gmail.com"
        port = Option.get("smtp_port")#587  # For starttls

        sender_email = Option.get("sender_email")#"my@gmail.com"

        password = Option.get("smtp_password")
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart()
        msg.set_unixfrom('author')
        msg['From'] = 'asenzor@woodridgeatcarrollwood.com'
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        mailserver = smtplib.SMTP_SSL(smtp_server ,int(port))
        mailserver.ehlo()
        mailserver.login(sender_email , password)

        mailserver.sendmail(sender_email ,receiver_email,msg.as_string())

        mailserver.quit()
             


    
        





