import re

############################
#Parse CELL & SECTORCARRIER#
############################

Cell_sectorCarrier = {}
file = open ("sectorCarrier_reservedby.txt", "r")

for line in file:
    if re.search("FDN", line):
        fdn = line.split(":")[1].strip().split(",")
        sectorcarrier = fdn[2].split("=")[1]+"_"+fdn[-1]
    if re.search("reservedBy", line):
        reserved = line.split(":")[1].strip().split()
        for mo in reserved:
            if re.search ("EUtranCell", mo):
                if (mo[-1] == ",") or (mo[-1] == "]"):
                    mo = mo[:-1]
                cell = mo.split(",")[-1]
                if not cell in Cell_sectorCarrier.keys():
                    Cell_sectorCarrier[cell] = sectorcarrier

###############################################
#Parse SECTORCARRIER & SectorEquipmentFunction #
################################################
sectorCarrier_sectorEquipmentFunction = {}
cell_sectorEquipmentFunction = {}

file = open ("sectorCarrier_sectorFunctionRef.txt", "r")

for line in file:
    if re.search("FDN", line):
        fdn = line.split(":")[1].strip().split(",")
        sectorcarrier = fdn[2].split("=")[1]+"_"+fdn[-1]
    if re.search("sectorFunctionRef", line):
        sectorFunctionRef = line.split(":")[1].strip().split(",")
        SectorEquipmentFunction = sectorFunctionRef[2].split("=")[1]+"_"+sectorFunctionRef[-1]
        if not sectorcarrier in sectorCarrier_sectorEquipmentFunction.keys():
            sectorCarrier_sectorEquipmentFunction[sectorcarrier] = SectorEquipmentFunction

for cell in Cell_sectorCarrier.keys():
    cell_sectorEquipmentFunction[cell] = sectorCarrier_sectorEquipmentFunction[Cell_sectorCarrier[cell]]
    
################################################
#Parse SectorEquipmentFunction - RFBRANCH      #
################################################
sectorEquipmentFunction_rfBranch = {}
cell_rfBranch = {}

file = open ("sectorEquipmentFunction_rfBranchRef.txt", "r")

for line in file:
    if re.search("FDN", line):
        fdn = line.split(":")[1].strip().split(",")
        SectorEquipmentFunction = fdn[2].split("=")[1]+"_"+fdn[-1]

    if re.search("rfBranchRef", line):
        rfBranchRef = line.split(":")[1].strip().split()[0][:-1].split(",")
        rfBranch = rfBranchRef[2]+"_"+rfBranchRef[-2]+"_"+rfBranchRef[-1]
        if not SectorEquipmentFunction in sectorEquipmentFunction_rfBranch.keys():
            sectorEquipmentFunction_rfBranch[SectorEquipmentFunction] = rfBranch
            

for cell in cell_sectorEquipmentFunction.keys():
    cell_rfBranch[cell] = sectorEquipmentFunction_rfBranch[cell_sectorEquipmentFunction[cell]]

    
################################################
#Parse RFBRANCH   - RFPORT                     #
################################################

rfBranch_rfPort = {}
cell_ru = {}

file = open ("rfbranch_rfportref.txt", "r")
for line in file:
    if re.search("FDN", line):
        fdn = line.split(":")[1].strip().split(",")
        rfBranch = fdn[2]+"_"+fdn[-2]+"_"+fdn[-1]
    if re.search("rfPortRef", line):
        rfPortRef = line.split(":")[1].strip().split(",")
        if not rfBranch in rfBranch_rfPort.keys():
            rfBranch_rfPort[rfBranch] = rfPortRef[-2].split("=")[1]
            
for cell in cell_rfBranch.keys():
    cell_ru[cell] = rfBranch_rfPort[cell_rfBranch[cell]]
    
################################################
#Parse RILINK   - RADIOUNIT                    #
################################################

rilink_ru = {}

file = open ("rilink.txt", "r")
for line in file:
    if re.search("FDN", line):
        fdn = line.split(":")[1].strip().split(",")
        rilink = fdn[2]+"_"+fdn[-1]
    if re.search("riPortRef", line) and re.search("RU-", line):
        rfPortRef = line.split(":")[1].strip().split(",")
        if not rilink in rilink_ru.keys():
            rilink_ru[rilink] = rfPortRef[-2].split("=")[1]
            
