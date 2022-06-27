#This script Merges PIDs with same thickness
import os
import ansa
from ansa import base
from ansa import constants
import time
from ansa import utils
import json

def main():
	e =0
	eid={}
	id=[]
	T = {}
	
	shells = base.PickEntities(constants.NASTRAN, "__ELEMENTS__")
	
#Getting PID/T list
	print("Reading PID's w.r.t Thickness")
	for i in range(len(shells)):
		b =str(shells[i]._id)
		id.append(b)
	print("TOTAL ELEMENTS: ",len(id))
	for key in id:
		shell = base.GetEntity(constants.NASTRAN, 'SHELL', int(key))
		if not shell:
			print('No entities were found.')
			break
		va = base.GetEntityCardValues(constants.NASTRAN,shell, ('PID',))
		va = str(va).split(" ")
		va = va[-1].replace("}","")
		pshell = base.GetEntity(constants.NASTRAN, 'PSHELL', int(va))
		val =base.GetEntityCardValues(constants.NASTRAN,pshell, ('T',)) 
		val = str(val).split(" ")
		val = val[-1].replace("}","")
		val = val[:4]
		if val[-1]=="0":
			val1 = val[:3]
			#print('replacing'+val+'By'  + val1)
			val = val1
		T[val]=va
		eid[key]=val
	print("Merging PID's with same Thickness")
#Setting PID to ID's w.r.t T
	for k in id:
		shell = base.GetEntity(constants.NASTRAN, 'SHELL', int(k))
		if not shell:
			print('No entities were found.')
			break
		p1 =base.GetEntityCardValues(constants.NASTRAN,shell, ('PID',)) 
		p1 = str(p1).split(" ")
		p1 = p1[-1].replace("}","")
		pshell = base.GetEntity(constants.NASTRAN, 'PSHELL', int(p1))
		t1 =base.GetEntityCardValues(constants.NASTRAN,pshell, ('T',)) 
		t1 = str(t1).split(" ")
		t1 = t1[-1].replace("}","")
		t1=t1[:4]
		if t1[-1] == "0":
			t1 = t1[:3]
		for key in T:
			pid = T[key]
			if t1[:4] == key[:4] :
				status=base.SetEntityCardValues(constants.NASTRAN, shell, {'PID':int(pid)})
				e=e+1
			else:
				continue
				
	print("TOTAL MODIFICATIONS:",e)
	print("DONE!!!")


	
