## v0.9.4

* Modernize use of `pip` and `honesty` to unstick a dependency cycle and make
  work on 3.12

## v0.9.3

* Obey `requires_python` when choosing versions, and preinstall older pip before
  solver became the default.  (A bad merge caused this to not be the case in
  0.9.2)

## v0.9.2 (yanked)

* Obey `requires_python` when choosing versions, and preinstall older pip before
  solver became the default.

## v0.9.1

* Add some missing dependencies that we were getting transitively before

## v0.9.0

* Handle some oddities that can exist in requirements.txt

## v0.8.0

* Limit `--fast` parallelism
* Allow customizing requirements
* Workflow to test itself
* Try somewhat to isolate from current venv

## v0.7.0

* Works on Windows
* Fixed/Variable split

## v0.6.0

* First really useful version, basic functionality

## v0.5.0

* Initial version

## v0.0.0

* Reserving name
