#!/usr/bin/env python
"""
Utility report functions
"""

__all__ = ['make_report_from_file','save_report_to_file']
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240810'

from ..processing import numfuncs, qualityanalysis, field

DQ:str="\""
LF:str="\n"
LCURLY:str="{"
RCURLY:str="}"
LSQUARE:str="["
RSQUARE:str="]"
COMMA:str=","


def save_report_to_file(file_uri:str, report:qualityanalysis.QualityAnalysis) -> str:
    """Write a QualityAnalysis report object to file in JSON
    
    file_uri: string URI to locally accessible file
    report: QualityAnalysis report object to be written to file in JSON

    returns: string message starting with notok: if error
    """


    msg:str=""
    temp:list=[]
    try:
        if file_uri is None:
            raise ValueError("no fileURI")
        elif len(file_uri.strip())==0:
            raise ValueError("fileURI is empty")
        if report is None or not isinstance(report, qualityanalysis.QualityAnalysis):
            raise ValueError("report is not QualityAnalysis object")
        
        temp= report.get_json(True)
        if len(temp)==0:
            raise ValueError("no json from report")
        elif temp[0].startswith("notok:"):
            raise ValueError(temp[0][6:])

        with open(file_uri,"w",encoding="utf-8") as f:
            for s in temp:
                f.write(s)

    except RuntimeError as rte:
        msg= "notok:" + str(rte)
    except OSError as ose:
        msg= "notok:" + str(ose)
    except ValueError as ve:
        msg= "notok:" + str(ve)
    return msg



def make_report_from_file(file_uri:str) -> qualityanalysis.QualityAnalysis:
    """Reads report file to parse into 
    QualityAnalysis object report. This should be a report written by VerityPy.

    file_uri: string URI to local or Cloud accessible file

    returns QualityAnalysis object. Its status property will start with notok: if there is an error
    """


    report: qualityanalysis.QualityAnalysis= qualityanalysis.QualityAnalysis()
    txt:str=""
    txt1:str=""
    elem:str=""
    elemval:str=""
    cursect:str=""
    cursect2:str=""
    cursect3:str=""
    lineinlc:str=""
    curfld:str=""
    reason:str=""
    nline:int=0
    n1:int=-1
    nval:int=-1
    nitem:int=-1
    hash_covalues:dict={}
    useline:bool=False
    try:
        if file_uri is None:
            raise ValueError("no fileURI")
        elif len(file_uri.strip())==0:
            raise ValueError("fileURI is empty")
        with open(file_uri,"r", encoding="utf-8") as f:
            for linein in f:
                if linein is None:
                    break
                if linein.endswith("\r\n"):
                    linein=linein[:-2]
                if linein.endswith("\n") or linein.endswith("\r"):
                    linein=linein[:-1]
                useline=True
                if len(linein)==0:
                    useline=False
                elif linein.startswith("#") or linein.startswith("//"):
                    useline= False
                elif linein in (LSQUARE,RSQUARE,LCURLY,RCURLY):
                    useline=False
                else:
                    if DQ in linein:
                        linein=linein.replace(DQ,"")
                    if linein.startswith(COMMA):
                        linein=linein[1:]
                    if linein.endswith(COMMA):
                        linein=linein[:-1]
                    if linein.startswith(LCURLY):
                        linein=linein[1:]
                    if linein.endswith(RCURLY):
                        linein=linein[:-1]
                    if len(linein)==0:
                        useline=False

                if useline:
                    nline +=1
                    lineinlc= linein.lower()
                    if nline==1:
                        if not "report:[" in linein:
                            raise ValueError("first line does not have required report:[ object name")
                        else:
                            cursect="report"
                    elif "err_stats:[" in lineinlc or "errstats:[" in lineinlc:
                        cursect="errstat"
                        cursect2=""
                        cursect3=""
                        curfld=""
                    elif "fields_err_datatype:[" in lineinlc or "fieldserrdatatype:[" in lineinlc:
                        cursect2="flderrdt"
                        cursect3=""
                        curfld=""
                    elif "fields_err_fmt:[" in lineinlc or "fieldserrfmt:[" in lineinlc or "fieldserrformat:[" in lineinlc:
                        cursect2="flderrfmt"
                        cursect3=""
                        curfld=""
                    elif "fields:[" in lineinlc:
                        cursect="fields"
                    elif "field_datatypes:[" in lineinlc or "fielddatatypes:[" in lineinlc:
                        cursect="fielddatatypes"
                        nitem=-1
                    elif "field_formats:[" in lineinlc or "fieldformats:[" in lineinlc:
                        cursect="fieldformats"
                        nitem=-1
                    elif "field_quality:[" in lineinlc or "fieldquality:[" in lineinlc:
                        cursect="fieldquality"
                        nitem=-1
                    elif "field_datatype_dists:[" in lineinlc or "fielddatatypedists:[" in lineinlc:
                        cursect="fielddatatypedists"
                        nitem=-1
                    elif "field_uniqvalues:[" in lineinlc or "fielduniqvalues:[" in lineinlc:
                        cursect="fielduniqvalues"
                        curfld=""
                    elif "field_spchar_dists:[" in lineinlc or "fieldspchardists:[" in lineinlc or "fieldspecchardists:[" in lineinlc:
                        cursect="fieldspchardists"
                        curfld=""
                    elif "spec_char_dists:[" in lineinlc or "specchardists:[" in lineinlc:
                        cursect="spchardists"
                    elif "spec_char_examples:[" in lineinlc or "speccharexamples:[" in lineinlc:
                        cursect="spcharexamples"
                    elif "err_datatype_examples:[" in lineinlc or "errdatatypeexamples:[" in lineinlc:
                        cursect="errdatatypeexamples"
                    elif "err_fmt_examples:[" in lineinlc or "errfmtexamples:[" in lineinlc:
                        cursect="errfmtexamples"
                    elif "rec_size_dist:[" in lineinlc or "recsizedist:[" in lineinlc:
                        cursect="recsizedist"
                    elif "rec_parse_dist:[" in lineinlc or "recparsedist:[" in lineinlc:
                        cursect="recparsedist"
                    elif "rec_parse_errs:[" in lineinlc or "recparseerrs:[" in lineinlc or "recparseerrors:[" in lineinlc:
                        cursect="recparseerrs"
                    elif "rec_parse_errs_examples:[" in lineinlc or "recparseerrsexamples:[" in lineinlc:
                        cursect="recparseerrsexamples"
                    elif "covalues:[" in lineinlc:
                        cursect="covalues"
                    elif "covalue_uniqvalues:[" in lineinlc or "covalueuniqvalues:[" in lineinlc:
                        cursect="covalueuniqvalues"
                        curfld=""
                    elif "reasons:[" in lineinlc:
                        if cursect=="errstat":
                            if cursect2=="":
                                raise ValueError("found errstat reasons:[ but for unknown child section at nline=" + str(nline))
                            elif curfld=="":
                                raise ValueError("found errstat." + cursect2 + " reasons:[ but for unknown field at nline=" + str(nline))
                            cursect3="reason"
                        else:
                            raise ValueError("found reasons:[ but for unexpected location at nline=" + str(nline))
                    elif cursect=="report":
                        if ":" in linein:
                            elem= linein[:linein.find(":")].lower()
                            elemval= linein[(linein.find(":")+1):]
                            if elem=="title":
                                report.title= elemval
                            elif elem=="status":
                                report.status= elemval
                            elif elem=="numrecs":
                                report.numrecs = numfuncs.is_int_get(elemval, "number", False)
                            elif elem=="maxuv":
                                report.maxuv = numfuncs.is_int_get(elemval, "number", False)
                            elif elem=="delim":
                                report.delim= elemval
                            elif elem in ("delim_char","delimchar"):
                                report.delim_char= elemval
                            elif elem in ("is_case_sens","iscasesens"):
                                report.is_case_sens = True if elemval=="true" else False
                            elif elem in ("is_quoted","isquoted"):
                                report.is_quoted = True if elemval=="true" else False
                            elif elem in ("has_header","hasheader"):
                                report.has_header = True if elemval=="true" else False
                            elif elem in ("extract_fields","extractfields"):
                                report.extract_fields = True if elemval=="true" else False
                    elif cursect=="fields":
                        elemval=linein
                        if elemval.lower() in report.hash_fields:
                            raise ValueError("duplicate field in fields section: " + elemval)
                        report.fields.append(field.Field(elemval))
                        report.hash_fields[elemval.lower()]= len(report.fields)-1
                        report.field_names_lower.append(elemval.lower())
                        report.field_datatype_dist.append({"int":0,"real":0,"bool":0,"date":0,"string":0,"empty":0})
                        report.field_uniqvals.append([])
                        report.field_quality.append("")
                        report.spec_char_dist_field.append({})
                    elif cursect=="fielddatatypes":
                        nitem +=1
                        elemval=linein
                        if nitem< len(report.fields):
                            report.fields[nitem].datatype= elemval
                    elif cursect=="fieldformats":
                        nitem +=1
                        elemval=linein
                        if nitem< len(report.fields):
                            txt=elemval.lower()
                            if "strcase:" in txt:
                                txt1= txt[(txt.find("strcase:")+8):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                report.fields[nitem].fmt_strcase=txt1
                            if "strlen:" in txt:
                                txt1= txt[(txt.find("strlen:")+7):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.fields[nitem].fmt_strlen= int(txt1)
                            if "decimal:" in txt:
                                txt1= txt[(txt.find("decimal:")+8):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.fields[nitem].fmt_decimal= int(txt1)
                            if "date:" in txt:
                                txt1= txt[(txt.find("date:")+5):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                report.fields[nitem].fmt_date=txt1
                            if "strcut:" in txt:
                                txt1= txt[(txt.find("strcut:")+7):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                report.fields[nitem].fmt_strcut=txt1
                            if "strpad:" in txt:
                                txt1= txt[(txt.find("strpad:")+7):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                report.fields[nitem].fmt_strpad=txt1
                            if "strpadchar:" in txt:
                                txt1= txt[(txt.find("strpadchar:")+11):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                report.fields[nitem].fmt_strpadchar=txt1
                    elif cursect=="fieldquality":
                        nitem +=1
                        elemval=linein
                        if nitem< len(report.fields):
                            report.field_quality[nitem]= elemval
                    elif cursect=="fielddatatypedists":
                        nitem +=1
                        elemval=linein
                        if nitem< len(report.fields):
                            txt=elemval.lower()
                            if "int:" in txt:
                                txt1= txt[(txt.find("int:")+4):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.field_datatype_dist[nitem]["int"]= int(txt1)
                            if "real:" in txt:
                                txt1= txt[(txt.find("real:")+5):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.field_datatype_dist[nitem]["real"]= int(txt1)
                            if "bool:" in txt:
                                txt1= txt[(txt.find("bool:")+5):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.field_datatype_dist[nitem]["bool"]= int(txt1)
                            if "date:" in txt:
                                txt1= txt[(txt.find("date:")+5):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.field_datatype_dist[nitem]["date"]= int(txt1)
                            if "string:" in txt:
                                txt1= txt[(txt.find("string:")+7):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.field_datatype_dist[nitem]["string"]= int(txt1)
                            if "empty:" in txt:
                                txt1= txt[(txt.find("empty:")+6):]
                                if COMMA in txt1:
                                    txt1=txt1[:txt1.find(COMMA)]
                                if numfuncs.is_int(txt1):
                                    report.field_datatype_dist[nitem]["empty"]= int(txt1)
                    elif cursect=="fielduniqvalues":
                        elemval=linein
                        if "field:" in elemval:
                            curfld= elemval[(elemval.find(":")+1):].lower()
                            if not curfld in report.hash_fields:
                                raise ValueError("fielduniqvalues has unknown field: " + curfld + " at nline=" + str(nline))
                        elif "uniqvalues:[" in elemval.lower():
                            # object name from DotNet lib JSON so ignore
                            continue
                        elif len(curfld)>0 and "uniqvalue:" in elemval and ",count:" in elemval:
                            elemval= elemval[(elemval.find("uniqvalue:") + 10):]
                            elem= elemval[:elemval.find(",count:")]
                            elemval= elemval[(elemval.find(",count:")+7):]
                            nitem= report.hash_fields[curfld]
                            if (nval := numfuncs.is_int_get(elemval, "number", False)) <0:
                                nval=0
                            report.field_uniqvals[nitem].append((elem,nval))
                    elif cursect=="covalues":
                        if linein.startswith(LCURLY):
                            linein=linein[1:]
                        if linein.endswith(RCURLY):
                            linein=linein[:-1]
                        if "title:" in linein:
                            elemval= linein[(linein.find("title:") + 6):]
                            if ",field1:" in elemval:
                                elemval= elemval[:elemval.find(",field1:")]
                            report.covalues.append(field.CoValue(elemval))
                            nitem= len(report.covalues)-1
                            hash_covalues[elemval.lower()]= nitem
                            report.covalue_uniqvals.append([])
                            if ",field1:" in linein:
                                elemval= linein[(linein.find(",field1:") + 8):]
                                if ",field2:" in elemval:
                                    elemval= elemval[:elemval.find(",field2:")]
                                report.covalues[nitem].field1=elemval
                            if ",field2:" in linein:
                                elemval= linein[(linein.find(",field2:") + 8):]
                                if ",field3:" in elemval:
                                    elemval= elemval[:elemval.find(",field3:")]
                                report.covalues[nitem].field2=elemval
                            if ",field3:" in linein:
                                elemval= linein[(linein.find(",field3:") + 8):]
                                if ",field1_index:" in elemval:
                                    elemval= elemval[:elemval.find(",field1_index:")]
                                report.covalues[nitem].field3=elemval
                            if ",field1_index:" in linein:
                                elemval= linein[(linein.find(",field1_index:") + 14):]
                                if ",field2_index:" in elemval:
                                    elemval= elemval[:elemval.find(",field2_index:")]
                                report.covalues[nitem].field1_index= n1 if (n1 := numfuncs.is_int_get(elemval, "number", False)) >=0 else -1
                            if ",field2_index:" in linein:
                                elemval= linein[(linein.find(",field2_index:") + 14):]
                                if ",field3_index:" in elemval:
                                    elemval= elemval[:elemval.find(",field3_index:")]
                                report.covalues[nitem].field2_index= n1 if (n1 := numfuncs.is_int_get(elemval, "number", False)) >=0 else -1
                            if ",field3_index:" in linein:
                                elemval= linein[(linein.find(",field3_index:") + 14):]
                                if ",numfields:" in elemval:
                                    elemval= elemval[:elemval.find(",numfields:")]
                                report.covalues[nitem].field3_index= n1 if (n1 := numfuncs.is_int_get(elemval, "number", False)) >=0 else -1
                            if ",numfields:" in linein:
                                elemval= linein[(linein.find(",numfields:") + 11):]
                                report.covalues[nitem].numfields= n1 if (n1 := numfuncs.is_int_get(elemval, "number", False)) >0 else 0
                    elif cursect=="covalueuniqvalues":
                        elemval=linein
                        if "covalue:" in lineinlc:
                            curfld= elemval[(elemval.find(":")+1):].lower()
                            if curfld not in hash_covalues:
                                raise ValueError("coValue from its uniqueValues is not known: " + curfld + " at nline=" + str(nline))
                        elif "uniqvalues:[" in lineinlc:
                            # object name from DotNet lib JSON so ignore
                            continue
                        elif len(curfld)>0 and "uniqvalue:" in lineinlc and ",count:" in elemval:
                              elemval= elemval[(lineinlc.find("uniqvalue:") + 10):]
                              elem= elemval[:elemval.find(",count:")]
                              elemval= elemval[(elemval.find(",count:")+7):]
                              nitem= hash_covalues[curfld]
                              if (nval := numfuncs.is_int_get(elemval, "number", False)) <0:
                                  nval=0
                              report.covalue_uniqvals[nitem].append((elem,nval))
                    elif cursect=="fieldspchardists":
                        elemval=linein
                        if "field:" in elemval:
                            curfld= elemval[elemval.find("field:")+6:].lower()
                            if curfld.endswith(":["):
                              curfld= curfld[:-2]
                            if not curfld in report.hash_fields:
                                raise ValueError("fieldspchardists has unknown field: " + curfld + " at nline=" + str(nline))
                        elif ":[" in elemval:
                            curfld= elemval[:elemval.find(":[")].lower()
                            if not curfld in report.hash_fields:
                                raise ValueError("fieldspchardists has unknown field: " + curfld + " at nline=" + str(nline))
                        elif len(curfld)>0:                            
                          if ":" in elemval:
                              elem= elemval[:elemval.find(":")]
                              elemval= elemval[(elemval.find(":")+1):]
                              nitem= report.hash_fields[curfld]
                              if (nval := numfuncs.is_int_get(elemval, "number", False)) <0:
                                  nval=0
                              report.spec_char_dist_field[nitem][elem]=nval
                    elif cursect=="spchardists":
                        elemval=linein
                        if ":" in elemval:
                            elem= elemval[:elemval.find(":")]
                            elemval= elemval[(elemval.find(":")+1):]
                            if (nval := numfuncs.is_int_get(elemval, "number", False)) <0:
                                nval=0
                            report.spec_char_dist[elem]=nval
                    elif cursect=="spcharexamples":
                        if "example:" in linein:
                            elemval= linein[(linein.find("example:")+8):]
                            txt=""
                            if ",rec:" in elemval:
                                txt= elemval[(elemval.find(",rec:")+5):]
                                elemval= elemval[:elemval.find(",rec:")]
                            elemval=elemval.replace("{","").replace("}","")
                            report.spec_char_examples.append(elemval + txt)
                    elif cursect=="errdatatypeexamples":
                        if "nline:" in linein:
                            elemval= linein[(linein.find("nline:")+6):]
                            txt=""
                            if ",rec:" in elemval:
                                txt= elemval[(elemval.find(",rec:")+5):]
                                elemval = elemval[:elemval.find(",rec:")]
                                elemval = "(" + elemval + ")" + txt
                            report.err_datatype_examples.append(elemval)
                    elif cursect=="errfmtexamples":
                            elemval= linein[(linein.find("nline:")+6):]
                            txt=""
                            if ",rec:" in elemval:
                                txt= elemval[(elemval.find(",rec:")+5):]
                                elemval = elemval[:elemval.find(",rec:")]
                                elemval = "(" + elemval + ")" + txt
                            report.err_fmt_examples.append(elemval)
                    elif cursect=="errstat":
                        if ":" in linein:
                            elem= linein[:linein.find(":")].lower()
                            elemval= linein[(linein.find(":")+1):]
                            if elem in ["numrecs_err","numrecserr"]:
                                report.err_stats["numrecs_err"]= numfuncs.is_int_get(elemval, "number", False)
                            elif elem in ["numrecs_err_datatype","numrecserrdatatype"]:
                                report.err_stats["numrecs_err_datatype"]= numfuncs.is_int_get(elemval, "number", False)
                            elif elem in ["numrecs_err_fmt","numrecserrfmt"]:
                                report.err_stats["numrecs_err_fmt"]= numfuncs.is_int_get(elemval, "number", False)
                            elif elem=="field":
                                if cursect2=="":
                                    raise ValueError("found field in errstat for unknown type at nline=" + str(nline))
                                if ",count:" in elemval:
                                    txt= elemval[(elemval.find(":")+1):]
                                    if numfuncs.is_int(txt):
                                        n1= int(txt)
                                    else:
                                        raise ValueError("no count for field in errstat." + cursect2 + " at nline=" + str(nline))
                                    curfld= elemval[:elemval.find(",count:")]
                                else:
                                    raise ValueError("no ,count: part for field in errstat." + cursect2 + " at nline=" + str(nline))
                                if cursect2=="flderrdt":
                                    report.err_stats["fields_err_datatype"][curfld]={}
                                    report.err_stats["fields_err_datatype"][curfld]["count"]=n1
                                    report.err_stats["fields_err_datatype"][curfld]["reasons"]={}
                                elif cursect2=="flderrfmt":
                                    report.err_stats["fields_err_fmt"][curfld]={}
                                    report.err_stats["fields_err_fmt"][curfld]["count"]=n1
                                    report.err_stats["fields_err_fmt"][curfld]["reasons"]={}
                            elif elem=="reason" and cursect3=="reason":
                                if cursect2=="":
                                    raise ValueError("found reason in errstat for unknown type at nline=" + str(nline))
                                if curfld=="":
                                    raise ValueError("found reason in errstat for unknown field at nline=" + str(nline))
                                if ",count:" in elemval:
                                    txt= elemval[(elemval.find(":")+1):]
                                    if numfuncs.is_int(txt):
                                        n1= int(txt)
                                    else:
                                        raise ValueError("no count for reason in errstat." + cursect2 + " at nline=" + str(nline))
                                    reason= elemval[:elemval.find(",count:")]
                                else:
                                    raise ValueError("no ,count: part for field in errstat." + cursect2 + " at nline=" + str(nline))
                                if cursect2=="flderrdt":
                                    report.err_stats["fields_err_datatype"][curfld]["reasons"][reason]=n1
                                elif cursect2=="flderrfmt":
                                    report.err_stats["fields_err_fmt"][curfld]["reasons"][reason]=n1
                    elif cursect=="recsizedist":
                        elemval=linein
                        if ":" in elemval:
                            elem= elemval[:elemval.find(":")]
                            elemval=elemval[(elemval.find(":")+1):]
                            if (nval := numfuncs.is_int_get(elemval, "number", False)) <0:
                                nval=0
                            report.rec_size_dist[elem]= nval
                    elif cursect=="recparsedist":
                        elemval=linein
                        if ":" in elemval:
                            elem= elemval[:elemval.find(":")]
                            elemval=elemval[(elemval.find(":")+1):]
                            if (nval := numfuncs.is_int_get(elemval, "number", False)) <0:
                                nval=0
                            report.rec_parse_dist[elem]= nval
                    elif cursect=="recparseerrs":
                        elemval=linein
                        if ":" in elemval:
                            elem= elemval[:elemval.find(":")].lower()
                            elemval=elemval[(elemval.find(":")+1):]
                            if (nval := numfuncs.is_int_get(elemval, "number", False)) <0:
                                nval=0
                            if "small1" in elem:
                                report.rec_parse_errs["small1"]= nval
                            elif "small2" in elem:
                                report.rec_parse_errs["small2"]= nval
                            elif "big" in elem:
                                report.rec_parse_errs["big"]= nval
                    elif cursect=="recparseerrsexamples":
                        if "small1:[" in lineinlc:
                            cursect2="small1"
                        elif "small2:[" in lineinlc:
                            cursect2="small2"
                        elif "big:[" in lineinlc:
                            cursect2="big"
                        elif "record:" in lineinlc:
                            elemval=linein[(linein.find(":")+1):]
                            report.rec_parse_errs[cursect2 + "_recs"].append(elemval)
    except RuntimeError as rte:
        print("runtime error: {0}", str(rte))
        report.status= "notok:" + str(rte)
    except OSError as ose:
        print("OS error: {0}", str(ose))
        report.status= "notok:" + str(ose)
    except ValueError as ve:
        print("value error: {0}", str(ve))
        report.status= "notok:" + str(ve)
    return report
