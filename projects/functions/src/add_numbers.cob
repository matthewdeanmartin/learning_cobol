       FUNCTION-ID. Add-Numbers.
       DATA DIVISION.
       LINKAGE SECTION.
       01 Param1 PIC 9(3).
       01 Param2 PIC 9(3).
       01 Summation PIC 9(4).
       PROCEDURE DIVISION USING Param1, Param2 RETURNING Summation.
           ADD Param1 TO Param2 GIVING Summation.
           GOBACK.
       END FUNCTION  Add-Numbers.
       