# Bootstrap Icons Repackaged for Django

[Bootstrap Icons](https://icons.getbootstrap.com/) packaged in a Django reusable app.

## Installation

    pip install django-js-lib-bootstrap-icons

## Usage

1. Add `"js_lib_bootstrap_icons"` to your `INSTALLED_APPS` setting like this::

       INSTALLED_APPS = [
           ...
           "js_lib_bootstrap_icons",
           ...
       ]

2. In your template use:
   
       {% load static %}
   
   ...
   
       <link rel="stylesheet" href="{% static "bootstrap-icons/css/font/bootstrap-icons.min.css">" %}">

   or
   
       <link rel="stylesheet" href="{% static "bootstrap-icons/css/font/bootstrap-icons.css">" %}">
