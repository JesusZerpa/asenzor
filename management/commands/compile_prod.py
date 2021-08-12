from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import Command as Runserver
import shutil,subprocess,os
def sass(self):
    if sys.argv[1]=="runserver":
        import subprocess
        proc = subprocess.Popen(
            ["sass","--watch",f"{self.name}/scss:{self.name}/css"],
            stdout=subprocess.PIPE,
            cwd=self.name+'/static/'
        )
        self.register_process(proc)
        """
        thread=threading.Thread(target=sass_compile)
        self.threads.append(thread)
        thread.start()
        """
class Command(Runserver):
    help = 'Closes the specified poll for voting'
 

    def handle(self, *args, **options):
        from django.conf import settings
        for name in settings.COMPILE_APPS_WEBPACK:
            print("@@@@@@@ ",name+"/static/"+name+"/py/")
            for folder in os.listdir(name+"/static/"+name+"/py/"):
                if not os.path.isfile(name+"/static/"+name+"/py/"+folder)\
                    and folder not in ["node_modules"]\
                    and os.path.exists(name+"/static/"+name+"/py/"+folder+"/webpack.prod.js"):

                    proc = subprocess.Popen(
                        ["npx","webpack","--config",
                        "webpack.prod.js"],
                        stdout=subprocess.PIPE,
                        cwd=name+"/static/"+name\
                            +"/py/"+folder
                    )
                    print(proc.communicate()[0].decode("utf-8"))
                    shutil.move(
                        name+"/static/"+name+"/py/"\
                        +folder+"/dist/main.js", 
                        name+"/static/"+name+"/dist/"\
                        +folder+".js")
 
        