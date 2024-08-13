"""
Field and CoValue objects
"""

__all__ = ['Field','CoValue']
__version__ = '1.0'
__author__ = 'Geoffrey Malafsky'
__email__ = 'gmalafsky@technikinterlytics.com'
__date__ = '20240627'


class Field:
    """
    Field object with attributes for title, datatype, formatting
    title: field name. Cannot use special characters
    datatype: field datatype (string, int, real, bool, date)
    fmt_strcase: for datatype=string, optionally specifies a value is upper or lower case. (upper,lower,"") 
    fmt_strlen: for datatype=string, optionally specifies a required integer length (1-n). If value < 1 then this is ignored.
    fmt_strcut: for datatype= string when strlen>0 and value length larger then chars removed from either front or back. Default is back (front,back)
    fmt_strpad: for datatype= string when strlen>0 and value length shorter then chars added to either front or back. Default is back (front,back)
    fmt_strpadchar: for datatype= string when padding uses this character. Must be 1 character or use one of names (space, fslash, bslash, tab). Default is _
    fmt_decimal: for datatype=real, optionally specifies a required integer number of decimal places (0-n)
    fmt_date: for datatype=date, optionally specifies a required date format as one of-
        mmddyy, mmdyy, mdyy, mmddyyyy, mmdyyyy, mdyyyy, 
        ddmmyy, ddmyy, dmyy, ddmmyyyy, ddmyyyy, dmyyyy,
        yymmdd, yymmd, yymd, yyyymmdd, yyyymmd, yyyymd, 
        yyyyddd (3 digit day number within year), 
        yyyyMMMdd, ddMMMyyyy (MMM = 3 letter month title like 'JAN'),
        'MONTHdd,yyyy', 'ddMONTH,yyyy', yyyyMONTHdd, ddMONTHyyyy, yyMONTHdd, ddMONTHyy (MONTH full title),
        *dmmyyyy, mm*dyyyy, *mddyyyy, dd*myyyy (*= can be 1 or 2 characters)
    mapto: when using this Field as an output (i.e. target) field then this specifies if it is 
        mapped to a source field which enables both renaming source fields and adding enrichment fields
    parse_error_action: Handle empty field values due to parsing errors. Used in Refining Data as: 
		a) value to assign like 'NA' to denote parse error
		b) set to '-ignore-' which causes the field value to remain as empty since 
		    no transform nor normalize will be done
		c) set to either '-use-' or '' which causes the empty field value to continue to 
		    transform and normalization routines. Note the transform function ifEmpty and ifNotEmpty can be used to set field specific values.
    """

    def __init__(self, title:str) -> None:
        self.title= title
        self.datatype=""
        self.fmt_strcase=""
        self.fmt_strlen=-1
        self.fmt_strcut="back"
        self.fmt_strpad="back"
        self.fmt_strpadchar="_"
        self.fmt_decimal=-1
        self.fmt_date=""
        self.mapto=""
        self.parse_error_action=""

    def get_json(self):
        """
        make JSON of field object as {"field":{"title":"xxxx","datatype":"xxxxx","strcase":fmt_strcase,"strlen":fmt_strlen....}}
        """

        result:str=""
        dblquote:str="\""
        result="{" + dblquote + "field" + dblquote + ":{"
        result += dblquote + "title" + dblquote + ":" + dblquote + self.title + dblquote
        result += "," + dblquote + "datatype" + dblquote + ":" + dblquote + self.datatype + dblquote
        result += "," + dblquote + "strcase" + dblquote + ":" + dblquote + self.fmt_strcase + dblquote
        result += "," + dblquote + "strlen" + dblquote + ":" + dblquote + str(self.fmt_strlen) + dblquote
        result += "," + dblquote + "strcut" + dblquote + ":" + dblquote + self.fmt_strcut + dblquote
        result += "," + dblquote + "strpad" + dblquote + ":" + dblquote + self.fmt_strpad + dblquote
        result += "," + dblquote + "strpadchar" + dblquote + ":" + dblquote + self.fmt_strpadchar + dblquote
        result += "," + dblquote + "decimal" + dblquote + ":" + dblquote + str(self.fmt_decimal) + dblquote
        result += "," + dblquote + "date" + dblquote + ":" + dblquote + self.fmt_date + dblquote
        result += "," + dblquote + "mapto" + dblquote + ":" + dblquote + self.mapto + dblquote
        result += "," + dblquote + "parserroraction" + dblquote + ":" + dblquote + self.parse_error_action + dblquote
        result += "}}"
        return result



class CoValue:
    """
    CoValue object to define 2 or 3 fields for joint value analysis
    
    * title: title which is concantenation of field titles using _ to join them
    * field1: required first field title
    * field2: required second field title
    * field3: optional third field title
    * field1_index: first field's array index assigned by function
    * field2_index: second field's array index assigned by function
    * field3_index: third field's array index assigned by function
    * numfields: number of fields to use either 2 or 3
    """


    def __init__(self, title:str) -> None:
        self.title= title
        self.field1=""
        self.field2=""
        self.field3=""
        self.field1_index=-1
        self.field2_index=-1
        self.field3_index=-1
        self.numfields= 0

    def get_json(self):
        """
        make JSON of object as {"covalue":{"title":"xxxx","field1":field1,"field2":field2,"field3":field3,"field1_index":field1_index,"field2_index":field2_index,"field3_index":field3_index, "numfields":numfields}}
        """

        result:str=""
        dblquote:str="\""
        result="{" + dblquote + "covalue" + dblquote + ":{"
        result += dblquote + "title" + dblquote + ":" + dblquote + self.title + dblquote
        result += "," + dblquote + "field1" + dblquote + ":" + dblquote + self.field1 + dblquote
        result += "," + dblquote + "field2" + dblquote + ":" + dblquote + self.field2 + dblquote
        result += "," + dblquote + "field3" + dblquote + ":" + dblquote + self.field3 + dblquote
        result += "," + dblquote + "field1_index" + dblquote + ":" + dblquote + str(self.field1_index) + dblquote
        result += "," + dblquote + "field2_index" + dblquote + ":" + dblquote + str(self.field2_index) + dblquote
        result += "," + dblquote + "field3_index" + dblquote + ":" + dblquote + str(self.field3_index) + dblquote
        result += "," + dblquote + "numfields" + dblquote + ":" + dblquote + str(self.numfields) + dblquote
        result += "}}"
        return result

