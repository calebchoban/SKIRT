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
	build-SKIRT

$(SKIRT_GIT_DIR):
	git clone $(SKIRT_GIT_SRC) $@
	cd $@ && chmod +rx configSKIRT.sh && chmod +rx makeSKIRT.sh && ./makeSKIRT.sh

.PHONY: run-SKIRT
run-SKIRT:
	echo "Need to set this up"

.PHONY: purge
purge:
	rm ic/{*.bin,*.txt,snapshot}
	rm -r git/ release/
