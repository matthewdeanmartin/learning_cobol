///usr/bin/true; exec ~/.cobols/gnucobol-3.2/cobc -xj -fmfcomment "$0" "$@"
       *> Sample GnuCOBOL program
       identification division.
       program-id. hellonew.
       procedure division.
       display
          "Hello, new world!"
       end-display
       goback.
       