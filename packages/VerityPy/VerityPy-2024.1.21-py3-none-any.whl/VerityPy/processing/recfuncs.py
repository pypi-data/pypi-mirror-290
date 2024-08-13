#!/usr/bin/env python
"""
Record Functions

Various worker functions to process data records.

char_aliases is a dictionary of alias to actual token and allow specifying disruptive 
characters in transforms. For example, -lsquare- is the left square [ character which has special 
meaning in Python and the coded data strings used within the classes and therefore 
cannot be included within a simple string value. In this case, use -lsquare- which 
will be interpreted and replaced in processing. 
"""

__all__ = ['delim_get_char',
           'split_quoted_line',
           'convert_special_notation',
           'convert_char_aliases',
           'is_math_alias',
           'get_math_alias',
           'is_field_its_datatype',
           'is_field_its_format',
           'char_aliases',
           'char_aliases_reverse',
            ]

__version__ = '1.1'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240804'

import math
from VerityPy.processing import datefuncs, numfuncs, field

DQ:str="\""
LF:str="\n"
LCURLY:str="{"
RCURLY:str="}"
LSQUARE:str="["
RSQUARE:str="]"
COMMA:str=","

char_aliases = {"-comma-": ",",
                "-space-":" ",
                "-tab-": "\t",
                "-pipe-": "|",
                "-bslash-": "\\",
                "-fslash-": "/",
                "-lparen-": "(",
                "-rparen-": ")",
                "-lcurly-": "{",
                "-rcurly-": "}",
                "-lsquare-": "[",
                "-rsquare-": "]",
                "-mathpi-": str(math.pi),
                "-mathe-": str(math.e),
                "-dblquote-":"\""
               }

char_aliases_reverse = {",":"-comma-",
                "\t":"-tab-",
                "|":"-pipe-",
                "\\":"-bslash-",
                "/":"-fslash-",
                "(":"-lparen-",
                ")":"-rparen-",
                "{":"-lcurly-",
                "}":"-rcurly-",
                "[":"-lsquare-",
                "]":"-rsquare-",
                "\"":"-dblquote-"
               }

def convert_char_aliases(strin:str) -> str:
    """
    Finds and converts character aliases in a string such as -comma- to ,
    Returns new string. Starts with notok: if error occurs
    """

    result:str=""
    try:
        result=strin
        for k,v in char_aliases.items():
            if k in result:
                result=result.replace(k, v)
    except (RuntimeError,ValueError,OSError) as err:
        result="notok:" + str(err)
    return result

def extract_char_aliases(strin:str,ignore:list) -> str:
    """
    Finds and converts troublesome characters into aliases in a string
    ignore: list of characters to not extract such as ["|",","]
    Returns new string. Starts with notok: if error occurs
    """

    result:str=""
    try:
        result=strin
        if ignore is None:
            ignore=[]
        for k,v in char_aliases_reverse.items():
            if k not in ignore and k in result:
                result=result.replace(k, v)
    except (RuntimeError,ValueError,OSError) as err:
        result="notok:" + str(err)
    return result

def is_math_alias(valnum:str) -> bool:
    """
    Checks if string is -mathpi- or -mathe-
    Returns bool
    """

    result:bool=False
    try :
        if valnum.lower() in ["-mathpi-","-mathe-"]:
            result=True
    except (RuntimeError, ValueError):
        result=False
    return result

def get_math_alias(valnum:str) -> str:
    """
    Checks if string is -mathpi- or -mathe-
    
    Returns string of Python value math.pi or math.e if string is -mathpi- or -mathe- which are Verity aliases. 
    Otherwise, returns original string unless error in which case starts with notok:reason
    """

    result:str=""
    try :
        if valnum.lower() in ["-mathpi-","-mathe-"]:
            valnum=valnum.lower()
            if valnum=="-mathpi-":
                result= str(math.pi)
            elif valnum=="-mathe-":
                result= str(math.e)
        else:
            result=valnum
    except (RuntimeError, ValueError) as err:
        result="notok:" + str(err)
    return result

def delim_get_char(delimin:str) -> str:
    """
    Converts name of delim into its character

    Delim can be words or char for: comma, pipe, tab, colon, caret, hyphen to become 
    char (, | \t : ^ -) . If not one of these then return is 'false:xxx'
    """

    delim_char:str=""
    delim:str=""
    try:
        delim= delimin.strip()
        if len(delim)==0:
            raise ValueError("delim is empty")
        delim=delim.lower()
        if delim in ("comma",","):
            delim_char=","
        elif delim in ("pipe","|"):
            delim_char="|"
        elif delim in("tab","\t"):
            delim_char="\t"
        elif delim==("colon",":"):
            delim_char=":"
        elif delim==("caret","^"):
            delim_char="^"
        elif delim==("hyphen","-"):
            delim_char="-"
        else:
            raise ValueError("unknown delim")
    except (ValueError,RuntimeError) as err:
        delim_char= "false:" + str(err)
    return delim_char

def convert_special_notation(strin:str) -> str:
    """
    Convert VerityX special notation

    Converts the VerityX product special notations into their mapped 
    strings. Returns decoded string or original value if not matched
    
    Notations:
    -comma-    ->  ,
    -tab-      ->  \t
    -space-    ->   
    -pipe-     ->  |
    -bslash-   ->  \\
    -fslash-   ->  /
    -lparen-   ->  (
    -rparen-   ->  )
    -lcurly-   ->  {
    -rcurly-   ->  }
    -lsquare-  ->  [
    -rsquare-  ->  ]
    -mathpi-   ->  math.pi value
    -mathe-    ->  math.e value
    -crlf-     ->  \r\n
    -lf-       ->  \n
    """

    str_out:str=""
    str_in:str=""
    try:
        str_in= strin.strip().lower()
        if len(str_in)==0:
            raise ValueError("str_in is empty")
        if str_in== "-comma-":
            str_out=","
        elif str_in== "-tab-":
            str_out="\t"
        elif str_in== "-space-":
            str_out=" "
        elif str_in== "-pipe-":
            str_out="|"
        elif str_in== "-bslash-":
            str_out="\\"
        elif str_in== "-fslash-":
            str_out="/"
        elif str_in== "-lparen-":
            str_out="("
        elif str_in== "-rparen-":
            str_out=")"
        elif str_in== "-lcurly-":
            str_out="{"
        elif str_in== "-rcurly-":
            str_out="}"
        elif str_in== "-lsquare-":
            str_out="["
        elif str_in== "-rsquare-":
            str_out="]"
        elif str_in== "-mathpi-":
            str_out= str(math.pi)
        elif str_in== "-mathe-":
            str_out= str(math.e)
        elif str_in== "-crlf-":
            str_out= "\r\n"
        elif str_in== "-lf-":
            str_out= "\n"
        else:
            raise ValueError("unknown notation: " + str_in)
    except (RuntimeError,ValueError):
        str_out= strin
    return str_out

def split_quoted_line(line_in:str,delim:str) -> list:
    """
    Decompose quoted record line. 
    line_in: string data record
    delim: name of delimiter (comma, pipe, tab, colon)
    Returns list of parsed values. If error, 0th entry starts with notok:
    """

    delim_char:str=""
    out_rec:list=[]
    cur_line:str
    cur_str:str
    dq:str= "\""
    dq_delim:str
    nqf:int
    nqb:int
    ndelim:int
    nqdelim:int
    has_last:bool=False
    try:
        if len(line_in)==0:
            return out_rec
        if len(delim)>1:
            delim_char= delim_get_char(delim)
        else:
            delim_char=delim
        if len(delim_char)==0 or delim_char.startswith("notok:"):
            raise ValueError("incorrect delim:" + delim)
        dq_delim= dq + delim_char
        cur_line=line_in
        while len(cur_line)>0:
            nqf=-1
            nqb=-1
            ndelim=-1
            nqdelim=-1
            nqf= cur_line.find(dq)
            cur_str=""
            if -1 < nqf < len(cur_line)-1:
                nqb= cur_line.find(dq,nqf+1)
            if delim_char in cur_line:
                ndelim= cur_line.find(delim_char)
                nqdelim= cur_line.find(dq_delim)
            if ndelim==0:
                if cur_line==delim_char:
                    has_last=True
                    cur_line=""
                elif len(cur_line)> 0:
                    cur_line= cur_line[1:]
                else:
                    cur_line=""
            elif nqf<0:
                if ndelim<0:
                    cur_str=cur_line
                    cur_line=""
                elif ndelim==len(cur_line)-1:
                    cur_str=cur_line[:ndelim]
                    has_last=True
                    cur_line=""
                else:
                    cur_str=cur_line[:ndelim]
                    cur_line=cur_line[ndelim+1:]
            elif nqf>=0:
                if 0< ndelim <nqf:
                    cur_str=cur_line[:ndelim]
                    cur_line=cur_line[ndelim+1:]
                elif nqb> nqf:
                    if nqdelim>= nqb:
                        # intermediate quotes within fld
                        cur_str=cur_line[nqf:nqdelim]
                        cur_line=cur_line[nqdelim+2:] # remove quote and delim (1 char delim)
                        if len(cur_line)==0:
                            has_last=True
                    elif nqdelim==nqf:
                        # missing leading quote so 1st instance is actual end of fld
                        cur_str=cur_line[:nqdelim]
                        cur_line=cur_line[nqdelim+2:]
                    else:
                        cur_str=cur_line[nqf:nqb]
                        cur_line=cur_line[nqb+1:]
                elif ndelim>nqf:
                    # assume errant quote
                    cur_str=cur_line[:ndelim]
                    cur_line=cur_line[ndelim+1:]
                else:
                    cur_str=cur_line[nqf+1:]
                    cur_line=""
                if dq in cur_str:
                    cur_str=cur_str.replace(dq,'')
            else:
                cur_str=cur_line
                cur_line=""
                if dq in cur_str:
                    cur_str=cur_str.replace(dq,'')

            out_rec.append(cur_str)
            if has_last:
                out_rec.append("")
                break
    except (RuntimeError,ValueError) as err:
        out_rec.clear()
        out_rec.append("notok:" + str(err))
    return out_rec

def detect_datatype(strin:str) -> str:
    """
    Detect Value Datatype

    Detect a value's data type by looking for known patterns of 
    characters and evaluating likely datatype.
    Returns datatype or starts with notok: if error
    """

    txt:str=""
    txt1:str=""
    txt2:str=""
    dtype:str=""
    try:
        if strin is None:
            raise ValueError("no value supplied")
        strin=strin.lower().strip()
        if len(strin)==0:
            return dtype
        if strin in ["true", "false"]:
            dtype="bool"
        elif strin in ["0", "-0"]:
            dtype="int"
        elif strin.startswith("00"):
            dtype="string"
        elif any(x in strin for x in ["e+","e-","e"]):
            txt= numfuncs.get_value_from_suspect_exp(strin)
            if len(txt)>0 and txt!=strin and not txt.startswith("notok:"):
                if "." in txt:
                    dtype="real"
                else:
                    dtype="int"
            else:
                dtype="string"
        elif 8<= len(strin) <=30 and ("/" in strin or "-" in strin):
            if strin.startswith("/") or strin.startswith("-"):
                dtype="string"
            else:
                txt=strin
                txt1=""
                if "t" in txt:
                    txt1=txt[txt.find("t")+1:].strip()
                    txt=txt[:txt.find("t")].strip()
                if 6> len(txt) >=50:
                    dtype="string"
                else:
                    txt2= datefuncs.convert_date_to_iso(txt,"",True)
                    if txt2.startswith("notok:") or len(txt2)<8:
                        dtype="string"
                    elif txt2.startswith("00"):
                        dtype="string"
                    elif txt2[4:6]=="00" or txt2[6:8]=="00":
                        dtype="string"
                    elif txt2.endswith(")") and "(" in txt2:
                        txt2=txt2[txt2.find("(")+1:-1]
                        if len(txt2)>=4:
                            if len(txt1)>0:
                                if ":" in txt1:
                                    txt1=txt1.replace(":","")
                                if "+" in txt1:
                                    txt1=txt1[:txt1.find("+")].strip()
                                elif "-" in txt1:
                                    txt1=txt1[:txt1.find("-")].strip()
                                elif " " in txt1:
                                    txt1=txt1[:txt1.find(" ")].strip()
                                if len(txt1)>0 and numfuncs.is_real(txt1):
                                    dtype="date"
                                else:
                                    dtype="string"
                            else:
                                dtype="date"
                        else:
                            dtype="string"
                    else:
                        dtype="string"
        elif "." in strin and len(strin)>1:
            if strin.startswith("."):
                txt= strin[1:]
                if "." not in txt and numfuncs.is_real(txt):
                    dtype="real"
                else:
                    dtype="string"
            elif numfuncs.is_real(strin):
                dtype="real"
            else:
                dtype="string"
        elif numfuncs.is_int(strin):
            dtype="int"
        else:
            dtype="string"

    except (RuntimeError,OSError, ValueError) as err:
        dtype="notok:" + str(err)
    return dtype

def assign_datatype_to_fields(datatype_dist_fields:list, settings:dict) -> list:
    """
    Uses list of distribution of detected datatypes for each fld to determine the most likely 
    datatype appropriate to assign to it. This uses threshhold settings and knowledge from 
    curated data sets across multiple domains and data systems.

    datatype_dist_fields: list of dict objects with keys [string, int, real, date, bool, empty] 
        and for each values = number of instances for each fld. 
        This should come from results of analyzequality.do_qualityinspect()
    settings: dict with keys for various settings including
        - include_empty: bool whether to include number of empty values in statistical calculation. Default is True
        - minfrac: real number minimum threshhold in either percentage (any value great than 1) or fraction (0-1). Default is 0.75
    
    returns: string list with datatypes (string, int, real, date, bool) per fld (or empty if cannot be determined). 
        0th entry will start with notok: if an error occurs
    """

    field_dtypes:list=[]
    try:
        if datatype_dist_fields is None or not isinstance(datatype_dist_fields, list) or len(datatype_dist_fields)==0:
            raise ValueError("datatype_dist_fields is not a list")
        for i in range(len(datatype_dist_fields)):
            if datatype_dist_fields[i] is None or not isinstance(datatype_dist_fields[i], dict):
                raise ValueError("datatype_dist at index " + str(i) + " is not a dict")
            elif "int" not in datatype_dist_fields[i] or not isinstance(datatype_dist_fields[i]["int"], int):
                raise ValueError("datatype_dist at index " + str(i) + " missing int key")
            elif "real" not in datatype_dist_fields[i] or not isinstance(datatype_dist_fields[i]["real"], int):
                raise ValueError("datatype_dist at index " + str(i) + " missing real key")
            elif "bool" not in datatype_dist_fields[i] or not isinstance(datatype_dist_fields[i]["bool"], int):
                raise ValueError("datatype_dist at index " + str(i) + " missing bool key")
            elif "date" not in datatype_dist_fields[i] or not isinstance(datatype_dist_fields[i]["date"], int):
                raise ValueError("datatype_dist at index " + str(i) + " missing date key")
            elif "string" not in datatype_dist_fields[i] or not isinstance(datatype_dist_fields[i]["string"], int):
                raise ValueError("datatype_dist at index " + str(i) + " missing string key")
            elif "empty" not in datatype_dist_fields[i] or not isinstance(datatype_dist_fields[i]["empty"], int):
                raise ValueError("datatype_dist at index " + str(i) + " missing empty key")
        for i in range(len(datatype_dist_fields)):
            field_dtypes.append(assign_datatype(datatype_dist_fields[i],settings))
    except (RuntimeError, OSError, ValueError) as err:
        field_dtypes.insert(0,"notok:" + str(err))
    return field_dtypes

def assign_datatype(datatype_dist:dict, settings:dict) -> str:
    """
    Uses distribution of detected datatypes for a fld to determine the most likely 
    datatype appropriate to assign to it. This uses threshhold settings and knowledge from 
    curated data sets across multiple domains and data systems.

    datatype_dist: dict object with keys [string, int, real, date, bool, empty]
        and for each values = number of instances. This should come from results of analyzequality.do_qualityinspect()
    settings: dict with keys for various settings including
        - include_empty: bool whether to include number of empty values in statistical calculation. Default is True
        - minfrac: real number minimum threshhold in either percentage (any value great than 1) or fraction (0-1). Default is 0.75
    
    returns: string with datatype (string, int, real, date, bool) or empty if cannot be determined. will start with notok: if an error occurs
    """

    dtype:str=""
    dint:float=0
    dreal:float=0
    dbool:float=0
    ddate:float=0
    dstr:float=0
    dempty:float=0
    ntotal:int=0
    ntotal_not_empty:int=0
    dmin:float=0
    dmax_count:float=0
    minfrac:float=.75
    inc_empty:bool=True
    dt_max:str=""
    try:
        if datatype_dist is None or not isinstance(datatype_dist, dict):
            raise ValueError("datatype_dist is not a dict")
        if not settings is None and isinstance(settings, dict):
            if "include_empty" in settings and settings["include_empty"].lower() =="false":
                inc_empty=False
            if "minfrac" in settings:
                minfrac= numfuncs.is_real_get(settings["minfrac"],"number")
                if 1< minfrac <= 100:
                    minfrac /= 100
                elif 0>= minfrac or minfrac>100:
                    minfrac=.75
        if "int" not in datatype_dist or not isinstance(datatype_dist["int"], int):
            raise ValueError("datatype_dist missing int key")
        elif "real" not in datatype_dist or not isinstance(datatype_dist["real"], int):
            raise ValueError("datatype_dist missing real key")
        elif "bool" not in datatype_dist or not isinstance(datatype_dist["bool"], int):
            raise ValueError("datatype_dist missing bool key")
        elif "date" not in datatype_dist or not isinstance(datatype_dist["date"], int):
            raise ValueError("datatype_dist missing date key")
        elif "string" not in datatype_dist or not isinstance(datatype_dist["string"], int):
            raise ValueError("datatype_dist missing string key")
        elif "empty" not in datatype_dist or not isinstance(datatype_dist["empty"], int):
            raise ValueError("datatype_dist missing empty key")
        dint=datatype_dist["int"] if datatype_dist["int"]>0 else 0
        dreal=datatype_dist["real"] if datatype_dist["real"]>0 else 0
        dbool=datatype_dist["bool"] if datatype_dist["bool"]>0 else 0
        ddate=datatype_dist["date"] if datatype_dist["date"]>0 else 0
        dstr=datatype_dist["string"] if datatype_dist["string"]>0 else 0
        dempty=datatype_dist["empty"] if datatype_dist["empty"]>0 else 0
        ntotal_not_empty= dint + dreal + dbool + ddate + dstr
        ntotal= ntotal_not_empty + dempty
        if ntotal==0:
            raise ValueError("no counts of any datatype")

        if inc_empty:
            dmin = math.floor(minfrac * ntotal)
            if dempty>=dmax_count:
                dmax_count=dempty
                dt_max="empty"
        else:
            if ntotal_not_empty==0:
                raise ValueError("no counts of any datatype excluding empty values")
            dmin = math.floor(minfrac * ntotal_not_empty)

        if dint>=dmax_count:
            dmax_count=dint
            dt_max="int"
        if dreal>=dmax_count:
            dmax_count=dreal
            dt_max="real"
        if dbool>=dmax_count:
            dmax_count=dbool
            dt_max="bool"
        if ddate>=dmax_count:
            dmax_count=ddate
            dt_max="date"
        if dstr>=dmax_count:
            dmax_count=dstr
            dt_max="string"
        if dmax_count<dmin:
            # no single type above min so try combining int and real
            if (dint + dreal)>= dmin:
                dt_max="real"
                dmax_count= dint + dreal
        if dmax_count<dmin and inc_empty:
            # still no clear datatype so combine date and string
            if (ddate + dempty)>= dmin:
                dt_max="date"
                dmax_count= ddate + dempty
        if dmax_count<dmin and inc_empty:
            # still no clear datatype so combine empty and string
            if (dstr + dempty)>= dmin:
                dt_max="string"
                dmax_count= dstr + dempty
        if dmax_count>=dmin:
            dtype= dt_max
    except (RuntimeError,OSError, ValueError) as err:
        dtype="notok:" + str(err)
    return dtype


def is_field_its_datatype(dtype:str, fieldval:str, datefmt:str="")->bool:
    """IsFieldItsDatatype
    Determines if a field's value is in its specified datatype

	dtype: field's defined datatype (int, real, bool, date, string)
	fieldval: field value
	datefmt: date format if checking for a date
	returns: bool
    """

    result:bool=False
    try:
        if dtype is None or fieldval is None:
            raise ValueError("missing dtype or fieldval since = None")
        dtype=dtype.lower()
        if len(dtype)==0:
            return True
        if dtype=="real":
            if numfuncs.is_real(fieldval):
                result=True
        elif dtype=="int":
            if numfuncs.is_int(fieldval):
                result=True
        elif dtype.startswith("date"):
            if len(fieldval)==0:
                result=False
            elif dtype=="datetime":
                result= datefuncs.is_iso_date_str(fieldval, True).startswith("true")
            elif datefmt=="iso":
                result= datefuncs.is_iso_date_str(fieldval, False).startswith("true")
            else:
                result= datefuncs.is_date_format(fieldval, datefmt)
        elif dtype=="bool":
            result = fieldval.lower() in ("true","false")
        elif dtype=="string":
            result= True
    except (OSError, RuntimeError, ValueError) as err:
        result=False
        print("ERROR:" + str(err) + "\n")
    return result


def is_field_its_format(fieldval:str, fld:field.Field, allow_empty:bool=False)->str:
    """IsFieldItsFormat
    Determines if field value conforms to its defined format (if set)

    fieldVal: field value to check
	fld: Field Object
	allow_empty: bool whether empty values (e.g null) are allowed
	returns: string as bool:message with bool =(true,false) and message= reason. If error, starts with notok:message
    """

    result:bool=False
    outmsg:str=""
    msg:str=""
    txt:str=""
    flag:bool=False
    flag1:bool=False
    n1:int=0
    try:
        if fieldval is None:
            raise ValueError("missing fieldval since = None")
        if fld is None:
            raise ValueError("missing field since = None")
        elif not isinstance(fld, field.Field):
            raise ValueError("field is not Field object")
        fld.datatype= fld.datatype.lower()
        fld.fmt_strcase= fld.fmt_strcase.lower()
        if len(fieldval.strip())==0:
            result=allow_empty
            msg="empty"
        elif fld.datatype.startswith("date"):
            if len(fld.fmt_date)>0:
                if is_field_its_datatype(fld.datatype, fieldval, fld.fmt_date):
                    result=True
                else:
                    msg="faildate"
            else:
                msg="missing date format"
        elif fld.datatype=="bool":
            if is_field_its_datatype(fld.datatype, fieldval):
                result=True
            else:
                msg="failbool"
        elif fld.datatype=="string":
            flag=False
            flag1=False
            if fld.fmt_strlen>0 and len(fieldval)!=fld.fmt_strlen:
                flag=True
                msg="faillength(" + str(len(fieldval)) + "/" + str(fld.fmt_strlen) + ")"
            if fld.fmt_strcase in ("upper","lower"):
                if fld.fmt_strcase=="upper":
                    txt= fieldval.upper()
                elif fld.fmt_strcase=="lower":
                    txt= fieldval.lower()
                if txt != fieldval:
                    flag=True
                    if len(msg)>0:
                        msg += ","
                    msg += "failcase(" + fld.fmt_strcase + ")"
            if not flag and not flag1:
                result= True
        elif fld.datatype in ("int","real"):
            if fld.datatype=="int":
                flag= numfuncs.is_int(fieldval)
            else:
                txt= numfuncs.is_real_get(fieldval, "string", False)
                flag= not txt.startswith("false")
            if not flag:
                msg="failnumber"
            elif fld.datatype=="real" and fld.fmt_decimal>0:
                n1=0
                if "." in txt:
                    n1= len(txt)-1 - txt.index(".")
                if n1 != fld.fmt_decimal:
                    msg= "faildecimal(" + str(n1) + "/" + str(fld.fmt_decimal) + ")"
                else:
                    result=True
            else:
                result=True
        outmsg= str(result).lower()
        if len(msg)>0:
            outmsg += ":" + msg
    except (OSError, RuntimeError, ValueError) as err:
        outmsg="notok:" + str(err)
    return outmsg

