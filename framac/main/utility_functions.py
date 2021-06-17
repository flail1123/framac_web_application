import os
from re import *
from .models import *


def getSelected(owner):
    selected = Selected.objects.filter(owner=owner)[0]
    return selected.selected_file, selected.selected_directory

def doFocusOnElements(file):
    os.system("touch temp_framac.c")
    with open("temp_framac.c", 'w') as f:
        f.write(file.code)
    os.system('frama-c -wp -wp-print temp_framac.c > result.txt')
    newResult = '<script> $(".short").hide(); $(".focus").click(function() { $(this).children().toggle();}); </script>'
    with open("result.txt", 'r') as f:
        result = f.read()
        reg = compile(r'.*returns (\w+)')
        for chunk in result.split("------------------------------------------------------------"):
            mo = reg.search(chunk)
            newResult += "------------------------------------------------------------"
            chunk = chunk.replace("\n", "<br/>")

            if mo != None:
                if mo.group(1) == "Valid":
                    newResult += f'<div class="focus" style="color: black; background-color:green"><div class="chunk">{chunk}</div> <div class="short"> Status: {mo.group(1)}, Lines: {chunk.count("<br/>")} </div></div>'
                elif mo.group(1) == "Unkown":
                    newResult += f'<div class="focus" style="color: black; background-color:yellow"><div class="chunk">{chunk}</div> <div class="short"> Status: {mo.group(1)}, Lines: {chunk.count("<br/>")} </div></div>'
                else:
                    newResult += f'<div class="focus" style="color: black; background-color:lightblue"><div class="chunk">{chunk}</div> <div class="short"> Status: {mo.group(1)}, Lines: {chunk.count("<br/>")} </div></div>'
            else:
                newResult += f'<div class="focus" style="color: white"><div class="chunk">{chunk}</div> <div class="short"> Lines: {chunk.count("<br/>")} </div></div>'
        return newResult

def getFile(selectedDirectory, selectedFile, owner):
    directory = Directory.objects.filter(owner=owner)[selectedDirectory]
    return File.objects.filter(directory=directory.id)[selectedFile]

def doResult(file):
    prover = file.prover
    vc = file.vc
    os.system("touch temp_framac.c")
    with open("temp_framac.c", 'w') as f:
        f.write(file.code)
    if prover == "":
        os.system('frama-c -wp -wp-log="r:result.txt" temp_framac.c')
    else:
        os.system("frama-c -wp -wp-prover " + prover + " " + vc + " temp_framac.c > result.txt")

    with open("result.txt", 'r') as f:
        return f.read().replace("\n", "<br/>")




