///usr/bin/true; exec /C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -xj -fmfcomment "$0" "$@"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. MainProgram.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY math-operations.

       PROCEDURE DIVISION.
           MOVE 123 TO addend1.
           MOVE 456 TO addend2.
           PERFORM procedure division END-PERFORM.
           STOP RUN.
