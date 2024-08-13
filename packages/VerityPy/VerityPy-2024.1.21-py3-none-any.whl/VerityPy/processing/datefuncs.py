#!/usr/bin/env python
"""
Date Functions

various functions to process and provide dates
"""

__all__ = ['get_current_iso_datetime',
           'is_iso_date_str',
           'convert_excel_date_to_iso',
           'is_year_leap',
           'convert_date_to_iso',
           'is_date_format'
            ]

__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240725'


import math
from time import *
from . import numfuncs


def get_current_iso_datetime(inctime:bool=False, tz:str="") -> str:
    """
    Get current date or datetime in ISO format 
    but without delimiters like 20240409 or 20240409T090245
    inctime: bool whether to include time part with T prefix
    tz: optional number hours timezone offset from UTC (e.g. Dallas TX is -5, Kolkata India is +5.5, New York NY is -4), 
      otherwise the computer's time zone is used so depends on server settings.
    Returns string starting with notok: if error
    """

    result:str=""
    dval:float=-99.0
    dtime_secs_since_epoch:float=-999999
    time_obj:struct_time
    try:
        dtime_secs_since_epoch= time()
        if len(tz)>0 and numfuncs.is_real(tz):
            dval= dtime_secs_since_epoch + round(float(tz),1) * 3600 # number seconds for offset hours
        else:
            dval= dtime_secs_since_epoch # uses localtime
        time_obj= localtime(dval)
        if inctime:
            result= strftime("%Y%m%dT%H%M%S", time_obj)
        else:
            result= strftime("%Y%m%d", time_obj)
    except (RuntimeError, ValueError, OSError) as err:
        result="notok:" + str(err)
    return result

def is_iso_date_str(strin:str,timereq:bool=False) -> str:
    """
    Determines if string is an ISO DateTime

    timereq: bool if time part is required. This is demarcated by either 
    T or a space after the date part as with 20240420T0730 or 20240420 0730
    
    All delimiters will be removed  (-  /) in date part, (:) in time part.
    Returns string as either false or true:<newdatetime>, or starts 
    with notok: if error
    """

    result:str=""
    nyr:int=0
    nmo:int=0
    ndy:int=0
    nhr:int=-1
    nmin:int=0
    nsec:int=0
    n1:int=-1
    timepart:str=""
    datepart:str=""
    tz:str=""
    delim:str=""
    txt1:str=""
    txt2:str=""
    txt3:str=""
    txt4:str=""
    fmterr:bool=False
    dayspermonth:list=[]
    try:
        if len(strin)==0:
            return "false"
        strin=strin.lower()
        if "t" in strin:
            n1=strin.find("t")
        elif timereq and " " in strin:
            n1=strin.find(" ")
        if n1>0:
            timepart= strin[n1+1:]
            datepart= strin[:n1]
        else:
            datepart=strin
        dayspermonth.append(31)
        dayspermonth.append(28)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)

        if timereq and len(timepart)==0:
            fmterr=True
        if not fmterr:
            if "-" in datepart:
                delim="-"
                n1=datepart.find(delim)
                txt1= datepart[:n1]
                txt2=datepart[n1+1:]
                n1=txt2.find(delim)
                if n1>-1:
                    txt3=txt2[n1+1:]
                    txt2=txt2[:n1]
            elif len(datepart)>=4:
                txt1=datepart[:4]
                if len(datepart)>=6:
                    txt2=datepart[4:6]
                if len(datepart)>=8:
                    txt3=datepart[6:]
            if len(txt1)==4 and numfuncs.is_int(txt1):
                nyr=int(txt1)
                if nyr<0:
                    fmterr=True
            else:
                fmterr=True
            if not fmterr and len(txt2)==2 and numfuncs.is_int(txt2):
                nmo=int(txt2)
                if nmo<=0 or nmo>=13:
                    fmterr=True
            else:
                fmterr=True
            if not fmterr and len(txt3)==2 and numfuncs.is_int(txt3):
                ndy=int(txt3)
                if ndy<=0 or ndy>=31:
                    fmterr=True
            else:
                fmterr=True
        if not fmterr and timereq:
            if len(timepart)>0:
                txt1=""
                txt2=""
                txt3=""
                txt4=""
                if timepart.endswith("z"):
                    tz="Z"
                    timepart=timepart[:len(timepart)-1]
                elif "+" in timepart:
                    n1=timepart.find("+")
                    tz=timepart[n1:]
                    timepart=timepart[:n1].strip()
                elif "-" in timepart:
                    n1=timepart.find("-")
                    tz=timepart[n1:]
                    timepart=timepart[:n1].strip()
                if ":" in timepart:
                    delim=":"
                    n1=timepart.find(delim)
                    txt1=timepart[:n1]
                    txt2=timepart[n1+1:]
                    if delim in txt2:
                        n1=txt2.find(delim)
                        txt3=txt2[n1+1:]
                        txt2=txt2[:n1]
                elif len(timepart)>2:
                    txt1=timepart[:2]
                    if len(timepart)>=4:
                        txt2=timepart[2:4]
                        if len(timepart)==6 or ("." in timepart and len(timepart)>7):
                            txt3=timepart[4:]
                            if "." in txt3:
                                n1= txt3.find(".")
                                txt4=txt3[(n1+1):]
                                txt3=txt3[:n1]
                
                if len(txt1)!=2 or not numfuncs.is_int(txt1):
                    fmterr=True
                else:
                    nhr=int(txt1)
                    if len(txt2)>0:
                        if len(txt2)!=2 or not numfuncs.is_int(txt2):
                            fmterr=True
                        else:
                            nmin=int(txt2)
                        if len(txt3)>0:
                            if len(txt3)!=2 or not numfuncs.is_int(txt3):
                                fmterr=True
                            else:
                                nsec=int(txt3)
                            if len(txt4)>0 and not numfuncs.is_int(txt4):
                                fmterr=True
            else:
                fmterr=True

        if not fmterr:
            if nyr<=0:
                fmterr=True
            elif 0> nmo >12:
                fmterr=True
            elif 0> ndy > 31:
                fmterr=True
            else:
                if nmo==2:
                    n1= 29 if is_year_leap(nyr) else 28
                else:
                    n1= dayspermonth[nmo-1]
                if ndy>n1:
                    fmterr= True

        if not fmterr:
            txt1=str(nyr)
            if len(txt1)==3:
                txt1="0" + txt1
            elif len(txt1)==2:
                txt1="00" + txt1
            elif len(txt1)==1:
                txt1="000" + txt1
            txt2=str(nmo)
            if len(txt2)==1:
                txt2 = "0" + txt2
            txt3=str(ndy)
            if len(txt3)==1:
                txt3 = "0" + txt3
            result= txt1 + txt2 + txt3
            if timereq:
                result += "T"
                txt1= str(nhr)
                if len(txt1)==1:
                    txt1 = "0" + txt1
                txt2=str(nmin)
                if len(txt2)==1:
                    txt2 = "0" + txt2
                txt3=str(nsec)
                if len(txt3)==1:
                    txt3 = "0" + txt3
                result += txt1 + txt2 + txt3
            result = "true:" + result
            if len(tz)>0:
                result += tz
        else:
            result="false"
    except (RuntimeError,ValueError,OSError) as err:
        result= "notok:" + str(err)
    return result

def convert_excel_date_to_iso(strin:str) -> str:
    """
    Excel numeric date to ISO format

    Converts a date in numeric excel format into ISO8601 yyyyMMdd format.
	Fractional days are removed. Jan 1 1900 is 1. Anything less than 1 is error.
    Example: 44106 = 20201002, 45393 = 20240411, 21012=19570711
	Return result as yyyyMMdd. Starts with notok: if there is an error
    """


    result:str=""
    str1:str=""
    ddays_400:int=0
    ddays_100:int=0
    ddays_4:int=0
    ddays_1:int=0
    curyr:int=0
    curmn:int=0
    curday:int=0
    dayspermonth:list=[]
    dval_days:float=0
    nyrs_400:int=0
    nyrs_100:int=0
    nyrs_4:int=0
    nyrs_1:int=0
    isleap:bool=False
    ndays:int=0
    ndaysprev:int=0
    addleap:bool=True
    try:
        dayspermonth.append(31)
        dayspermonth.append(28)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(29) #leap years

        ddays_1=365
        ddays_4= 365*4
        if addleap:
            # 1 leap year
            ddays_4 += 1
        ddays_100= 365*100
        if addleap:
            # 24 leap years since number 100 is not
            ddays_100 += 24
        ddays_400= ddays_100*4
        if addleap:
            # 400th year is leap
            ddays_400 += 1
        str1=strin
        if "." in str1:
            str1=str1[:str1.find(".")]
        dval_days= int(str1)
        if dval_days<1:
            raise ValueError("min number to supply is 1 not: " + str1)
        dval_days -= 1  #since Excel starts with day 1

        if dval_days>ddays_400:
            nyrs_400= math.floor(dval_days/ddays_400)
            dval_days -= nyrs_400 * ddays_400
        if dval_days> ddays_100:
            nyrs_100= math.floor(dval_days/ddays_100)
            dval_days -= nyrs_100 * ddays_100
        if dval_days > ddays_4:
            nyrs_4= math.floor(dval_days/ddays_4)
            dval_days -= nyrs_4 * ddays_4
        if dval_days > ddays_1:
            nyrs_1= math.floor(dval_days/ddays_1)
            dval_days -= nyrs_1 * ddays_1

        curyr= 1900 + 400*nyrs_400 + 100*nyrs_100 + 4*nyrs_4 + nyrs_1
        isleap= is_year_leap(curyr)

        if dval_days>0:
            for i in range(12):
                if i>0:
                    ndaysprev=ndays
                if isleap and i==1:
                    ndays += dayspermonth[12]
                else:
                    ndays += dayspermonth[i]
                if ndays>=dval_days:
                    curmn= i+1
                    curday=dval_days- ndaysprev
                    break
        curmn= max(curmn,1)
        curday= max(curday,1)
        result= str(curyr)
        str1= str(curmn)
        if len(str1)==1:
            str1="0" + str1
        result += str1
        str1= str(curday)
        if len(str1)==1:
            str1="0" + str1
        result += str1
    except (RuntimeError,ValueError,OSError) as err:
        result="notok:" + str(err)
    return result

def is_year_leap(nyear:int) -> bool:
    """
    Is Year a Leap Year

    uses rule that every 4th year is leap except when 
    multiple of 100, but when multiple of 400 it is leap
    nyear: integer year to evaluate
    returns: bool
    """

    isleap=False
    try:
        if nyear>=400 and nyear%400==0:
            isleap=True
        elif nyear>=100 and nyear%100==0:
            isleap=False
        elif nyear>=4 and nyear%4==0:
            isleap=True
    except (RuntimeError,ValueError,OSError):
        pass
    return isleap

def convert_date_to_iso(datein:str,formatin:str,detectfmt:bool=False) -> str:
    """
    Converts a datetime into ISO8601 format based on specified format. 
    Time portions should be removed prior to sending into this method.
    Four delimiters in date part will be automatically detected: ( - / _ . )

    datein: incoming date string not in ISO8601 and without time part. 
    formatin: required unless detectfmt is True
        mmddyy, mmdyy, mdyy, mmddyyyy, mmdyyyy, mdyyyy, 
        ddmmyy, ddmyy, dmyy, ddmmyyyy, ddmyyyy, dmyyyy,
        yymmdd, yymmd, yymd, yyyymmdd, yyyymmd, yyyymd, 
        yyyyddd (3 digit day number within year), 
        yyyyMMMdd, ddMMMyyyy (MMM = 3 letter month title like 'JAN'),
        'MONTHdd,yyyy', 'ddMONTH,yyyy', yyyyMONTHdd, ddMONTHyyyy, yyMONTHdd, ddMONTHyy (MONTH full title),
        *dmmyyyy, mm*dyyyy, *mddyyyy, dd*myyyy (*= can be 1 or 2 characters)

        With these formats, incoming string must have all characters required so for mmddyyyy there must be 
        8 characters meaning 1122011 fails but 01122011 is good.
        Leading title of day is removed like for Wednesday, March 14, 2001 which will be changed to 
        March 14, 2001 and then will match formatin of MONTHdd,yyyy since spaces are removed
    detectfmt: optional bool when True the format will be detected if possible. To do so, the date 
        part should have a delimiter ( / - ) like 12/20/2021 or 2024-04-02, and preferably 
        where day value is unambiguous relative to month (i.e. > 12 )
    Returns - result as yyyymmdd with suffix (dateformat) if detectfmt=True. Starts with 'notok:' if there is an error
    """

    result:str=""
    dayspermonth:list=[]
    hash_month_names:dict={}
    hash_month_longnames:dict={}
    hash_day_names:dict={}
    hash_day_longnames:dict={}
    has_short_month:bool=False
    has_long_month:bool=False
    has_day:bool=False
    month_name_used:str=""
    delimin:str=""
    yr:str=""
    mo:str=""
    dy:str=""
    liststr:list=[]
    n1:int=-1
    n2:int=-1
    nidx:int=-1
    ndy:int=-1
    nmo:int=-1
    nyr:int=-1
    isleap:bool=False
    str1:str=""
    str2:str=""
    str3:str=""
    txt:str=""
    txt1:str=""
    txt2:str=""
    prior_yr_min=69
    prior_yr_max=99
    try:
        dayspermonth.append(31)
        dayspermonth.append(28)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(30)
        dayspermonth.append(31)
        dayspermonth.append(29) #leap years

        hash_month_names["jan"]="01"
        hash_month_names["feb"]="02"
        hash_month_names["mar"]="03"
        hash_month_names["apr"]="04"
        hash_month_names["may"]="05"
        hash_month_names["jun"]="06"
        hash_month_names["jul"]="07"
        hash_month_names["aug"]="08"
        hash_month_names["sep"]="09"
        hash_month_names["oct"]="10"
        hash_month_names["nov"]="11"
        hash_month_names["dec"]="12"
        hash_month_longnames["january"]="01"
        hash_month_longnames["february"]="02"
        hash_month_longnames["march"]="03"
        hash_month_longnames["april"]="04"
        hash_month_longnames["may"]="05"
        hash_month_longnames["june"]="06"
        hash_month_longnames["july"]="07"
        hash_month_longnames["august"]="08"
        hash_month_longnames["september"]="09"
        hash_month_longnames["october"]="10"
        hash_month_longnames["november"]="11"
        hash_month_longnames["december"]="12"

        hash_day_names["mon"]=1
        hash_day_names["tue"]=2
        hash_day_names["wed"]=3
        hash_day_names["thu"]=4
        hash_day_names["fri"]=5
        hash_day_names["sat"]=6
        hash_day_names["sun"]=7
        hash_day_longnames["monday"]=1
        hash_day_longnames["tuesday"]=2
        hash_day_longnames["wednesday"]=3
        hash_day_longnames["thursday"]=4
        hash_day_longnames["friday"]=5
        hash_day_longnames["saturday"]=6
        hash_day_longnames["sunday"]=7

        datein=datein.lower().strip()
        formatin=formatin.lower().strip()

        if len(datein)==0:
            raise ValueError("no datein")
        if len(formatin)==0 and not detectfmt:
            raise ValueError("missing formatin")

        for k,v in hash_day_longnames.items():
            if datein.startswith(k):
                has_day=True
                datein=datein[(len(k)+1):].strip()
                if datein.startswith(","):
                    datein=datein[1:].strip()
                break
        if not has_day:
            for k,v in hash_day_names.items():
                if datein.startswith(k):
                    has_day=True
                    n1=datein.find(",")
                    n2=datein.find(" ")
                    if 0<n1<n2:
                        datein=datein[(n1+1):].strip()
                    elif 0<n2<n1:
                        datein=datein[(n2+1):].strip()
                    else:
                        datein=datein[(len(k)+1):].strip()
                    if datein.startswith(","):
                        datein=datein[1:].strip()
                    break

        for k,v in hash_month_longnames.items():
            if k in datein:
                has_long_month=True
                month_name_used=k
                mo=v
                break
        if not has_long_month:
            for k,v in hash_month_names.items():
                if k in datein:
                    has_short_month=True
                    month_name_used=k
                    mo=v
                    break
        if "-" in formatin:
            formatin=formatin.replace("-","")
        if "/" in formatin:
            formatin=formatin.replace("/","")
        if "_" in formatin:
            formatin=formatin.replace("_","")
        if "." in formatin:
            formatin=formatin.replace(".","")

        if "-" in datein:
            delimin="-"
        elif "_" in datein:
            delimin="_"
        elif "/" in datein:
            delimin="/"
        elif "." in datein:
            delimin="."

        if len(formatin)>0:
            if not "month" in formatin and not "*" in formatin:
                str1=datein
                if len(delimin)>0 and delimin in str1:
                    str1=str1.replace(delimin,"")
                if len(str1)> len(formatin):
                    raise ValueError("too many characters for formatin: " + str(len(str1)) + " for " + formatin)
                if len(str1)< len(formatin):
                    raise ValueError("too few characters for formatin: " + str(len(str1)) + " for " + formatin)
            elif "*" in formatin:
                if len(datein)< (len(formatin)-1):
                    raise ValueError("too few characters #= " + str(len(datein)) + " for formatin: " + formatin)

        # attempt to detect format
        if detectfmt and len(formatin)==0 and len(delimin)>0:
            nidx= datein.find(delimin)
            if nidx==4:
                txt1= datein[nidx+1:]
                nidx= txt1.find(delimin)
                if nidx==3:
                    if has_short_month:
                        formatin="yyyymmmdd"
                elif nidx in (1,2):
                    txt2= txt1[nidx+1:]
                    txt1=txt1[:nidx]
                    n1=-1
                    n2=-1
                    if numfuncs.is_int(txt1):
                        n1=int(txt1)
                    if numfuncs.is_int(txt2):
                        n2=int(txt2)
                    if n1>-1 and n2>-1:
                        if n1>12:
                            str1="d" if len(txt1)==1 else "dd"
                            str2="m" if len(txt2)==1 else "mm"
                        else:
                            str1="m" if len(txt1)==1 else "mm"
                            str2="d" if len(txt2)==1 else "d"
                        formatin="yyyy" + str1 + str2
            elif nidx in (1,2):
                txt1= datein[nidx+1:]
                txt2=datein[:nidx]
                n1=-1
                n2=-1
                if numfuncs.is_int(txt2):
                    n2=int(txt2)
                nidx= txt1.find(delimin)
                if nidx==3:
                    if has_short_month:
                        txt1=txt1[nidx+1:]
                        if len(txt1)==4:
                            formatin="ddmmmyyyy"
                        elif len(txt1)<4 and numfuncs.is_int(txt1):
                            n1=int(txt1)
                            if n1>31:
                                formatin="ddmmmyy"
                            elif n2>31:
                                formatin="yymmmdd"
                elif nidx in (1,2):
                    txt=txt2
                    txt2= txt1[nidx+1:]
                    txt1=txt1[:nidx]
                    n1=-1
                    if numfuncs.is_int(txt1):
                        n1=int(txt1)
                    if n1>-1 and n2>-1:
                        if n2>12:
                            str1="d" if len(txt)==1 else "dd"
                            str2="m" if len(txt1)==1 else "mm"
                            str3="yyyy" if len(txt2)>=4 else "yy"
                        else:
                            str1="m" if len(txt)==1 else "mm"
                            str2="d" if len(txt1)==1 else "dd"
                            str3="yyyy" if len(txt2)>=4 else "yy"
                        formatin= str1 + str2 + str3
                elif nidx==4:
                    txt=txt2
                    txt2=txt1[nidx+1:]
                    if numfuncs.is_int(txt2):
                        n1=n2
                        n2=int(txt2)
                        if n1>12:
                            str1="d" if len(txt)==1 else "dd"
                            str2="yy" if len(txt1)==2 else "yyyy"
                            str3="m" if len(txt2)==1 else "mm"
                        else:
                            str1="m" if len(txt)==1 else "mm"
                            str2="yy" if len(txt1)==2 else "yyyy"
                            str3="d" if len(txt2)==1 else "dd"
                        formatin= str1 + str2 + str3

        if len(formatin)==0:
            raise ValueError("no formatin")

        if "dmonthy" in formatin or "ymonthd" in formatin:
            datein=datein.replace(" ","")
            if formatin in ["yyyymonthdd","yymonthdd"]:
                if formatin.startswith("yyyy"):
                    n1=4
                else:
                    n1=2
                yr= datein[:n1]
                datein=datein[n1:]
                if (has_long_month or has_short_month):
                    mo=month_name_used
                    if len(datein)> len(month_name_used):
                        dy= datein[len(month_name_used):]
                        if len(dy)>2:
                            dy=dy[:2]
            elif formatin in ["ddmonthyyyy","ddmonthyy"]:
                dy=datein[:2]
                datein=datein[2:]
                if (has_long_month or has_short_month):
                    mo=month_name_used
                    if len(datein)> len(month_name_used):
                        yr= datein[len(month_name_used):]
        elif formatin in ["monthdd,yyyy","ddmonth,yyyy"]:
            datein=datein.replace(" ","")
            if "," in datein:
                n1= datein.find(",")
                yr=datein[n1+1:]
                datein=datein[:n1]
            if len(month_name_used)>0:
                mo=month_name_used
                if formatin.startswith("dd"):
                    dy=datein[:datein.find(month_name_used)]
                else:
                    dy=datein[len(month_name_used):]
        elif len(delimin)>0:
            liststr=datein.split(delimin)
            if formatin in ["ddmmmyyyy","ddmmmyy"]:
                if len(liststr)>=1:
                    dy=liststr[0]
                if len(liststr)>=2:
                    mo=liststr[1]
                if len(liststr)>=3:
                    yr=liststr[2]
            elif formatin in ["yyyymmmdd","yymmmdd"]:
                if len(liststr)>=1:
                    yr=liststr[0]
                if len(liststr)>=2:
                    mo=liststr[1]
                if len(liststr)>=3:
                    dy=liststr[2]
            elif formatin in ["","mmddyy","mddyy","mmdyy","mdyy","mmddyyyy","mddyyyy","mmdyyyy","mdyyyy"]:
                if len(liststr)>=1:
                    mo=liststr[0]
                if len(liststr)>=2:
                    dy=liststr[1]
                if len(liststr)>=3:
                    yr=liststr[2]
            elif formatin in ["ddmmyy","ddmyy","dmmyy","dmyy","ddmmyyyy","ddmyyyy","dmmyyyy","dmyyyy"]:
                if len(liststr)>=1:
                    dy=liststr[0]
                if len(liststr)>=2:
                    mo=liststr[1]
                if len(liststr)>=3:
                    yr=liststr[2]
            elif formatin in ["yyddmm","yyddm","yydmm","yydm","yyyyddmm","yyyyddm","yyyydmm","yyyydm"]:
                if len(liststr)>=1:
                    yr=liststr[0]
                if len(liststr)>=2:
                    dy=liststr[1]
                if len(liststr)>=3:
                    mo=liststr[2]
            elif formatin in ["yymmdd","yymdd","yymmd","yymd","yyyymmdd","yyyymdd","yyyymmd","yyyymd"]:
                if len(liststr)>=1:
                    yr=liststr[0]
                if len(liststr)>=2:
                    mo=liststr[1]
                if len(liststr)>=3:
                    dy=liststr[2]
            elif formatin=="yyyyddd":
                if len(liststr)>=1:
                    yr=liststr[0]
                if len(liststr)>=2:
                    dy=liststr[1]
                if len(dy)>0 and numfuncs.is_int(dy):
                    ndy=int(dy)
                    if ndy>0:
                        isleap=is_year_leap(int(yr))
                        n1=0
                        for i in range(12):
                            if i==1 and isleap:
                                n2 = dayspermonth[12]
                            else:
                                n2 = dayspermonth[i]
                            if ndy<=(n1+n2):
                                mo=str(i+1)
                                ndy -= n1
                                dy=str(ndy)
                                break
                            n1 += n2
            else:
                raise ValueError("unknown date format supplied: " + formatin)
        elif formatin in ["ddmmmyyyy", "ddmmmyy"]:
            if len(month_name_used)>0:
                # must have month
                mo=month_name_used
                dy=datein[:2]
                yr=datein[(datein.find(month_name_used)+len(month_name_used)):]
        elif formatin in ["yyyymmmdd", "yymmmdd"]:
            if len(month_name_used)>0:
                # must have month
                mo=month_name_used
                yr=datein[:datein.find(month_name_used)]
                dy=datein[(datein.find(month_name_used)+len(month_name_used)):]
        elif "*" in formatin:
            if formatin.endswith("yyyy"):
                yr = datein[-4:]
                if formatin.startswith("*dmm"):
                    mo=datein[-6:-4]
                    if len(datein)==7:
                        dy=datein[:1]
                    else:
                        dy=datein[:2]
                elif formatin.startswith("*mdd"):
                    dy=datein[-6:-4]
                    if len(datein)==7:
                        mo=datein[:1]
                    else:
                        mo=datein[:2]
                elif formatin.startswith("dd*m"):
                    dy=datein[:2]
                    if len(datein)==7:
                        mo=datein[-5:-4]
                    else:
                        mo=datein[-6:-4]
                elif formatin.startswith("mm*d"):
                    mo=datein[:2]
                    if len(datein)==7:
                        dy=datein[-5:-4]
                    else:
                        dy=datein[-6:-4]
        elif formatin in ["mmddyy","mmddyyyy","mmdyy","mmdyyyy"]:
            n1=len(datein)
            if n1<=2:
                mo=datein
            elif n1==3:
                mo=datein[:2]
                dy=datein[2:]
            elif n1>=8:
                mo=datein[:2]
                dy=datein[2:4]
                yr=datein[4:8]
            elif n1>=4:
                if "mdy" in formatin:
                    mo=datein[:2]
                    dy=datein[2:3]
                    yr=datein[3:]
                else:
                    mo=datein[:2]
                    dy=datein[2:4]
                    if n1>4:
                        yr=datein[4:]
                if formatin.endswith("dyy"):
                    if len(yr)>2:
                        yr=yr[:2]
                elif len(yr)>4:
                    yr=yr[:4]
                if "mdy" in formatin and len(dy)>1:
                    dy=dy[1:2]
        elif formatin in ["mddyy","mddyyyy","mdyy","mdyyyy"]:
            n1=len(datein)
            if n1==1:
                mo=datein
            elif n1==2:
                mo=datein[:1]
                dy=datein[1:]
            elif n1>=8:
                mo=datein[:2]
                dy=datein[2:4]
                yr=datein[4:8]
            elif n1>=3:
                if "mdy" in formatin:
                    mo=datein[:1]
                    dy=datein[1:2]
                    yr=datein[2:]
                else:
                    mo=datein[:1]
                    dy=datein[1:3]
                    if n1>3:
                        yr=datein[3:]
                if formatin.endswith("dyy"):
                    if len(yr)>2:
                        yr=yr[:2]
                elif len(yr)>4:
                    yr=yr[:4]
                if "mdy" in formatin and len(dy)>1:
                    dy=dy[1:2]
        elif formatin in ["ddmmyy","ddmmyyyy","ddmyy","ddmyyyy"]:
            n1=len(datein)
            if n1<=2:
                dy=datein
            elif n1==3:
                dy=datein[:2]
                mo=datein[2:]
            elif n1>=8:
                dy=datein[:2]
                mo=datein[2:4]
                yr=datein[4:8]
            elif n1>=4:
                dy=datein[:2]
                if "dmy" in formatin:
                    mo=datein[2:3]
                    yr=datein[3:]
                else:
                    mo=datein[2:4]
                    if n1>4:
                        yr=datein[4:]
                if formatin.endswith("myy"):
                    if len(yr)>2:
                        yr=yr[:2]
                elif len(yr)>4:
                    yr=yr[:4]
        elif formatin in ["dmmyy","dmmyyyy","dmyy","dmyyyy"]:
            n1=len(datein)
            if n1==1:
                dy=datein
            elif n1==2:
                dy=datein[:1]
                mo=datein[1:]
            elif n1>=8:
                dy=datein[:2]
                mo=datein[2:4]
                yr=datein[4:8]
            elif n1>=3:
                dy=datein[:1]
                if "dmy" in formatin:
                    mo=datein[1:2]
                    yr=datein[2:]
                else:
                    mo=datein[1:3]
                    if n1>4:
                        yr=datein[3:]
                if formatin.endswith("myy"):
                    if len(yr)>2:
                        yr=yr[:2]
                elif len(yr)>4:
                    yr=yr[:4]
        elif formatin in ["yyddmm","yyddm","yydmm","yydm"]:
            n1=len(datein)
            if n1<=2:
                yr=datein
            elif n1==3:
                yr=datein[:2]
                dy=datein[2:]
            elif n1>=8:
                yr=datein[:4]
                dy=datein[4:6]
                mo=datein[6:8]
            elif n1>=4:
                yr=datein[:2]
                if "ydm" in formatin:
                    dy=datein[2:3]
                    mo=datein[3:]
                else:
                    dy=datein[2:4]
                    if n1>4:
                        mo=datein[4:]
                if formatin.endswith("dm"):
                    if len(mo)>1:
                        mo=mo[:1]
        elif formatin in ["yyyyddmm","yyyyddm","yyyydmm","yyyydm"]:
            n1=len(datein)
            if n1<=4:
                yr=datein
            elif n1==5:
                yr=datein[:4]
                mo=datein[4:]
            elif n1>=8:
                yr=datein[:4]
                dy=datein[4:6]
                mo=datein[6:8]
            elif n1>=6:
                yr=datein[:4]
                if "ydm" in formatin:
                    dy=datein[4:5]
                    mo=datein[5:]
                else:
                    dy=datein[4:6]
                    if n1>6:
                        mo=datein[6:]
                if formatin.endswith("dm"):
                    if len(mo)>1:
                        mo=mo[:1]
        elif formatin in ["yymmdd","yymmd","yymdd","yymd"]:
            n1=len(datein)
            if n1<=2:
                yr=datein
            elif n1==3:
                yr=datein[:2]
                mo=datein[2:]
            elif n1>=8:
                yr=datein[:4]
                mo=datein[4:6]
                dy=datein[6:8]
            elif n1>=4:
                yr=datein[:2]
                if "ymd" in formatin:
                    mo=datein[2:3]
                    dy=datein[3:]
                else:
                    mo=datein[2:4]
                    if n1>4:
                        dy=datein[4:]
                if formatin.endswith("md"):
                    if len(dy)>1:
                        dy=dy[:1]
        elif formatin in ["yyyymmdd","yyyymmd","yyyymdd","yyyymd"]:
            n1=len(datein)
            if n1<=4:
                yr=datein
            elif n1==5:
                yr=datein[:4]
                mo=datein[4:]
            elif n1>=8:
                yr=datein[:4]
                mo=datein[4:6]
                dy=datein[6:8]
            elif n1>=6:
                yr=datein[:4]
                if "ymd" in formatin:
                    mo=datein[4:5]
                    dy=datein[5:]
                else:
                    mo=datein[4:6]
                    if n1>6:
                        dy=datein[6:]
                if formatin.endswith("md"):
                    if len(dy)>1:
                        dy=dy[:1]
        elif formatin=="yyyyddd":
            n1=len(datein)
            if n1<=4:
                yr=datein
            elif n1==7:
                yr=datein[:4]
                dy=datein[4:]
            isleap=is_year_leap(int(yr))
            if len(dy)>0 and numfuncs.is_int(dy):
                ndy=int(dy)
                if ndy>0:
                    n1=0
                    for i in range(12):
                        if i==1 and isleap:
                            n2 = dayspermonth[12]
                        else:
                            n2 = dayspermonth[i]
                        if ndy<=(n1+n2):
                            mo=str(i+1)
                            ndy -= n1
                            dy=str(ndy)
                            break
                        n1 += n2
        else:
            raise ValueError("unknown date format supplied: " + formatin)

        if len(yr)==2 and numfuncs.is_int(yr):
            nyr=int(yr)
            str1= get_current_iso_datetime()
            n1=20
            if not str1.startswith("notok:") and len(str1)>=4:
                str1=str1[:2]
                if numfuncs.is_int(str1):
                    n1=int(str1)
            if prior_yr_min<= nyr <=prior_yr_max:
                yr= str(n1-1) + yr
            else:
                yr= str(n1) + yr
        if numfuncs.is_int(yr):
            nyr=int(yr)
        if numfuncs.is_int(dy):
            ndy=int(dy)
        if len(mo)>0:
            if has_long_month:
                nmo= int(hash_month_longnames[mo])
            elif has_short_month:
                nmo= int(hash_month_names[mo])
            elif numfuncs.is_int(mo):
                nmo=int(mo)

        if nyr<=0:
            raise ValueError("year is less than 1: " + str(nyr))

        if 1<= nmo <=12:
            if nmo==2:
                if isleap:
                    n1=29
                else:
                    n1=28
            else:
                n1=dayspermonth[nmo-1]
            if ndy>n1:
                raise ValueError("days are greater than month max. Month=" + str(nmo) + ",days=" + str(ndy))
        elif nmo<=0:
            raise ValueError("month is less than 1: " + str(nmo))
        elif nmo>12:
            raise ValueError("month is greater than 12: " + str(nmo))

        if ndy<=0:
            raise ValueError("day is less than 1: " + str(ndy))
        if ndy>31:
            raise ValueError("day is greater than 31: " + str(ndy))

        yr=str(nyr)
        mo=str(nmo)
        dy=str(ndy)
        if len(yr)<4:
            if len(yr)==1:
                yr="000" + yr
            elif len(yr)==2:
                yr="00" + yr
            elif len(yr)==3:
                yr="0" + yr
        if len(mo)==1:
            mo="0"+mo
        if len(dy)==1:
            dy="0"+dy
        result= yr + mo + dy
        if detectfmt:
            result += "(" + formatin + ")"
    except (RuntimeError,ValueError,OSError) as err:
        result="notok:" + str(err)
    return result

def is_date_format(datein:str,formatin:str) -> bool:
    """
    Determines if date string is in specified format. 
    Time portions should be removed prior to sending into this method.
    Four delimiters in date part will be automatically detected: ( - / _ . )
    datein: incoming date string without time part. 
    formatin: required 
        mmddyy, mmdyy, mdyy, mmddyyyy, mmdyyyy, mdyyyy, 
        ddmmyy, ddmyy, dmyy, ddmmyyyy, ddmyyyy, dmyyyy,
        yymmdd, yymmd, yymd, yyyymmdd, yyyymmd, yyyymd, 
        yyyyddd (3 digit day number within year), 
        yyyyMMMdd, ddMMMyyyy (MMM = 3 letter month title like 'JAN'),
        'MONTHdd,yyyy', 'ddMONTH,yyyy', yyyyMONTHdd, ddMONTHyyyy, yyMONTHdd, ddMONTHyy (MONTH full title),
        *dmmyyyy, mm*dyyyy, *mddyyyy, dd*myyyy (*= can be 1 or 2 characters)
    With these formats, incoming string must have all characters required so for mmddyyyy there must be 
    8 characters meaning 1122011 fails but 01122011 is good.
    Leading title of day is removed like for Wednesday, March 14, 2001 which will be changed to 
    March 14, 2001 and then will match formatin of MONTHdd,yyyy since spaces are removed
    Returns - bool True/False
    """


    is_date_fmt:bool=False
    result:str=""
    try:
        result= convert_date_to_iso(datein,formatin)
        if len(result)>0 and not result.startswith("notok:"):
            is_date_fmt=True
    except (RuntimeError,ValueError,OSError) as err:
        print("ERROR:" + str(err))
    return is_date_fmt
