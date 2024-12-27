///usr/bin/true; exec /C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -Wall -xj -fmfcomment "$0" "$@"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. ListFiles.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
       SELECT FILE-LIST ASSIGN TO "filelist.txt"
           ORGANIZATION IS SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  FILE-LIST.
       01  FILE-RECORD PIC X(256).


       WORKING-STORAGE SECTION.
       01  WS-COMMAND PIC X(256) VALUE SPACES.
       01  WS-EOF       PIC X VALUE "N".
       01  WS-DISPLAY-RECORD PIC X(256).
       01 WS-LENGTH        PIC 9(3) VALUE 0.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
       MOVE "ls > filelist.txt" TO WS-COMMAND.
       CALL "SYSTEM" USING WS-COMMAND.

       OPEN INPUT FILE-LIST.
       PERFORM UNTIL WS-EOF = "Y"
           MOVE SPACES TO FILE-RECORD
           READ FILE-LIST INTO FILE-RECORD
               AT END MOVE "Y" TO WS-EOF
               NOT AT END
                   DISPLAY FILE-RECORD
           END-READ
       END-PERFORM.

       CLOSE FILE-LIST.
       STOP RUN.
