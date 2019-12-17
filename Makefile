SKIRT_GIT_SRC ?= https://github.com/SKIRT/SKIRT9.git

SKIRT_GIT_DIR = git
SKIRT_RELEASE_DIR = release
OUTPUT_DIR = output

.PHONY: compile
compile: SKIRT 

.PHONY: build
build:
	source ./module-reset.sh && skirt

# Downloads and compiles SKIRT
$(SKIRT_GIT_DIR):
	git clone $(SKIRT_GIT_SRC) $@
	./compile_tscc.sh $@
	cd $@ && ./downloadResources.sh

# Compiles data from snapshot
.PHONY: compile_data
compile_data:
	python run.py

.PHONY: submit
submit:
	qsub job.pbs

.PHONY: purge
purge:
	rm -r git/ release/ resources/
