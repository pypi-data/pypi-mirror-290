#!/usr/bin/env python
"""
Exec Transform

Process transforms. 
"""

__all__ = ['do_transform']
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240619'


import math
import random
from ..transforms import lookup, transform, optypes
from . import recfuncs, datefuncs, numfuncs


def do_transform(
        transobj: transform.Transform,
        initial_value:str,
        result_datatype:str="",
        hash_fields:dict=None,
        field_values:list=None,
        lookup_dicts:list=None,
        hash_lookup_dicts:dict=None,
        current_record_index:int=0,
        current_field_index:int=-1
        ) -> str:
    """
    Do Transform

    Processes a transform and uses LookUpDicts as needed. For lookups and by 
    reference functions, there must also be passed in dict of field titles (lower case) to index in list. 
    Lookups also require pre-processing the LookUp Dictionaries and passing into this function that list as well 
    as the hash dictionary of the titles.
    
    Inputs:
    transobj: Transform object to be processed
    initial_value: initial value to begin with. This can be empty string.
    result_datatype: optional datatype for final value (int,real,string,date,bool) default is string
    hash_fields: dictionary key=field title lower case, value= array index in fields. This is required for Ref operations that use referenced field_values.
    field_values: list of record values
    lookup_dicts: optional list of LookUpDict objects
    hash_lookup_dicts: dictionary of hashed lookup dict title to index position
    current_record_index: integer index of record for which this transform is being processed. 0-based. If less than 0 it is ignored.
    current_field_index: integer index of field in output record for which this transform is being processed. 0-based. If less than 0 it is ignored.
    
    Return: If error start with notok: otherwise string of result value
    """

    lval: int=0
    lval1: int=0
    dval: float=0
    dval1: float=0
    dval2: float=0
    result: str=""
    str1:str=""
    str2:str=""
    str3:str=""
    fldval:str=""
    fldval2:str=""
    fldval3:str=""
    if_result_true:bool=False
    prior_was_if:bool=False
    stop_now:bool=False
    ismatch:bool
    isnotmatch:bool
    wildf:bool=False
    wildb:bool=False
    isok:bool=False
    doclean:bool=False
    flag:bool
    doclean:bool=False
    param1:str
    param2:str
    param3:str
    oper:str
    nfld:int=-1
    nfld2:int=-1
    nfld3:int=-1
    nidx:int=-1
    nkeys:int=0
    n1:int=-1
    n2:int=-1
    items:list=[]
    str_list:list=[]
    dbl_list:list=[]
    keyand:list=[]
    keynot:list=[]
    lkup:lookup.LookUpDict=lookup.LookUpDict()
    i:int=-1
    try:
        if transobj is None or not isinstance(transobj, transform.Transform):
            raise ValueError("empty transform supplied")
        if initial_value is None:
            raise ValueError("missing initial_value")
        if field_values is None:
            field_values=[]
        if hash_fields is None:
            hash_fields={}
        if lookup_dicts is None:
            lookup_dicts=[]
        if hash_lookup_dicts is None:
            hash_lookup_dicts={}

        random.seed()

        result=initial_value
        result_datatype=result_datatype.lower().strip()
        i=-1
        while i < len(transobj.ops):
            dval=0
            dval1=0
            lval=0
            lval1=0
            param1=""
            param2=""
            param3=""
            oper=""
            stop_now=False
            doclean=False

            i += 1
            if prior_was_if:
                if if_result_true:
                    i += 1 # skip over false
                else:
                    stop_now=True  #  stop after doing current Op since False IF

            prior_was_if= False # reset
            if_result_true= False
            if i>= len(transobj.ops):
                break

            oper= transobj.ops[i].title.lower()
            param1=transobj.ops[i].param1
            param2=transobj.ops[i].param2
            param3=transobj.ops[i].param3

            str1= recfuncs.get_math_alias(result)
            if len(str1)>0 and not str1.startswith("notok:"):
                if not oper.endswith("refs"):
                    if oper.startswith("mult") or oper.startswith("div") or oper.startswith("add") or oper.startswith("subtract"):
                        doclean= param2.lower()!="false"
                    else:
                        doclean=False
                else:
                    doclean= param3.lower()!="false"

                dval= numfuncs.is_real_get(str1, "number", doclean)
                if dval== -999999:
                    dval=0

            if oper.startswith("ifstr") or oper.startswith("ifnotstr"):
                items.clear()
                if len(param1)>0:
                    items= param1.split("|")

            if oper=="noop":
                pass
            elif oper=="settovalue":
                if param1.lower() in recfuncs.char_aliases:
                    result= recfuncs.char_aliases[param1.lower()]
                else:
                    result=param1
            elif oper=="settoindex":
                if len(param1)==0 or (lval := numfuncs.is_int_get(param1, "number", True)) < 0:
                    lval=0 # base index
                lval1 = current_record_index if current_record_index>=0 else 0
                lval += lval1
                result = str(lval)
            elif oper=="settoref":
                param1=param1.lower()
                if param1 in hash_fields:
                    nfld=hash_fields[param1]
                    if nfld<0 or nfld>= len(field_values):
                        result="-novalue-"
                    else:
                        result=recfuncs.get_math_alias(field_values[nfld])
                else:
                    result="-novalue-"
            elif oper=="settorandom":
                flag=False
                if len(param3)>0 and (dval := numfuncs.is_real_get(param3, "number", True)) != -999999:
                    if 0 <= dval <= 1:
                        if random.random()<dval:
                            flag=True
                else:
                    flag=True
                    dval=0
                if flag:
                    if len(param1)==0 or (dval := numfuncs.is_real_get(param1, "number", True)) == -999999:
                        dval=0
                    if len(param2)==0 or (dval2 := numfuncs.is_real_get(param2, "number", True)) == -999999:
                        dval2=0
                    if dval>=dval2:
                        dval2 += 1
                    dval1= random.random() * (dval2-dval) + dval
                    result= str(round(dval1,5))
                else:
                    result=str(9.99e10)
            elif oper=="settofreqlist":
                flag=False
                if len(param1)>0 and len(param2)>0:
                    str_list=param1.split("|")
                    dbl_list.clear()
                    flag=True
                    dval=0
                    for s in str_list:
                        if (dval1 := numfuncs.is_real_get(s, "number", True))!= -999999:
                            dval += dval1
                            dbl_list.append(dval)
                        else:
                            flag=False
                            break
                    if dval==0 or len(dbl_list)==0:
                        flag=False
                    if flag:
                        str_list=param2.split("|")
                        if len(str_list)!=len(dbl_list):
                            flag=False
                        else:
                            for j in range(len(dbl_list)):
                                dbl_list[j] /= dval
                nidx=-1
                if flag:
                    dval=-1
                    if len(param3)>0:
                        if (dval := numfuncs.is_real_get(param3, "number", True))!= -999999:
                            if 0 > dval > 1:
                                dval=1
                        elif param3.lower() in hash_fields:
                            nfld= hash_fields[param3.lower()]
                            str1= recfuncs.get_math_alias(field_values[nfld])
                            if len(str1)>0 and (dval := numfuncs.is_real_get(str1, "number", True))== -999999:
                                dval= -1
                    if 0 > dval > 1:
                        dval= random.random()
                    for j in range(len(dbl_list)):
                        if dval< dbl_list[j]:
                            nidx=j
                            break
                if not flag or nidx<0:
                    result="-notassign-"
                else:
                    result= recfuncs.get_math_alias(str_list[nidx])
            elif oper=="round":
                if (dval := numfuncs.is_real_get(result, "number", True))!= -999999:
                    n1=0
                    if len(param1)>0 and numfuncs.is_int(param1):
                        n1=max(0,int(param1))

                    result= str(round(dval,n1))
                    if result_datatype=="real" and "." not in result:
                        result += ".00"
            elif oper=="floor":
                if (dval := numfuncs.is_real_get(result, "number", True))!= -999999:
                    result= str(math.floor(dval))
                    if result_datatype=="real" and "." not in result:
                        result += ".00"
            elif oper=="ceiling":
                if (dval := numfuncs.is_real_get(result, "number", True))!= -999999:
                    result= str(math.ceil(dval))
                    if result_datatype=="real" and "." not in result:
                        result += ".00"
            elif oper=="cleannumber":
                result= numfuncs.clean_number(result)
            elif oper in ["multbyref","divbyref","addbyref","subtractbyref","divfromref","subtractfromref"]:
                param1=param1.lower()
                doclean= param2.lower()!="false"
                dval1=0
                if param1 in hash_fields:
                    nfld= hash_fields[param1]
                    str1= recfuncs.get_math_alias(field_values[nfld])
                    if doclean:
                        str1= numfuncs.clean_number(str1)
                    if (dval1 := numfuncs.is_real_get(str1, "number", False))== -999999:
                        dval1= 0

                if oper.startswith("mult"):
                    dval *= dval1
                elif oper.startswith("divfrom"):
                    if dval==0:
                        dval= 9.99e10
                    else:
                        dval = dval1/dval
                elif oper.startswith("div"):
                    if dval1==0:
                        dval= 9.99e10
                    else:
                        dval /= dval1
                elif oper.startswith("add"):
                    dval += dval1
                elif oper.startswith("subtractfrom"):
                    dval= dval1- dval
                elif oper.startswith("subtract"):
                    dval -= dval1
                if result_datatype.startswith("int"):
                    result= str(round(dval))
                else:
                    result= str(dval)
            elif oper in ["multrefs","addrefs"]:
                if len(param2)>0:
                    param1 += "," + param2
                param1= param1.lower()
                doclean= param3.lower()!="false"
                str_list= param1.split(",")
                dval=0
                for j in range(len(str_list)):
                    dval1=0
                    str1= str_list[j].lower().strip()
                    if str1 in hash_fields:
                        nfld= hash_fields[str1]
                        str1= recfuncs.get_math_alias(field_values[nfld])
                        if doclean:
                            str1= numfuncs.clean_number(str1)
                        if (dval1 := numfuncs.is_real_get(str1, "number", False))== -999999:
                            dval1= 0
                    if j==0:
                        dval= dval1
                    else:
                        if oper=="multrefs":
                            dval *= dval1
                        elif oper=="addrefs":
                            dval += dval1
                if result_datatype.startswith("int"):
                    result= str(round(dval))
                else:
                    result= str(dval)
            elif oper in ["mult","div","divfrom","add","subtract","subtractfrom"]:
                dval=0
                dval1=0
                doclean= param2.lower()!="false"
                if doclean:
                    result= numfuncs.clean_number(result)
                if (dval := numfuncs.is_real_get(result, "number", False))== -999999:
                    dval= 0
                param1= recfuncs.get_math_alias(param1)
                if doclean:
                    param1= numfuncs.clean_number(param1)
                if (dval1 := numfuncs.is_real_get(param1, "number", False))== -999999:
                    dval1= 0
                if oper=="mult":
                    dval *= dval1
                elif oper=="div":
                    if dval1==0:
                        dval= 9.99e10
                    else:
                        dval /= dval1
                elif oper=="divfrom":
                    if dval1==0:
                        dval= 0
                    elif dval==0:
                        dval= 9.99e10
                    else:
                        dval = dval1/dval
                elif oper=="add":
                    dval += dval1
                elif oper=="subtract":
                    dval -= dval1
                elif oper=="subtractfrom":
                    dval= dval1-dval
                if result_datatype.startswith("int"):
                    result= str(round(dval))
                else:
                    result= str(dval)
            elif oper in ["abs","negate"]:
                if result_datatype.startswith("int"):
                    lval=0
                    if (lval := numfuncs.is_int_get(result, "number", True))== -999999:
                        lval= 0
                        if (dval := numfuncs.is_real_get(result, "number", True))!= -999999:
                            lval= math.floor(dval)

                    if oper=="abs":
                        lval= abs(lval)
                    elif oper=="negate":
                        lval *= -1
                    result= str(lval)
                else:
                    if (dval := numfuncs.is_real_get(result, "number", True))== -999999:
                        dval=0
                    if oper=="abs":
                        dval= abs(dval)
                    elif oper=="negate":
                        dval *= -1
                    result= str(dval)
            elif oper in ["log","ln"]:
                dval=0
                if (dval := numfuncs.is_real_get(result, "number", True))== -999999:
                    dval=0
                if dval>0:
                    if oper=="log":
                        dval1= math.log10(dval)
                    elif oper=="ln":
                        dval1= math.log(dval)
                else:
                    dval1= -10e6
                if result_datatype.startswith("int"):
                    lval= math.floor(dval1)
                    result= str(lval)
                else:
                    result= str(dval1)
            elif oper in ["pow10","powe"]:
                dval=0
                if (dval := numfuncs.is_real_get(result, "number", True))== -999999:
                    dval=0
                if dval==0:
                    result="1"
                else:
                    if oper=="pow10":
                        dval= pow(10,dval)
                    else:
                        dval= math.exp(dval)
                    result= str(dval)
            elif oper=="setdecimal":
                n1=result.find(".")
                if n1==0:
                    str1=result[1:]
                    result=""
                elif n1>0:
                    str1=result[n1+1:]
                    result=result[:n1]
                else:
                    str1=""
                n1=-1
                if numfuncs.is_int(param1):
                    n1=int(param1)
                n1= max(n1,0)
                if n1>0:
                    n2=len(str1)
                    if n1>n2:
                        for j in range(n1-n2):
                            str1 += "0"
                    elif n1<n2:
                        str1=str1[:n1]
                    result += "." + str1
            elif oper=="trim":
                result=result.strip()
            elif oper=="ltrim":
                result=result.lstrip()
            elif oper=="rtrim":
                result=result.rstrip()
            elif oper=="tolower":
                result=result.lower()
            elif oper=="toupper":
                result=result.upper()
            elif oper=="totitle":
                result=result.capwords()
            elif oper in ["front","end","back","before","after"]:
                if len(param1)>0:
                    str1= recfuncs.convert_char_aliases(param1).lower()
                    n1= result.lower().find(str1)
                    if n1>=0:
                        n2= len(str1)
                        if oper=="front":
                            result= result[:(n1+n2)]
                        elif oper in ("end","back"):
                            result=result[n1:]
                        elif oper=="before":
                            result=result[:n1]
                        elif oper=="after":
                            result=result[(n1+n2):]
            elif oper in ("frontn","endn", "backn"):
                if numfuncs.is_int(param1):
                    n1=int(param1)
                    if 0< n1 < len(result):
                        if oper=="frontn":
                            result= result[:n1]
                        elif oper in ("endn","backn"):
                            result=result[(len(result)-n1):]
            elif oper=="mid":
                str1= recfuncs.convert_char_aliases(param1)
                str2= recfuncs.convert_char_aliases(param2)
                n1= result.lower().find(str1.lower())
                if 0< n1 < len(result):
                    result=result[n1:]
                if len(str2)>0:
                    n1= result.lower().find(str2.lower())
                    if 0< n1 < len(result):
                        result=result[:n1]
            elif oper=="midn":
                if numfuncs.is_int(param1):
                    n1=int(param1)
                    if 0< n1 < len(result):
                        result=result[n1:]
                        if numfuncs.is_int(param2):
                            n2=int(param2)
                            if 0< n2 < len(result):
                                result=result[:n2]
            elif oper=="charat":
                if numfuncs.is_int(param1):
                    n1=int(param1)
                    if 0< n1 < len(result):
                        result=result[n1:n1+1]
            elif oper=="setlength":
                n1=-1
                if numfuncs.is_int(param1):
                    n1=int(param1)
                param2=param2.lower()
                if n1>0:
                    if "left" in param2 or "front" in param2:
                        str1="left"
                    else:
                        str1="right"
                    str2= recfuncs.convert_char_aliases(param3)
                    if len(str2)==0:
                        str2="x"
                    elif len(str2)>1:
                        str2=str2[:1]
                    if n1< len(result):
                        if str1=="left":
                            result= result[(len(result)-n1):]
                        else:
                            result=result[:n1]
                    elif n1>len(result):
                        n2=n1-len(result)
                        for j in range(n2):
                            if str1=="left":
                                result = str2 + result
                            else:
                                result += str2
            elif oper=="prepend":
                str1= recfuncs.convert_char_aliases(param1)
                result = str1 + result
            elif oper=="append":
                str1= recfuncs.convert_char_aliases(param1)
                result += str1
            elif oper=="remove":
                str2= recfuncs.convert_char_aliases(param1).lower()
                str1=result.lower()
                n1= str1.find(str2)
                while n1>=0:
                    if n1==0:
                        result=result[len(str2):]
                    elif n1==len(result)-len(str2):
                        result=result[:-len(str2)]
                    else:
                        str1=result[:n1]
                        result=result[(n1+len(str2)):]
                        result= str1 + result
                    str1=result.lower()
                    n1= str1.find(str2)
            elif oper=="replace":
                str2= recfuncs.convert_char_aliases(param1).lower()
                str3= recfuncs.convert_char_aliases(param2)
                if str2 != str3.lower():
                    str1=result.lower()
                    n1= str1.find(str2)
                    while n1>=0:
                        if n1==0:
                            result=result[len(str2):] + str3
                        elif n1==len(result)-len(str2):
                            result=result[:-len(str2)] + str3
                        else:
                            str1=result[:n1]
                            result=result[(n1+len(str2)):]
                            result= str1 + str3 + result
                        str1=result.lower()
                        n1= str1.find(str2)
            elif oper=="exceldatenumbertoiso":
                result= datefuncs.convert_excel_date_to_iso(result)
            elif oper=="datetoiso":
                result= datefuncs.convert_date_to_iso(result, param1)
            elif oper=="settoisodate":
                param1=param1.lower().strip()
                flag=False
                if param1 in ["today","now",""]:
                    if param1=="now":
                        flag=True
                    result= datefuncs.get_current_iso_datetime(flag, param2)
                else:
                    if "t" in param1:
                        flag=True
                    str1= datefuncs.is_iso_date_str(param1,flag)
                    if str1.startswith("true"):
                        if ":" in str1:
                            result=str1[str1.find(":")+1:]
                        else:
                            result=param1
                    else:
                        result=""
            elif oper=="convertmainframenumber":
                result= numfuncs.convert_mainframe(result)
            elif oper=="convertfromexp":
                result= numfuncs.get_value_from_suspect_exp(result)
            elif oper.startswith(("ifgte","ifgt","iflte","iflt","ifnotgte","ifnotgt","ifnotlte","ifnotlt","ifeq","ifnoteq")):
                # includes byref
                prior_was_if=True
                if_result_true=False
                param1=param1.lower()
                dval1=0
                if oper.endswith("ref"):
                    if len(param1)==0:
                        raise ValueError("missing reference field title in: " + oper)
                    if param1 in hash_fields:
                        nfld= hash_fields[param1]
                        str1= recfuncs.get_math_alias(field_values[nfld])
                        if (dval1 := numfuncs.is_real_get(str1, "number", True))== -999999:
                            dval1=0
                    else:
                        raise ValueError("reference field title not in fields: " + param1 + ", oper=" + oper)
                    oper=oper[:-3]
                else:
                    str1= recfuncs.get_math_alias(param1)
                    if (dval1 := numfuncs.is_real_get(str1, "number", True))== -999999:
                        dval1=0
                # dval set at start of next index in Ops loop
                if oper in ["ifgte","ifnotgte"]:
                    if dval >= dval1:
                        if_result_true=True
                elif oper in ["ifgt","ifnotgt"]:
                    if dval > dval1:
                        if_result_true=True
                elif oper in ["iflte","ifnotlte"]:
                    if dval <= dval1:
                        if_result_true=True
                elif oper in ["iflt","ifnotlt"]:
                    if dval < dval1:
                        if_result_true=True
                elif oper in ["ifeq","ifnoteq"]:
                    if dval == dval1:
                        if_result_true=True
                if oper.startswith("ifnot"):
                    if_result_true = not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifempty","ifnotempty"]:
                prior_was_if=True
                if_result_true=False
                if len(result)==0:
                    if_result_true=True
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifstreq","ifnotstreq"]:
                prior_was_if=True
                if_result_true=False
                str1=result
                if not param2=="true":
                    str1=str1.lower()
                for j in range(len(items)):
                    str2= recfuncs.convert_special_notation(items[j])
                    if not param2=="true":
                        str2=str2.lower()
                    if str1==str2:
                        if_result_true=True
                        break
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifstrstarts","ifnotstrstarts"]:
                prior_was_if=True
                if_result_true=False
                str1=result
                if not param2=="true":
                    str1=str1.lower()
                for j in range(len(items)):
                    str2= recfuncs.convert_special_notation(items[j])
                    if not param2=="true":
                        str2=str2.lower()
                    if str1.startswith(str2):
                        if_result_true=True
                        break
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifstrends","ifnotstrends"]:
                prior_was_if=True
                if_result_true=False
                str1=result
                if not param2=="true":
                    str1=str1.lower()
                for j in range(len(items)):
                    str2= recfuncs.convert_special_notation(items[j])
                    if not param2=="true":
                        str2=str2.lower()
                    if str1.endswith(str2):
                        if_result_true=True
                        break
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifstrcontains","ifnotstrcontains"]:
                prior_was_if=True
                if_result_true=False
                str1=result
                if not param2=="true":
                    str1=str1.lower()
                if param3=="true":
                    str1=str1.replace(" ","")
                for j in range(len(items)):
                    str2= recfuncs.convert_special_notation(items[j])
                    if not param2=="true":
                        str2=str2.lower()
                    if str2 in str1:
                        if_result_true=True
                        break
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifint","ifnotint"]:
                prior_was_if=True
                if_result_true=False
                lval=0
                if numfuncs.is_int(result):
                    lval=int(result)
                    if_result_true=True
                if param1=="positive" and lval<=0:
                    if_result_true=False
                elif param1=="negative" and lval>=0:
                    if_result_true=False
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifreal","ifnotreal"]:
                prior_was_if=True
                if_result_true=False
                dval=0
                if (dval := numfuncs.is_real_get(result, "number", True))== -999999:
                    dval=0
                else:
                    if_result_true=True
                if param1=="positive" and dval<=0:
                    if_result_true=False
                elif param1=="negative" and dval>=0:
                    if_result_true=False
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper.startswith(("ifmatch","ifnotmatch")):
                # includes byref
                prior_was_if=True
                if_result_true=False
                str1=result.lower()
                str2=""
                param1=param1.lower()
                if oper.endswith("ref"):
                    if len(param1)==0:
                        raise ValueError("missing reference field title in: " + oper)
                    if param1 in hash_fields:
                        nfld= hash_fields[param1]
                        str2= recfuncs.get_math_alias(field_values[nfld])
                    else:
                        raise ValueError("reference field title not in fields: " + param1 + ", oper=" + oper)
                else:
                    str2=param1
                str1=recfuncs.convert_special_notation(str1)
                str2=recfuncs.convert_special_notation(str2)
                wildf=False
                wildb=False
                ismatch=False
                if str2.startswith("*"):
                    wildf=True
                    str2=str2[1:]
                if len(str2)==0:
                    wildb=True
                elif str2.endswith("*"):
                    wildb=True
                    str2=str2[:-1]
                if wildf and wildb and len(str2)==0:
                    ismatch=True
                elif len(str1)>0 and len(str2)>0:
                    if wildf and wildb and str2 in str1:
                        ismatch=True
                    elif wildf and not wildb and str1.endswith(str2):
                        ismatch=True
                    elif not wildf and wildb and str1.startswith(str2):
                        ismatch=True
                    elif not wildf and not wildb and str1==str2:
                        ismatch=True
                if_result_true=ismatch
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifisodate","ifnotisodate"]:
                prior_was_if=True
                if_result_true=False
                str1= datefuncs.is_iso_date_str(result, False)
                if_result_true= str1.startswith("true")
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper in ["ifdateformat","ifnotdateformat"]:
                prior_was_if=True
                if_result_true= datefuncs.is_date_format(result, param1)
                if oper.startswith("ifnot"):
                    if_result_true= not if_result_true
                if i== len(transobj.ops)-1:
                    result= str(if_result_true).lower()
            elif oper=="lookup":
                isok=False
                if hash_fields is None or len(hash_fields)==0:
                    raise ValueError("no hash fields defined so cannot do transform:" + transobj.title + ",op index=" + str(i))
                if lookup_dicts is None or len(lookup_dicts)==0:
                    raise ValueError("no lookupdicts defined, transform:" + transobj.title + ",op index=" + str(i))
                if hash_lookup_dicts is None:
                    raise ValueError("no hash lookupdicts defined, transform:" + transobj.title + ",op index=" + str(i))
                param1=param1.lower()
                if param1 not in hash_lookup_dicts:
                    raise ValueError("transform lookupdict not defined:" + param1 + ",transform="\
                                      + transobj.title + ",op index=" + str(i))
                nidx= hash_lookup_dicts[param1]
                lkup= lookup_dicts[nidx]
                nkeys=1  # number keys defined in Op always has base value as first
                str2=""
                str3=""
                nfld2=-1
                nfld3=-1
                fldval2=""
                fldval3=""
                param2=param2.lower()
                if len(param2)>0:
                    n1= param2.find("|")
                    if "|" in param2 and len(param2)>(1+ n1):
                        nkeys += 2
                        str2= param2[:n1]
                        str3=param2[(n1+1):]
                    else:
                        nkeys += 1
                        str2=param2
                if len(str2)>0:
                    if str2 in hash_fields:
                        nfld2=hash_fields[str2]
                    else:
                        raise ValueError("lookup field 2 is not in supplied record fields: " + str2)
                if len(str3)>0:
                    if str3 in hash_fields:
                        nfld3=hash_fields[str3]
                    else:
                        raise ValueError("lookup field 3 is not in supplied record fields: " + str3)

                if nfld2>=0:
                    fldval2= field_values[nfld2]
                if nfld3>=0:
                    fldval3= field_values[nfld3]
                if not lkup.is_case_sens:
                    if nfld2>=0:
                        fldval2=fldval2.lower()
                    if nfld3>=0:
                        fldval3=fldval3.lower()

                for j in range(len(lkup.recs)):
                    if isok:
                        break

                    ismatch=False
                    for f in range(nkeys):
                        if f==0:
                            fldval= recfuncs.convert_special_notation(result)
                            if not lkup.is_case_sens:
                                fldval=fldval.lower()
                            keyand=lkup.recs[j].key1_and
                            keynot=lkup.recs[j].key1_not
                        elif f==1:
                            fldval=fldval2
                            keyand=lkup.recs[j].key2_and
                            keynot=lkup.recs[j].key2_not
                        elif f==2:
                            fldval=fldval3
                            keyand=lkup.recs[j].key3_and
                            keynot=lkup.recs[j].key3_not
                        else:
                            break

                        isnotmatch=False
                        # check NOT first. Done as OR so any match means NOT met
                        for k in range(len(keynot)):
                            flag=False
                            str1=keynot[k]
                            if not lkup.is_case_sens:
                                str1=str1.lower()

                            if f==0:
                                wildf=lkup.recs[j].key1_not_front_wild[k]
                                wildb=lkup.recs[j].key1_not_back_wild[k]
                            elif f==1:
                                wildf=lkup.recs[j].key2_not_front_wild[k]
                                wildb=lkup.recs[j].key2_not_back_wild[k]
                            elif f==2:
                                wildf=lkup.recs[j].key3_not_front_wild[k]
                                wildb=lkup.recs[j].key3_not_back_wild[k]

                            if wildf and wildb and len(str1)==0:
                                flag=True
                            elif len(fldval)>0 and len(str1)>0:
                                if wildf and wildb and str1 in fldval:
                                    flag=True
                                elif wildf and not wildb and fldval.endswith(str1):
                                    flag=True
                                elif not wildf and wildb and fldval.startswith(str1):
                                    flag=True
                                elif not wildf and not wildb and fldval==str1:
                                    flag=True
                            if flag:
                                isnotmatch=True
                                break

                        if len(keyand)==0:
                            ismatch=True
                        if not isnotmatch:
                            flag=True
                            for k in range(len(keyand)):
                                flag=False
                                str1=keyand[k]
                                if not lkup.is_case_sens:
                                    str1=str1.lower()
                                if f==0:
                                    wildf=lkup.recs[j].key1_and_front_wild[k]
                                    wildb=lkup.recs[j].key1_and_back_wild[k]
                                elif f==1:
                                    wildf=lkup.recs[j].key2_and_front_wild[k]
                                    wildb=lkup.recs[j].key2_and_back_wild[k]
                                elif f==2:
                                    wildf=lkup.recs[j].key3_and_front_wild[k]
                                    wildb=lkup.recs[j].key3_and_back_wild[k]

                                if wildf and wildb and len(str1)==0:
                                    flag=True
                                elif len(fldval)>0 and len(str1)>0:
                                    if wildf and wildb and str1 in fldval:
                                        flag=True
                                    elif wildf and not wildb and fldval.endswith(str1):
                                        flag=True
                                    elif not wildf and wildb and fldval.startswith(str1):
                                        flag=True
                                    elif not wildf and not wildb and fldval==str1:
                                        flag=True
                                if not flag:
                                    ismatch=False
                                    break
                                ismatch=True

                        if not ismatch or isnotmatch:
                            # failed conditions so no need to check other fields
                            break

                    #all fields checked so must be ok at this point to set result
                    if ismatch and not isnotmatch:
                        result= lkup.recs[j].result
                        isok=True
                        break

            if stop_now:
                break

    except (RuntimeError,ValueError,OSError) as err:
        result="notok:" + str(err)
    return result
