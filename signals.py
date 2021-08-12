import django
render_started=django.dispatch.Signal(providing_args=["book", "author"])
app_loaded=django.dispatch.Signal(providing_args=["book", "author"])