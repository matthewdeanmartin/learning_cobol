///usr/bin/true; exec /C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -xj -fmfcomment "$0" "$@"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. MainProgram.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *COPY person.
       01 PersonIndex PIC 9(3).
       01 NewName PIC X(20).
       01 PersonName PIC X(20).


       PROCEDURE DIVISION.
           DISPLAY "Setting names for 3 persons..."

           MOVE 1 TO PersonIndex.
           MOVE "Alice" TO NewName.
           CALL "person" USING PersonIndex NewName PersonName.

           MOVE 2 TO PersonIndex.
           MOVE "Bob" TO NewName.
           CALL "person" USING PersonIndex NewName PersonName.

           MOVE 3 TO PersonIndex.
           MOVE "Charlie" TO NewName.
           CALL "person" USING PersonIndex NewName PersonName.

           DISPLAY "Retrieving names for each person..."
           PERFORM VARYING PersonIndex FROM 1 BY 1 UNTIL PersonIndex > 3
               MOVE SPACES TO NewName
               CALL "person" USING PersonIndex NewName PersonName
               DISPLAY "person " PersonIndex " Name: " PersonName
           END-PERFORM.


           DISPLAY "Pretty-printing names..."
           PERFORM VARYING PersonIndex FROM 1 BY 1 UNTIL PersonIndex > 3
               CALL "PrettyPrint" USING BY REFERENCE PersonIndex
           END-PERFORM.

           STOP RUN.
