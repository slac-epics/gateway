TOP=..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

PYTESTS += gwtests.py TestDBEValue.py TestDBEAlarm.py TestDBELog.py TestDBEProp.py
PYTESTS += TestPropertyCache.py
PYTESTS += IOCControl.py GatewayControl.py

TESTFILES += ../test.db
TESTFILES += ../pvlist.txt ../access.txt

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

ifdef T_A
runtests:
	nosetests

tapfiles:
	nosetests --with-tap

%.py: ../%.py
	install -m644 $< $@

# Workaround for 3.14 make rules: go through common dir
$(COMMON_DIR)/%: ../%
	install -m644 $< $@
runtests tapfiles: testfiles $(PYTESTS)
testfiles: $(TESTFILES:../%=$(COMMON_DIR)/%)
	install -m644 $^ .
endif