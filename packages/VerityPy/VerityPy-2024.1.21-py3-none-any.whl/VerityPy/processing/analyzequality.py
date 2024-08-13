#!/usr/bin/env python
"""
Analyze Quality

Performs deep inspection of data records supplied as List of strings 
which must be delimited. The delimiter should be specified in a dict supplied 
as settings in call to function. Various results are returned in a 
QualityAnalysis object.
"""

__all__ = ['do_qualityinspect','detect_parsing_error','qc_fields']
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240723'

import copy
from . import recfuncs, datefuncs, numfuncs, qualityanalysis, field


DQ:str= "\""
LF:str="\n"

def do_qualityinspect(fields:list=None, covalues:list=None, recs:list=None, settings:dict=None) -> qualityanalysis.QualityAnalysis:
    """
    Do Quality Inspect. Performs deep inspection of data records to discover and assess 
    a variety of structure, syntax, and semantic problems and inconsistencies. 
    Field information can either be supplied with the 'fields' parameter or extracted from a header line in 
    records. If using 'fields', there can also be specified datatypes and formats per field which will be 
    used to detect errors when values do not meet these rules. 
    fields: list of field objects with attributes-
        title: field name
        datatype: int, real, bool, date, string. For date, 
            there should be an entry in field.fmt_date specifying the date format otherwise it is set to ISO yyyyMMdd
        fmt_strlen: integer number of characters (>0) if a fixed size is required. Ignored if < 0
        fmt_strcase: (upper, lower, empty)
        fmt_strcut: (front, back, empty). Used in Refining records. Side to cut characters from if it is larger than specified fmt_strlen. Default is back.
        fmt_strpad: (front, back, empty). Used in Refining records. Side to add characters to if it is smaller than specified fmt_strlen. Default is back.
        fmt_strpadchar: single character or character alias (-space-, -fslash-, -bslash-, -tab-). Used in Refining records. Character to add if needed to make too small string meet specified fmt_strlen. Default is _
        fmt_decimal: number of decimal digits (0-N). Ignored if < 0
        fmt_date: without time part- yyyymmdd, yymmdd, yyyyddmm, yyddmm, mmddyyyy, mmddyy, ddmmyyyy, ddmmyy
            (mmm= month abbreviation like Jan) yyyymmmdd, yyyyddmmm, ddmmmyyyy, ddmmmyy
            (month= full month name like January) yyyymonthdd, yyyyddmonth, ddmonthyyyy, ddmonthyy
            with time part: suffix to above date formats as (T=letter T, S=space)- Thhmmss, Thhmm, Thh, 
                Shhmmss, Shhmm, Shh like mmddyyyyThhmm for 11282024T1407 or 11/28/2024T14:07 or 11-28-2024 14:07
            with time zone: if time zone is required at end of time part add suffix Z like mmddyyyyThhmmZ 11282024T1407
    covalues: optional list of field titles (2-3) for joint value analysis with each list entry as field1,field2 and optionally with ,field3
    recs: list of records. The delimiter should be specified in the settings object ('delim'= comma,pipe,tab,colon)
    settings: dictionary object with entries for options to use in inspection. Includes:
        delim: record delimiter (comma,pipe,tab,colon). Default is comma.
        is_case_sens: is case sensitive (true,false). Default is false.
        is_quoted: field values may be enclosed (allows delimiter within) by double quotes (true, false). Default is false.
        maxuv: optional. string of integer value that is maximum number of unique values per field 
            to collect. Default is 50 and set to default if supplied value <1 or >1000
        extract_fields: bool whether to read in field titles from header line (first non-comment, non-empty line). 
            Default is False. If True then has_header must also be True, and submitted 'fields' list will only be 
            used to copy its datatype and formatting to the report field object. Thus, you can extract field 
            titles from data set and still define characteristics if desired. If not, ensure 'fields' is empty.
        has_header: bool whether has header line in file. Default is True. Must be True if extract_fields is True
    Returns report as a QualityAnalysis class instance.
    """

    hash_temp:dict={}
    report: qualityanalysis.QualityAnalysis= qualityanalysis.QualityAnalysis()
    linein:str=""
    txt:str=""
    txt1:str=""
    txt2:str=""
    fldname:str=""
    fldval:str=""
    fldval2:str=""
    fldval3:str=""
    nrec:int=-1
    nflds:int=-1
    nfld1:int=-1
    nfld2:int=-1
    nfld3:int=-1
    n1:int=-1
    f1:float=0
    f2:float=0
    rec_has_err:bool=False
    rec_has_dt_err:bool=False
    rec_has_fmt_err:bool=False
    field_values:list=[]
    tempint:list={}
    tempbool:list={}
    hash_srcfields:dict={}
    try :
        if recs is None or len(recs)==0:
            raise ValueError("no records")

        if not settings is None and isinstance(settings, dict):
            for k,v in settings.items():
                txt= k.lower()
                txt1= str(v).lower()
                if txt in ("is_case_sens","iscasesens"):
                    report.is_case_sens= txt1=="true"
                elif txt in ("isquoted","is_quoted"):
                    report.is_quoted= txt1=="true"
                elif txt in ("hasheader","has_header"):
                    report.has_header= txt1 != "false"
                elif txt in ("extract_fields","extractfields"):
                    report.extract_fields= txt1=="true"
                elif txt =="delim":
                    if len(txt1)==0:
                        raise ValueError("empty delim specified")
                    report.delim= txt1
                    report.delim_char= recfuncs.delim_get_char(report.delim)
                elif txt=="maxuv":
                    report.maxuv= numfuncs.is_int_get(txt1,"number")
                    if 1> report.maxuv > 1000:
                        report.maxuv=50

        if report.extract_fields and not report.has_header:
            raise ValueError("extract_fields is True which requires a header line but has_header is False")

        if (fields is None or len(fields)==0) and not report.extract_fields:
            raise ValueError("no fields")

        if report.delim_char.startswith("false") or len(report.delim_char)==0:
            raise ValueError("no delim in settings")

        for i in range(len(fields)):
            if isinstance(fields[i], field.Field):
                txt =fields[i].title.lower().strip()
                if len(txt)==0:
                    raise ValueError("empty field title at index " + str(i))
                if txt in hash_srcfields:
                    raise ValueError("duplicate field:" + txt)
                hash_srcfields[txt]=i
                txt= fields[i].datatype.strip()
                if txt.startswith("int"):
                    txt1="int"
                elif txt in ["real","float"]:
                    txt1="real"
                elif txt.startswith("date"):
                    txt1="date"
                elif txt.startswith("bool"):
                    txt1="bool"
                elif len(txt)>0:
                    txt1="string"
                fields[i].datatype=txt1  # normalize
            else:
                raise ValueError("source field is not a Field object at index=" + str(i))

        if not report.extract_fields:
            for i in range(len(fields)):
                if isinstance(fields[i], field.Field):
                    txt=fields[i].title.lower().strip()
                    if txt in report.hash_fields:
                        raise ValueError("duplicate field:" + txt)
                    report.fields.append(field.Field(fields[i].title.strip()))
                    n1= len(report.fields)-1
                    report.hash_fields[txt]= n1
                    report.field_names_lower.append(txt)
                    report.fields[n1].datatype= fields[i].datatype
                    report.fields[n1].fmt_strcase= fields[i].fmt_strcase
                    report.fields[n1].fmt_strlen= fields[i].fmt_strlen
                    report.fields[n1].fmt_strcut= fields[i].fmt_strcut
                    report.fields[n1].fmt_strpad= fields[i].fmt_strpad
                    report.fields[n1].fmt_strpadchar= fields[i].fmt_strpadchar
                    report.fields[n1].fmt_decimal= fields[i].fmt_decimal
                    report.fields[n1].fmt_date= fields[i].fmt_date
                    report.fields[n1].mapto= fields[i].mapto

                    report.field_datatype_dist.append({'int':0,'real':0,'date':0,'bool':0,'string':0,'empty':0})
                    report.field_uniqvals.append({})
                    report.spec_char_dist_field.append({})
                    report.field_quality.append("")
                else:
                    raise ValueError("field entry is not a Field object at index=" + str(i))

            for i in range(len(covalues)):
                if "," in covalues[i]:
                    n1= covalues[i].find(",")
                    txt=covalues[i][:n1].lower().strip()
                    txt1=covalues[i][(n1+1):].lower().strip()
                    txt2=""
                    n1=txt1.find(",")
                    if n1>0:
                        txt2=txt1[(n1+1):].strip()
                        txt1=txt1[:n1].strip()
                        nflds=3
                    else:
                        nflds=2

                    fldname= txt + "," + txt1
                    if nflds==3:
                        fldname += "," + txt2

                    if fldname not in hash_temp:
                        if txt not in report.hash_fields:
                            raise ValueError("covalue field " + txt + "is not in record fields")
                        nfld1= report.hash_fields[txt]
                        if txt1 not in report.hash_fields:
                            raise ValueError("covalue field " + txt1 + "is not in record fields")
                        nfld2= report.hash_fields[txt1]
                        if nflds==3:
                            if txt2 not in report.hash_fields:
                                raise ValueError("covalue field " + txt2 + "is not in record fields")
                            nfld3= report.hash_fields[txt2]

                        report.covalues.append(field.CoValue(fldname))
                        n1= len(report.covalues)-1
                        report.covalues[n1].field1=txt
                        report.covalues[n1].field2=txt1
                        report.covalues[n1].field3=txt2
                        report.covalues[n1].field1_index= nfld1
                        report.covalues[n1].field2_index= nfld2
                        report.covalues[n1].field3_index= nfld3
                        report.covalues[n1].numfields= nflds

                        report.covalue_uniqvals.append({})
                        hash_temp[fldname]= len(report.covalues)-1

        nrec=0
        for iloop in range(len(recs)):
            rec_has_err=False
            rec_has_dt_err=False
            rec_has_fmt_err=False

            linein=recs[iloop]
            txt=linein.strip()
            if len(txt)>0 and not txt.startswith("#") and not txt.startswith("//"):
                nrec +=1
                if report.is_quoted and DQ in linein:
                    field_values=recfuncs.split_quoted_line(linein, report.delim_char)
                    if len(field_values)>0 and field_values[0].startswith("notok:"):
                        raise RuntimeError("error splitting quoted string: " + field_values[0][6:])
                else:
                    field_values=linein.split(report.delim_char)

                if nrec==1 and report.extract_fields:
                    for i in range(len(field_values)):
                        txt=field_values[i].lower().strip()
                        if len(txt)==0:
                            raise ValueError("empty extracted field title at index " + str(i))
                        elif txt in report.hash_fields:
                            raise ValueError("duplicate extracted field:" + report.fields[i].title)
                        report.field_names_lower.append(txt)
                        report.fields.append(field.Field(field_values[i].strip()))
                        report.hash_fields[txt]=i
                        if (txt in hash_srcfields):
                            n1=hash_srcfields[txt]
                            report.fields[i].datatype= fields[n1].datatype
                            report.fields[i].fmt_strcase= fields[n1].fmt_strcase
                            report.fields[i].fmt_strlen= fields[n1].fmt_strlen
                            report.fields[i].fmt_strcut= fields[n1].fmt_strcut
                            report.fields[i].fmt_strpad= fields[n1].fmt_strpad
                            report.fields[i].fmt_strpadchar= fields[n1].fmt_strpadchar
                            report.fields[i].fmt_decimal= fields[n1].fmt_decimal
                            report.fields[i].fmt_date= fields[n1].fmt_date
                            report.fields[i].mapto= fields[n1].mapto

                        report.field_datatype_dist.append({'int':0,'real':0,'date':0,'bool':0,'string':0,'empty':0})
                        report.field_uniqvals.append({})
                        report.spec_char_dist_field.append({})
                        report.field_quality.append("")

                    if len(report.fields)==0:
                        raise ValueError("no fields from extracted header (delim=" + report.delim_char + ") line:" + linein)

                    for i in range(len(covalues)):
                        if "," in covalues[i]:
                            n1= covalues[i].find(",")
                            txt=covalues[i][:n1].lower().strip()
                            txt1=covalues[i][(n1+1):].lower().strip()
                            txt2=""
                            n1=txt1.find(",")
                            if n1>0:
                                txt2=txt1[(n1+1):].strip()
                                txt1=txt1[:n1].strip()
                                nflds=3
                            else:
                                nflds=2

                            fldname= txt + "," + txt1
                            if nflds==3:
                                fldname += "," + txt2

                            if fldname not in hash_temp:
                                if txt not in report.hash_fields:
                                    raise ValueError("covalue field " + txt + " is not in record fields")
                                nfld1= report.hash_fields[txt]
                                if txt1 not in report.hash_fields:
                                    raise ValueError("covalue field " + txt1 + " is not in record fields")
                                nfld2= report.hash_fields[txt1]
                                if nflds==3:
                                    if txt2 not in report.hash_fields:
                                        raise ValueError("covalue field " + txt2 + " is not in record fields")
                                    nfld3= report.hash_fields[txt2]

                                report.covalues.append(field.CoValue(fldname))
                                n1= len(report.covalues)-1
                                report.covalues[n1].field1=txt
                                report.covalues[n1].field2=txt1
                                report.covalues[n1].field3=txt2
                                report.covalues[n1].field1_index= nfld1
                                report.covalues[n1].field2_index= nfld2
                                report.covalues[n1].field3_index= nfld3
                                report.covalues[n1].numfields= nflds

                                report.covalue_uniqvals.append({})
                                hash_temp[fldname]= len(report.covalues)-1
                elif nrec>1 or not report.has_header:
                    txt=str(len(linein))
                    if txt in report.rec_size_dist:
                        report.rec_size_dist[txt] +=1
                    elif len(report.rec_size_dist)<100:
                        report.rec_size_dist[txt] =1
                    report.numrecs += 1

                    #check for parsing errors with number of parsed fields
                    txt= detect_parsing_error(linein, field_values, report, nrec)
                    if txt.startswith("notok:"):
                        raise ValueError("error detecting parsing: " + txt[6:])
                    if "rec_has_err=true" in txt:
                        rec_has_err=True

                    # go through fields for datatypes, formats, unique values
                    txt = qc_fields(linein, field_values, report, nrec)
                    if txt.startswith("notok:"):
                        raise ValueError("error doing qc: " + txt[6:])
                    if "rec_has_fmt_err=true" in txt:
                        rec_has_fmt_err=True
                    if "rec_has_dt_err=true" in txt:
                        rec_has_dt_err=True

                    if rec_has_dt_err:
                        rec_has_err=True
                        report.err_stats["numrecs_err_datatype"] += 1
                    if rec_has_fmt_err:
                        rec_has_err=True
                        report.err_stats["numrecs_err_fmt"] += 1
                    if rec_has_err:
                        report.err_stats["numrecs_err"] += 1

                    # get covalue data
                    for jloop in range(len(report.covalues)):
                        nfld1=report.covalues[jloop].field1_index
                        nfld2=report.covalues[jloop].field2_index
                        nfld3=report.covalues[jloop].field3_index
                        fldval=""
                        fldval2=""
                        fldval3=""
                        if nfld1<len(field_values):
                            fldval= field_values[nfld1]
                        if nfld2<len(field_values):
                            fldval2= field_values[nfld2]
                        if 0<=nfld3<len(field_values):
                            fldval3= field_values[nfld3]

                        txt= fldval + "_" + fldval2
                        if nfld3>-1:
                            txt += "_" + fldval3
                        if not report.is_case_sens:
                            txt=txt.lower()
                        if txt not in report.covalue_uniqvals[jloop] and len(report.covalue_uniqvals[jloop])>=report.maxuv:
                            txt="-other-"
                        if txt not in report.covalue_uniqvals[jloop]:
                            report.covalue_uniqvals[jloop][txt]=0
                        report.covalue_uniqvals[jloop][txt] +=1

        # sort uniquevalues and change to list instead of dict
        for i in range(len(fields)):
            report.field_uniqvals[i]=sorted(report.field_uniqvals[i].items(), key=lambda x:x[1], reverse=True)

        for i in range(len(report.covalues)):
            report.covalue_uniqvals[i]=sorted(report.covalue_uniqvals[i].items(), key=lambda x:x[1], reverse=True)

        # compute field quality
        for i in range(len(fields)):
            tempint={"totalinst":0,"dterr":0,"dtdist":0,"fmterr":0,"fmtstrcase":0,"fmtstrlen":0,"fmtdate":0,"fmtdec":0,"spchar":0}
            tempbool={"totalinst":False,"dterr":False,"dtdist":False,"fmterr":False,"fmtstrcase":False,"fmtstrlen":False,"fmtdate":False,"fmtdec":False,"spchar":False}
            fldname= fields[i].title.lower()
            if fldname in report.err_stats["fields_err_datatype"]:
                tempint["dterr"]= report.err_stats["fields_err_datatype"][fldname]["count"]
                tempbool["dterr"]= True
            if fldname in report.err_stats["fields_err_fmt"]:
                tempint["fmterr"]= report.err_stats["fields_err_fmt"][fldname]["count"]
                tempbool["fmterr"]= True
                for reason in report.err_stats["fields_err_fmt"][fldname]["reasons"]:
                    if fields[i].datatype=="string":
                        if "uppercase" in reason or "lowercase" in reason:
                            tempint["fmtstrcase"] += report.err_stats["fields_err_fmt"][fldname]["reasons"][reason]
                            tempbool["fmtstrcase"] = True
                        elif "length" in reason:
                            tempint["fmtstrlen"] += report.err_stats["fields_err_fmt"][fldname]["reasons"][reason]
                            tempbool["fmtstrlen"] = True
                    elif fields[i].datatype=="real":
                        if "decimal" in reason:
                            tempint["fmtdec"] += report.err_stats["fields_err_fmt"][fldname]["reasons"][reason]
                            tempbool["fmtdec"] = True
                    elif fields[i].datatype=="date":
                        if "format" in reason:
                            tempint["fmtdate"] += report.err_stats["fields_err_fmt"][fldname]["reasons"][reason]
                            tempbool["fmtdate"] = True
            for dtyp in report.field_datatype_dist[i]:
                if dtyp!= fields[i].datatype:
                    tempint["dtdist"] += report.field_datatype_dist[i][dtyp]
                    tempbool["dtdist"] = True
            for sc in report.spec_char_dist_field[i]:
                tempint["spchar"] += report.spec_char_dist_field[i][sc]
                tempbool["spchar"]= True
            for j in range(len(report.field_uniqvals[i])):
                tempint["totalinst"] += report.field_uniqvals[i][j][1]
                tempbool["totalinst"]= True
            if tempint["totalinst"]>0:
                f1=100
                if tempint["dterr"]>0 and tempint["dtdist"]>0:
                    if tempint["dterr"]> tempint["dtdist"]:
                        f1 = 100- round(100*tempint["dterr"]/tempint["totalinst"],1)
                    else:
                        f1 = 100- round(100*tempint["dtdist"]/tempint["totalinst"],1)
                elif tempint["dterr"]>0:
                    f1 = 100- round(100*tempint["dterr"]/tempint["totalinst"],1)
                elif tempint["dtdist"]>0:
                    f1 = 100- round(100*tempint["dtdist"]/tempint["totalinst"],1)
                if f1>100:
                    f1=100
                elif f1<0:
                    f1=0
                # f1 is base goodness factor. next we reduce it when other issues exist based on datatype
                if fields[i].datatype=="real":
                    if tempbool["fmtdec"] and tempint["fmtdec"]>0:
                        f2= 100- round(100*tempint["fmtdec"]/tempint["totalinst"],1)
                        if f2<= 50:
                            f1 /= 2
                        elif f2<= 75:
                            f1 /= 1.5
                        elif f2<= 85:
                            f1 /= 1.3
                        elif f2<= 95:
                            f1 /= 1.1
                        elif f2< 99.9:
                            f1 /= 1.05
                elif fields[i].datatype=="date":
                    if tempbool["fmtdate"] and tempint["fmtdate"]>0:
                        f2= 100- round(100*tempint["fmtdate"]/tempint["totalinst"],1)
                        if f2<= 50:
                            f1 /= 2
                        elif f2<= 75:
                            f1 /= 1.5
                        elif f2<= 85:
                            f1 /= 1.3
                        elif f2<= 95:
                            f1 /= 1.1
                        elif f2< 99.9:
                            f1 /= 1.05
                elif fields[i].datatype=="string":
                    f1=100 # reset since strings can have any datatype per value
                    if tempbool["fmtstrcase"] and tempint["fmtstrcase"]>0:
                        f2= 100- round(100*tempint["fmtstrcase"]/tempint["totalinst"],1)
                        if f2<= 50:
                            f1 /= 2
                        elif f2<= 75:
                            f1 /= 1.5
                        elif f2<= 85:
                            f1 /= 1.3
                        elif f2<= 95:
                            f1 /= 1.1
                        elif f2< 99.9:
                            f1 /= 1.05
                    if tempbool["fmtstrlen"] and tempint["fmtstrlen"]>0:
                        f2= 100- round(100*tempint["fmtstrlen"]/tempint["totalinst"],1)
                        if f2<= 50:
                            f1 /= 2
                        elif f2<= 75:
                            f1 /= 1.5
                        elif f2<= 85:
                            f1 /= 1.3
                        elif f2<= 95:
                            f1 /= 1.1
                        elif f2< 99.9:
                            f1 /= 1.05

                if tempbool["spchar"] and tempint["spchar"]>0:
                    f2= 100- round(100*tempint["spchar"]/tempint["totalinst"],1)
                    if f2<=  75:
                        f1 *= .85
                    elif f2<= 90:
                        f1 *= .90
                    elif f2< 99:
                        f1 *= .95
                    else:
                        f1 *= .99

                f1 = round(f1,1)
                report.field_quality[i]= str(f1)

    except (RuntimeError, OSError, ValueError, copy.Error) as err:
        report.status="notok:" + str(err)
    return report


def detect_parsing_error(linein:str, field_values:list, report:qualityanalysis.QualityAnalysis, nrec:int) -> str:
    """
    Assess parsed record values in 'field_values' list relative to number fields 
    and collect distribution and note errors in report which is updated here

    linein: original record line before parsing
    field_values: parsed field values in list
    report: QualityAnalysis object passed by reference so is changed in this function. Inbound 
        must have fields property as list of field titles. Results are added to this object's
        rec_parse_dist[], rec_parse_errs[x] x= ('small1', 'small2', 'big', 'small1_recs', 'small2_recs', 'big_recs') 
        with _recs being example lines stored as (nline)linein
    nrec: integer current record number

    Returns: string empty if no problems, notok:message if error, (rec_has_err=true) if parsing error
    """


    n1:int=0
    msg:str=""
    txt:str=""
    rec_has_err:bool=False
    try:
        n1=len(field_values)
        txt=str(n1)
        if txt not in report.rec_parse_dist:
            report.rec_parse_dist[txt]=0
        report.rec_parse_dist[txt] += 1
        if n1<len(report.fields):
            rec_has_err=True
            if n1+1==len(report.fields):
                report.rec_parse_errs["small1"] += 1
                if len(report.rec_parse_errs["small1_recs"])<50:
                    report.rec_parse_errs["small1_recs"].append(f"({nrec}){linein}")
            else:
                report.rec_parse_errs["small2"] += 1
                if len(report.rec_parse_errs["small2_recs"])<50:
                    report.rec_parse_errs["small2_recs"].append(f"({nrec}){linein}")
        elif n1>len(report.fields):
            rec_has_err=True
            report.rec_parse_errs["big"] += 1
            if len(report.rec_parse_errs["big_recs"])<50:
                report.rec_parse_errs["big_recs"].append(f"({nrec}){linein}")
        if rec_has_err:
            msg="(rec_has_err=true)"
    except (RuntimeError, OSError, ValueError, copy.Error) as err:
        msg="notok:" + str(err)
    return msg


def qc_fields(linein:str, field_values:list, report:qualityanalysis.QualityAnalysis, nrec:int) -> str:
    """
    Do Quality Control analysis of field values. Report is modified with assessments 
    for datatypes, formats, unique values.

    linein: original record line before parsing
    field_values: parsed field values in list
    report: QualityAnalysis object passed by reference so is changed in this function. Inbound 
        must have fields property as list of field titles. Results are added to this object's
        field_uniqvals[], fields[], err_stats{}, field_datatype_dist[], 
        spec_char_dist[], field_quality[], spec_char_examples[] with latter stored as 
        (nline)[comma delimited field:spchar pairs found in this record]linein with nline being the line number read 
        (excluding empty and comments lines) and is therefore 1 larger than the line's index 
        in the Python list (i.e. nline is 1 based while lists are 0-based).
    nrec: integer current record number
    
    Returns: string empty if no problems, notok:message if error, 
        possibly (rec_has_fmt_err=true) and/or (rec_has_dt_err=true)
    """

    txt:str=""
    msg:str=""
    fldval:str=""
    fldname:str=""
    fld_has_fmt_err:bool=False
    rec_has_dt_err:bool=False
    rec_has_fmt_err:bool=False
    is_fld_empty:bool=False
    spec_chars:list=[]
    err_dt_flds:list=[]
    err_fmt_flds:list=[]
    try:
        for jloop in range(len(report.fields)):
            fld_has_fmt_err=False
            is_fld_empty=False
            fldval=""
            fldname= report.field_names_lower[jloop]
            if jloop< len(field_values):
                fldval= field_values[jloop]
            if len(fldval)==0:
                txt="-empty-"
                is_fld_empty=True
            elif not report.is_case_sens:
                txt=fldval.lower()
            else:
                txt=fldval

            # unique value counts
            if txt not in report.field_uniqvals[jloop] and len(report.field_uniqvals[jloop])>= report.maxuv:
                txt="-other-"
            if txt not in report.field_uniqvals[jloop]:
                report.field_uniqvals[jloop][txt]=0
            report.field_uniqvals[jloop][txt] += 1

            # special chars
            if len(fldval)>0:
                for kloop in range(len(fldval)):
                    txt=""
                    n1=ord(fldval[kloop:kloop+1])
                    if n1==9:
                        txt="tab"
                    elif n1==33:
                        txt="!"
                    elif n1==34:
                        txt="doublequote"
                    elif n1==35:
                        txt="#"
                    elif n1==60:
                        txt="<"
                    elif n1==62:
                        txt=">"
                    elif n1==91:
                        txt="["
                    elif n1==92:
                        txt="backslash"
                    elif n1==93:
                        txt="]"
                    elif n1==94:
                        txt="^"
                    elif n1==123:
                        txt="{"
                    elif n1==125:
                        txt="}"
                    elif n1==126:
                        txt="~"
                    elif n1<=31 or 127 <= n1 <=255:
                        txt= "ascii_" + str(n1)
                    elif 256 <= n1 <= 65535:
                        txt= "unicode_" + str(n1)

                    if len(txt)>0:
                        spec_chars.append(report.fields[jloop].title +":"+txt)
                        if txt not in report.spec_char_dist:
                            report.spec_char_dist[txt]=0
                        report.spec_char_dist[txt] += 1
                        if txt not in report.spec_char_dist_field[jloop]:
                            report.spec_char_dist_field[jloop][txt]=0
                        report.spec_char_dist_field[jloop][txt] += 1

            if is_fld_empty:
                report.field_datatype_dist[jloop]["empty"] += 1

            # check for datatype errors
            if len(report.fields[jloop].datatype)>0:
                txt=""
                if report.fields[jloop].datatype=="int":
                    if is_fld_empty:
                        txt="false:empty"
                    else:
                        txt=numfuncs.is_int_get(fldval,"string")
                elif report.fields[jloop].datatype=="real":
                    if is_fld_empty:
                        txt="false:empty"
                    else:
                        txt=numfuncs.is_real_get(fldval,"string")
                elif report.fields[jloop].datatype=="bool":
                    if is_fld_empty:
                        txt="false:empty"
                    elif fldval.lower() not in ["true","false"]:
                        txt="false:not true/false"
                if txt.startswith("false"):
                    reason=""
                    if txt.startswith("false:"):
                        reason= txt[txt.find(":")+1:]
                    rec_has_dt_err=True
                    if fldname not in report.err_stats["fields_err_datatype"]:
                        report.err_stats["fields_err_datatype"][fldname]={'count':0,'reasons':{}}
                    report.err_stats["fields_err_datatype"][fldname]["count"] += 1
                    if len(reason)>0:
                        if reason not in report.err_stats["fields_err_datatype"][fldname]["reasons"]:
                            report.err_stats["fields_err_datatype"][fldname]["reasons"][reason]=0
                        report.err_stats["fields_err_datatype"][fldname]["reasons"][reason] += 1
                        txt= fldval if not is_fld_empty else "-empty-"
                        err_dt_flds.append(f"[{fldname}:{reason}:{txt}]")
                    # detect datatype
                    if not is_fld_empty:
                        txt= recfuncs.detect_datatype(fldval)
                        if not txt.startswith("notok:") and len(txt)>0 and txt in report.field_datatype_dist[jloop]:
                            report.field_datatype_dist[jloop][txt] +=1
                else:
                    if report.fields[jloop].datatype=="int":
                        report.field_datatype_dist[jloop]["int"] += 1
                    elif report.fields[jloop].datatype=="real":
                        report.field_datatype_dist[jloop]["real"] += 1
                    elif report.fields[jloop].datatype=="date":
                        report.field_datatype_dist[jloop]["date"] += 1
                    elif report.fields[jloop].datatype=="bool":
                        report.field_datatype_dist[jloop]["bool"] += 1
                    elif report.fields[jloop].datatype=="string":
                        report.field_datatype_dist[jloop]["string"] += 1
            elif not is_fld_empty:
                txt= recfuncs.detect_datatype(fldval)
                if txt.startswith("notok:"):
                    raise ValueError(txt[6:])
                if len(txt)==0:
                    raise ValueError("no datatype returned for fldval=" + fldval)
                if txt in report.field_datatype_dist[jloop]:
                    report.field_datatype_dist[jloop][txt] +=1
                else:
                    raise ValueError("datatype returned not known: " + txt + ", fldval=" + fldval)

            # check format
            if len(report.fields[jloop].datatype)>0:
                reason=""
                if report.fields[jloop].datatype=="string":
                    if report.fields[jloop].fmt_strcase=="upper" and not fldval.isupper():
                        fld_has_fmt_err=True
                        reason="string not uppercase"
                    elif report.fields[jloop].fmt_strcase=="lower" and not fldval.islower():
                        fld_has_fmt_err=True
                        reason="string not lowercase"

                    if report.fields[jloop].fmt_strlen>0 and len(fldval) != report.fields[jloop].fmt_strlen:
                        fld_has_fmt_err=True
                        reason="string incorrect length"
                elif report.fields[jloop].datatype=="real":
                    if report.fields[jloop].fmt_decimal>=0:
                        txt=""
                        if "." in fldval:
                            txt= fldval[(fldval.find(".")+1):]
                        if len(txt) != report.fields[jloop].fmt_decimal:
                            fld_has_fmt_err=True
                            reason="real incorrect decimals"
                elif report.fields[jloop].datatype=="date":
                    if len(report.fields[jloop].fmt_date)>0:
                        if len(fldval)==0:
                            fld_has_fmt_err=True
                            reason="date empty"
                        elif not datefuncs.is_date_format(fldval, report.fields[jloop].fmt_date):
                            fld_has_fmt_err=True
                            reason="date incorrect format"
                if fld_has_fmt_err:
                    rec_has_fmt_err=True
                    if fldname not in report.err_stats["fields_err_fmt"]:
                        report.err_stats["fields_err_fmt"][fldname]={'count':0,'reasons':{}}
                    report.err_stats["fields_err_fmt"][fldname]["count"] += 1
                    if len(reason)>0:
                        if reason not in report.err_stats["fields_err_fmt"][fldname]["reasons"]:
                            report.err_stats["fields_err_fmt"][fldname]["reasons"][reason]=0
                        report.err_stats["fields_err_fmt"][fldname]["reasons"][reason] += 1
                        txt= fldval if not is_fld_empty else "-empty-"
                        err_fmt_flds.append(f"[{fldname}:{reason}:{txt}]")

        if len(spec_chars)>0 and len(report.spec_char_examples)<50:
            txt="["
            for i in range(len(spec_chars)):
                if i>0:
                    txt += ","
                txt += spec_chars[i]
            txt += "]" + linein
            report.spec_char_examples.append(f"({nrec}){txt}")

        msg=""
        if rec_has_fmt_err:
            msg += "(rec_has_fmt_err=true)"
            if len(report.err_fmt_examples)<50 and len(err_fmt_flds)>0:
                report.err_fmt_examples.append(f"({nrec}){'|'.join(err_fmt_flds)}")
        if rec_has_dt_err:
            msg += "(rec_has_dt_err=true)"
            if len(report.err_datatype_examples)<50 and len(err_dt_flds)>0:
                report.err_datatype_examples.append(f"({nrec}){'|'.join(err_dt_flds)}")

    except (RuntimeError, OSError, ValueError, copy.Error) as err:
        msg="notok:" + str(err)
    return msg
