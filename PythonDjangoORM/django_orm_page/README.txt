1. Copy views.py into your Django app directory.
2. Copy urls.py into your Django app directory, or merge its path into your existing app urls.py.
3. Copy templates/your_app/orm_dashboard.html to <app>/templates/your_app/orm_dashboard.html.
4. Copy static/your_app/css/orm.css to <app>/static/your_app/css/orm.css.
5. In the project urls.py include your app urls, for example path('', include('your_app.urls')).
6. Ensure the app is in INSTALLED_APPS and django.contrib.staticfiles is enabled.
7. Open /orm/.

IMPORTANT: views.py assumes your app's model classes are named Employees, Countries, Jobs, Locations and their fields match the sample database. Change imports/model field names if your models differ. This page only reads data; it does not create, update or delete records.
