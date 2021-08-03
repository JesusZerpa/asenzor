from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import Command as Runserver

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
        print("ERRRRRRRR")
        """
        if self.name in settings.COMPILE_APPS_WEBPACK:
            self.webpack()
        if self.name in settings.COMPILE_APPS_SASS:
            self.sass()   
        self.observer = Observer()
        self.observer.schedule(MyEventHandler(self.name,self.threads),"./"+self.name+"/static/"+self.name+"/py/", recursive=False)
        self.observer.start()
        print(threading.get_ident(),self.name)
        def alive():
            try:
                while self.observer.is_alive():
                    self.observer.join(1)
            except KeyboardInterrupt:
                self.observer.stop()
            self.observer.join()
       
        thread=threading.Thread(target=alive)
        self.threads.append(thread)
        thread.start()
        """
        
        Runserver.handle(self,*args,**options)