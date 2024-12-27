///usr/bin/true; exec /C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -xj -fmfcomment "$0" "$@"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. main.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 the-number PIC 9(5) VALUE 5.
       01 factorial-result PIC 9(18).
       PROCEDURE DIVISION.
           CALL "factorial" USING the-number RETURNING factorial-result.
           DISPLAY "Factorial of " the-number " is " factorial-result.
           STOP RUN.
