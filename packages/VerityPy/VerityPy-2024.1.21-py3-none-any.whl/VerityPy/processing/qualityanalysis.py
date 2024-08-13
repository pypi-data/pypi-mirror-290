"""
Quality Analysis object and functions
"""

__all__ = ['QualityAnalysis']
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240810'

from . import recfuncs, field


DQ:str= "\""
LF:str="\n"


class QualityAnalysis:
    """
    QualityAnalysis

    Object containing settings and results of quality inspection.

    title: name for this object usually the name of the job run to make it
    status: system assigned value which will be notok:reason if there is an error
    debug: empty, info, trace
    delim: name of delimiter to parse source records (comma, tab, pipe, colon, caret). Default comma
    delim_char: character for delim used in code. Default ,
    maxuv: maximum number of unique values to collect per field with remainder into category '-other-'. Default=50
    is_case_sens: bool whether values are case sensitive. Default=False
    is_quoted: bool whether source records can have quoted values. Default= False
    has_header: bool whether source records have header line as first non-empty, non-comment line. Default= True
    extract_fields: bool whether fields should be extracted from header line instead of supplied in 'fields' list. Default= False
    fields: list of field objects which have attributes for title, datatype, and formatting
    field_names_lower: list of field titles in lower case
    hash_fields: dictionary key= field title lower case with value= list index
    numrecs: integer count of records used

    field_datatype_dist: list of field datatype distributions correlated to fields list. 
        Each field has counts for detected datatypes (int, real, bool, date, string, empty).
    field_uniqvalues: list correlated to fields. Each entry is a descending sorted list of 
        uniquevalue tuples with each tuple (uv,count) where uv= string of unique value 
        and count= integer number of instances. A maximum number of values are kept (default=50) with additional 
        grouped into -other-
    field_quality: list correlated to fields. String of an integer 0-100 as a quality metric computed from 
        discovered field characteristics
    rec_size_dist: dictionary of record sizes (byte lengths) to counts. Max 100 sizes.
    rec_parse_errs: dictionary of parsing errors (number fields after parsing 
        relative to defined fields) by type as small1 (1 too few fields), small2 
        (2 or more missing fields), big (1 or more too many fields). Also, has 
        keys for lists of example records small1_recs, small2_recs, 
        big_recs (each max 50). 
    rec_parse_dist: dictionary of number of parsed fields to count
    spec_char_dist: dictionary of special characters and their counts. Special 
        characters are (some use aliases as dictionary keys): 
        tab, !, doublequote, #, <, >, [, ], backslash, ^, {, }, ~, ascii_[0-31, 127-255], 
        unicode_[256-65535]
    spec_char_dist_field: list correlated to fields[] with each being a dictionary 
        of special characters to their counts for that specific field. Same organization 
        as in spec_char_dist
    spec_char_examples: list of examples of discovered special characters. Each entry is 
        (nline)[sp char list]record with nline being the number line read from source data 
        (excluding empty and comments lines) and is therefore 1 larger than the line's index 
        in the Python list (i.e. nline is 1 based while lists are 0-based).
        [sp char list] comma delimited string of each special character 
        found in the record such as [spchar1,spchar2]lineIn. A single field can have  
        more than 1 special character. For example, input line (pipe delimited) as record line 
        #5 (although actual file line number could be larger due to comments and empty lines) and data =
        !dog|{House}|123^456 will be stored as an example as 
        (5)[!,{,},^]!dog|{House}|123^456
    covalues: list of CoValue objects to collect unique value information. 
    covalue_uniqvalues: correlated to covalues array. Similar to field unique values.
    err_stats: dictionary of properties and counts. 
        numrecs_err: number records with any kind of error
        numrecs_err_datatype: number records with datatype error
        numrecs_err_fmt: number records with format error
        fields_err_datatype: dictionary of fields with datatype errors and counts
        fields_err_fmt: dictionary of fields with format errors and counts
    err_datatype_examples: list of delimited fields within records with datatype errors. 
        Syntax is: (nline)[fieldinfo]|[fieldinfo].....  where [fieldinfo] is 
        fieldTitle:reason:fieldValue  . fieldValue will be set to -empty- if the actual value is 
        empty. nline is the number line read from source data 
        (excluding empty and comments lines) and is therefore 1 larger than the line's index 
        in the Python list (i.e. nline is 1 based while lists are 0-based).
    err_fmt_examples: list of delimited fields within records with format errors. 
        Syntax is: (nline)[fieldinfo]|[fieldinfo].....  where [fieldinfo] is 
        fieldTitle:reason:fieldValue  . fieldValue will be set to -empty- if the actual value is 
        empty. nline is the number line read from source data 
        (excluding empty and comments lines) and is therefore 1 larger than the line's index 
        in the Python list (i.e. nline is 1 based while lists are 0-based).
    """

    def __init__(self):
        self.title=""
        self.status=""
        self.debug=""
        self.delim="comma"
        self.delim_char=","
        self.maxuv=50
        self.is_case_sens=False
        self.is_quoted=False
        self.has_header=True
        self.extract_fields=False
        self.fields=[]
        self.field_names_lower=[]
        self.hash_fields={}
        self.field_datatype_dist=[]
        self.field_uniqvals=[]
        self.field_quality=[]
        self.rec_size_dist={}
        self.rec_parse_errs={
            'small1':0,
            'small2':0,
            'big':0,
            'small1_recs':[],
            'small2_recs':[],
            'big_recs':[],
        }
        self.rec_parse_dist={}
        self.spec_char_dist={}
        self.spec_char_dist_field=[]
        self.spec_char_examples=[]
        self.covalues=[]
        self.covalue_uniqvals=[]
        self.numrecs=0
        self.err_stats={
            'numrecs_err':0,
            'numrecs_err_datatype':0,
            'numrecs_err_fmt':0,
            'fields_err_datatype':{},
            'fields_err_fmt':{},
        }
        self.err_datatype_examples=[]
        self.err_fmt_examples=[]


    def get_json(self,add_lf:bool=False):
        """
        Constructs array of json strings for components of this object.
        add_lf: if True then line feed added at end of each entry. This is 
            unnecessary if returned array is printed as line per entry.
        Returns string list with first entry starting with notok: if error
        """

        outline:str=""
        outarray:list=[]
        c:str=","
        qcom:str= DQ + c
        qcq:str= DQ + ":" + DQ
        qc:str= DQ + ":"
        lb:str="{"
        lbq:str= lb + DQ
        clb:str= c + lb
        clbq:str= c + lb + DQ
        rb:str="}"
        qrb:str= DQ + rb
        ls:str="["
        rs:str="]"
        n1:int=-1
        n2:int=-1
        txt:str=""
        try:
            outarray.append(lbq+"report" + qc + ls)
            outarray.append(lbq+"title"+qcq+self.title+qrb)
            outarray.append(clbq+"status"+qcq+self.status+qrb)
            outarray.append(clbq+"debug"+qcq+self.debug+qrb)
            outarray.append(clbq+"numrecs"+qcq+str(self.numrecs)+qrb)
            outarray.append(clbq+"maxuv"+qcq+str(self.maxuv)+qrb)
            outarray.append(clbq+"delim"+qcq+self.delim+qrb)
            outarray.append(clbq+"delim_char"+qcq+self.delim_char+qrb)
            outarray.append(clbq+"is_case_sens"+qcq+str(self.is_case_sens).lower()+qrb)
            outarray.append(clbq+"is_quoted"+qcq+str(self.is_quoted).lower()+qrb)
            outarray.append(clbq+"has_header"+qcq+str(self.has_header).lower()+qrb)
            outarray.append(clbq+"extract_fields"+qcq+str(self.extract_fields).lower()+qrb)

            outarray.append(clbq+"fields"+qc+ls)
            for i in range(len(self.fields)):
                if isinstance(self.fields[i], field.Field):
                    outline=""
                    if i>0:
                        outline=c
                    outline += DQ + self.fields[i].title + DQ
                    outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"field_datatypes"+qc+ls)
            for i in range(len(self.fields)):
                if isinstance(self.fields[i], field.Field):
                    outline=""
                    if i>0:
                        outline=c
                    outline += DQ + self.fields[i].datatype + DQ
                    outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"field_formats"+qc+ls)
            for i in range(len(self.fields)):
                if isinstance(self.fields[i], field.Field):
                    outline=""
                    if i>1:
                        outline=c
                    outline += lb
                    outline+=DQ+"strcase"+qcq+ self.fields[i].fmt_strcase +DQ
                    outline+=c+DQ+"strlen"+qcq+str(self.fields[i].fmt_strlen)+DQ
                    outline+=c+DQ+"decimal"+qcq+str(self.fields[i].fmt_decimal)+DQ
                    outline+=c+DQ+"date"+qcq+self.fields[i].fmt_date+DQ
                    outline+=c+DQ+"strcut"+qcq+str(self.fields[i].fmt_strcut)+DQ
                    outline+=c+DQ+"strpad"+qcq+str(self.fields[i].fmt_strpad)+DQ
                    outline+=c+DQ+"strpadchar"+qcq+str(self.fields[i].fmt_strpadchar)+DQ
                    outline += rb
                    outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"field_quality"+qc+ls)
            for i in range(len(self.fields)):
                outline=""
                if i>0:
                    outline=c
                txt=""
                if i< len(self.field_quality):
                    txt=self.field_quality[i]
                outline += DQ + txt + DQ
                outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"field_datatype_dists"+qc+ls)
            for i in range(len(self.fields)):
                if i>0:
                    outline= clb
                else:
                    outline=lb
                if i< len(self.field_datatype_dist):
                    n1=0
                    for k,v in self.field_datatype_dist[i].items():
                        n1 += 1
                        if n1>1:
                            outline += c
                        outline += DQ + k + qc + str(v)
                outline += rb
                outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"field_uniqvalues"+qc+ls)
            n1=0
            for i in range(len(self.fields)):
                if isinstance(self.fields[i], field.Field) and len(self.field_uniqvals[i])>0:
                    n1 += 1
                    outline=""
                    if n1>1:
                        outline += c
                    outline += lbq + "field" + qcq + self.fields[i].title +qcom
                    outarray.append(outline)
                    outline= DQ + "uniqvalues" + qc + ls
                    outarray.append(outline)
                    for j in range(len(self.field_uniqvals[i])):
                        outline=""
                        if j>0:
                            outline=c
                        txt= recfuncs.extract_char_aliases(self.field_uniqvals[i][j][0],["|","/"])
                        outline += lbq + "uniqvalue" + qcq + txt + qcom + DQ + "count" + qc + str(self.field_uniqvals[i][j][1]) + rb
                        outarray.append(outline)
                    outarray.append(rs)
                    outarray.append(rb)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"covalues"+qc+ls)
            for i in range(len(self.covalues)):
                outline=""
                if i>0:
                    outline=c
                outline += self.covalues[i].get_json()
                outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"covalue_uniqvalues"+qc+ls)
            n1=0
            for i in range(len(self.covalues)):
                if len(self.covalue_uniqvals[i])>0:
                    n1 += 1
                    outline=""
                    if n1>1:
                        outline += c
                    outline += lbq + "covalue" + qcq + self.covalues[i].title + qcom
                    outarray.append(outline)
                    outline= DQ + "uniqvalues" + qc+ls
                    outarray.append(outline)
                    for j in range(len(self.covalue_uniqvals[i])):
                        outline=""
                        if j>0:
                            outline=c
                        txt= recfuncs.extract_char_aliases(self.covalue_uniqvals[i][j][0],["|","/"])
                        outline += lbq + "uniqvalue" + qcq + txt + qcom
                        outline += DQ + "count" + qc + str(self.covalue_uniqvals[i][j][1]) + rb
                        outarray.append(outline)
                    outarray.append(rs)
                    outarray.append(rb)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"field_spchar_dists"+qc+ls)
            for i in range(len(self.fields)):
                outline=""
                if i>0:
                    outline += c
                outline += lbq + "field" + qcq + self.fields[i].title +qc+ls
                outarray.append(outline)
                n1=0
                if i< len(self.spec_char_dist_field):
                    for k,v in self.spec_char_dist_field[i].items():
                        outline=""
                        n1 += 1
                        if n1>1:
                            outline += c
                        outline += lbq + k + qc + str(v) + rb
                        outarray.append(outline)
                    outarray.append(rs)
                    outarray.append(rb)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"spec_char_dists"+qc+ls)
            n1=0
            for k,v in self.spec_char_dist.items():
                n1 += 1
                outline=""
                if n1>1:
                    outline=c
                outline += lbq + k + qc + str(v) + rb
                outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"spec_char_examples"+qc+ls)
            for i in range(len(self.spec_char_examples)):
                outline=""
                if i>0:
                    outline=c
                txt=self.spec_char_examples[i]
                txt1=""
                if txt.find("[")>-1 and txt.find("]")>-1:
                    txt1=txt[:txt.find("]")+1]
                    txt=txt[txt.find("]")+1:]
                txt= recfuncs.extract_char_aliases(txt,[",","|","/","(",")"])
                if len(txt1)>0:
                    outline += lbq + "example" + qc + DQ + txt1 + DQ
                    outline += c+ DQ + "rec" + qcq + txt + qrb
                    outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            # err_stats
            outarray.append(clbq+"err_stats"+qc+ls)
            outarray.append(lbq+"numrecs_err"+qc+str(self.err_stats["numrecs_err"])+rb)
            outarray.append(clbq+"numrecs_err_datatype"+qc+str(self.err_stats["numrecs_err_datatype"])+rb)
            outarray.append(clbq+"numrecs_err_fmt"+qc+str(self.err_stats["numrecs_err_fmt"])+rb)
            outarray.append(clbq+"fields_err_datatype"+qc+ls)
            n1=0
            for f,b in self.err_stats["fields_err_datatype"].items():
                n1 += 1
                outline=""
                if n1>1:
                    outline=c
                outline += lbq + "field" + qcq + str(f) + qcom
                outline += DQ + "count" + qc + str(b["count"]) + c
                outarray.append(outline)
                outarray.append(DQ+"reasons"+qc + ls)
                n2=0
                for r,n in b["reasons"].items():
                    n2 += 1
                    outline=""
                    if n2>1:
                        outline=c
                    outline += lbq + "reason" + qcq + str(r) + qcom
                    outline += DQ + "count" + qc + str(n) + rb
                    outarray.append(outline)
                outarray.append(rs)
                outarray.append(rb)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"fields_err_fmt"+qc+ls)
            n1=0
            for f,b in self.err_stats["fields_err_fmt"].items():
                n1 += 1
                outline=""
                if n1>1:
                    outline=c
                outline += lbq + "field" + qcq + str(f) + qcom
                outline += DQ + "count" + qc + str(b["count"]) + c
                outarray.append(outline)
                outarray.append(DQ+"reasons"+qc + ls)
                n2=0
                for r,n in b["reasons"].items():
                    n2 += 1
                    outline=""
                    if n2>1:
                        outline=c
                    outline += lbq + "reason" + qcq + str(r) + qcom
                    outline += DQ + "count" + qc + str(n) + rb
                    outarray.append(outline)
                outarray.append(rs)
                outarray.append(rb)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(rs)
            outarray.append(rb)
            # end err_stats

            outarray.append(clbq+"err_datatype_examples"+qc+ls)
            for i in range(len(self.err_datatype_examples)):
                outline=""
                if i>0:
                    outline=c
                txt=self.err_datatype_examples[i]
                txt1=""
                if txt.startswith("("):
                    txt1=txt[1:txt.find(")")]
                    txt=txt[txt.find(")")+1:]
                txt= recfuncs.extract_char_aliases(txt,[",","|","/","(",")","[","]"])
                if len(txt1)>0:
                    outline += lbq + "nline" + qc + txt1
                    outline += c+ DQ + "rec" + qcq + txt + qrb
                    outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"err_fmt_examples"+qc+ls)
            for i in range(len(self.err_fmt_examples)):
                outline=""
                if i>0:
                    outline=c
                txt=self.err_fmt_examples[i]
                txt1=""
                if txt.startswith("("):
                    txt1=txt[1:txt.find(")")]
                    txt=txt[txt.find(")")+1:]
                txt= recfuncs.extract_char_aliases(txt,[",","|","/","(",")","[","]"])
                if len(txt1)>0:
                    outline += lbq + "nline" + qc + txt1
                    outline += c+ DQ + "rec" + qcq + txt + qrb
                    outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"rec_size_dist"+qc+ls)
            n1=0
            for k,v in self.rec_size_dist.items():
                n1 += 1
                outline=""
                if n1>1:
                    outline=c
                outline += lbq + k + qc + str(v) + rb
                outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"rec_parse_dist"+qc+ls)
            n1=0
            for k,v in self.rec_parse_dist.items():
                n1 += 1
                outline=""
                if n1>1:
                    outline=c
                outline += lbq + k + qc + str(v) + rb
                outarray.append(outline)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"rec_parse_errs"+qc+ls)
            outarray.append(lbq + "small1" + qc + str(self.rec_parse_errs["small1"]) + rb)
            outarray.append(clbq + "small2" + qc + str(self.rec_parse_errs["small2"]) + rb)
            outarray.append(clbq + "big" + qc + str(self.rec_parse_errs["big"]) + rb)
            outarray.append(rs)
            outarray.append(rb)

            outarray.append(clbq+"rec_parse_errs_examples"+qc+ls)
            n1=0
            if len(self.rec_parse_errs["small1_recs"])>0:
                n1 += 1
                outarray.append(lbq + "small1" + qc + ls)
                for i in range(len(self.rec_parse_errs["small1_recs"])):
                    outline=""
                    if i>0:
                        outline=c
                    txt= recfuncs.extract_char_aliases(self.rec_parse_errs["small1_recs"][i],[","," ","|","/","(",")"])
                    outline += lbq + "record" + qcq + txt + qrb
                    outline += lbq+txt+qrb
                    outarray.append(outline)
                outarray.append(rs)
                outarray.append(rb)
            if len(self.rec_parse_errs["small2_recs"])>0:
                n1 += 1
                txt=""
                if n1>1:
                    txt=c
                outarray.append(txt+lbq + "small2" + qc + ls)
                for i in range(len(self.rec_parse_errs["small2_recs"])):
                    outline=""
                    if i>0:
                        outline=c
                    txt= recfuncs.extract_char_aliases(self.rec_parse_errs["small2_recs"][i],[","," ","|","/","(",")"])
                    outline += lbq + "record" + qcq + txt + qrb
                    outarray.append(outline)
                outarray.append(rs)
                outarray.append(rb)
            if len(self.rec_parse_errs["big_recs"])>0:
                n1 += 1
                txt=""
                if n1>1:
                    txt=c
                outarray.append(txt+lbq + "big" + qc + ls)
                for i in range(len(self.rec_parse_errs["big_recs"])):
                    outline=""
                    if i>0:
                        outline=c
                    txt= recfuncs.extract_char_aliases(self.rec_parse_errs["big_recs"][i],[","," ","|","/","(",")"])
                    outline += lbq + "record" + qcq + txt + qrb
                    outarray.append(outline)
                outarray.append(rs)
                outarray.append(rb)
            outarray.append(rs)
            outarray.append(rb)

            # final closing
            outarray.append(rs)
            outarray.append(rb)

            if add_lf:
                for i in range(len(outarray)):
                    outarray[i] += LF
        except (RuntimeError, OSError, ValueError) as err:
            outarray.insert(0,"notok:" + str(err))
        return outarray
