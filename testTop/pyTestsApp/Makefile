TOP=..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

TESTSCRIPTS_HOST += gwtests.py TestDBEValue.py TestDBEAlarm.py TestDBELog.py TestDBEProp.py
TESTSCRIPTS_HOST += TestPropertyCache.py
TESTSCRIPTS_HOST += IOCControl.py GatewayControl.py

TESTFILES += test.db
TESTFILES += pvlist.txt access.txt

CLEANS += *.pyc $(TESTFILES) gateway.*

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

ifeq ($(T_A),$(EPICS_HOST_ARCH))

ifeq ($(BASE_3_14),YES)
clean::
	@$(RM) $(CLEANS)
endif

runtests:
	nosetests

tapfiles:
	nosetests --with-tap

%.py: ../%.py
	$(ECHO) "Copying test script $@"
	@$(INSTALL) -m $(INSTALL_PERMISSIONS) $< .

# Workaround for 3.14 make rules: special target to avoid circular dependencies
build runtests: testfiles
testfiles: $(TESTFILES:%=../%)
	$(ECHO) "Copying test files $(TESTFILES)"
	@$(CP) $^ .
endif
