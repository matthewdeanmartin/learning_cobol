       IDENTIFICATION DIVISION.
       PROGRAM-ID. ReusableFunctionExample.


       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       REPOSITORY.
           FUNCTION Add-Numbers.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 Number1 PIC 9(3).
       01 Number2 PIC 9(3).
       01 Result PIC 9(4).


       PROCEDURE DIVISION.
       Main-Logic.
           DISPLAY "Enter the first number: " WITH NO ADVANCING.
           ACCEPT Number1.
           DISPLAY "Enter the second number: " WITH NO ADVANCING.
           ACCEPT Number2.

           COMPUTE Result = Function Add-Numbers(Number1, Number2).

           DISPLAY "The result of addition is: " Result.
           STOP RUN.
