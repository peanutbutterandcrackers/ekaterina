.PHONY: env environment
env environment: guix-env-manifest.scm
	guix environment --manifest=$<

.PHONY: tests
tests:
	pytest -v
