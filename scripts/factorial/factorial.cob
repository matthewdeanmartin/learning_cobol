///usr/bin/true; exec /C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -xjc -fmfcomment "$0" "$@"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. factorial.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 result PIC 9(18) VALUE 1.
       LINKAGE SECTION.
       01 input-number PIC 9(5).
       01 output-factorial PIC 9(18).
       PROCEDURE DIVISION USING input-number output-factorial.
           PERFORM VARYING result FROM 1 BY 1 UNTIL result > input-number
               MULTIPLY result BY output-factorial
           END-PERFORM.
           EXIT PROGRAM.