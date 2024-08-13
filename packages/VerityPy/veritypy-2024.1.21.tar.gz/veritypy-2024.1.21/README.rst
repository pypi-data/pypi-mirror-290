Overview
========

**VerityPy** is a Python library by Technik Interlytics for Better Data = Better AI. 
It is a Data Inspector, Remediator, Normalizer on large structured data sets. 
It combines curated human expert knowledge gained from in-depth forensic analysis and remediating data in many fields, 
with Machine Learning pattern extraction results to know where to look, what to look for, and what to do about problems. 
It automates labor-intensive, difficult tasks to improve data quality, remediate errors, 
and enrich data sets ML, Data Science, analytics, forensics, auditing, and warehousing.

|
|

Structured Data Functions
==========================

There are two main types of functions provided on structured data sets:

1. Analyzing: inspects data records for structural and value consistency, 
   anomalies, errors especially deeply buried problems that may only occur in a few records within millions 
   but enough to cause significant bias, discrepancies, and failed validations. Our human experts have discovered many problems common 
   in data systems across business and technical fields that are either not detected or cannot be remediated with standard DataOps. Some examples:

      * data variations (types, formats, encoding) from import/export in different systems especially spreadsheets and legacy mainframes
      * special characters not visible to users causing downstream problems
      * small number of anomalies buried within very large data sets overwhelming tools
      * mismatched joint field values such as geographic location codes and names
      * long strings of digits used as codes (e.g. accounting, ERP) cast into number format stripping digits thereby corrupting codes
      * records broken into multiple lines causing fields to be misaligned, partial records, and incorrect values
      * open source data with embedded information-only records (e.g. IRS USA Migration demographics, Covid disease census) unknown to users

|

2. Normalizing & Enriching: this encompasses everything necessary to get data records 
   accurate for structure (field positions, data types, formats), 
   values (numeric ranges, codes, lists of allowed values), and enrichment 
   (added metadata fields for forensics, training models, analytics). 
   Our human experts have worked extensively in 
   the entire lifecycle of data in multiple fields allowing them to see and understand how and where data can become infected with 
   problems and both the indicators of these problems and how to correct and annotate them to pass scrutiny by human and 
   computer QC. Some examples are:

      * rebuilding records broken into multiple lines
      * adding enrichment fields to annotate pedigree, trust, privacy, increased granularity with conditional logic and controlled vocabulary
      * several levels of conditional testing of multiple fields within single records to correctly encode/decode, transform field values
      * allowing multiple versions of lookup decoding per field based on other field indicators (e.g. time varying encoding schemes)
      * identifying when long values of numeric digits are strings or numbers and handling accordingly
      * lookup dictionary replacements using 1 or multiple fields as well as wildcard tokens and both boolean AND and NOT conditions

|
|

Why Use **VerityPy**
=======================

It was created to solve the need to not just make data accurate, but also provide high visibility into how and why it 
was handled with transforms and codings such that it can be managed like other key business assets with oversight and collaborative review. 
All too often, the actual manipulation of data is handled by proficient engineers but the people who most need to review, understand, and adjust 
what is done are unable to decipher the complicated code, scripts, and technical documentation. Our human experts witnessed this situation in 
many clients and had to solve this challenge before the technical results would be accepted. Doing so led us to develop new data processing and 
reporting approaches that jointly handled complicated data engineering requirements along with visible and easy to understand business reporting. 
**VerityPy** was created to provide this capability to a wide community with the following key concepts:

   * easily reuse and adjust processing parameters for multiple iterations of transforms, codings, rules with reviews of results in end-use applications
   * review data processing steps and intermediate results throughout the entire process (i.e. no black boxes)
   * use processing commands that can be reviewed by business and technical people at both staff and manager levels
   * enable drop-in reporting with summary and detailed charts and tables of data actions, discoveries, and results
   * provide multiple views of data before and after to maximize understanding and discovery among all user types


|
|

What **VerityPy** Does
=======================


Analysis
-----------

**VerityPy** analyzes structured source data and generates a thorough assessment of each field's 
actual value space for data types, formats, ranges, special characters, unique values and even coValues 
which are joint field (2 or 3) value distributions. This is a quick way to both profile source 
data, extract its schema, and discover anomalies that can be overlooked by other tools or 
missed by manual Quality Control reviews. A comprehensive report is returned in a Python object 
that can be used in further processing to make tables and charts such as in Jupyter Notebook.



Goal
+++++++++

The goal of analysis is to characterize data to know its structure, range of values, 
and presence of anomalies in relation to what it should be as defined by its architecture. 
Ideally, the documentation would describe the details of how it was collected, stored, and 
the meaning of the data in the context of its intended use. In this ideal case, unit tests could be 
made to automatically measure quality metrics both as the data is received and processed, and 
as it is distributed and used. Unfortunately, this ideal situation rarely exists and we are forced 
to manage data with uncertain quality, pedigree, and trustworthiness. When the use can tolerate 
imperfect data then this is not much of a problem. However, we now have increasingly stringent needs for 
better data to feed Artificial Intelligence (AI), Data Science (DataSci), and more sophisticated 
forecasting models in financial markets, global supply chain, consumer activity, and many others.




Objectives
++++++++++++++

We have learned from in-depth analysis and thorough reconstruction of data sets across many fields 
and types of data systems that there are several specific types of anomalies that frequenetly exist and 
go undetected by even the most modern tools. Part of this expert assessment included following and measuring 
the impact of the imperfect data on the end-use business activities for how outcome errors impacted 
decision making, audit, compliance, analytics, forecast accuracy, etc. From this we created a combined 
human expert and big data Machine Learning (ML) technology to filter through all data to find several types 
of problems and reliable approaches to correcting them automatically. This led to the following key objectives 
of the VerityX (X denotes both the Python and DotNet libraries) analysis process:

    * capture details of field datatype and format for all records and visibly showcase even infrequent variations.
         - many tools limit the depth and breadth of records analyzed and variations captured due to processing, memory, and storage limitations.
    * capture complete range of values for each field and emphasize low frequency instances since this is how anomalies can be quickly discovered.
    * capture complete range of values for combinations of several fields as another quick way of detecting 
      anomalies and overall quality of fields that are linked by what they mean in end use cases.
    * track number of field values parsed per record as key indicator of presence of extra delimiters and line feeds 
      that are not apparent during human review but which cause parsing code to break what should be a single record 
      into multiple partial records or generate more field values than there are fields. This is surprisingly common 
      in many mid and large size data systems. 
    * provide automated correction algorithms that repair all of the above problems with minimal required data 
      architecture and engineering which tends to be so complicated and labor intensive that it often lags 
      actual data cuasing serious 'technical debt'.
    * provide multiple views and types of results into data quality and problems since real world data teams are typically 
      too constrained in time and personnel to probe every data set, system, and operation in detail.





Results
+++++++++

Results are coordinated in a Python class 'QualityAnalysis' allowing concise handling 
of the setup parameters and the breadth and depth of discovered characteristics and 
known/suspected errors. These results include:

   * field unique values: per field unique values with count of instances.
   * field datatype distributions: each field has counts for detected datatypes (int, real, bool, date, string, empty).
   * field quality: each field is assigned a quality factor 0-100 based on discovered characteristics and knowledge-based algorithms.
   * record size distribution: record sizes (byte lengths) to count of instances.
   * record parsing errors: parsing errors (number fields after parsing relative to defined fields) 
     by small1 (1 too few fields), small2 (2 or more missing fields), big (1 or more too many fields). Also, has example records.
   * record parsing distribution: number of parsed fields to count of instances.
   * special character distribution: special characters and their count of instances, as well as example records.
   * coValues: field combinations (2 or 3) unique value information. 
   * error statistics: values such as number records with any kind of error, number records 
     with datatype error, number records with format error and more



Normalize & Enrich
-------------------

**VerityPy's** transforms allow Normalizing and Enriching source data with 
a higher level of quality, accuracy, and meaning to support demanding use cases. There are five 
kinds of transforms (see transforms page for details):

   1. Assignment: assigns values to field as a fixed value, reference to another field in record, random number, list of categories via frequencies, lookup dictionaries
   2. Conditional: conditional tests of equality and inequality for numeric, string, and date values
   3. Numeric: numeric calculation functions including using other fields in record by reference
   4. Text: manipulate with slicing, adding, padding, replacing
   5. Date: Change date format to ISO 8601 including from special Excel format 

This is an example of a transform to populate an enrichment field 'useAGI' that denotes whether the record should be used 
in analytics based on the value of a numeric source field 'AGI'.

   1. setToRef("AGI")
   2. ifEq("-1")
   3. setToValue("true")
   4. setToValue("false")

In order to allow chaining of conditional functions, the flow is condition -> [false action] else [true action]. Thus, if step 2 above is False 
then step 3 is done and the chain stops, whereas if step 2 is True then step 3 is skipped and step 4 is done (and any steps after it if they existed). 
The net result is this simple transform fills an enrichment field with boolean value enabling easy filtering downstream in a spreadsheet, database, 
or analytics dashboard.

A slightly more complicated logic flow that includes fixing formatting is the following transform that uses a source field 'y2_statefips' containing a 2 character 
code to lookup the corresponding title in an external lookup dictionary and then assigns that to an enrichment field 'DestStateName' since the 
original source data only had the code making it non-intuitive for users to understand the data records. 

   1. setToRef("y2_statefips")
   2. setLength("2","left","0")
   3. lookup("StateName")

Step 1 gets the value of the field 'y2_statefips' from the current record. Step 2 fixes the string length to 2 characters with changes made 
to the left side of the string if it is too long (characters cut from left) or too short (characters added to left) with the character to 
add set to be '0' (zero). This is critical for code lookups since a very common problem when data is moved among systems is for leading 
zeros to be removed thereby changing a code like '01' into '1' which would not be found in the lookup. This ensures that such an error 
is fixed prior to doing the lookup which occurs in step 3 to a dictionary name 'StateName' (loaded during the setup phase of the job).

|
|

License
===========

This is not open source software and cannot be included in an open source project as its license will break the open source license. 
However, there is a license allowing free use for non-commercial, personal applications. 
Read the license file for full details about allowed scope of free use. 
Paid licenses are required for commercial products either distributed or web hosted (e.g. SaaS), as well as enterprise applications with multiple users. 
There are licenses for developers, royalty inclusion in other products, and support.
