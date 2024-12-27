      *> --- TestMain ---
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TestMain.

       PROCEDURE DIVISION.
           DISPLAY "Running tests..."
           CALL "TestPerson"
           DISPLAY "Tests complete."
           IF RETURN-CODE = 0
               DISPLAY "TestPerson: SUCCESS"
           ELSE
               DISPLAY "TestPerson: FAILURE"
           END-IF
           STOP RUN.

       END PROGRAM TestMain.
