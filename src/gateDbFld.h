#ifndef _GATEDBFLD_H_
#define _GATEDBFLD_H_

struct DBFLD
{
    static const int D_STRING;
    static const int D_CHAR;
    static const int D_UCHAR;
    static const int D_SHORT;
    static const int D_USHORT;
    static const int D_LONG;
    static const int D_ULONG;
// db_access.h does not define DBR_INT64 and channel access sends int64 as a double
// so these are not currently used in the gateway
#ifdef DBR_INT64
    static const int D_INT64;
    static const int D_UINT64;
#endif
    static const int D_FLOAT;
    static const int D_DOUBLE;
    static const int D_ENUM;
};

#endif /* _GATEDBFLD_H_ */
