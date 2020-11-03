(use-modules (gnu packages))

(specifications->manifest
 (list "python"
       "python-pytest"))

;; guix-supplied gnucash does not have it's python bindings enabled.
;; I have sent in a patch: https://issues.guix.gnu.org/44309 but in
;; the meantime, I am working with gnucash-python readily available
;; on my local machine (using the first patch in the thread). Once
;; the patch is merged, the list above will probably include the
;; required package. Hopefully, "gnucash:python". But for now, this
;; environment manifest file does not create a ready-to-develop-in
;; environment. Gnucash python bindings are missing. For now.
