#!/usr/bin/env python

import os
from os import walk, getcwd
from xml.etree import ElementTree as et

SETTINGS_FILE_PATH = "${Absolut_path}\.m2\settings.xml"
REPOSITORY = "repository name"
URL = "Azure url repo feed"


def getVersion(file):
    ns = "http://maven.apache.org/POM/4.0.0"
    et.register_namespace('', ns)
    tree = et.ElementTree()
    tree.parse(file)
    p = tree.getroot().find("{%s}version" % ns)
    return p.text


def getGroupId(file):
    ns = "http://maven.apache.org/POM/4.0.0"
    et.register_namespace('', ns)
    tree = et.ElementTree()
    tree.parse(file)
    p = tree.getroot().find("{%s}groupId" % ns)
    return p.text


def ls(ruta=getcwd()):
    listaarchivos = []
    for (folder, subfolders, archivos) in walk(ruta):
        for archivo in archivos:
            filePath = os.path.join(os.path.abspath(folder), archivo)
            listaarchivos.append([filePath, archivo])
    return listaarchivos


def clean_list(listaarchivos):
    jar_pom_list = []
    for archivo in listaarchivos:
        if archivo[0].endswith(".jar") or archivo[0].endswith(".pom"):
            jar_pom_list.append(archivo)
    return jar_pom_list


def main():
    listaarchivos = clean_list(ls(ruta="${Absoulut_path}\\.m2\\repository"))
    for archivo in listaarchivos:
        if(archivo[0].endswith(".jar")):
            try:
                version = getVersion(archivo[0][:-3]+"pom")
                groupid = getGroupId(archivo[0][:-3]+"pom")
                print archivo[0]
                print version
                print groupid
                sentence = "mvn deploy:deploy-file -Dfile=" + archivo[0] + " -DrepositoryId=" + REPOSITORY + " -Durl=" + URL + " -s " + SETTINGS_FILE_PATH + " -DartifactId=" + archivo[1][:-4] + " -DgroupId=" + groupid + " -Dversion=" + version
                print sentence
                os.system(sentence)
            except Exception:
                print "no present version in pom for: "+archivo[0]
                continue


if __name__ == '__main__':
    main()
