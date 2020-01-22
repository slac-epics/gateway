// caPutLog uses dbFldTypes.h for DBR_xxx types, but gateway uses db_access.h elsewhere
// so we provide a mapping here to avoid a name clash

#include <dbFldTypes.h>
#include "gateDbFld.h"

const int DBFLD::D_STRING = DBR_STRING;
const int DBFLD::D_CHAR = DBR_CHAR;
const int DBFLD::D_UCHAR = DBR_UCHAR;
const int DBFLD::D_SHORT = DBR_SHORT;
const int DBFLD::D_USHORT = DBR_USHORT;
const int DBFLD::D_LONG = DBR_LONG;
const int DBFLD::D_ULONG = DBR_ULONG;
#ifdef DBR_INT64
const int DBFLD::D_INT64 = DBR_INT64;
const int DBFLD::D_UINT64 = DBR_UINT64;
#endif
const int DBFLD::D_FLOAT = DBR_FLOAT;
const int DBFLD::D_DOUBLE = DBR_DOUBLE;
const int DBFLD::D_ENUM = DBR_ENUM;
