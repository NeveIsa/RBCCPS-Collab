import os
import json
import jsonschema
import sys

cwd = os.getcwd()
#base_dir_abs_path = cwd+'/'+sys.argv[3]
base_dir_abs_path = cwd+'/'

if (len(sys.argv[1:])==0):
  print "Usage: python jsonschema_val.py rel-path-to-item [rel-path-to-schema-dir]"
  exit()
elif (len(sys.argv[1:])==1):
  schema_path = base_dir_abs_path
else:
  schema_path = os.path.join(base_dir_abs_path, sys.argv[2])

#schema_path = os.path.join('/home/abhay/work/tmp_schemas', 'isco_base_schema.json')

# Your data
#data_path = os.path.join('/home/abhay/work/tmp_schemas', 'Sample_Catalogue_Item.json')
data_path = os.path.join(base_dir_abs_path, sys.argv[1])
with open(data_path) as data_object:
    data = json.load(data_object)

schema_file= os.path.join(schema_path, data['refCatalogueSchema'])

print "SCHEMA_PATH:",schema_path
print "SCHEMA_FILE:",schema_file

print "SCHEMA_RES:",'file://' + schema_path

with open(schema_file) as file_object:
    schema = json.load(file_object)


# Note that the second parameter does nothing.
#resolver = jsonschema.RefResolver('file://' + base_dir_abs_path + '/', None)
resolver = jsonschema.RefResolver('file://' + schema_path, None)

# This will find the correct validator and instantiate it using the resolver.
# Requires that your schema a line like this: "$schema": "http://json-schema.org/draft-04/schema#"
print jsonschema.validate(data, schema, resolver=resolver)
