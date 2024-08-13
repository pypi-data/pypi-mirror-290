#!/usr/bin/env python
"""
Number Functions

various worker functions to manipulate numbers
"""

__all__ = ['convert_mainframe',
           'get_value_from_suspect_exp',
           'is_int',
           'is_real',
           'is_int_get',
           'is_real_get',
           'clean_number',
            ]

__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240614'


def is_int(valnum:str) -> bool:
    """
    Checks if string is integer number. Returns bool
    """
    result:bool=False
    try :
        result= is_int_get(valnum,"bool")
    except (RuntimeError, ValueError):
        result=False
    return result

def is_real(valnum:str) -> bool:
    """
    Checks if string is real number. Returns bool
    """
    result:bool=False
    try :
        result= is_real_get(valnum,"bool")
    except (RuntimeError, ValueError):
        result=False
    return result

def is_int_get(valnum:str, typ:str="", remove_front_chars:bool=False):
    """
    Checks if string is integer number. 
    
    valnum: input string to check
    typ: optional return type (string, number, bool)
    remove_front_chars: optional. bool whether non-numeric chars as prefix will be removed
        and therefore not declare non-numeric
    Return depends on typ. Default is bool. 
        number: converted integer or -999999 if error
        string: string of integer or false:reason if not. Reason will 
            be detected issue such as decimal (has decimal point),
            empty, non-numeric
    """
    isneg:bool=False
    resultstr:str=""
    resultbool:bool=False
    resultnum:int=-999999
    numstr:str=""
    charstr:str=""
    nstart:int=-1
    numes:int=0
    reason:str=""
    try :
        typ=typ.lower().strip()
        if typ not in ["bool","number","string"]:
            typ="bool"
        valnum=valnum.lower().strip()
        if valnum.startswith("-"):
            valnum= valnum[1:]
            isneg=True
        elif valnum.startswith("(") and valnum.endswith(")"):
            valnum= valnum[1:-1]
            isneg=True
        elif valnum.startswith("+"):
            valnum= valnum[1:]
        if len(valnum)==0:
            resultstr= "false"
            reason="empty"
        elif any(x in valnum for x in ["e+","e-"]):
            numstr= get_value_from_suspect_exp(valnum)
            if len(numstr)==0 or numstr.startswith("notok:") or numstr==valnum:
                resultstr= "false"
                reason="non-numeric"
            elif "." in numstr:
                resultstr= "false"
                reason="decimal"
            else:
                try:
                    resultnum=int(numstr)
                except ValueError:
                    resultstr= "false"
                    reason="non-numeric"
        elif "." in valnum:
            resultstr= "false"
            reason="decimal"
        elif not remove_front_chars:
            try:
                resultnum=int(valnum)
            except ValueError:
                resultstr= "false"
                reason="non-numeric"
        else:
            for i in range(len(valnum)):
                charstr= valnum[i:i+1]
                if charstr.isdigit():
                    numstr += charstr
                    if nstart<0:
                        nstart=i
                elif charstr==".":
                    resultstr= "false"
                    reason="decimal"
                    break
                elif charstr=="e" and numes==0:
                    numes=1
                elif nstart> -1:
                    resultstr= "false"
                    reason="non-numeric"
                    break
            if nstart<0:
                resultstr= "false"
                reason="non-numeric"

            if len(reason)==0 and nstart>-1 and (numes==1 or len(numstr)>0):
                try:
                    if numes==1:
                        resultnum=int(valnum)
                    elif len(numstr)>0:
                        resultnum= int(numstr)
                except ValueError:
                    resultstr= "false"
                    reason="non-numeric"
        if len(reason)>0:
            resultstr = "false:" + reason
            resultbool=False
        elif not remove_front_chars and nstart>0:
            if typ=="bool":
                resultbool=False
            elif typ=="number":
                resultnum= -999999
        else:
            resultbool=True
            if isneg:
                resultnum *= -1
            resultstr= str(resultnum)
        if typ=="bool":
            return resultbool
        if typ=="number":
            return resultnum
    except (RuntimeError, ValueError):
        resultstr= "false:error"
    return resultstr

def is_real_get(valnum:str, typ:str="", remove_front_chars:bool=False):
    """
    Checks if string is real number. 
    
    valnum: input string to check
    typ: optional return type (string, number, bool)
    remove_front_chars: optional. bool whether non-numeric chars as prefix will be removed
        and therefore not declare non-numeric
    Return depends on typ. Default is bool. 
        number: converted real or -999999 if error
        string: string of real or false:reason if not. Reason will 
            be detected issue such as empty, non-numeric
    """
    isneg:bool=False
    resultstr:str=""
    resultbool:bool=False
    resultnum:float=-999999
    numstr:str=""
    charstr:str=""
    nstart:int=-1
    nperiod:int=-1
    numes:int=0
    reason:str=""
    try :
        typ=typ.lower().strip()
        if typ not in ["bool","number","string"]:
            typ="bool"
        valnum=valnum.lower().strip()
        if valnum.startswith("-"):
            valnum= valnum[1:]
            isneg=True
        elif valnum.startswith("(") and valnum.endswith(")"):
            valnum= valnum[1:-1]
            isneg=True
        elif valnum.startswith("+"):
            valnum= valnum[1:]
        if len(valnum)==0:
            resultstr= "false"
            reason="empty"
        elif any(x in valnum for x in ["e+","e-"]):
            numstr= get_value_from_suspect_exp(valnum)
            if len(numstr)==0 or numstr.startswith("notok:") or numstr==valnum:
                resultstr= "false"
                reason="non-numeric"
            else:
                try:
                    resultnum=float(numstr)
                except ValueError:
                    resultstr= "false"
                    reason="non-numeric"
        elif not remove_front_chars:
            try:
                resultnum=float(valnum)
            except ValueError:
                resultstr= "false"
                reason="non-numeric"
        else:
            for i in range(len(valnum)):
                charstr= valnum[i:i+1]
                if charstr.isdigit():
                    numstr += charstr
                    if nstart<0:
                        nstart=i
                elif charstr==".":
                    if nperiod<0:
                        numstr += charstr
                        nperiod=i
                    else:
                        resultstr= "false"
                        reason="duplicate decimal"
                        break
                elif charstr=="e" and numes==0:
                    numes=1
                elif nstart> -1:
                    resultstr= "false"
                    reason="non-numeric"
                    break
            if nstart<0:
                resultstr= "false"
                reason="non-numeric"

            if len(reason)==0 and nstart>-1 and (numes==1 or len(numstr)>0):
                try:
                    if numes==1:
                        resultnum=float(valnum)
                    elif len(numstr)>0:
                        resultnum= float(numstr)
                except ValueError:
                    resultstr= "false"
                    reason="non-numeric"
        if len(reason)>0:
            resultstr = "false:" + reason
            resultbool=False
        elif not remove_front_chars and nstart>0:
            if typ=="bool":
                resultbool=False
            elif typ=="number":
                resultnum= -999999
        else:
            resultbool=True
            if isneg:
                resultnum *= -1
            resultstr= str(resultnum)
            if "." not in resultstr:
                resultstr += ".0"
        if typ=="bool":
            return resultbool
        if typ=="number":
            return resultnum
    except (RuntimeError, ValueError):
        resultstr= "false:error"
    return resultstr

def convert_mainframe(valnum:str) -> str:
    """
    Convert MainFrame formatted number string

    Converts a string representing a main frame formatted number with an encoded last character into a string of a 
    real along with sign reversal if necessary 
    Always makes last 2 digits into decimal portion so no further divide by 100 is necessary. If special char is 
    within input string it becomes the end char and the 
    remaining suffix is discarded. Leading zeros are truncated so 000.12 becomes 0.12 . Codes are:
    {= 0
    }= 0 and negate
    a= 1
    j= 1 and negate
    b= 2
    k= 2 and negate
    c= 3
    l= 3 and negate
    d= 4
    m= 4 and negate
    e= 5
    n= 5 and negate
    f= 6
    o= 6 and negate
    g= 7
    p= 7 and negate
    h= 8
    q= 8 and negate
    i= 9
    r= 9 and negate
    Return result or starts with 'notok:' if error. If no special char found then original string returned
    """

    str_out:str=""
    str1:str=""
    str_in:str=""
    codechar:str=""
    chg_sign:bool=False
    signtyp:str=""
    n1:int=-1
    dval:float=-1
    try:
        str_in= valnum.strip().lower()
        if len(str_in)==0:
            raise ValueError("str_in is empty")
        if str_in.startswith("-"):
            signtyp="-"
            str_in=str_in[1:]
        if len(str_in)>=2:
            for i in range(20):
                if i==0:
                    str1="{"
                elif i==1:
                    str1="}"
                elif i==2:
                    str1="a"
                elif i==3:
                    str1="j"
                elif i==4:
                    str1="b"
                elif i==5:
                    str1="k"
                elif i==6:
                    str1="c"
                elif i==7:
                    str1="l"
                elif i==8:
                    str1="d"
                elif i==9:
                    str1="m"
                elif i==10:
                    str1="n"
                elif i==11:
                    str1="f"
                elif i==12:
                    str1="o"
                elif i==13:
                    str1="g"
                elif i==14:
                    str1="p"
                elif i==15:
                    str1="h"
                elif i==16:
                    str1="q"
                elif i==17:
                    str1="i"
                elif i==18:
                    str1="r"
                else:
                    break
                if str1 in str_in:
                    n1= str_in.find(str1)
                    break

            if n1>=0:
                codechar= str_in[n1:(n1+1)]
                str_out=str_in[:n1]
            else:
                return str_in
            str1=""
            if codechar=="{":
                str1="0"
            elif codechar=="}":
                str1="0"
                chg_sign=True
            elif codechar=="a":
                str1="1"
            elif codechar=="j":
                str1="1"
                chg_sign=True
            elif codechar=="b":
                str1="2"
            elif codechar=="k":
                str1="2"
                chg_sign=True
            elif codechar=="c":
                str1="3"
            elif codechar=="l":
                str1="3"
                chg_sign=True
            elif codechar=="d":
                str1="4"
            elif codechar=="m":
                str1="4"
                chg_sign=True
            elif codechar=="e":
                str1="5"
            elif codechar=="n":
                str1="5"
                chg_sign=True
            elif codechar=="f":
                str1="6"
            elif codechar=="o":
                str1="6"
                chg_sign=True
            elif codechar=="g":
                str1="7"
            elif codechar=="p":
                str1="7"
                chg_sign=True
            elif codechar=="h":
                str1="8"
            elif codechar=="q":
                str1="8"
                chg_sign=True
            elif codechar=="i":
                str1="9"
            elif codechar=="r":
                str1="9"
                chg_sign=True
            elif codechar.isdigit():
                str1=codechar
            str_out += str1
            if len(str_out)>=2 and "." not in str_out:
                str1=str_out[-2:]
                str_out=str_out[:-2]
                str_out += "." + str1
            if chg_sign:
                if signtyp=="-":
                    signtyp=""
                else:
                    signtyp="-"

            if (dval := is_real_get(str_out,"number",True))!= -999999:
                str_out=str(dval)
                if str_out.startswith("."):
                    str_out= "0" + str_out
                elif "." in str_out:
                    n1=str_out.find(".")
                    str1= str_out[(n1+1):]
                    str_out=str_out[:(n1+1)]
                    if len(str1)==0:
                        str1="00"
                    elif len(str1)==1:
                        str1+= "0"
                    str_out += str1
                else:
                    str_out="0.00"
            else:
                str_out="0.00"
            if signtyp=="-":
                str_out= signtyp + str_out
    except (RuntimeError,ValueError) as err:
        str_out="notok:" + str(err)
    return str_out

def get_value_from_suspect_exp(valnum:str) -> str:
    """
    Get Value From Suspected Exponential

    Check string to see if it is an exponential number 
    which is extracted into real number if so
    Returns string of number if converted or original string. Starts with notok: if error
    """

    result:str=""
    orignum:str=""
    numstr:str=""
    intpart:str=""
    decpart:str=""
    exppart:str=""
    isexpneg:bool=False
    isnegval:bool=False
    flag:bool=False
    n1:int=-1
    dexp:float=-1
    numexp:float=-1
    dval:float=-1
    nper:int=-1
    try:
        result=valnum
        orignum=valnum.lower()
        if orignum.startswith("-"):
            isnegval=True
            orignum=orignum[1:]
        elif orignum.startswith("(") and orignum.endswith(")"):
            isnegval=True
            orignum=orignum[1:-1]
        if "e-" in orignum:
            isexpneg=True
        if "e" in orignum:
            numstr= orignum[:orignum.find("e")]
            exppart=orignum[orignum.find("e")+1:]
            if len(exppart)>0 and is_real(exppart):
                flag=True
        if flag:
            if not is_real(numstr):
                flag=False

        if flag:
            dval= is_real_get(numstr, "number", True)
            if exppart.startswith("+") or exppart.startswith("-"):
                exppart=exppart[1:]
            if len(exppart)>0 and (dexp := is_real_get(exppart, "number", True))!= -999999:
                if isexpneg:
                    dexp *= -1
                numexp= 10**dexp
            else:
                numexp=1
            dval *= numexp
            result= str(dval)
            if "." in result:
                nper=result.find(".")
                decpart=result[nper+1:]
                intpart=result[:nper]
                if is_int(decpart):
                    n1=int(decpart)
                    if n1==0:
                        result=intpart
                    elif len(decpart)==0:
                        result = intpart + ".00"
                    elif len(decpart)==1:
                        result = intpart + "." + decpart + "0"
                else:
                    result=intpart
            if result.startswith("."):
                result = "0" + result

        if flag and isnegval:
            result= "-" + result
    except (RuntimeError, ValueError, OSError) as err:
        result= "notok:" + str(err)
    return result

def clean_number(valnum:str) -> str:
    """
    Cleans non-numeric prefix and suffix characters from number. 
	Enclosing parens which is interpreted as negative indicator and replaced with -, 
    while leading + is removed.
    returns string starting with notok: if error
    """

    resultstr:str=""
    txt:str=""
    charstr:str=""
    isneg:bool=False
    isok:bool=False
    nstart:int=-1
    ndec:int=-1
    numes:int=0
    dval:float=0
    try:
        valnum=valnum.lower().strip()
        if valnum.startswith("-"):
            valnum= valnum[1:]
            isneg=True
        elif valnum.startswith("(") and valnum.endswith(")"):
            valnum= valnum[1:-1]
            isneg=True
        elif valnum.startswith("+"):
            valnum= valnum[1:]
        if len(valnum)==0:
            resultstr= "-false-"
        else:
            try:
                dval=float(valnum)
                resultstr=valnum
                isok=True
            except ValueError:
                resultstr= ""

        if not isok and not resultstr=="-false-":
            if any(x in valnum for x in ["e+","e-"]):
                txt= get_value_from_suspect_exp(valnum)
                if len(txt)==0 or txt.startswith("notok:") or txt==valnum:
                    resultstr= "-false-"
                else:
                    try:
                        dval=float(txt)
                        resultstr=txt
                        isok=True
                    except ValueError:
                        resultstr= "-false-"
            else:
                for i in range(len(valnum)):
                    if i>=50:
                        resultstr= "-false-"
                        break

                    charstr= valnum[i:i+1]
                    if charstr.isdigit():
                        resultstr += charstr
                        if nstart<0:
                            nstart=i
                    elif charstr=="-":
                        if not isneg:
                            isneg=True
                            if nstart<0:
                                nstart=i
                        elif nstart>-1:
                            break
                    elif charstr==".":
                        if ndec<0:
                            resultstr += charstr
                            ndec=i
                        else:
                            resultstr= "-false-"
                            break
                    elif charstr=="e" and numes==0:
                        numes=1
                    elif nstart> -1:
                        break
                if nstart<0:
                    resultstr= "-false-"

                if not resultstr=="-false-" and nstart>-1:
                    if numes==1:
                        try:
                            dval=float(valnum)
                            resultstr= str(dval)
                        except ValueError:
                            resultstr="-false-"
                    elif len(resultstr)>0:
                        try:
                            dval=float(resultstr)
                        except ValueError:
                            resultstr="-false-"
        if resultstr=="-false-":
            resultstr=""
        elif isneg and len(resultstr)>0 and not resultstr=="0" and not resultstr.startswith("-"):
            resultstr= "-" + resultstr
    except (RuntimeError,ValueError) as err:
        resultstr="notok:" + str(err)
    return resultstr
