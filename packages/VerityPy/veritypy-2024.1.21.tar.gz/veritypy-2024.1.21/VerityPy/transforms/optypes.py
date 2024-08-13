#!/usr/bin/env python
"""
Types for transform operation objects. Each operation category (OpCat)
has one or more functions each of which is defined by an OpFunc object.

Function setup_op_cats is a convenience method to make list 
transform_types which contains OpCat objects, each of which defines a category 
of transform operations (Ops), and contains a child list of OpFunc objects. 
"""

__all__ = ['OpFunc', 'OpCat', 'setup_op_cats']
__version__ = '1.1'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240804'


class OpFunc:
    """
    Function definition for defining transform operations. 
    This is intended to be used for the specification of available transform operations.
    title: name of function such as ifEq
    desc: description
    param1req: true/false whether param1 is required to be set
    param1typ: datatype of param1 if it is restricted to one type
    param2req: true/false whether param2 is required to be set
    param2typ: datatype of param2 if it is restricted to one type
    param3req: true/false whether param3 is required to be set
    param3typ: datatype of param3 if it is restricted to one type
    """

    title:str
    desc:str
    param1req: bool
    param1typ: str
    param2req: bool
    param2typ: str
    param3req: bool
    param3typ: str

    def __init__(self, title:str):
        self.title=title
        self.desc=""
        self.param1req=False
        self.param1typ=""
        self.param2req=False
        self.param2typ=""
        self.param3req=False
        self.param3typ=""


class OpCat:
    """
    Category for transform operations grouped by either type of action performed 
    or datatype it is applied to. Categories include: assignment, conditional, 
    numeric, text, date. Member 'funcs' is a list of OpFunc objects.
    """

    category: str
    funcs: list

    def __init__(self, category:str):
        self.category=category
        self.funcs=[]


def setup_op_cats() -> list:
    """
    Function to fill list with OpCat objects and for each their list of child OpFunc objects

    Returns list of OpCat objects
    """

    transform_types:list=[]
    try:
        # ASSIGNMENT
        oc = OpCat("assignment")
        #    --------
        f = OpFunc("noOp")
        f.desc= "No operation. Use to stop operations in conditional sequence."
        oc.funcs.append(f)
        #    --------
        f = OpFunc("setToValue")
        f.desc= "Assign a fixed value. Param1: value"
        f.param1req=True
        f.param1typ="string"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("setToIndex")
        f.desc= "Assign a fixed value equal to the record's index in output set. "
        f.desc += "Param1: optional as integer start index >=0. Default is 0. "
        f.desc += "Application code must supply current record index to exectransform.do_transform. Default = 0. "
        f.desc += "Assigned index = Param1 + current_record_index"
        f.param1req=False
        f.param1typ="int"
        oc.funcs.append(f)
        #    --------
        f=OpFunc("setToRef")
        f.desc="Assigns the value of a referenced source field in the current record. Param1: title of field"
        f.param1req=True
        f.param1typ="string"
        oc.funcs.append(f)
        #    --------
        f=OpFunc("setToRandom")
        f.desc = "Uses random number generator to produce a value scaled between the minimum and maximum values. "
        f.desc += "Param1: optional as minimum. Default is 0. "
        f.desc += "Param2: optional as maximum. Default is 1. If this is < min then set to min + 1. "
        f.param1req=False
        f.param1typ="real"
        f.param2req=False
        f.param2typ="real"
        oc.funcs.append(f)
        #    --------
        f=OpFunc("setToFreqList")
        f.desc = "Applies a value from a list using relative frequencies of occurrence for a base value. "
        f.desc += "Param1: relative frequencies of occurrence. Can use any real >0 and will be scaled to sum. "
        f.desc += "Since list, enter delimited by pipe such as 2|7|.5|9 where the second list item "
        f.desc += "occurs 37.8% percent (7/18.5) of the time. "
        f.desc += "Param2: list of values correlated to Param1 frequencies and "
        f.desc += "entered with pipe delimiter like red|green|blue|orange. "
        f.desc += "Param3: optional. If used, either a reference field title to use as source of base value, or a real number 0.0-1.0 . "
        f.desc += "Otherwise, the default is to use a random number."
        f.param1req=True
        f.param1typ="string"
        f.param2req=True
        f.param2typ="string"
        f.param3req=False
        f.param3typ="string"
        oc.funcs.append(f)
        #    --------
        f=OpFunc("lookup")
        f.desc= "Assigns a value from a lookup list based on matching values to keys where keys can use wildcards. "\
        "The match can be made to one, two, or three source fields in the record with field 1 always "\
        "the current value while fields 2 and 3 are optional if set in Param2. "\
        "Leave Param2 empty to use only 1 field as the match value. All selected fields must match their "\
        "respective conditions for a lookup result to be assigned. "\
        "The lookup dictionary has records each with properties: key1, key2, key3, value "\
        "depending on how many keys are used which is set by Param1 and Param2. "\
        "Keys can use front and/or back wildcard (*) like top*, *night, *state* to allow token matching. "\
        "Param1: title of list that has been pre-loaded into array of lists as part of initialization. "\
        "Param2: Field 2 title, or fields 2 and 3 titles. If both supplied use pipe to delimit as with field2|field3. "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="string"
        oc.funcs.append(f)
        transform_types.append(oc)
        # CONDITIONAL
        oc = OpCat("conditional")
        #    --------
        f = OpFunc("ifEmpty")
        f.desc= "If value is empty. Compares current value as string"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotEmpty")
        f.desc= "If value is not empty. Compares current value as string"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifEq")
        f.desc= "If equals. Compares current value as real number (converted from string) to Param1 "
        f.desc += "(also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotEq")
        f.desc= "If not equals. Compares current value as real number (converted from string) to Param1 "
        f.desc += "(also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifGte")
        f.desc= "If greater than or equals. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotGte")
        f.desc= "If not greater than or equals. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifGt")
        f.desc= "If greater than. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotGt")
        f.desc= "If not greater than. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifLte")
        f.desc= "If less than or equals. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotLte")
        f.desc= "If not less than or equals. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifLt")
        f.desc= "If less than. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotLt")
        f.desc= "If not less than. Compares current value as real number (converted from string) "
        f.desc += "to Param1 (also converted) from string or one of the char_aliases for PI (math.pi) or E (math.e)"
        f.param1req=True
        f.param1typ="real"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifStrEq")
        f.desc= "If strings are equal. Compares current value to Param1 as string or one of the char_aliases. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotStrEq")
        f.desc= "If strings are not equal. Compares current value to Param1 as string or one of the char_aliases. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifStrStarts")
        f.desc= "If current value starts with Param1. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotStrStarts")
        f.desc= "If current value not starts with Param1. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifStrContains")
        f.desc= "If current value contains Param1. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.desc += "Param3: optional whether remove all spaces from current value before comparing "
        f.desc += "so 'this is me' becomes 'thisisme' (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        f.param3req=False
        f.param3typ="bool"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotStrContains")
        f.desc= "If current value not contains Param1. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.desc += "Param3: optional whether remove all spaces from current value before comparing "
        f.desc += "so 'this is me' becomes 'thisisme' (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        f.param3req=False
        f.param3typ="bool"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifStrEnds")
        f.desc= "If current value ends with Param1. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        oc.funcs.append(f)
        #    --------
        f = OpFunc("ifNotStrEnds")
        f.desc= "If current value not ends with Param1. "
        f.desc += "You can specify multiple test strings by delimiting with pipe (no spacing) as "
        f.desc += "with Strong|strENGTH|power . "
        f.desc += "Param1: comparison value. "
        f.desc += "Param2: optional whether case sensitive (default is false). "
        f.param1req=True
        f.param1typ="string"
        f.param2req=False
        f.param2typ="bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifInt")
        f.desc= "If integer. Param1 specifies if must be positive integer, negative, or any. "
        f.desc += "Param1: optional ['any','positive','negative'] default=any"
        f.param1req=False
        f.param1typ="string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifNotInt")
        f.desc= "If not integer. Param1 specifies if must be positive integer, negative, or any. "
        f.desc += "Param1: optional ['any','positive','negative'] default=any"
        f.param1req=False
        f.param1typ="string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifReal")
        f.desc= "If real. Param1 specifies if must be positive, negative, or any. "
        f.desc += "Param1: optional ['any','positive','negative'] default=any"
        f.param1req=False
        f.param1typ="string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifNotReal")
        f.desc= "If not real. Param1 specifies if must be positive, negative, or any. "
        f.desc += "Param1: optional ['any','positive','negative'] default=any"
        f.param1req=False
        f.param1typ="string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifISODate")
        f.desc= "If in ISO DateTime format of yyyyMMdd with optional time part of Thhmmss. "
        f.desc += "Date part may use delimiters / or -. "
        f.desc += "Time part may use delimiter :. Examples: 2024-03-24T14:33:05, 20240324T143305, 20240324"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifNotISODate")
        f.desc= "If not in ISO DateTime format of yyyyMMdd with optional time part of Thhmmss. "
        f.desc += "Date part may use delimiters / or -. "
        f.desc += "Time part may use delimiter :. Examples: 2024-03-24T14:33:05, 20240324T143305, 20240324"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifDateFormat")
        f.desc= "If in supplied date format. Date may use delimiters / or -. "
        f.desc += "Param1: format with MMM for month abbreviation like Jan or Aug, "
        f.desc += "and MONTH for full name like January. "
        f.desc += "Formats: mmddyy, mmdyy,mdyy,mmddyyyy,mmdyyyy,mdyyyy,ddmmyy,ddmyy,dmyy,ddmmyyyy,ddmyyyy,dmyyyy,"
        f.desc += "yymmdd,yymmd,yymd,yyyymmdd,yyyymmd,yyyymd,yyyyddd,yyyyMMMdd,ddMMMyyyy,"
        f.desc += "MONTHdd,yyyy,ddMONTH,yyyy,yyyyMONTHdd,ddMONTHyyyy,yyMONTHdd,ddMONTHyy"
        f.param1req=True
        f.param1typ="string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ifNotDateFormat")
        f.desc= "If not in supplied date format. Date may use delimiters / or -. "
        f.desc += "Param1: format with MMM for month abbreviation like Jan or Aug, "
        f.desc += "and MONTH for full name like January. "
        f.desc += "Formats: mmddyy, mmdyy,mdyy,mmddyyyy,mmdyyyy,mdyyyy,ddmmyy,ddmyy,dmyy,ddmmyyyy,ddmyyyy,dmyyyy,"
        f.desc += "yymmdd,yymmd,yymd,yyyymmdd,yyyymmd,yyyymd,yyyyddd,yyyyMMMdd,ddMMMyyyy,"
        f.desc += "MONTHdd,yyyy,ddMONTH,yyyy,yyyyMONTHdd,ddMONTHyyyy,yyMONTHdd,ddMONTHyy"
        f.param1req=True
        f.param1typ="string"
        oc.funcs.append(f)
        transform_types.append(oc)
        # NUMERIC
        oc = OpCat("numeric")
        #    --------
        f= OpFunc("convertMainFrameNumber")
        f.desc= "Converts a number in string representation in coded main frame format to string of real number. "
        f.desc += "Encoded last character is indicator of this formatting including sign reversal if necessary. "
        f.desc += "Always makes last 2 digits into decimal portion so no further divide by 100 is necessary. "
        f.desc += "If special char is within input string it becomes the end char and the "
        f.desc += "remaining suffix is discarded. Leading zeros are truncated so 000.12 becomes 0.12 . Codes are:"
        f.desc += "{= 0, }= 0 and negate; "
        f.desc += "a= 1, j= 1 and negate; "
        f.desc += "b= 2, k= 2 and negate; "
        f.desc += "c= 3, l= 3 and negate; "
        f.desc += "d= 4, m= 4 and negate; "
        f.desc += "e= 5, n= 5 and negate; "
        f.desc += "f= 6, o= 6 and negate; "
        f.desc += "g= 7, p= 7 and negate; "
        f.desc += "h= 8, q= 8 and negate; "
        f.desc += "i= 9, r= 9 and negate"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("round")
        f.desc= "Rounds number to specified number of decimal digits. If "
        f.desc += "number digits=0 (default) then nearest integer made (real datatype ends .00). "
        f.desc += "Midpoint goes to even number."
        f.param1req= False
        f.param1typ= "integer"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("floor")
        f.desc= "Returns the largest integral value less than or equal to number. "
        f.desc += "If for a real datatype, will end with .00"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ceiling")
        f.desc= "Returns the smallest integral value greater than or equal to number. "
        f.desc += "If for a real datatype, will end with .00"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("abs")
        f.desc= "Returns absolute value"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("negate")
        f.desc= "Inverts sign"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("mult")
        f.desc= "Multiply current value by supplied number. May use special notations. "
        f.desc += "Param1: number for operation"
        f.desc += "Param2: optional boolean whether to clean number of non-numeric prefix and suffix characters. Default is true."
        f.param1req= True
        f.param1typ= "real"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("div")
        f.desc= "Divide current value by supplied number (current/x). May use special notations. "
        f.desc += "Param1: number for operation. If =0 then result= 9.99 x 10^10 "
        f.desc += "Param2: optional boolean whether to clean number of non-numeric prefix and suffix characters. Default is true."
        f.param1req= True
        f.param1typ= "real"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("divfrom")
        f.desc= "Divide current value from supplied number (x/current). May use special notations. "
        f.desc += "Param1: number for operation. If =0 then result=0 while if current value=0 then result= 9.99 x 10^10 "
        f.desc += "Param2: optional boolean whether to clean number of non-numeric prefix and suffix characters. Default is true."
        f.param1req= True
        f.param1typ= "real"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("add")
        f.desc= "Add current value by supplied number. May use special notations. "
        f.desc += "Param1: number for operation"
        f.desc += "Param2: optional boolean whether to clean number of non-numeric prefix and suffix characters. Default is true."
        f.param1req= True
        f.param1typ= "real"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("subtract")
        f.desc= "Subtract current value by supplied number (current-x). May use special notations. "
        f.desc += "Param1: number for operation"
        f.desc += "Param2: optional boolean whether to clean number of non-numeric prefix and suffix characters. Default is true."
        f.param1req= True
        f.param1typ= "real"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("subtractFrom")
        f.desc= "Subtract current value from supplied number (x-current). May use special notations. "
        f.desc += "Param1: number for operation"
        f.desc += "Param2: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "real"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("multByRef")
        f.desc= "Multiply current value by value of referenced field. "
        f.desc += "Param1: source field title"
        f.desc += "Param2: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("divByRef")
        f.desc= "Divide current value by value of referenced field (current/ref). "
        f.desc += "If Param1=0 then result= 9.99 x 10^10"
        f.desc += "Param1: source field title"
        f.desc += "Param2: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("divFromRef")
        f.desc= "Divide current value from value of referenced field (ref/current). "
        f.desc += "If current=0 then result= 9.99 x 10^10"
        f.desc += "Param1: source field title"
        f.desc += "Param2: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("addByRef")
        f.desc= "Add current value by value of referenced field. "
        f.desc += "Param1: source field title"
        f.desc += "Param2: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("subtractByRef")
        f.desc= "Subtract current value by value of referenced field (current-ref). "
        f.desc += "Param1: source field title"
        f.desc += "Param2: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("subtractFromRef")
        f.desc= "Subtract current value from value of referenced field (ref-current). "
        f.desc += "Param1: source field title"
        f.desc += "Param2: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("multRefs")
        f.desc= "Multiply referenced fields. "
        f.desc += "Param1: first field title"
        f.desc += "Param2: second field title or multiple field titles separated by commas like title2,title3,title4"
        f.desc += "Param3: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= True
        f.param2typ= "string"
        f.param3req= False
        f.param3typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("addRefs")
        f.desc= "Add referenced fields. "
        f.desc += "Param1: first field title"
        f.desc += "Param2: second field title or multiple field titles separated by commas like title2,title3,title4"
        f.desc += "Param3: optional boolean whether to use cleanNumber before action. Default is true."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= True
        f.param2typ= "string"
        f.param3req= False
        f.param3typ= "bool"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("log")
        f.desc= "Base 10 log of current value. If value<0 then result= -10^10. "
        f.desc += "If datatype is int then result uses FLOOR. "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ln")
        f.desc= "Base E log of current value. If value<0 then result= -10^10. "
        f.desc += "If datatype is int then result uses FLOOR. "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("pow10")
        f.desc= "Base 10 exponential of current value. "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("powe")
        f.desc= "Base E exponential of current value. "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("setDecimal")
        f.desc= "Sets number of decimal places for number. If <=0 then value is truncated to integer. "
        f.desc += "If less than number's decimals, excess digits cut. If greater, decimal places padded right with 0. "
        f.desc += "Param1: integer number of decimal places"
        f.param1req= True
        f.param1typ= "integer"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("convertFromExp")
        f.desc= "Convert a string representing exponential number into non-exponential number. "
        f.desc += "String will be checked for format n.nnEsnn where n is integer digit, "
        f.desc += "and s is an optional + or -. String can also have front - or be enclosed in parentheses. Examples: "
        f.desc += "1.3E05 converted to 130000, -1.23e-1 converted to -0.123"
        oc.funcs.append(f)
        transform_types.append(oc)
        # TEXT
        oc = OpCat("text")
        #    --------
        f= OpFunc("trim")
        f.desc= "Remove whitespace left (i.e. front) and right (i.e. back)"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("ltrim")
        f.desc= "Remove whitespace left side (front). "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("rtrim")
        f.desc= "Remove whitespace right side (back). "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("toLower")
        f.desc= "Set to lower case. "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("toUpper")
        f.desc= "Set to upper case. "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("toTitle")
        f.desc= "Set to title case. "
        oc.funcs.append(f)
        #    --------
        f= OpFunc("front")
        f.desc= "Take characters from front of string. "
        f.desc += "Matching part is found in current value and then cut after its first occurrence, "
        f.desc += "such as 'r' for value 'horse' yields 'hor'."
        f.desc += "Param1: string to find match"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("before")
        f.desc= "Take characters from before a string match. "
        f.desc += "Matching part is found in current value and then cut before its first occurrence, "
        f.desc += "such as 'r' for value 'horse' yields 'ho'."
        f.desc += "Param1: string to find match"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("frontN")
        f.desc= "Take N characters from front of string. "
        f.desc += "Param1: number chars"
        f.param1req= True
        f.param1typ= "integer"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("end")
        f.desc= "Take characters from end of string including match. "
        f.desc += "Matching part is found in current value and then cut at its first occurrence to end, "
        f.desc += "such as 'r' for value 'horse' yields 'rse'."
        f.desc += "Param1: string to find match"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("after")
        f.desc= "Take characters from end of string after the match. "
        f.desc += "Matching part is found in current value and then cut after its first occurrence to end, "
        f.desc += "such as 'r' for value 'horse' yields 'se'."
        f.desc += "Param1: string to find match"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("endN")
        f.desc= "Take N characters from end of string. "
        f.desc += "Param1: number chars"
        f.param1req= True
        f.param1typ= "integer"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("mid")
        f.desc= "Take characters from middle of string. "
        f.desc += "Matching part is found in current value and then cut after its first occurrence, "
        f.desc += "If Param2 not used, result is after cutting with Param1. "
        f.desc += "If Param2 is used, then initial result is again cut after Param2's occurrence "
        f.desc += "meaning result is string including Param1 and Param2 only. "
        f.desc += "For value 'Semantics' Param1='m' and Param2='c' yields 'mantic'. "
        f.desc += "For value 'mishmash' Param1='ma' and Param2='s' yields 'mas'."
        f.desc += "Param1: string to find match"
        f.desc += "Param2: optional string to find second match"
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("midN")
        f.desc= "Take N characters from middle of string. Result is after cutting at Param1 character index from front of string. "
        f.desc += "If Param2 not used,   to end of string. "
        f.desc += "For value 'Semantics' Param1='2' and Param2='6' yields 'mantic' , and "
        f.desc += "for value 'mishmash' Param1='4' and Param2='3' yields 'mas'."
        f.desc += "Param1: integer starting position using 0-based indexing"
        f.desc += "Param2: optional second integer for number of characters to take"
        f.param1req= True
        f.param1typ= "integer"
        f.param2req= False
        f.param2typ= "integer"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("charAt")
        f.desc= "Take 1 character at position (0-based). "
        f.desc += "Param1: number char"
        f.param1req= True
        f.param1typ= "integer"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("prepend")
        f.desc= "Add string to front of value. "
        f.desc += "Param1: string to add"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("append")
        f.desc= "Adds string to end of value. "
        f.desc += "Param1: string to add"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("remove")
        f.desc= "Removes all instances string from value. "
        f.desc += "Param1: string to remove"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("replace")
        f.desc= "Replaces all instances string in value. "
        f.desc += "Param1: string to remove. "
        f.desc += "Param2: string to insert"
        f.param1req= True
        f.param1typ= "string"
        f.param2req= True
        f.param2typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("setLength")
        f.desc= "Sets value to specific length by cutting or padding characters as needed. "
        f.desc += "Param1: integer character length. "
        f.desc += "Param2: optional side to act on (cut or pad) if existing string is not N chars. "
        f.desc += "Either left (i.e front) or right (i.e. back). Default is right. "
        f.desc += "Param3: optional char to pad with if needed. Default is x. If longer than 1 char only first used."
        f.param1req= True
        f.param1typ= "integer"
        f.param2req= False
        f.param2typ= "string"
        f.param3req= False
        f.param3typ= "string"
        oc.funcs.append(f)
        transform_types.append(oc)
        # DATE
        oc = OpCat("date")
        #    --------
        f= OpFunc("setToISODate")
        f.desc= "Creates an ISO 8601 DateTime string yyyyMMddThhmmss. "
        f.desc += "Param1: Either today for current date, now for current date and time, or ISO DateTime. "
        f.desc += "Param2: optional for either 'today' or 'now' (ignored when Param1 is ISO dateTime) the number hours timezone offset from UTC (e.g. Dallas TX is -5, Kolkata India is +5.5, New York NY is -4), "
        f.desc += "otherwise the computer's time zone is used so depends on server settings."
        f.param1req= True
        f.param1typ= "string"
        f.param2req= False
        f.param2typ= "real"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("dateToISO")
        f.desc= "Converts data in specified format to ISO 8601 date yyyyMMdd. "
        f.desc += "Param1: format with MMM for month abbreviation like Jan or Aug, "
        f.desc += "and MONTH for full name like January. "
        f.desc += "Formats: mmddyy, mmdyy,mdyy,mmddyyyy,mmdyyyy,mdyyyy,ddmmyy,ddmyy,dmyy,ddmmyyyy,ddmyyyy,dmyyyy,"
        f.desc += "yymmdd,yymmd,yymd,yyyymmdd,yyyymmd,yyyymd,yyyyddd,yyyyMMMdd,ddMMMyyyy,"
        f.desc += "MONTHdd,yyyy,ddMONTH,yyyy,yyyyMONTHdd,ddMONTHyyyy,yyMONTHdd,ddMONTHyy"
        f.param1req= True
        f.param1typ= "string"
        oc.funcs.append(f)
        #    --------
        f= OpFunc("excelDateNumberToISO")
        f.desc= "Converts a date in numeric excel format into ISO8601 yyyymmdd format with "
        f.desc += "fractional days removed. Excel uses "
        f.desc += "number days since January 1, 1900 as its counting base. "
        f.desc += "Example: 44416 = 20210808, 42855 = 20170430"
        oc.funcs.append(f)
        transform_types.append(oc)
    except RuntimeError as err:
        print("error:",err)
    return transform_types
