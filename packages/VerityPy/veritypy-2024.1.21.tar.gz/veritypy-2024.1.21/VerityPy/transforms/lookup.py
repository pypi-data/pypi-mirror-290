#!/usr/bin/env python
"""
Lookup dictionary functions

Lookup dictionary object for transform processing. Transforms have an 
operation (Op) that allows assigning a value based on looking up 
the current value in a dictionary. 1, 2, 3 keys are allowed with 
the replacement value coming from the following column. This Op is in 
transform_types for category=assignment, function=lookup. 

The description of this function and how it uses the lookup is:

    Assigns a value from a lookup list based on matching values to keys where keys can use wildcards. 
    The match can be made to one, two, or three source fields in the record with field 1 always 
    the current value while fields 2 and 3 are optional if set in Param2. 
    Leave Param2 empty to use only 1 field as the match value. 
    All selected fields must match their respective conditions for a lookup result to be assigned. 
    The conditions and the result to assign are in an object for each list entry 
    with properties: key1, key2, key3, value defined as example 
    {'key1':'top*','key2':'*blue*','key3':'*left','value':'Orange'}. 
    Conditions can use front and/or back wildcard (*) like top*, *night, *state* to allow token matching. 
    To use multiple conditions for the same replacement value ( OR condition ), 
    enter them as separate list entries. 
    To use AND and NOT conditions, use special notations as delimiters: 
    top*-and-*night-not-*blue* which means a match requires both top* and *night be true 
    as well as no instances of the token blue. 

    Param1: title of list that has been pre-loaded into array of lists as part of initialization. 
    Param2: Fields 2 and 3 both of which are optional and if both supplied use 
    pipe to delimit as with color|position. 
    For this example, current value must start with top (key1 condition), the field color 
    must contain blue, and the field position must end with left. 
    All of these must be true for a match in which case the value of Orange is assigned.
"""


__all__ = ['LookUpRec',
           'LookUpDict',
           'make_lookups', 
           'make_lookup_from_list',
           ]
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240616'

from ..processing import recfuncs

class LookUpRec:
    """
    Record within a lookup dictionary

    Each lookup record has 1-3 keys with matching conditions. Each key value can use 
    wildcards at front and/or back. In addition, each key can have a combined condition 
    using more than one token joined using special notation for boolean AND and NOT conditions. 
    For example, a key might be top*-and-*food*-not-*juice which means the field value being 
    checked muct statisfy starting with 'top', containing 'food', and not ending with 
    'juice'. Therefore, each key is parsed into lists that are aligned:
    AND tokens and for each corresponding front_wild and back_wild lists. Similarly, NOT 
    tokens and wild lists. After parsing, key1_and is a list of tokens minus front and back 
    wildcards if they were supplied, and if so, they are in correlated lists key1_and_front_wild 
    and key1_and_back_wild.

    key1: single or combined value(s) to check
    key2: optional. single or combined value(s) to check
    key3: optional. single or combined value(s) to check
    key1_and: list of AND conditions for key1 (at least 1)
    key1_not: list of NOT conditions for key1 (0 or more)
    key2_and: optional. list of AND conditions for key2 (at least 1 if used)
    key2_not: optional. list of NOT conditions for key2 (0 or more)
    key3_and: optional. list of AND conditions for key3 (at least 1 if used)
    key3_not: optional. list of NOT conditions for key3 (0 or more)
    key1_and_front_wild: bool for key1_and entry if it had front wildcard *
    key1_and_back_wild: bool for key1_and entry if it had back wildcard *
    key1_not_front_wild: bool for key1_not entry if it had front wildcard *
    key1_not_back_wild: bool for key1_not entry if it had back wildcard *
    key2_and_front_wild: bool for key2_and entry if it had front wildcard *
    key2_and_back_wild: bool for key2_and entry if it had back wildcard *
    key2_not_front_wild: bool for key2_not entry if it had front wildcard *
    key2_not_back_wild: bool for key2_not entry if it had back wildcard *    
    key3_and_front_wild: bool for key3_and entry if it had front wildcard *
    key3_and_back_wild: bool for key3_and entry if it had back wildcard *
    key3_not_front_wild: bool for key3_not entry if it had front wildcard *
    key3_not_back_wild: bool for key3_not entry if it had back wildcard *
    result: string final value
    """

    key1:str
    key2:str
    key3:str
    key1_and: list
    key1_not: list
    key2_and: list
    key2_not: list
    key3_and: list
    key3_not: list
    key1_and_front_wild: list
    key1_and_back_wild: list
    key1_not_front_wild: list
    key1_not_back_wild: list
    key2_and_front_wild: list
    key2_and_back_wild: list
    key2_not_front_wild: list
    key2_not_back_wild: list
    key3_and_front_wild: list
    key3_and_back_wild: list
    key3_not_front_wild: list
    key3_not_back_wild: list
    result:str

    def __init__(self) -> None:
        self.key1=""
        self.key2=""
        self.key3=""
        self.key1_and=[]
        self.key1_not=[]
        self.key2_and=[]
        self.key2_not=[]
        self.key3_and=[]
        self.key3_not=[]
        self.key1_and_front_wild=[]
        self.key1_and_back_wild=[]
        self.key1_not_front_wild=[]
        self.key1_not_back_wild=[]
        self.key2_and_front_wild=[]
        self.key2_and_back_wild=[]
        self.key2_not_front_wild=[]
        self.key2_not_back_wild=[]
        self.key3_and_front_wild=[]
        self.key3_and_back_wild=[]
        self.key3_not_front_wild=[]
        self.key3_not_back_wild=[]
        self.result=""


class LookUpDict:
    """
    Dictionary with keys (either 1,2,3 field values) mapped to replacement value. The 
    keys can use wild cards and also special notations for AND and NOT conditions. 

    title: used in function 'lookup' to select which LookUpDict to use
    file_uri: URI to file. Empty if made from list object.
    is_case_sens: if false then all text changed to lowercase
    num_keys: integer number of keys used 1-3
    delim: delimiter (comma, pipe, tab, colon)
    fields: list of field titles which must correspond to columns in data set
    recs:list of LookUpRec objects
    """

    title:str
    file_uri:str
    is_case_sens:bool
    num_keys:int
    delim:str
    fields:list
    recs:list

    def __init__(self):
        self.title=""
        self.file_uri=""
        self.is_case_sens=False
        self.num_keys=-1
        self.delim=""
        self.fields=[]
        self.recs=[]


def make_lookups(lookups:list) -> dict:
    """
    Makes lookup dicts from files supplied in list of LookUpDict objects. 
    
    lookups: list of LookUpDict objects each of which must have its title, file_uri, num_keys. 
    delim and is_case_sens are optional. 
    The text file must have a header line as the first non-empty and non-comment (comment lines begin with either // or #) line. 
    Field names delimited by parameter 'delim'. 
    There must be num_keys + 1 fields in the header and each record. 
    The num_keys + 1 field is the result when a match occurs. 

    returns object with keys:
    dicts: list of LookUpDict objects made from supplied list with lists of fields and recs filled.
    hash: dictionary as hash table of LookUpDicts with key = each LookUpDict title and value= index in 'dicts' array
    """

    lkdict:LookUpDict
    lookup_dicts=[]
    hash_lookup_dicts={}
    try:
        for i in range(len(lookups)):
            try:
                lkdict=LookUpDict()
                if not isinstance(lookups[i],LookUpDict):
                    raise ValueError("not lookup dict index: " + str(i))
                lkdict=lookups[i]
                if len(lkdict.file_uri)==0:
                    raise ValueError('lookupdict missing fileuri at index: ' + str(i))
                if len(lkdict.title)==0:
                    raise ValueError('lookupdict missing title at index: ' + str(i))
                if len(lkdict.title)>80:
                    raise ValueError('lookupdict title too long: ' + str(lkdict.title))
                if lkdict.num_keys<1:
                    raise ValueError('lookupdict too few number keys: ' + str(lkdict.num_keys))
                if lkdict.num_keys>3:
                    raise ValueError('lookupdict too many number keys: ' + str(lkdict.num_keys))
                if len(lkdict.delim)==0:
                    raise ValueError('lookupdict missing delimiter at index: ' + str(i))

                lkdict= make_lookup_from_file(lkdict.title,
                                    lkdict.file_uri,
                                    lkdict.delim,
                                    lkdict.is_case_sens,
                                    lkdict.num_keys
                                    )

            except (RuntimeError, ValueError, OSError, TypeError) as err1:
                lkdict.title= "notok:" + str(err1)

            lookup_dicts.append(lkdict)
            if not lkdict.title.startswith("notok:"):
                hash_lookup_dicts[lkdict.title.lower()]=i

    except (RuntimeError,OSError) as err:
        print("ERROR:" + str(err))

    return {'dicts':lookup_dicts,'hash':hash_lookup_dicts}


def make_lookup_from_file(title:str,file_uri:str,delim:str,is_case_sens:bool,num_keys:int) -> LookUpDict:
    """
    Builds a LookUpDict from text file

    File will be read and columns extracted by splitting lines with delimiter. 
    Empty and comment (begins with # or //) lines are ignored. 
    First data containing line must contain delimited field names. 
    num_keys specifies how many columns will be used as keys (1-3) and then the next column will be used as value. 
    This number of columns must be present after splitting. 
    If double quote is in line then more precise (but slower) column separation will be used.
    LookupDict will have its fields and recs lists filled.

    Returns LookUpDict object whose title will start with notok: if there is an error.
    """

    lkdict:LookUpDict= LookUpDict()
    lkrec:LookUpRec
    err_msg:str=""
    nline:int=0
    cols:list=[]
    delim_char:str=""
    dq:str= "\""
    try:
        if len(title)==0:
            raise ValueError("title is empty")
        if num_keys<=0 or num_keys>3:
            raise ValueError("num_keys is not 1-3: " + str(num_keys))
        if len(delim)==0:
            raise ValueError("delim is empty")
        delim_char= recfuncs.delim_get_char(delim)
        lkdict.title=title
        lkdict.num_keys=num_keys
        lkdict.is_case_sens=is_case_sens
        lkdict.file_uri=file_uri
        lkdict.delim=delim

        with open(file_uri, "r", encoding="utf-8") as f:
            for line in f:
                if line is None:
                    break
                line= line.strip()
                if line.endswith("\n"):
                    line=line[:len(line)-1]
                if len(line)>0 and not line.startswith("#") and not line.startswith("//"):
                    nline += 1
                    if nline==1:
                        if line.find(delim_char)<1:
                            raise ValueError("first data line does not contain delimiter: " + delim_char)
                        if line.find(dq)>-1:
                            line=line.replace(dq,'')
                        lkdict.fields= line.split(delim_char)
                        if len(lkdict.fields)< (num_keys+1):
                            raise ValueError("too few fields found with delim=" + delim_char + ",#fields=" + len(lkdict.fields)\
                                              + "/" + str(num_keys+1))
                    else:
                        if line.find(dq)>-1:
                            cols=recfuncs.split_quoted_line(line,delim_char)
                            if len(cols)>0 and cols[0].startswith("notok:"):
                                raise RuntimeError("error splitting quoted string: " + cols[0][6:])
                        else:
                            cols=line.split(delim_char)

                        if len(cols)< (num_keys+1):
                            raise ValueError("too few fields found at nline=" + str(nline) + ",#fields=" + len(cols)\
                                              + "/" + str(num_keys+1))
                        lkrec=LookUpRec()
                        lkrec.key1= cols[0]
                        if num_keys>=2:
                            lkrec.key2=cols[1]
                        if num_keys>=3:
                            lkrec.key3=cols[2]
                        lkrec.result=cols[num_keys]

                        if not is_case_sens:
                            lkrec.key1= lkrec.key1.lower()
                            if num_keys>=2:
                                lkrec.key2= lkrec.key2.lower()
                            if num_keys>=3:
                                lkrec.key3= lkrec.key3.lower()

                        lkdict.recs.append(lkrec)
        lkdict= extract_lookup_record_key_info(lkdict)
        if lkdict.title.startswith("notok:"):
            raise ValueError("Error extracting record keys: " + lkdict.title[6:])

    except (RuntimeError, ValueError, OSError) as err:
        err_msg= "notok:" + str(err)

    if len(err_msg)>0:
        lkdict.title=err_msg
    return lkdict


def make_lookup_from_list(title:str,lkup_list:list,delim:str,is_case_sens:bool,num_keys:int) -> LookUpDict:
    """
    Builds a LookUpDict from list that contains what would be read from a file. 
    
    List will be read and columns extracted by splitting lines with delimiter. 
    Empty and comment (begins with # or //) lines are ignored. 
    First data containing line must contain delimited field names. 
    num_keys specifies how many columns will be used as keys (1-3) and then the next column will be used as value. 
    This number of columns must be present after splitting. 
    If double quote is in line then more precise (but slower) column separation will be used.
    LookupDict will have its fields and recs lists filled.

    Returns LookUpDict object whose title will start with notok: if there is an error.
    """

    lkdict:LookUpDict
    lkrec:LookUpRec
    err_msg:str=""
    nline:int=0
    cols:list=[]
    delim_char:str=""
    dq:str= "\""
    linein:str=""
    try:
        if len(title)==0:
            raise ValueError("title is empty")
        if num_keys<=0 or num_keys>3:
            raise ValueError("num_keys is not 1-3: " + str(num_keys))
        if len(delim)==0:
            raise ValueError("delim is empty")
        delim_char= recfuncs.delim_get_char(delim)
        lkdict= LookUpDict()
        lkdict.title=title
        lkdict.num_keys=num_keys
        lkdict.is_case_sens=is_case_sens
        lkdict.file_uri=""
        lkdict.delim=delim

        for line in lkup_list:
            linein=line
            if linein is None:
                break
            linein= linein.strip()
            if linein.endswith("\n"):
                linein=linein[:-1]
            if len(linein)>0 and not linein.startswith("#") and not linein.startswith("//"):
                nline += 1
                if nline==1:
                    if linein.find(delim_char)<1:
                        raise ValueError("first data line does not contain delimiter: " + delim_char)
                    if linein.find(dq)>-1:
                        linein=linein.replace(dq,'')
                    lkdict.fields= linein.split(delim_char)
                    if len(lkdict.fields)< (num_keys+1):
                        raise ValueError("too few fields found with delim=" + delim_char + ",#fields=" + len(lkdict.fields)\
                                            + "/" + str(num_keys+1))
                else:
                    if linein.find(dq)>-1:
                        cols=recfuncs.split_quoted_line(line,delim_char)
                        if len(cols)>0 and cols[0].startswith("notok:"):
                            raise RuntimeError("error splitting quoted string: " + cols[0][6:])
                    else:
                        cols=linein.split(delim_char)

                    if len(cols)< (num_keys+1):
                        raise ValueError("too few fields found at nline=" + str(nline) + ",#fields=" + len(cols)\
                                            + "/" + str(num_keys+1))
                    lkrec=LookUpRec()
                    lkrec.key1= cols[0]
                    if num_keys>=2:
                        lkrec.key2=cols[1]
                    if num_keys>=3:
                        lkrec.key3=cols[2]
                    lkrec.result=cols[num_keys]
                    if not is_case_sens:
                        lkrec.key1= lkrec.key1.lower()
                        if num_keys>=2:
                            lkrec.key2= lkrec.key2.lower()
                        if num_keys>=3:
                            lkrec.key3= lkrec.key3.lower()

                    lkdict.recs.append(lkrec)

        lkdict= extract_lookup_record_key_info(lkdict)
    except (RuntimeError, ValueError, OSError) as err:
        err_msg= "notok:" + str(err)

    if len(err_msg)>0:
        lkdict.title=err_msg
    return lkdict


def extract_lookup_record_key_info(lkdict:LookUpDict) -> LookUpDict:
    """
    Extracts lookup key information and parses into various arrays tokens, wildcards, 
    and boolean AND and NOT conditions to accelerate matching.

    lkdict: LookUpDict object to process

    Returns modified LookUpDict object with parsed record information. Title will start with notok: if there is an error.
    """

    err_msg:str=""
    key_str:str=""
    key_str_typ:str=""
    str_temp:str=""
    nand:int=-1
    nnot:int=-1
    front_wild:bool=False
    back_wild:bool=False
    temp_list:list=[]
    nkeyand:int=-1
    nkeynot:int=-1
    new_recs:list=[]
    nrec:int=-1
    try:
        for i in range(len(lkdict.recs)):
            new_recs.append(LookUpRec())
            nrec= len(new_recs)-1
            new_recs[nrec].result= lkdict.recs[i].result
            for j in range(lkdict.num_keys):
                key_str=""
                if j==0:
                    key_str= lkdict.recs[i].key1
                    new_recs[nrec].key1=key_str
                elif j==1:
                    key_str= lkdict.recs[i].key2
                    new_recs[nrec].key2=key_str
                elif j==2:
                    key_str= lkdict.recs[i].key3
                    new_recs[nrec].key3=key_str

                while "-and-" in key_str or "-not-" in key_str:
                    if key_str.startswith("-and-") or key_str.startswith("-not-"):
                        if key_str.startswith("-and-"):
                            key_str_typ="and"
                        else:
                            key_str_typ="not"
                        key_str=key_str[5:]
                    else:
                        # no prefix for this fragment so assign as AND
                        key_str_typ="and"

                    nand= key_str.find("-and-")
                    nnot= key_str.find("-not-")
                    if nand>0 and (nnot<0 or nand<nnot):
                        str_temp= key_str[:nand]
                        key_str= key_str[nand:]
                    elif nnot>0 and (nand<0 or nnot<nand):
                        str_temp= key_str[:nnot]
                        key_str= key_str[nnot:]
                    else:
                        str_temp=key_str
                        key_str=""

                    if key_str_typ=="and":
                        if j==0:
                            new_recs[i].key1_and.append(str_temp)
                            nkeyand=len(new_recs[i].key1_and)-1
                            new_recs[i].key1_and_front_wild.append(False)
                            new_recs[i].key1_and_back_wild.append(False)
                        elif j==1:
                            new_recs[i].key2_and.append(str_temp)
                            nkeyand=len(new_recs[i].key2_and)-1
                            new_recs[i].key2_and_front_wild.append(False)
                            new_recs[i].key2_and_back_wild.append(False)
                        elif j==2:
                            new_recs[i].key3_and.append(str_temp)
                            nkeyand=len(new_recs[i].key3_and)-1
                            new_recs[i].key3_and_front_wild.append(False)
                            new_recs[i].key3_and_back_wild.append(False)
                    elif key_str_typ=="not":
                        if j==0:
                            new_recs[i].key1_not.append(str_temp)
                            nkeynot=len(new_recs[i].key1_not)-1
                            new_recs[i].key1_not_front_wild.append(False)
                            new_recs[i].key1_not_back_wild.append(False)
                        elif j==1:
                            new_recs[i].key2_not.append(str_temp)
                            nkeynot=len(new_recs[i].key2_not)-1
                            new_recs[i].key2_not_front_wild.append(False)
                            new_recs[i].key2_not_back_wild.append(False)
                        elif j==2:
                            new_recs[i].key3_not.append(str_temp)
                            nkeynot=len(new_recs[i].key3_not)-1
                            new_recs[i].key3_not_front_wild.append(False)
                            new_recs[i].key3_not_back_wild.append(False)

                if len(key_str)>0:
                    if j==0:
                        new_recs[i].key1_and.append(key_str)
                        nkeyand=len(new_recs[i].key1_and)-1
                        new_recs[i].key1_and_front_wild.append(False)
                        new_recs[i].key1_and_back_wild.append(False)
                    elif j==1:
                        new_recs[i].key2_and.append(key_str)
                        nkeyand=len(new_recs[i].key2_and)-1
                        new_recs[i].key2_and_front_wild.append(False)
                        new_recs[i].key2_and_back_wild.append(False)
                    elif j==2:
                        new_recs[i].key3_and.append(key_str)
                        nkeyand=len(new_recs[i].key3_and)-1
                        new_recs[i].key3_and_front_wild.append(False)
                        new_recs[i].key3_and_back_wild.append(False)
                    key_str=""

                temp_list=[]
                if j==0:
                    temp_list=new_recs[i].key1_and
                elif j==1:
                    temp_list=new_recs[i].key2_and
                elif j==2:
                    temp_list=new_recs[i].key3_and

                nkeyand=-1
                for s in temp_list:
                    nkeyand += 1
                    front_wild=False
                    back_wild=False
                    if len(s)==0:
                        front_wild=True
                        back_wild=True
                        key_str=""
                    elif s.startswith("*"):
                        key_str=s[1:]
                        front_wild=True
                        if len(key_str)==0:
                            back_wild=True
                        elif key_str.endswith("*"):
                            key_str=key_str[:len(key_str)-1]
                            back_wild=True
                    elif s.endswith("*"):
                        key_str=s[:len(s)-1]
                        back_wild=True
                    else:
                        key_str=s

                    if j==0:
                        new_recs[i].key1_and[nkeyand]=key_str
                        new_recs[i].key1_and_front_wild[nkeyand]=front_wild
                        new_recs[i].key1_and_back_wild[nkeyand]=back_wild
                    elif j==1:
                        new_recs[i].key2_and[nkeyand]=key_str
                        new_recs[i].key2_and_front_wild[nkeyand]=front_wild
                        new_recs[i].key2_and_back_wild[nkeyand]=back_wild
                    elif j==2:
                        new_recs[i].key3_and[nkeyand]=key_str
                        new_recs[i].key3_and_front_wild[nkeyand]=front_wild
                        new_recs[i].key3_and_back_wild[nkeyand]=back_wild

                temp_list=[]
                if j==0:
                    temp_list=new_recs[i].key1_not
                elif j==1:
                    temp_list=new_recs[i].key2_not
                elif j==2:
                    temp_list=new_recs[i].key3_not

                nkeynot=-1
                for s in temp_list:
                    nkeynot += 1
                    front_wild=False
                    back_wild=False
                    if len(s)==0:
                        front_wild=True
                        back_wild=True
                        key_str=""
                    elif s.startswith("*"):
                        key_str=s[1:]
                        front_wild=True
                        if len(key_str)==0:
                            back_wild=True
                        elif key_str.endswith("*"):
                            key_str=key_str[:-1]
                            back_wild=True
                    elif s.endswith("*"):
                        key_str=s[:len(s)-1]
                        back_wild=True
                    else:
                        key_str=s

                    if j==0:
                        new_recs[i].key1_not[nkeynot]=key_str
                        new_recs[i].key1_not_front_wild[nkeynot]=front_wild
                        new_recs[i].key1_not_back_wild[nkeynot]=back_wild
                    elif j==1:
                        new_recs[i].key2_not[nkeynot]=key_str
                        new_recs[i].key2_not_front_wild[nkeynot]=front_wild
                        new_recs[i].key2_not_back_wild[nkeynot]=back_wild
                    elif j==2:
                        new_recs[i].key3_not[nkeynot]=key_str
                        new_recs[i].key3_not_front_wild[nkeynot]=front_wild
                        new_recs[i].key3_not_back_wild[nkeynot]=back_wild

        lkdict.recs.clear()
        for rec in new_recs:
            lkdict.recs.append(rec)

    except (RuntimeError, ValueError, OSError) as err:
        err_msg= "notok:" + str(err)

    if len(err_msg)>0:
        lkdict.title=err_msg
    return lkdict
