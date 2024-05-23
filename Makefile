SKIRT_GIT_SRC ?= https://github.com/SKIRT/SKIRT9.git

SKIRT_GIT_DIR = git

.PHONY: compile
compile: $(SKIRT_GIT_DIR) 

.PHONY: build
build:
	source ./module-reset.sh && skirt

# Downloads and compiles SKIRT
$(SKIRT_GIT_DIR):
	mkdir release run $@
	git clone $(SKIRT_GIT_SRC) $@
	./compile.sh $@
	cd $@ && ./downloadResources.sh

# Compiles data from snapshot
.PHONY: compile_data
compile_data:
	python run.py

.PHONY: submit
submit:
	sbatch job.sh

.PHONY: purge
purge:
	rm -r git/ release/ resources/

.PHONY: pts
pts:
	mkdir PTS
	cd PTS && mkdir run pts && git clone https://github.com/SKIRT/PTS9.git pts