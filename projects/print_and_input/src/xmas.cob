///usr/bin/true; exec /C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -xj -fmfcomment "$0" "$@"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. ChristmasTree.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 HEIGHT           PIC 99 VALUE 5.
       01 CURRENT-ROW      PIC 99 VALUE 0.
       01 SPACERS          PIC X(50) VALUE SPACES.
       01 STARS            PIC X(50) VALUE ALL "*".
       01 NUM-STARS        PIC 99.
       01 NUM-SPACES       PIC 99.

       PROCEDURE DIVISION.
      *    DISPLAY "Enter the height of the tree (1-50):".
      *    ACCEPT HEIGHT.
           MOVE ALL "*" TO STARS
           MOVE SPACES TO SPACERS
               
           PERFORM VARYING CURRENT-ROW FROM 0 BY 1 
                   UNTIL CURRENT-ROW >= HEIGHT
               COMPUTE NUM-SPACES = HEIGHT - CURRENT-ROW - 1
               COMPUTE NUM-STARS = (2 * CURRENT-ROW) + 1
               DISPLAY SPACERS(1:NUM-SPACES) STARS(1:NUM-STARS)
           END-PERFORM.

           STOP RUN.
