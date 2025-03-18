from jinja2 import Environment, FileSystemLoader
import json
import os
from parser import Parser

fileName = "login.tsx"

parser = Parser('inputs/'+fileName)
functionInfo = parser.getFunctionInfo()
env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('testing.jinja')
output = template.render(functionInfo = functionInfo)
with open("renders/"+fileName, 'w') as f:
    print(output, file = f)

'''
service = Service(jsonData)
env = Environment(loader = FileSystemLoader('templates'))

# mongo functions
template = env.get_template('MongoFunctionsTemplate.jinja')
output = template.render(Service = service)
with open("renders/mongo_functions.js", 'w') as f:
    print(output, file = f)

# models
template = env.get_template('MongoModelsTemplate.jinja')
output = template.render(Service = service)
with open("renders/models.js", 'w') as f:
    print(output, file = f)


# models test
template = env.get_template('ModelsTestTemplate.jinja')
output = template.render(Service = service)
with open("renders/models_test.js", 'w') as f:
    print(output, file = f)


# mongo functions test
template = env.get_template('MongoFunctionsTestTemplate.jinja')
output = template.render(Service = service)
with open("renders/mongo_functions_test.js", 'w') as f:
    print(output, file = f)


# package.json
template = env.get_template('PackageTemplate.jinja')
output = template.render(Service = service)
with open("renders/package.json", 'w') as f:
    print(output, file = f)
'''