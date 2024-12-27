# Compiler
COBC = cobc

# Sources, copybooks, and binary
SRC = $(wildcard src/*.cob src/*/*.cob)
OBJECTS_DIR = out
OBJECTS = $(patsubst src/%.cob, out/%.o, $(SRC))
CPY_DIR = src/copybooks
CPY = $(wildcard src/copybooks/*.cpy)

# app parts
MAIN_SRC = main.cob
BIN = main


# Test sources and binary
TEST_SRC = test.cob $(wildcard tests/*.cob)
TEST_BIN = test

.PHONY: all clean data run test

all: $(BIN)

clean:
	rm -rf $(OBJECTS_DIR)
	rm -f $(BIN)
	rm -f $(TEST_BIN)
	rm -rf data

run: all
	COB_PRE_LOAD=.venv ./$(BIN)

$(OBJECTS): out/%.o: src/%.cob $(CPY)
	@mkdir -p $(@D)
	$(COBC) -c -O2 -debug -Wall -fnotrunc  -I $(CPY_DIR) -o $@ $<

$(BIN): $(CPY) $(MAIN_SRC) $(OBJECTS)
	# --free
	$(COBC) -x -O2 -debug -Wall -fnotrunc -I $(CPY_DIR) -o $@ $(MAIN_SRC) $(OBJECTS)

test: $(TEST_SRC) $(SRC) $(CPY) $(UTIL_LIB)
	$(COBC) -x -debug -Wall -fnotrunc -lstdc++ -I $(CPY_DIR) -o $@ $(TEST_SRC) $(SRC)
	COB_PRE_LOAD=.venv ./$(TEST_BIN)