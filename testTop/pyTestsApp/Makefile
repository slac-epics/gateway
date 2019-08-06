TOP=..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

TESTSCRIPTS_HOST += gwtests.py TestDBEValue.py TestDBEAlarm.py TestDBELog.py TestDBEProp.py
TESTSCRIPTS_HOST += TestPropertyCache.py
TESTSCRIPTS_HOST += TestEnumPropCache.py
TESTSCRIPTS_HOST += TestStructures.py
TESTSCRIPTS_HOST += TestWaveformWithCAMaxArrayBytes.py
TESTSCRIPTS_HOST += IOCControl.py GatewayControl.py

TESTFILES += test.db
TESTFILES += access.txt

# Which pvlist.txt file depends on USE_PCRE
USE_PCRE ?= NO
PVLIST_YES = pvlist_pcre.txt
PVLIST_NO = pvlist_bre.txt


CLEANS += *.pyc $(TESTFILES) pvlist.txt gateway.*

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
build runtests: testfiles pvlist.txt
testfiles: $(TESTFILES:%=../%)
	$(ECHO) "Copying test files $(TESTFILES)"
	@$(CP) $^ .

pvlist.txt: ../$(PVLIST_$(USE_PCRE))
	$(ECHO) "Copying $< to $@ (USE_PCRE: $(USE_PCRE))"
	@$(CP) $< $@

endif
