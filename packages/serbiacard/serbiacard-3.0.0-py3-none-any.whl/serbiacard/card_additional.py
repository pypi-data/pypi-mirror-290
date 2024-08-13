import ctypes


class EID_DOCUMENT_DATA(ctypes.Structure):
    _fields_ = [
        ("docRegNo", ctypes.c_char * 9),
        ("docRegNoSize", ctypes.c_int),
        ("documentType", ctypes.c_char * 2),
        ("documentTypeSize", ctypes.c_int),
        ("issuingDate", ctypes.c_char * 10),
        ("issuingDateSize", ctypes.c_int),
        ("expiryDate", ctypes.c_char * 10),
        ("expiryDateSize", ctypes.c_int),
        ("issuingAuthority", ctypes.c_char * 100),
        ("issuingAuthoritySize", ctypes.c_int),
        ("documentSerialNumber", ctypes.c_char * 10),
        ("documentSerialNumberSize", ctypes.c_int),
        ("chipSerialNumber", ctypes.c_char * 14),
        ("chipSerialNumberSize", ctypes.c_int),
    ]


class EID_FIXED_PERSONAL_DATA(ctypes.Structure):
    _fields_ = [
        ("personalNumber", ctypes.c_char * 13),
        ("personalNumberSize", ctypes.c_int),
        ("surname", ctypes.c_char * 200),
        ("surnameSize", ctypes.c_int),
        ("givenName", ctypes.c_char * 200),
        ("givenNameSize", ctypes.c_int),
        ("parentGivenName", ctypes.c_char * 200),
        ("parentGivenNameSize", ctypes.c_int),
        ("sex", ctypes.c_char * 2),
        ("sexSize", ctypes.c_int),
        ("placeOfBirth", ctypes.c_char * 200),
        ("placeOfBirthSize", ctypes.c_int),
        ("stateOfBirth", ctypes.c_char * 200),
        ("stateOfBirthSize", ctypes.c_int),
        ("dateOfBirth", ctypes.c_char * 10),
        ("dateOfBirthSize", ctypes.c_int),
        ("communityOfBirth", ctypes.c_char * 200),
        ("communityOfBirthSize", ctypes.c_int),
        ("statusOfForeigner", ctypes.c_char * 200),
        ("statusOfForeignerSize", ctypes.c_int),
        ("nationalityFull", ctypes.c_char * 200),
        ("nationalityFullSize", ctypes.c_int),
    ]


class EID_VARIABLE_PERSONAL_DATA(ctypes.Structure):
    _fields_ = [
        ("state", ctypes.c_char * 100),
        ("stateSize", ctypes.c_int),
        ("community", ctypes.c_char * 200),
        ("communitySize", ctypes.c_int),
        ("place", ctypes.c_char * 200),
        ("placeSize", ctypes.c_int),
        ("street", ctypes.c_char * 200),
        ("streetSize", ctypes.c_int),
        ("houseNumber", ctypes.c_char * 20),
        ("houseNumberSize", ctypes.c_int),
        ("houseLetter", ctypes.c_char * 8),
        ("houseLetterSize", ctypes.c_int),
        ("entrance", ctypes.c_char * 10),
        ("entranceSize", ctypes.c_int),
        ("floor", ctypes.c_char * 6),
        ("floorSize", ctypes.c_int),
        ("apartmentNumber", ctypes.c_char * 12),
        ("apartmentNumberSize", ctypes.c_int),
        ("addressDate", ctypes.c_char * 10),
        ("addressDateSize", ctypes.c_int),
        ("addressLabel", ctypes.c_char * 60),
        ("addressLabelSize", ctypes.c_int),
    ]


class EID_PORTRAIT(ctypes.Structure):
    _fields_ = [("portrait", ctypes.c_byte * 7700), ("portraitSize", ctypes.c_int)]


class EID_CERTIFICATE(ctypes.Structure):
    _fields_ = [("certificate", ctypes.c_byte * 2048), ("certificateSize", ctypes.c_int)]
