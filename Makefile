.PHONY: env environment
env environment: guix-env-manifest.scm
	guix environment --manifest=$<

.PHONY: check
check:
	pytest -v

gnucash_api_docs: $(shell guix build --source gnucash)
	tar xvfj $<
	$(eval src-dir := $(shell tar --list -f $< | head -n1 | tr -d /))
	mkdir $(src-dir)/build
	cd $(src-dir)/build && \
	    guix environment gnucash --ad-hoc doxygen -- cmake .. && make doc
	mkdir $@
	mv $(src-dir)/build/libgnucash/doc/html $@
	rm -rvf $(src-dir)
	cd $@ && ln -s html/index.html .
