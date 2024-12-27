       01 addends.
          05 addend1       pic 9(3) value 0.
          05 addend2       pic 9(3) value 0.
          05 result        pic 9(4) value 0.

       procedure division.
           ADD addend1 addend2 GIVING result.
           DISPLAY "The result of adding " addend1 " and "
                addend2 " is " result.
           STOP RUN.
           