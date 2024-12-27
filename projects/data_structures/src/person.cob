       IDENTIFICATION DIVISION.
       PROGRAM-ID. person.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 Persons.
           05 Person OCCURS 3 TIMES.
               10 HumanName PIC X(20) VALUE SPACES.

       LINKAGE SECTION.
       COPY "person.cpy".
      *01 PersonIndex PIC 9(3).
      *01 NewName PIC X(20).
      *01 PersonName PIC X(20).

       PROCEDURE DIVISION  USING BY REFERENCE PersonIndex
           BY REFERENCE NewName BY REFERENCE PersonName.
           DISPLAY "Running..."

           EVALUATE TRUE
               WHEN PersonIndex = 1 OR PersonIndex = 2 
                       OR PersonIndex = 3
                   IF NewName NOT = SPACES
                       DISPLAY "New name is not equal to spaces"
                       MOVE NewName TO HumanName(PersonIndex)
                       MOVE HumanName(PersonIndex) TO PersonName
                       DISPLAY "N(PI) " HumanName(PersonIndex)
                       DISPLAY "PN: "  PersonName
                   ELSE
                       DISPLAY "GET: HN(PI)"   HumanName(PersonIndex)
                       MOVE HumanName(PersonIndex) TO PersonName
                       DISPLAY "PN :" PersonName
                   END-IF
               WHEN OTHER
                   DISPLAY "Invalid index."
           END-EVALUATE
           GOBACK.

       ENTRY "PrettyPrint" USING BY REFERENCE PersonIndex.
       DISPLAY "BACK!"
       IF PersonIndex >= 1 AND PersonIndex <= 3
           DISPLAY "Person " PersonIndex ": " HumanName(PersonIndex)
       ELSE
           DISPLAY "Invalid index for pretty-print."
       END-IF
       GOBACK.
