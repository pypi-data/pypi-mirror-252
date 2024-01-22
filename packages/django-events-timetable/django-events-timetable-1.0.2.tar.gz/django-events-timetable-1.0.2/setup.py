import setuptools

with open("django_events_timetable/README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-events-timetable",
    version="1.0.2",
    author="Mohammad Golam Dostogir, Amit Kumar",
    author_email="contact@dostogir.dev, amitmodi06@gmail.com",
    description="Django Events Timetable is an app component offering easy integration with Django, Django CMS, and Wagtail CMS. It features a user-friendly interface for managing event items, customizable and responsive templates with Dark and Light themes, and a color picker for design personalization. Designed to complement any project seamlessly, it is also extendable and customizable to meet specific needs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dostogircse171/django_events_timetable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'Django>=3.0',
    ],
    project_urls={ 
        'Source': 'https://github.com/dostogircse171/django_events_timetable',
        'Tracker': 'https://github.com/dostogircse171/django_events_timetable/issues',
        'Demo': 'https://eventdemoapp-ceaa9c531c9c.herokuapp.com/',
    },
)
