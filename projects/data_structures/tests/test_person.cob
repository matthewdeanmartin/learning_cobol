///usr/bin/true; exec /C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -xj -fmfcomment "$0" "$@"
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TestPerson.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       COPY person.
       01 AliceName PIC X(20) VALUE "Alice".
       01 NameToSet PIC X(20) VALUE SPACES.
       01 RetrievedName PIC X(20) VALUE SPACES.
       01 TestName PIC X(20) VALUE SPACES.
       01 CopyName PIC X(20) VALUE SPACES.
       01 TheIndex PIC 9(3).

       PROCEDURE DIVISION.
           MOVE 1 to TheIndex
           CALL "person" USING TheIndex AliceName RetrievedName.
           MOVE SPACES TO NameToSet
           CALL "person" USING TheIndex NameToSet RetrievedName.
           DISPLAY "GOT BACK " RetrievedName
           DISPLAY "Testing retrieved name..."
           MOVE "Alice" to TestName
      * Trying to deref the value
           STRING RetrievedName DELIMITED BY SIZE
                  INTO RetrievedName
           END-STRING.
           DISPLAY "GOT BACK " RetrievedName
           DISPLAY RetrievedName 
           DISPLAY TestName 
           move RetrievedName to CopyName
      * IF CopyName(1:5) EQUALS TestName(1:5)
           IF CopyName EQUALS TestName
               DISPLAY "TEST PASSED: Retrieved name is Alice."
               MOVE 0 TO RETURN-CODE  *> Indicating success
           ELSE
               DISPLAY "TEST FAILED: Retrieved name is not Alice."
               MOVE 1 TO RETURN-CODE  *> Indicating failure
           END-IF

           GOBACK.
