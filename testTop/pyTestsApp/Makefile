TOP=..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

TESTS += runTests.py
TESTFILES += ../test.db
TESTFILES += ../pvlist.txt ../access.txt

TESTSCRIPTS_HOST += $(TESTS:%=%.t)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

%.py: ../%.py
	install -m755 $< $@

# Workaround for 3.14 make rules: go through common dir
$(COMMON_DIR)/%: ../%
	install -m644 $< $@
runTests.py: testfiles
testfiles: $(TESTFILES:../%=$(COMMON_DIR)/%)
	install -m644 $^ .

runTests.py: gwtests.py DBEValueTest.py DBEAlarmTest.py DBELogTest.py DBEPropTest.py
runTests.py: PropertyCacheTest.py
runTests.py: IOCControl.py GatewayControl.py
