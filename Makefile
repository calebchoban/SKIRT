SKIRT_GIT_SRC ?= https://github.com/SKIRT/SKIRT9.git

SKIRT_GIT_DIR = git

.PHONY: compile
compile: $(SKIRT_GIT_DIR) 

# Downloads and compiles SKIRT
$(SKIRT_GIT_DIR):
	mkdir -p release run $@
	git clone $(SKIRT_GIT_SRC) $@
	./compile.sh $@
	cd $@ && ./downloadResources.sh

.PHONY: purge
purge:
	rm -r git/ release/ resources/ PTS/ run/

.PHONY: pts
pts:
	mkdir PTS
	cd PTS && mkdir -p run pts && git clone https://github.com/SKIRT/PTS9.git pts
