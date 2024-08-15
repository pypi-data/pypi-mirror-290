#!/usr/bin/env python3

class Course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    # def __str__(self):
    def __repr__(self):
        return f"[+] {self.name} [{self.duration} horas] ({self.link})"



courses = [
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de entorno en linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/"),
    Course("Python Ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/")
]

def listCourses():
    for course in courses:
        print(course)

def getCourseByName(name):
    for course in courses:
        if course.name.lower() == name.lower():
            return course

    return f"No se encontró el curso con el nombre: {name}"

