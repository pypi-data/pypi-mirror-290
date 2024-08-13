#!/usr/bin/env python
"""
Class definition of Transform and its child Op, with functions

Functions to read and write transforms in text file, pre-process 
transforms to make lists of lookup dicts used, 
as well as fields referenced.
"""

__all__ = ['Op',
           'Transform',
           'read_transforms_from_file',
           'write_transforms_to_file',
           'extract_lookup_titles',
           'set_lookup_fields',
           'extract_refs',
           ]
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240721'


from ..processing import numfuncs


class Op:
    """
    Operation (Op) for transforms. 
    
    Each Op has a title which is the name of the function. 
    It specifies the function and its category along with several possible 
    parameters (Param1, Param2, Param3) that depend on the specific 
    function. 
    """

    title:str
    category:str
    param1:str
    param2:str
    param3:str
    order:int = -1
    p1list:list
    p2list:list
    p3list:list
    def __init__(self, title:str, param1:str="", param2:str="", param3:str="", order:int=-1):
        self.title=title
        self.category=""
        self.param1=param1
        self.param2=param2
        self.param3=param3
        self.order= order
        self.p1list=[]
        self.p2list=[]
        self.p3list=[]

class Transform:
    """
    Transform object for modifying source field value

    A transform contains a sequence of operations that may include 
    conditional testing of values and referenced fields. It operates on the 
    field whose name is the title of the transform. 
    This field may be a source data 
    field or an enrichment field added to the output record. 
    """

    title:str
    ops:list

    def __init__(self, title:str):
        self.title=title
        self.ops=[]

    def get_json(self, add_lf:bool, add_quote:bool):
        """
        Get JSON string of transform properties

        Constructs a JSON string of the transform. 
        add_lf: whether to add line feed at ends of each JSON property (default false)
        add_quote: whether to enclose keys and values in double quotes (default false)
        """

        lf:str = ""
        dq:str = ""
        result:str = ""
        lc:str = "{"
        rc:str = "}"
        c:str = ","

        try:
            if add_lf:
                lf= "\n"

            if add_quote:
                dq= "\""
            result= lc + dq + "transform" + dq + ":["
            result += lc + dq + "title" + dq + ":" + dq + self.title + dq + rc + lf
            result += c + lc + dq + "ops" + dq + ":[" + lf
            for i in range(len(self.ops)):
                if i > 0:
                    result += c

                result += lc + dq + "title" + dq + ":" + dq + self.ops[i].title + dq
                result += c + dq + "order" + dq + ":" + dq + str(self.ops[i].order) + dq
                result += c + dq + "param1" + dq + ":" + dq + self.ops[i].param1 + dq
                result += c + dq + "param2" + dq + ":" + dq + self.ops[i].param2 + dq
                result += c + dq + "param3" + dq + ":" + dq + self.ops[i].param3 + dq
                result += rc + lf

            result += "]" + rc + lf   # close ops
            result += "]" + lf  # close transform
            result += rc+ lf  # close object
        except RuntimeError as err:
            result="error:"+ str(err)
        return result


def read_transforms_from_file(file_uri:str) -> list:
    """
    Read transform file. Reads text file containing JSON formatted specification of transforms. 
    file_uri: file must exist and be accessible. Otherwise, returned title will begin with notok: and have error message    
    Returns transforms list of Transform objects. If error occurs then transforms[0].title will start with notok:
    """
    err_msg:str=""
    jstr:str=""
    dq:str="\""
    curstr:str=""
    tarray:list=[]
    oparray:list=[]
    tobj:Transform
    opobj:Op
    transforms:list=[]
    hash_transforms:dict={}
    try:
        file_uri=file_uri.strip()
        if len(file_uri)==0:
            raise ValueError("missing file_uri")

        with open(file_uri,"r",encoding="utf-8") as f:
            jstr=f.read()
        jstr=jstr.replace("\r\n","").replace("\r","").replace("\n","")
        jstr=jstr.replace(dq,"")
        if "{transform:[" not in jstr:
            raise ValueError("no transforms found in read file lines")
        tarray= jstr.split("{transform:[")
        for s in tarray:
            jstr=s
            if jstr.startswith(","):
                jstr=jstr[1:]
            if jstr.endswith(","):
                jstr=jstr[:-1]
            if jstr.endswith("}"):
                jstr=jstr[:-1]
            if jstr.endswith("]"):
                jstr=jstr[:-1]
            if "{title:" in jstr:
                jstr=jstr[jstr.find("{title:")+7:]
                curstr=jstr[:jstr.find("}")]
                curstr=curstr.strip()
                jstr=jstr[jstr.find("}")+1:]
                if jstr.startswith(","):
                    jstr=jstr[1:]
                if len(curstr)==0:
                    raise ValueError("transform title is empty")
                if curstr.lower() in hash_transforms:
                    raise ValueError("duplicate transform title: " + curstr.lower())
                tobj=Transform(curstr)
                if "{ops:[" in jstr:
                    jstr=jstr[jstr.find("{ops:[")+6:]
                    if jstr.endswith(","):
                        jstr=jstr[:-1]
                    if jstr.endswith("}"):
                        jstr=jstr[:-1]
                    if jstr.endswith("]"):
                        jstr=jstr[:-1]
                    oparray.clear()
                    if "{title:" in jstr:
                        oparray= jstr.split("{title:")
                        for s1 in oparray:
                            if ",order:" in s1:
                                curstr=s1[:s1.find(",order:")]
                                jstr= s1[s1.find(",order:")+1:]
                                if jstr.endswith(","):
                                    jstr=jstr[:-1]
                                if jstr.endswith("}"):
                                    jstr=jstr[:-1]
                                if jstr.startswith(","):
                                    jstr=jstr[1:]
                                if len(curstr)>0:
                                    opobj=Op(curstr)
                                    tobj.ops.append(opobj)
                                    if "order:" in jstr:
                                        curstr=jstr[jstr.find("order:")+6:]
                                        curstr=curstr[:curstr.find(",")]
                                        if numfuncs.is_int(curstr):
                                            opobj.order= int(curstr)
                                    if "param1:" in jstr:
                                        curstr=jstr[jstr.find("param1:")+7:]
                                        if ",param" in curstr:
                                            curstr=curstr[:curstr.find(",param")]
                                        opobj.param1=curstr
                                    if "param2:" in jstr:
                                        curstr=jstr[jstr.find("param2:")+7:]
                                        if ",param" in curstr:
                                            curstr=curstr[:curstr.find(",param")]
                                        opobj.param2=curstr
                                    if "param3:" in jstr:
                                        curstr=jstr[jstr.find("param3:")+7:]
                                        opobj.param3=curstr
                hash_transforms[tobj.title.lower()]= len(transforms)
                transforms.append(tobj)
    except (RuntimeError, ValueError, OSError) as err:
        err_msg= "notok:" + str(err)
        transforms.clear()
        transforms.append(Transform(err_msg))
    return transforms


def write_transforms_to_file(file_uri:str, transforms:list) -> str:
    """
    Write transform file

    Writes text file containing JSON formatted specification of transforms. 
    file_uri: file must exist and be accessible. 
    transforms: list of Transform object to write to file in JSON
    Returns message that starts with notok: if error occurs.
    """
    err_msg:str=""
    delim:str=""
    try:
        file_uri=file_uri.strip()
        if len(file_uri)==0:
            raise ValueError("missing file_uri")
        if len(transforms)==0:
            raise ValueError("missing transforms")

        with open(file_uri, "w", encoding="utf-8") as f:
            for i in range(len(transforms)):
                if not isinstance(transforms[i], Transform):
                    raise ValueError("object in transforms list is not type=Transform")
                if i>0:
                    delim=","
                else:
                    delim=""
                f.write(delim + transforms[i].get_json(True,True))
    except (RuntimeError, ValueError, OSError) as err:
        err_msg= "notok:" + str(err)
    return err_msg


def extract_lookup_titles(transforms:list) -> list:
    """
    Extract list of lookup dict titles used in transforms
    transforms: list of Transform objects
    Returns list of lookup dict titles. If error occurs, 0th entry will have 
    title starting with notok:
    """

    lkupdicts:list=[]
    hash_lkupdicts:dict={}
    parm_str:str
    try:
        if len(transforms)==0:
            return lkupdicts
        for t in transforms:
            if not isinstance(t, Transform):
                raise ValueError("object in transforms list is not type=Transform")
            for op in t.ops:
                if not isinstance(op, Op):
                    raise ValueError("object in transform " + t.title + " Ops is not type=Op")
                if op.title.lower().startswith("lookup"):
                    parm_str= op.param1.lower()
                    if len(parm_str)>0 and parm_str not in hash_lkupdicts:
                        lkupdicts.append(parm_str)
                        hash_lkupdicts[parm_str]= len(lkupdicts)-1
    except (RuntimeError, ValueError, OSError) as err:
        lkupdicts.insert(0,"notok:" + str(err))
    return lkupdicts


def set_lookup_fields(transforms:list) -> list:
    """
    Finds fields set in param2,param3 of tranform Ops for lookup
    transforms: list of Transform objects
    Returns new transform collection with lookup Ops having fields in 
    param2,param3 extracted into p2list,p3list. 
    """

    parm_str:str
    fld:str=""
    atemp:list=[]
    try:
        if len(transforms)==0:
            return transforms
        for t in transforms:
            if not isinstance(t, Transform):
                raise ValueError("object in transforms list is not type=Transform")
            for op in t.ops:
                if not isinstance(op, Op):
                    raise ValueError("object in transform " + t.title + " Ops is not type=Op")
                if op.title.lower().startswith("lookup"):
                    parm_str= op.param2.lower()
                    if len(parm_str)>0:
                        atemp= parm_str.split("|")
                        for s in atemp:
                            fld=s.strip()
                            if len(fld)>0:
                                op.p2list.append(fld)
                    parm_str= op.param3.lower()
                    if len(parm_str)>0:
                        atemp= parm_str.split("|")
                        for s in atemp:
                            fld=s.strip()
                            if len(fld)>0:
                                op.p3list.append(fld)
    except (RuntimeError, ValueError, OSError):
        pass
    return transforms


def extract_refs(transforms:list) -> dict:
    """
    Extract referenced fields used in transforms
    transforms: list of Transform objects
    Returns dictionary with keys= field titles and thier values=number instances used. If error occurs, there will be a
      key starting with notok:<error reason>
    """

    hash_fields:dict={}
    parm_str:str=""
    parm_str2:str=""
    optitle:str=""
    try:
        if len(transforms)==0:
            return hash_fields
        for t in transforms:
            if not isinstance(t, Transform):
                raise ValueError("object in transforms list is not type=Transform")
            for op in t.ops:
                optitle= op.title.lower()
                if not isinstance(op, Op):
                    raise ValueError("object in transform " + t.title + " Ops is not type=Op")
                if optitle.endswith("ref") or optitle.endswith("refs"):
                    parm_str= op.param1.lower()
                    if len(parm_str)>0:
                        if parm_str not in hash_fields:
                            hash_fields[parm_str]= 0
                        hash_fields[parm_str] += 1
                    if optitle.endswith("refs"):
                        parm_str= op.param2.lower()
                        if len(parm_str)>0:
                            if parm_str not in hash_fields:
                                hash_fields[parm_str]= 0
                            hash_fields[parm_str] += 1
                        parm_str= op.param3.lower()
                        if len(parm_str)>0:
                            if parm_str not in hash_fields:
                                hash_fields[parm_str]= 0
                            hash_fields[parm_str] += 1
                elif optitle=="settofreqlist":
                    parm_str= op.param3.lower()
                    if len(parm_str)>0:
                        if parm_str not in hash_fields:
                            hash_fields[parm_str]= 0
                        hash_fields[parm_str] += 1
                elif optitle=="lookup":
                    parm_str= op.param2.lower()
                    if len(parm_str)>0:
                        parm_str2=""
                        if "|" in parm_str:
                            parm_str2= parm_str[(parm_str.find("|")+1):]
                            parm_str= parm_str[:parm_str.find("|")]
                        if parm_str not in hash_fields:
                            hash_fields[parm_str]= 0
                        hash_fields[parm_str] += 1
                        if len(parm_str2)>0:
                            if parm_str2 not in hash_fields:
                                hash_fields[parm_str2]= 0
                            hash_fields[parm_str2] += 1
    except (RuntimeError, ValueError, OSError) as err:
        hash_fields["notok:" + str(err)]=0
    return hash_fields
