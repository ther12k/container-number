import json
ISO_CODE = True
if ISO_CODE:
    __file_json = open('config/iso_code.json')
    ISO_CODE_JSON = json.loads(__file_json.read())
    ISO_CODE_LIST = [i for i in ISO_CODE_JSON.keys()]
    
    
# Correction Word result OCR
REMOVE_WORD = [
    'AEC1', 'AECI', '99C'
]

WORD_FOR_REPLACE = {
    # Number to text
    '0' : 'U',
	'6' : 'G',
	'O' : '0',
	# Text to number
	'F' : '0',
	'H' : '0',
    'M' : '0',
    'A' : '4',
    'D' : '0',
    'B' : '8',
	'E' : '0',
    'R' : '3',
    'S' : '3',
	# Number to number
	'1' : '4'
}


# Compnames
COMPNAMES = [
    'SLSU', 'AXIU', 'CXDU', 'TCLU', 'CAXU', 'TEMU', 'SEGU', 'YMLU', 'DFSU', 'MEDU', 'UACU', 'MRKU', 'FCIU', 
    'BSIU', 'SUDU', 'TCNU', 'BMOU', 'WDFU', 'PHRU', 'CMAU', 'APHU', 'TCKU', 'EISU', 'NEXU', 'EITU', 'TRIU', 
    'PONU', 'BEAU', 'FSCU', 'KMBU', 'WWWU', 'MOTU', 'TRLU', 'IRSU', 'TRHU', 'TGHU', 'ZCSU', 'MSKU', 'WKCU', 
    'CRSU', 'DRYU', 'SKHU', 'STXU', 'TWCU', 'SNWU', 'CLHU', 'EGHU', 'HALU', 'MSCU', 'UESU', 'MAGU', 'CAIU', 
    'TTNU', 'GESU', 'IPXU', 'HDMU', 'CARU', 'HMCU', 'FESU', 'APZU', 'PCIU', 'GATU', 'UETU', 'GLDU', 'NLLU', 
    'HLXU', 'HLBU', 'MAEU', 'GCSU', 'XINU', 'IMTU', 'POLU', 'OOLU', 'SBAU', 'TOLU', 'NIUU', 'YMMU', 'ECMU', 
    'MNBU', 'MSLU', 'ZIMU', 'MRSU', 'DAYU', 'LYGU', 'EGSU', 'CBHU', 'WFHU', 'HJCU', 'RFCU', 'HNSU', 'CZTU', 
    'TLXU', 'GRXU', 'TIHU', 'CNSU', 'RMKU', 'VARU', 'SKLU', 'KKTU', 'SKIU', 'PARU', 'CCLU', 'SFFU', 'MOEU', 
    'HASU', 'FRLU', 'MMAU', 'ESPU', 'MBFU', 'BSBU', 'CRXU', 'SIMU', 'HJLU', 'AMFU', 'SGRU', 'KKFU', 'TLLU', 
    'MSWU', 'FCGU', 'NYKU', 'STTU', 'RWLU', 'TGBU', 'YMKU', 'CSLU', 'WHLU', 'MTEU', 'OOCU', 'EMCU', 'NIDU', 
    'ETMU', 'SNBU', 'SZLU', 'CXRU', 'ONTU', 'SSXU', 'DVDU', 'TSTU', 'KMTU', 'TGCU', 'GURU', 'INBU', 'MBOU', 
    'IRNU', 'TYLU', 'PRSU', 'OCGU', 'ESGU', 'CPSU', 'SITU', 'IEMU', 'UAGU', 'SCTU', 'TGAU', 'APRU', 'MWMU', 
    'SSNU', 'CSDU', 'WSDU', 'UNIU', 'TSLU', 'MWCU', 'IKSU', 'GVCU', 'EURU', 'MSMU', 'JOTU', 'ONEU', 'ISLU', 
    'CXTU', 'GAOU', 'MORU', 'FDCU', 'FBIU', 'CPWU', 'MTBU', 'FCBU', 'HMMU', 'CSNU', 'WHSU'
]