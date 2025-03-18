from jinja2 import Environment, FileSystemLoader
import json
import os
from parser import Parser

fileName = "index.tsx"

parser = Parser('inputs/'+fileName)
functionInfo = parser.getFunctionInfo()
env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('testing.jinja')
output = template.render(functionInfo = functionInfo)
with open("renders/"+fileName, 'w') as f:
    print(output, file = f)