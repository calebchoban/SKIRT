SKIRT_GIT_SRC ?= https://github.com/SKIRT/SKIRT9.git
MPIRUN ?= mpirun
RESTART_FLAG ?=

SKIRT_GIT_DIR = git
SKIRT_RELEASE_DIR = release

.PHONY: compile
compile: SKIRT 

.PHONY: build-SKIRT
build-SKIRT:
	echo "Need to set this up"

SKIRT: $(SKIRT_GIT_DIR)
	echo "Need to set this up"

# This downloads and compiles SKIRT
$(SKIRT_GIT_DIR):
	git clone $(SKIRT_GIT_SRC) $@
	./compile_tscc.sh $@
	cd $@ && ./downloadResources.sh

.PHONY: run-SKIRT
run-SKIRT:
	echo "Need to set this up"

.PHONY: purge
purge:
	rm -r git/ release/
