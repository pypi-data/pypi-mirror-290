#!/usr/bin/env python
"""
Refinery to process analysis and transforms for full data set
"""


__all__ = ['do_refine']
__version__ = "1.0"
__author__ ="Geoffrey Malafsky"
__email__ = "gmalafsky@technikinterlytics.com"
__date__ = "20240715"


from ..transforms import transform, lookup
from . import recfuncs, field, exectransform, numfuncs, datefuncs

DQ:str= "\""
LF:str="\n"


def do_refine(outfields:list, transforms:list, settings:dict, lookup_dicts:list, srcfields:list, srcrecs:list) -> list:
    """
    Refines a set of data records to correct, normalize, and enrich

    outfields-list of Field objects for output fields that will be assigned values in each output record. 
        As Field objects, each can specify rules for datatype and format that will be applied after transforms 
        (if defined for the field) or passing through original value (if no transform defined).
        - title: field name
        - datatype: int, real, bool, date, string. For date, there should be an entry specifying the format otherwise it is set to ISO yyyyMMdd
        - fmt_strlen: integer number of characters (\>0) if a fixed size is required. Ignored if \< 0
        - fmt_strcase: (upper, lower, empty)
        - fmt_strcut: (front, back, empty). Side to cut characters from if it is larger than specified fmt_strlen. Default is back.
        - fmt_strpad: (front, back, empty). Side to add characters to if it is smaller than specified fmt_strlen. Default is back.
        - fmt_strpadchar: single character or character alias (-space-, -fslash-, -bslash-, -tab-). Character to add if needed to make too small string meet specified fmt_strlen. Default is _
        - fmt_decimal: number of decimal digits (0-N). Ignored if \< 0
        - fmt_date:
            + without time part- yyyymmdd, yymmdd, yyyyddmm, yyddmm, mmddyyyy, mmddyy, ddmmyyyy, ddmmyy, 
            + (mmm= month abbreviation like Jan) yyyymmmdd, yyyyddmmm, ddmmmyyyy, ddmmmyy
            + (month= full month name like January) yyyymonthdd, yyyyddmonth, ddmonthyyyy, ddmonthyy
            + with time part: suffix to above date formats as- Thhmmss, Thhmm, Thh like mmddyyyyThhmm for 11282024T1407 or 11/28/2024T14:07
            + (S is space) Shhmmss, Shhmm, Shh like 11-28-2024 14:07
            + with time zone: if time zone is required at end of time part add suffix Z like mmddyyyyThhmmZ 11282024T1407

    transforms-list of transform objects

    settings-dictionary with various settings. required: 
        delim- (delimiter for parsing records) as comma, tab, pipe, caret, hyphen
    	delim_out- optional specified delimiter for output records (default is to use delim) as comma, tab, pipe, caret, hyphen
    	is_quoted - bool whether some field values are enclosed in double quotes to allow delimiter within the field value. Default is True.
    	has_header - bool whether first used line is delimited field titles. Default is true
    	use_comment - bool whether to use comment lines (start with # or //) or ignore them. Default is False so they are ignored.
    	normalize- bool whether to apply datatype and format rules to output field value. Default is true. 
            If datatype is int or real and field value is not numeric then the value will be set to 0 for int and 0.00 for real. 
    		If datatype is bool and field value is neither true nor false then value will be set to false. 
    		If datatype is date and field value is not in date format then value will be set to empty string.
    	embed_delim- new character(s) for replacing delim when a field contains delim. Default is a space.
    
    lookup_dicts-list of LookUpDict objects. These should be made from files or arrays prior to invoking this method
    
    srcfields-list of field objects in order correlated to input records when parsed using delimiter specified in settings
    
    srcrecs-list of strings each of which is one input record. Default is to ignore empty lines and those 
        beginning with # or // as comments. This can be overidden with the setting useComments. 
        If the setting hasHeader is True (which is default) then the first used line must be a delimited line of field titles.
    
    RETURNS outrecs as list of Refined data records including header of delimited fields names. If error, 0th entry will start with notok:
    """

    txt:str=""
    txt1:str=""
    delim:str=""
    delimchar:str=""
    delimout:str=""
    delimoutchar:str=""
    linein:str=""
    fldval:str=""
    lineout:str=""
    embed_delim:str=" "
    hashdr:bool=True
    usecomment:bool=False
    isquoted:bool=True
    iscomment:bool=False
    normalize:bool=True
    doparseerror:bool=False
    lrec:int=0
    lcmt:int=0
    lemp:int=0
    nf:int=-1
    nt:int=-1
    n1:int=-1
    outrecs:list=[]
    keys:list=[]
    hash_lookups:dict={}
    hash_srcfields:dict={}
    hash_outfields:dict={}
    hash_out_to_src:dict={}
    hash_src_to_out:dict={}
    hash_out_to_transform:dict={}
    src_values:list=[]
    try:
        if outfields is None or not isinstance(outfields, list):
            raise ValueError("no outfields")
        if srcfields is None or not isinstance(srcfields, list):
            raise ValueError("no srcfields")
        if srcrecs is None or not isinstance(srcrecs, list):
            raise ValueError("no srcrecs")
        if settings is None or not isinstance(settings, dict):
            settings={}
        if lookup_dicts is None or not isinstance(lookup_dicts, list):
            lookup_dicts=[]
        if transforms is None or not isinstance(transforms, list):
            transforms=[]
        keys= list(settings)
        for i in range(len(keys)):
            txt=keys[i].lower()
            txt1= str(settings[keys[i]]).lower()
            if txt in ("isquoted","is_quoted"):
                isquoted = txt1=="true"
            elif txt in ("hasheader","has_header"):
                hashdr = txt1=="true"
            elif txt in ("use_comment","usecomment"):
                usecomment = txt1=="true"
            elif txt=="normalize":
                normalize = txt1=="true"
            elif txt=="delim":
                delim=txt1
                delimchar= recfuncs.delim_get_char(delim)
            elif txt in ("delim_out","delimout"):
                delimout=txt1
                delimoutchar= recfuncs.delim_get_char(delimout)
            elif txt in ("embed_delim","embeddelim"):
                embed_delim= txt1 if len(txt1)>0 else " "

        if len(delim)==0:
            raise ValueError("no delim specified")
        if len(delimchar)==0:
            raise ValueError("unrecognized delim: " + delim)
        if len(outfields)==0:
            raise ValueError("no output fields specified")
        if len(srcfields)==0:
            raise ValueError("no source fields specified")
        if len(srcrecs)==0:
            raise ValueError("no data records supplied")

        if len(delimout)==0 or len(delimoutchar)==0:
            delimoutchar= delimchar
        for i in range(len(lookup_dicts)):
            if not isinstance(lookup_dicts[i], lookup.LookUpDict):
                raise ValueError("lookup_dict " + str(i) + " is not a LookUpDict object")
            txt= lookup_dicts[i].title.lower().strip()
            if len(txt)==0:
                raise ValueError("lookup_dict " + str(i) + " has empty title")
            elif txt in hash_lookups:
                raise ValueError("lookup_dict " + str(i) + " has duplicate title")
            hash_lookups[txt]=i
        for i in range(len(srcfields)):
            if not isinstance(srcfields[i], field.Field):
                raise ValueError("source field " + str(i) + " is not a Field object")
            txt= srcfields[i].title.lower().strip()
            if len(txt)==0:
                raise ValueError("source field " + str(i) + " has empty title")
            elif txt in hash_srcfields:
                raise ValueError("source field " + str(i) + " has duplicate title")
            hash_srcfields[txt]=i
            txt= srcfields[i].parse_error_action.lower().strip()
            if txt in ["-use-","-ignore-",""]:
                srcfields[i].parse_error_action=txt
        for i in range(len(outfields)):
            if not isinstance(outfields[i], field.Field):
                raise ValueError("output field " + str(i) + " is not a Field object")
            txt= outfields[i].title.lower().strip()
            if len(txt)==0:
                raise ValueError("output field " + str(i) + " has empty title")
            elif txt in hash_outfields:
                raise ValueError("output field " + str(i) + " has duplicate title")
            hash_outfields[txt]=i
            txt1= outfields[i].mapto.lower().strip()
            if txt in hash_srcfields:
                hash_out_to_src[i]=hash_srcfields[txt]
                hash_src_to_out[hash_srcfields[txt]]=i
            elif txt1 in hash_srcfields:
                hash_out_to_src[i]=hash_srcfields[txt1]
                hash_src_to_out[hash_srcfields[txt1]]=i
            else:
                hash_out_to_src[i]=-1
            txt= outfields[i].fmt_strcase.lower().strip()
            outfields[i].fmt_strcase = txt if txt in ("upper","lower") else ""
            txt= outfields[i].fmt_strcut.lower().strip()
            outfields[i].fmt_strcut = "front" if txt in ("front","left","start") else "back"
            txt= outfields[i].fmt_strpad.lower().strip()
            outfields[i].fmt_strpad = "front" if txt in ("front","left","start") else "back"
            txt= outfields[i].fmt_strpadchar.lower().strip()
            if len(txt)==0:
                outfields[i].fmt_strpadchar="_"
            elif txt in ("space","-space-"):
                outfields[i].fmt_strpadchar=" "
            elif txt in ("fslash","-fslash-"):
                outfields[i].fmt_strpadchar="/"
            elif txt in ("bslash","-bslash-"):
                outfields[i].fmt_strpadchar="\\"
            elif txt in ("tab","-tab-"):
                outfields[i].fmt_strpadchar="\t"
        for i in range(len(transforms)):
            if not isinstance(transforms[i], transform.Transform):
                raise ValueError("transforms " + str(i) + " is not a Transform object")
            txt= transforms[i].title.lower().strip()
            if len(txt)==0:
                raise ValueError("transforms " + str(i) + " has empty title")
            if txt in hash_outfields:
                hash_out_to_transform[hash_outfields[txt]]=i
            elif txt in hash_srcfields:
                if hash_srcfields[txt] in hash_src_to_out:
                    hash_out_to_transform[hash_src_to_out[hash_srcfields[txt]]]=i
            for j in range(len(transforms[i].ops)):
                if transforms[i].ops[j].title.lower().startswith("lookup"):
                    if transforms[i].ops[j].param1.lower() not in hash_lookups:
                        raise ValueError("unknown LookUpDict specified in transform " + str(i) + ", op " + str(j) + ": " + transforms[i].ops[j].param1)

        lineout=""
        for i in range(len(outfields)):
            if i>0:
                lineout += delimoutchar
            lineout += outfields[i].title
        outrecs.append(lineout)

        for i in range(len(srcrecs)):
            linein= srcrecs[i]
            if len(linein.strip())>0:
                txt= linein.lstrip()
                iscomment = txt.startswith("#") or txt.startswith("//")
                if iscomment:
                    lcmt += 1
                if usecomment or not iscomment:
                    lrec += 1
                    if lrec>1 or not hashdr:
                        if isquoted and DQ in linein:
                            src_values= recfuncs.split_quoted_line(linein, delimchar)
                            if len(src_values)>0 and src_values[0].startswith("notok:"):
                                raise ValueError("error splitting quoted line #rec=" + str(lrec) + ": " + src_values[0][6:])
                        else:
                            src_values= linein.split(delimchar)

                        lineout=""
                        for ifld in range(len(outfields)):
                            fldval=""
                            nf=hash_out_to_src[ifld]
                            doparseerror=True
                            if nf>=0:
                                if nf< len(src_values):
                                    fldval=src_values[nf]
                                elif srcfields[nf].parse_error_action=="-ignore-":
                                    doparseerror= False
                                elif srcfields[nf].parse_error_action=="-use-" or len(srcfields[nf].parse_error_action)==0:
                                    fldval="" # there is a parse error so we keep value empty and proceed to transforms and normalize
                                else:
                                    fldval= srcfields[nf].parse_error_action  # string value to assign
                                    doparseerror= False
                            else:
                                fldval="" # no mapped source

                            if ifld in hash_out_to_transform:
                                if nf< len(src_values) or doparseerror:
                                    nt= hash_out_to_transform[ifld]
                                    fldval= exectransform.do_transform(transforms[nt], fldval, outfields[ifld].datatype,
                                        hash_srcfields,
                                        src_values,
                                        lookup_dicts,
                                        hash_lookups
                                        )

                                    if fldval.startswith("notok:"):
                                        raise ValueError(fldval[6:])
                            # normalize if set to do so and either not a parsing error (no source field or has source value) or set to do parsing error
                            if normalize:
                                if nf<0 or nf< len(src_values) or doparseerror:
                                    if outfields[ifld].datatype=="string":
                                        if outfields[ifld].fmt_strlen>0:
                                            n1= len(fldval)- outfields[ifld].fmt_strlen
                                            if n1>0:
                                                if outfields[ifld].fmt_strcut=="front":
                                                    fldval= fldval[n1:]
                                                else:
                                                    fldval= fldval[:-n1]
                                            elif n1<0:
                                                if outfields[ifld].fmt_strpad=="front":
                                                    fldval= fldval.ljust(outfields[ifld].fmt_strlen,outfields[ifld].fmt_strpadchar)
                                                else:
                                                    fldval= fldval.rjust(outfields[ifld].fmt_strlen,outfields[ifld].fmt_strpadchar)
                                        if outfields[ifld].fmt_strcase=="upper":
                                            fldval= fldval.upper()
                                        elif outfields[ifld].fmt_strcase=="lower":
                                            fldval= fldval.lower()
                                    elif outfields[ifld].datatype=="int":
                                        if "." in fldval:
                                            fldval= fldval[:fldval.find(".")]
                                        if len(fldval)==0:
                                            fldval="0"
                                        else:
                                            fldval= numfuncs.is_int_get(fldval, "string", True)
                                            if fldval.startswith("false:"):
                                                fldval="0"
                                    elif outfields[ifld].datatype=="real":
                                        if len(fldval)==0:
                                            fldval="0.00"
                                        else:
                                            fldval= numfuncs.is_real_get(fldval, "string", True)
                                            if fldval.startswith("false:"):
                                                fldval="0.00"
                                            elif outfields[ifld].fmt_decimal>=0:
                                                if "." in fldval:
                                                    txt1=fldval[fldval.find(".")+1:]
                                                    txt=fldval[:fldval.find(".")]
                                                else:
                                                    txt=fldval
                                                    txt1=""
                                                n1= len(txt1)- outfields[ifld].fmt_decimal
                                                if outfields[ifld].fmt_decimal==0:
                                                    txt1=""
                                                elif n1>0:
                                                    txt1=txt1[:-n1]
                                                elif n1<0:
                                                    txt1=txt1.rjust(outfields[ifld].fmt_decimal,"0")
                                                fldval= txt + "." + txt1
                                    elif outfields[ifld].datatype=="bool":
                                        fldval= "true" if fldval.lower()=="true" else "false"
                                    elif outfields[ifld].datatype=="date":
                                        if len(outfields[ifld].fmt_date)>0:
                                            if not datefuncs.is_date_format(fldval, outfields[ifld].fmt_date):
                                                fldval=""

                            #check for embedded delimiter
                            if delimoutchar in fldval:
                                fldval= fldval.replace(delimoutchar, embed_delim)

                            if ifld>0:
                                lineout += delimoutchar
                            lineout += fldval

                        outrecs.append(lineout)
            else:
                lemp += 1

    except (RuntimeError, OSError, ValueError) as err:
        outrecs.insert(0,"notok:" + str(err))
    return outrecs
