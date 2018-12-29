#!/usr/bin/python
import sys
import csv

header = open("chilled_door_mib.header")

for line in header.readlines():
	print line,

mib_data = {}

def get_mib_data_oid_name(mib_data):
	return mib_data[1]['oidName']

c = csv.DictReader(filter(lambda row: row[0]!='#', open("chilled_door_mib.csv")))
for row in c:
	var_type = row['pcoVarType']
	var_id = row['pcoVarId']
	oid_name = row['oidName']

	id_tuple = (var_type, var_id)
	if id_tuple in mib_data:
		print "Duplicate type/id detected:"
		print mib_data[id_tuple]
		print row
		sys.exit(1)

	if oid_name in map(lambda x: x[1]['oidName'], mib_data.items()):
		print "Duplicate oid name %s detected" % oid_name
		sys.exit(1)

	mib_data[id_tuple] = row

	print """%s OBJECT-TYPE
                SYNTAX          %s
                MAX-ACCESS      %s
                STATUS          %s
                DESCRIPTION
                        "%s"
                ::= { %s %s }\n""" % (row['oidName'], row['unit'], row['readwrite'],
					row['current'], row['description'], var_type, var_id)

print "END"
#for mib_entry in map(lambda x: x[1], mib_data.items()):
#	print mib_entry
#print mib_data
