#      $ cobc -c subr1.cob
    #  $ cobc -c subr2.cob
    #  $ cobc -c -fmain main.cob
    #  $ cobc -o prog main.o subr1.o subr2.o
/C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -c add_function.cob
/C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -cx add_em.cob 
/C/Users/matth/Desktop/GnuCobolDocs/GC32M-BDB-x64/bin/cobc -xo add_em add_em.o add_function.o
