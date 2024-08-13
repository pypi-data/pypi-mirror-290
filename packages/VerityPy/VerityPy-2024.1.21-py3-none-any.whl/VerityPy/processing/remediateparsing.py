#!/usr/bin/env python
"""
Remediate Parsing

Remediates (i.e fixes) records that parse incorrectly leading to incorrect number of field values relative to number fields in schema. 
This has three types:
    big: too many field values typically due to embedded delimiters in some field values
    small1: too few fields by 1 which can either be an error or acceptable since some databases intentionally drop last field if it is empty setting it as null
    small2: too few fields by 2 or more typically caused by line feeds in fields or problems exporting records across data system types
This class detects and corrects these errors making new records that are correct
"""

__all__ = ['shift_array_entries','fix_record_field_split']
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240807'

import math
from VerityPy.processing import recfuncs, field

DQ="\""

def shift_array_entries(origvals:list, recflds:list, hashrecflds:dict, pinflds:list)->list:
    """
    Shifts array of parsed field values to correct having more values than defined fields. 
	Uses algorithm assessing best field and field + 1 (index positions in record) to join 
	based on datatypes, formats and known patterns of root causes of this error.

    * origvals: array of parsed field values
	* recflds: list of Field object containing datatype and format specifications
	* hashrecflds: Dictionary of field title lowercase to its array index
	* pinflds: optional list of field titles that are pinned meaning their position cannot be changed
	
    returns: new array of parsed field values. If error, 0th entry starts with notok:
    """

    txt:str=""
    txt1:str=""
    elem:str=""
    elemval:str=""
    ndelta:int=-1
    nmaxdt:int=0
    nmaxf:int=0
    nindexdt:int=-1
    nindexf:int=-1
    ndt:int=0
    nf:int=0
    n1:int=-1
    n2:int=-1
    n3:int=-1
    n4:int=-1
    ntot:int=0
    nflds:int=0
    nmaxfthresh:int=0
    ndist:int=-1
    dval:float=0
    didmove:bool=False
    newvals:list=[]
    outvals:list=[]
    pinrecs:list=[]
    pinindex:list=[]
    hashpinindex:dict={}
    pinshiftscores:list=[]
    joinstr:str=""
    try:
        nflds= len(recflds)
        ndelta= len(origvals)- nflds
        if ndelta<=0:
            return origvals
        if len(pinflds)>0:
            for s in pinflds:
                if s in hashrecflds:
                    pinindex.append(hashrecflds[s])
                    pinshiftscores.append(0)
            if len(pinindex)>0:
                pinshiftscores.append(0) # next to last index for equal distribution
                pinshiftscores.append(0) # last index for staggered distribution
                pinindex.sort()
                for i in range(len(pinindex)):
                    hashpinindex[pinindex[i]]=i
                for i in range(3):
                    pinrecs.append([])
                    for j in range(nflds):
                        pinrecs[i].append("")

        # compute a threshhold of % fields with data types
        dval= 0.6
        if len(pinindex)==1:
            dval= 0.8 # high threshold if there is a defined pinned
        elif len(pinindex)>1:
            dval= 0.72 # slightly lower if more than 1 pinned
        n1 = round(dval * nflds,0)
        nmaxfthresh= n1 if n1>=1 else 1

        # do metric with specified data types first and then if necessary use pinned field
        for h in range(nflds):
            # begin with original record
            # shift with current field pinned and calculate score of how many fields meet datatype
            # move array entries above current field into it for number of extra fields in record
            newvals=[]
            for i in range(len(origvals)):
                newvals.append(origvals[i])
            txt= newvals[h]
            for i in range(ndelta):
                txt += joinstr + newvals[i+1+h]
            newvals[h]=txt
            n2= nflds-1
            # move higher fields into lower ones with skip= #extra fields in record
            # so, if current index=4, and nDelta=2 we moved indexes 5-6 into 4, and now 7->5 and 8->6
            for i in range(h+1,n2+1):
                n3=i+ndelta
                txt= "" if n3>= len(newvals) else newvals[n3]
                newvals[i]=txt

            # calculate score by datatype match and format for real and string
            ndt=0
            nf=0
            for i in range(nflds):
                elemval=newvals[i]
                if len(elemval)>0 and len(recflds[i].datatype)>0:
                    if recflds[i].datatype.startswith("date"):
                        if len(recflds[i].fmt_date)>0 and recfuncs.is_field_its_datatype(recflds[i].datatype, elemval, recflds[i].fmt_date):
                            ndt += 1
                    elif recfuncs.is_field_its_datatype(recflds[i].datatype, elemval):
                        ndt += 1
                        if recflds[i].datatype=="real":
                            if recflds[i].fmt_decimal>0:
                                if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                    nf += 1
                        elif recflds[i].datatype=="string":
                            if recflds[i].fmt_strcase in ("upper","lower") or recflds[i].fmt_strlen>0:
                                if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                    nf += 1

            if ndt>nmaxdt:
                nmaxdt=ndt
                nindexdt=h

            # weight score for datatype add addl if declared pinned
            n2 = 10*ndt + round(10*nf/nflds)
            if h in hashpinindex:
                n2 += 10
            if n2>nmaxf:
                nmaxf=n2
                nindexf=h
            
        # newVals contains updated record field values although its Count is larger than # fields            
        # if no pinned fields or format score is above threshold make final shift
        newvals=[]
        for i in range(len(origvals)):
            newvals.append(origvals[i])
        if len(pinindex)==0 or nmaxf>=nmaxfthresh:
            # use the single pivot pt from data type and format matching
            n1= nindexf if nindexf>=0 else nindexdt
            txt=newvals[n1]
            for i in range(ndelta):
                txt += joinstr + newvals[i+1+n1]
            newvals[n1]=txt
            n2= nflds-1
            # move higher fields into lower ones with skip= #extra fields in record
            # so, if current index=4, and nDelta=2 we moved indexes 5-6 into 4, and now 7->5 and 8->6
            for i in range(n1+1,n2+1):
                n3= i + ndelta
                txt="" if n3>= len(newvals) else newvals[n3]
                newvals[i]=txt
            didmove=True
        elif len(pinindex)==1:
            didmove=True
            n1=pinindex[0]
            txt=newvals[n1]
            for i in range(ndelta):
                txt += joinstr + newvals[i+1+n1]
            newvals[n1]=txt
            n2= nflds-1
            # move higher fields into lower ones with skip= #extra fields in record
            for i in range(n1+1,n2+1):
                n3= i + ndelta
                txt="" if n3>= len(newvals) else newvals[n3]
                newvals[i]=txt
        elif len(pinindex)>1:
            # if delta fields > # pinned fields we will test equally alloting shifting to each 
            # as well as scoring assigning all shifting to one and 
            # staggered priority shifting where we start from lowest index and shift no more than to next pin index
            nmaxdt = -1 
            nmaxf = -1 
            nindexdt = -1 
            nindexf = -1
            # 2 addl tests above #pinned fields
            for h in range(len(pinindex)+2):
                newvals=[]
                for i in range(len(origvals)):
                    newvals.append(origvals[i])
                ntot=0

                if h< len(pinindex):
                    n1=pinindex[h]
                    txt=newvals[n1]
                    for i in range(ndelta):
                        txt += joinstr + newvals[i+1+n1]
                    newvals[n1]=txt
                    n2= nflds-1
                    for i in range(n1+1,n2+1):
                        n3= i + ndelta
                        txt="" if n3>= len(newvals) else newvals[n3]
                        newvals[i]=txt

                    ndt=0
                    nf=0
                    for i in range(nflds):
                        elemval= newvals[i]
                        if len(recflds[i].datatype)>0:
                            if recfuncs.is_field_its_datatype(recflds[i].datatype, elemval, recflds[i].fmt_date):
                                ndt += 1
                                if recflds[i].datatype=="real":
                                    if recflds[i].fmt_decimal>0:
                                        if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                            nf += 1
                                elif recflds[i].datatype=="string":
                                    if recflds[i].fmt_strcase in ("upper","lower") or recflds[i].fmt_strlen>0:
                                        if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                            nf += 1
                    if ndt>nmaxdt:
                        nmaxdt=ndt
                        nindexdt=h
                    n2= (10*ndt) + nf
                    if n2>nmaxf:
                        nmaxf=n2
                        nindexf=h
                    
                    for i in range(nflds):
                        pinrecs[0][i]=newvals[i]

                elif h==len(pinindex):
                    # equal allotment if # pinned is at least # delta fields
                    if len(pinindex)>= ndelta:
                        ndist= math.floor(ndelta/len(pinindex))
                        for p in range(len(pinindex)):
                            n1=pinindex[p]
                            txt=newvals[n1]
                            n4= ndist if p<len(pinindex)-1 else ndelta-ntot
                            for i in range(1, n4+1):
                                ntot += 1
                                txt += joinstr + newvals[i+n1]
                            newvals[n1]=txt
                            n2=nflds-1
                            for i in range(n1+1,n2+1):
                                n3=i+n4
                                txt= "" if n3>= len(newvals) else newvals[n3]
                                newvals[i]=txt

                        ndt=0
                        nf=0
                        for i in range(nflds):
                            elemval=newvals[i]
                            if len(recflds[i].datatype)>0:
                                if recfuncs.is_field_its_datatype(recflds[i].datatype, elemval, recflds[i].fmt_date):
                                    ndt += 1
                                    if recflds[i].datatype=="real":
                                        if recflds[i].fmt_decimal>0:
                                            if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                                nf += 1
                                    elif recflds[i].datatype=="string":
                                        if recflds[i].fmt_strcase in ("upper","lower") or recflds[i].fmt_strlen>0:
                                            if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                                nf += 1

                        if ndt>nmaxdt:
                            nmaxdt=ndt
                            nindexdt=h
                        n2= (10*ndt) + nf
                        if n2>nmaxf:
                            nmaxf=n2
                            nindexf=h
                        
                        for i in range(nflds):
                            pinrecs[1][i]=newvals[i]

                elif h==len(pinindex)+1:
                    # staggered
                    for p in range(len(pinindex)):
                        n1=pinindex[p]
                        txt=newvals[n1]
                        # variable delta between pinned fields
                        n4= (pinindex[p+1]-pinindex[p]-1) if p<len(pinindex)-1 else ndelta-ntot
                        for i in range(1, n4+1):
                            ntot += 1
                            txt += joinstr + newvals[i+n1]
                        newvals[n1]=txt
                        n2=nflds-1
                        for i in range(n1+1,n2+1):
                            n3=i+n4
                            txt= "" if n3>= len(newvals) else newvals[n3]
                            newvals[i]=txt

                    ndt=0
                    nf=0
                    for i in range(nflds):
                        elemval=newvals[i]
                        if len(recflds[i].datatype)>0:
                            if recfuncs.is_field_its_datatype(recflds[i].datatype, elemval, recflds[i].fmt_date):
                                ndt += 1
                                if recflds[i].datatype=="real":
                                    if recflds[i].fmt_decimal>0:
                                        if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                            nf += 1
                                elif recflds[i].datatype=="string":
                                    if recflds[i].fmt_strcase in ("upper","lower") or recflds[i].fmt_strlen>0:
                                        if recfuncs.is_field_its_format(elemval, recflds[i], False).startswith("true"):
                                            nf += 1

                    if ndt>nmaxdt:
                        nmaxdt=ndt
                        nindexdt=h
                    n2= (10*ndt) + nf
                    if n2>nmaxf:
                        nmaxf=n2
                        nindexf=h
                    
                    for i in range(nflds):
                        pinrecs[2][i]=newvals[i]

            # final move
            if nindexf>=0:
                newvals=[]
                if nindexf<len(pinindex):
                    didmove=True
                    for i in range(len(pinrecs[0])):
                        newvals.append(pinrecs[0][i])
                elif nindexf==len(pinindex):
                    didmove=True
                    for i in range(len(pinrecs[1])):
                        newvals.append(pinrecs[1][i])
                elif nindexf==len(pinindex)+1:
                    didmove=True
                    for i in range(len(pinrecs[2])):
                        newvals.append(pinrecs[2][i])

        # assign result array
        if didmove:
            for i in range(nflds):
                outvals.append(newvals[i])
        else:
            for i in range(nflds):
                outvals.append(origvals[i])

    except (RuntimeError, OSError, ValueError) as err:
        outvals.insert(0, "notok:" + str(err))
    return outvals

def fix_record_field_split(settings:dict, srcfields:list, srcrecs:list)->list:
    """Fix Record Field Splitting
    
    Repairs records with parsing problems having too many or too few field values relative to defined 
    number of fields. This occurs due to embedded delimiters in some field values causing too many parsed values, 
    and records broken across multiple lines causing too few values. These situations are categorized into 3 types:
    1) big (too many parsed values), 2) small1 (1 too few values), 3) small2 (2 or more too few values). small1 is a 
    special case since some data systems purposefully eliminate the fnal field value in a record if it is empty by 
    making it null thereby saving storage and memory space. In this case, the record is actually fine but is missing its final 
    field value. This can be accepted by having the setting 'allowLastEmpty' = TRUE leading to a default value assigned 
    to this last record field based on datatype: int and real assigned 0, bool assigned FALSE, others assigned empty string.

        * settings: Dictionary of setting parameters. Both key and value are strings. Settings:
            - allow_last_empty: bool whether to allow last field to be empty (i.e. small1 parsing) and assign it default value. Default is TRUE
            - is_quoted: bool whether fields values may be enclosed by double quotes as is common when data exported from SpreadSheets and some databases. Default is FALSE.
            - has_header: bool whether first non-empty record is a header row of delimited field titles. Default is FALSE.
            - ignore_empty: bool whether to ignore empty records. Default is TRUE.
            - pin_fields: field titles delimited by pipe (if more than 1) that are pinned meaning if record has too many fields (i.e. big) then these fields will not shifted as 
                    the algorithm finds the best way to merge values to make corrected record
            - ignore_start_str: string parts delimited by pipe (if more than 1) that will cause records starting with any one of them to be ignored. Always case insensitive. 
                    A common use for this is to filter out comment lines such as those starting with # or // in which case set to #|//
            - delim: name of delimiter to use to parse records: comma, pipe, tab, colon, caret. This is required.
            - join_char: token (max 10 chars) or alias to insert when joining lines to remediate parsing. Default is to use nothing. 
		  					Aliases include: -comma-, -tab-, -pipe-, -space-, -bslash-, -fslash-, -lparen-, -rparen-, 
		  					-lcurly-, -rcurly-, -lsquare-, -rsquare-, -dblquote-, -mathpi-, -mathe-
        * srcfields: list of Field objects comprising records
        * srcrecs: list of string source records

    returns: list of new records. If error, 0th entry starts with notok: otherwise 0th entry is string of stats, 
        entry[1] is header of field titles. For stats, examples may have prefix of (nline) with nline being the line number read 
        (excluding empty and comments lines) and is therefore 1 larger than the line's index 
        in the Python list (i.e. nline is 1 based while lists are 0-based).
    """

    txt:str=""
    txt1:str=""
    elem:str=""
    recin:str=""
    recin_lc:str=""
    recout:str=""
    delim:str=""
    delimchar:str=""
    join_char:str=""
    nflds_act:int=0
    nflds_new:int=0
    ndelta:int=-1
    nflds_prior:int=0
    lrecsin:int=0
    lrecsout:int=0
    lbig:int=0
    lsm1:int=0
    lsm2:int=0
    ljoin:int=0
    lempty:int=0
    lignore:int=0
    lfix:int=0
    lnotfix:int=0
    doing_join:bool=False
    allow_last_empty:bool=False
    isquoted:bool=False
    hasheader:bool=False
    ignore_empty:bool=False
    userec:bool=False
    didsave:bool=False
    fldvals:list=[]
    fldvalsprior:list=[]
    pinflds:list=[]
    temp:list=[]
    ignore_start_str:list=[]
    outrecs:list=[]
    fld_is_datatype:list=[]
    hashflds:dict={}
    hashpinflds:dict={}

    try:
        nflds_act=len(srcfields)
        if nflds_act==0:
            raise ValueError("no fields supplied")
        if len(srcrecs)==0:
            raise ValueError("no records supplied")
        for i in range(nflds_act):
            if not isinstance(srcfields[i], field.Field):
                raise ValueError("source field is not Field object at index " + str(i))
            elem=srcfields[i].title.lower().strip()
            if len(elem)==0:
                raise ValueError("source field title is empty at index " + str(i))
            if elem in hashflds:
                raise ValueError("duplicate source field title " + elem)
            hashflds[elem]=i
            srcfields[i].title=srcfields[i].title.strip()
            srcfields[i].datatype=srcfields[i].datatype.lower().strip()

        for k,v in settings.items():
            if isinstance(k,str):
                txt= k.lower()
                txt1= str(v).lower()
                if txt in ("allow_last_empty","allowlastempty"):
                    allow_last_empty= txt1=="true"
                elif txt in ("isquoted","is_quoted"):
                    isquoted= txt1=="true"
                elif txt in ("hasheader","has_header"):
                    hasheader= txt1=="true"
                elif txt in ("ignore_empty","ignoreempty"):
                    ignore_empty= txt1=="true"
                elif txt in ("ignore_start_str","ignorestartstr"):
                    temp=txt1.split("|")
                    for s in temp:
                        txt=s.strip()
                        if len(txt)>0:
                            ignore_start_str.append(txt)
                elif txt in ("pin_fields","pinfields"):
                    temp=txt1.split("|")
                    for s in temp:
                        txt=s.strip()
                        if len(txt)>0 and txt not in hashpinflds:
                            pinflds.append(txt)
                            hashpinflds[txt]= len(pinflds)-1
                elif txt =="delim":
                    if len(txt1)==0:
                        raise ValueError("empty delim specified")

                    delimchar= recfuncs.delim_get_char(txt1)
                    if delimchar.startswith("notok:"):
                        raise ValueError(delimchar[6:])
                    elif len(delimchar)==0:
                        raise ValueError("unknown delim specified:" + txt1)
                elif txt in ("join_char","joinchar"):
                    join_char= txt1
                    if join_char.startswith("-") and join_char.endswith("-"):
                        join_char= recfuncs.convert_char_aliases(join_char)
                    else:
                        if len(join_char)>10:
                            join_char=join_char[:10]

        if len(delimchar)==0:
            raise ValueError("no delim specified:" + txt1)

        recout=""
        for i in range(nflds_act):
            if i>0:
                recout += delimchar
            recout += srcfields[i].title
        outrecs.append(recout)

        for nidx in range(len(srcrecs)):
            recin= srcrecs[nidx]
            userec=True
            if len(recin.strip())==0:
                lempty += 1
                userec= not ignore_empty
            elif len(ignore_start_str)>0:
                recin_lc= recin.lower()
                for s in ignore_start_str:
                    if s in recin_lc:
                        userec=False
                        lignore += 1
                        break
            
            if userec:
                lrecsin += 1
                didsave=False
                if lrecsin>1 or not hasheader:
                    if isquoted and DQ in recin:
                        fldvals= recfuncs.split_quoted_line(recin, delimchar)
                        if len(fldvals)>0 and fldvals[0].startswith("notok:"):
                            raise ValueError("error splitting line index " + str(nidx) + ":" + fldvals[6:])
                    else:
                        fldvals= recin.split(delimchar)
                    nflds_new= len(fldvals)
                    ndelta= nflds_new-nflds_act

                    if doing_join:
                        if ndelta>=0 or nflds_prior+nflds_new-1 > nflds_act:
                            # problem since either current record is complete and therefore cannot be used to add to prior record
                            # or joining will create too many fields so keep prior as is despite it missing some values
							              # add empty values to complete all fields
                            for i in range(nflds_act-nflds_prior):
                                fldvalsprior.append("")
                            recout= delimchar.join(fldvalsprior)
                            outrecs.append(recout)
                            lrecsout += 1
                            doing_join=False
                            didsave=True
                            lnotfix += 1
                        else:
                            ljoin += 1
                            if ndelta==-1:
                                lsm1 +=1
                            else:
                                lsm2 +=1
                            
                            for i in range(nflds_new):
                                if i==0:
                                    fldvalsprior[nflds_prior-1]+= join_char + fldvals[i]
                                else:
                                    fldvalsprior.append(fldvals[i])

                            # calc new ndelta
                            ndelta= len(fldvalsprior)- nflds_act
                            if ndelta==0:
                                recout= delimchar.join(fldvalsprior)
                                outrecs.append(recout)
                                lrecsout += 1
                                doing_join=False
                                didsave=True
                                lfix += 1

                    if not doing_join and not didsave:
                        if ndelta==0:
                            outrecs.append(recin)
                            lrecsout += 1
                            didsave=True
                        elif ndelta>0:
                            lbig += 1
                            temp= shift_array_entries(fldvals, srcfields, hashflds, pinflds)
                            if len(temp)== nflds_act:
                                lfix += 1
                            else:
                                lnotfix += 1
                            recout= delimchar.join(temp)
                            outrecs.append(recout)
                            lrecsout += 1
                            didsave=True
                        elif ndelta== -1 and allow_last_empty:
                            recout = recin + delimchar
                            outrecs.append(recout)
                            lrecsout += 1
                            didsave=True
                        elif ndelta<0:
                            if ndelta== -1:
                                lsm1 +=1
                            else:
                                lsm2 +=1
                            if nidx==len(srcrecs)-1:
                                # cannot add more records so this one fails
                                for i in range(nflds_act-nflds_new):
                                    fldvalsprior.append("")
                                recout= delimchar.join(fldvalsprior)
                                outrecs.append(recout)
                                lrecsout += 1
                                lnotfix += 1
                                didsave=True
                            else:
                                nflds_prior=nflds_new
                                doing_join=True
                                fldvalsprior=[]
                                fldvalsprior=fldvals


        txt = "ok:recin=" + str(lrecsin) + ",recout=" + str(lrecsout) + ",big=" + str(lbig) + ",small1=" + str(lsm1) + ",small2=" + str(lsm2) + ",join=" + str(ljoin) + ",fix=" + str(lfix) + ",notfix=" + str(lnotfix)
        outrecs.insert(0,txt)
    except (RuntimeError, OSError, ValueError) as err:
        outrecs.insert(0,"notok:" + str(err))
    return outrecs

