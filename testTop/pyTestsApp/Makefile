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

%.txt: ../%.txt
	install -m755 $< $@

%.db: ../%.db
	install -m755 $< $@

runTests.py: IOCControl.py test.db
runTests.py: gwtests.py DBEValueTest.py DBEAlarmTest.py DBELogTest.py DBEPropTest.py
runTests.py: PropertyCacheTest.py
runTests.py: GatewayControl.py pvlist.txt access.txt
