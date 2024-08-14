import ctypes
import io
import os
import random
import string
import datetime

import PIL.Image as Image

from serbiacard.card_additional import (
    EID_CERTIFICATE,
    EID_DOCUMENT_DATA,
    EID_FIXED_PERSONAL_DATA,
    EID_PORTRAIT,
    EID_VARIABLE_PERSONAL_DATA,
)


class CarCard:
    pass


class IDCard:
    """With all data fields from ID with .start_card_reader() to
    start reader, collect from chip, end reader and store information in this object.

    More information available through the CelikAPI documentation.
    Vise informacija u CelikAPI dokumentaciji.

        docRegNo: ID Number (Broj Licne)
        documentType: Information
        issuingDate: Information
        expiryDate: Information
        issuingAuthority: Information
        documentSerialNumber: Information
        chipSerialNumber: Information

        personalNumber: Information
        surname (or lastName): Information
        givenName (or firstName): Information
        parentGivenName: Information
        sex: Information
        placeOfBirth: Information
        stateOfBirth: Information
        dateOfBirth: Information
        communityOfBirth: Information
        statusOfForeigner: Information
        nationalityFull: Information

        state: Information
        community: Information
        place: Information
        street: Information
        houseNumber: Information
        houseLetter: Information
        entrance: Information
        floor: Information
        apartmentNumber: Information
        addressDate: Information
        addressLabel: Information

        portrait: Information.BytesIO()

        certificate: Information.BytesIO()
    """

    def __init__(self):
        self.docRegNo = None
        self.documentType = None
        self.issuingDate = None
        self.expiryDate = None
        self.issuingAuthority = None
        self.documentSerialNumber = None
        self.chipSerialNumber = None

        self.personalNumber = None
        self.surname = None
        self.givenName = None
        self.parentGivenName = None
        self.sex = None
        self.placeOfBirth = None
        self.stateOfBirth = None
        self.dateOfBirth = None
        self.communityOfBirth = None
        self.statusOfForeigner = None
        self.nationalityFull = None

        self.state = None
        self.community = None
        self.place = None
        self.street = None
        self.houseNumber = None
        self.houseLetter = None
        self.entrance = None
        self.floor = None
        self.apartmentNumber = None
        self.addressDate = None
        self.addressLabel = None

        self.portrait = io.BytesIO()

        self.certificate = None

        # Flag for checking if ID is read correctly
        # if read correctly > True, if not then False, default False
        self.idCheck = False
        self.startup_result = None

    def start_card_reader(self):
        """Full complete: Completes reading, filling all information and closing the reader.

        This method does all tasks, finishes them completely including starting the reader,
        reading and filling the data inside the object values and closing the reader.
        """
        self.readerStart()
        self.readData()
        self.readerEnd()
        self.validate()

        self._encodeFields()

    def simulate_card_reader(self):
        """Emulate reading the card reader with fixed data for testing purposes."""
        fixed_data = {
            'docRegNo': self._generate_random_number(9),
            'documentType': 'ID',
            'issuingDate': self._random_date(datetime.date(2015, 1, 1), datetime.date(2020, 1, 1)).strftime('%d.%m.%Y'),
            'expiryDate': self._random_date(datetime.date(2026, 1, 1), datetime.date(2030, 1, 1)).strftime('%d.%m.%Y'),
            'issuingAuthority': 'ПУ У НОВОМ ПАЗАРУ',
            'documentSerialNumber': '',
            'chipSerialNumber': '',
            'personalNumber': self._generate_jmbg(),
            'surname': self._random_surname(),
            'givenName': self._random_given_name(),
            'parentGivenName': self._random_given_name(),
            'sex': random.choice(['M', 'F']),
            'placeOfBirth': 'NOVI PAZAR',
            'stateOfBirth': 'REPUBLIKA SRBIJA',
            'dateOfBirth': self._random_date(datetime.date(1960, 1, 1), datetime.date(2005, 1, 1)).strftime('%d.%m.%Y'),
            'communityOfBirth': 'NOVI PAZAR',
            'statusOfForeigner': '',
            'nationalityFull': '',
            'state': 'SRB',
            'community': 'NOVI PAZAR',
            'place': 'NOVI PAZAR',
            'street': self._random_street(),
            'houseNumber': self._generate_random_number(3),
            'houseLetter': '',
            'entrance': '',
            'floor': '',
            'apartmentNumber': '',
            'addressDate': self._random_date(datetime.date(2010, 1, 1), datetime.date(2020, 1, 1)).strftime('%d.%m.%Y'),
            'addressLabel': 'prebivalište',
            'portrait': 'Object portrait',
            'certificate': 'Object certificate',
            'idCheck': True,
            'startup_result': 0,
            'firstName': 'Elvir',
            'lastName': ''
        }

        fixed_data['firstName'] = fixed_data['givenName']
        fixed_data['lastName'] = fixed_data['surname']

        for key, value in fixed_data.items():
            setattr(self, key, value)

        self.portrait = io.BytesIO(b'Test portrait data')
        self.certificate = io.BytesIO(b'Test certificate data')

    def __repr__(self):
        information = self.__dict__
        if 'celikApi' in information:
            del information["celikApi"]
        information["portrait"] = "Object portrait"
        information["certificate"] = "Object certificate"
        return f"{information}"

    def readerStart(self):
        # Getting the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # celik_path is the dll path of the API
        celik_path = os.path.join(script_dir, "CelikApi.dll")
        self.celikApi = ctypes.CDLL(celik_path)

        self.startup_result = self.celikApi.EidStartup(3)
        self.idCheck = True if not self.celikApi.EidBeginRead(ctypes.c_char(), 0) else False

    def readerEnd(self):
        self.celikApi.EidEndRead()
        self.celikApi.EidCleanup()

    def readData(self):
        # read all the fields
        self.setDocumentData()
        self.setFixedPersonalData()
        self.setVariablePersonalData()
        self.setPortrait()
        self.setCertificate()

    def setDocumentData(self):
        INTP = ctypes.POINTER(ctypes.c_int)
        obj = EID_DOCUMENT_DATA()
        addr = ctypes.addressof(obj)
        pointer_addr = ctypes.cast(addr, INTP)
        self.celikApi.EidReadDocumentData(pointer_addr)

        self.docRegNo = obj.docRegNo
        self.documentType = obj.documentType
        self.issuingDate = obj.issuingDate
        self.expiryDate = obj.expiryDate
        self.issuingAuthority = obj.issuingAuthority
        self.documentSerialNumber = obj.documentSerialNumber
        self.chipSerialNumber = obj.chipSerialNumber

        return True

    def setFixedPersonalData(self):
        INTP = ctypes.POINTER(ctypes.c_int)
        obj = EID_FIXED_PERSONAL_DATA()
        addr = ctypes.addressof(obj)
        pointer_addr = ctypes.cast(addr, INTP)
        self.celikApi.EidReadFixedPersonalData(pointer_addr)

        self.personalNumber = obj.personalNumber
        self.surname = obj.surname
        self.givenName = obj.givenName

        # additional
        self.firstName = self.givenName
        self.lastName = self.surname

        self.parentGivenName = obj.parentGivenName
        self.sex = obj.sex
        self.placeOfBirth = obj.placeOfBirth
        self.stateOfBirth = obj.stateOfBirth
        self.dateOfBirth = obj.dateOfBirth
        self.communityOfBirth = obj.communityOfBirth
        self.statusOfForeigner = obj.statusOfForeigner
        self.nationalityFull = obj.nationalityFull

        return True

    def setVariablePersonalData(self):
        INTP = ctypes.POINTER(ctypes.c_int)
        obj = EID_VARIABLE_PERSONAL_DATA()
        addr = ctypes.addressof(obj)
        pointer_addr = ctypes.cast(addr, INTP)
        self.celikApi.EidReadVariablePersonalData(pointer_addr)

        self.state = obj.state
        self.community = obj.community
        self.place = obj.place
        self.street = obj.street
        self.houseNumber = obj.houseNumber
        self.houseLetter = obj.houseLetter
        self.entrance = obj.entrance
        self.floor = obj.floor
        self.apartmentNumber = obj.apartmentNumber
        self.addressDate = obj.addressDate
        self.addressLabel = obj.addressLabel

        return True

    def setPortrait(self):
        INTP = ctypes.POINTER(ctypes.c_int)
        obj = EID_PORTRAIT()
        addr = ctypes.addressof(obj)
        pointer_addr = ctypes.cast(addr, INTP)
        self.celikApi.EidReadPortrait(pointer_addr)

        self.portrait = io.BytesIO(obj.portrait)

        return True

    # TODO: multiple types of certificate available
    def setCertificate(self, cert_choice=3):
        INTP = ctypes.POINTER(ctypes.c_int)
        obj = EID_CERTIFICATE()
        addr = ctypes.addressof(obj)
        pointer_addr = ctypes.cast(addr, INTP)
        self.celikApi.EidReadCertificate(pointer_addr)

        self.certificate = obj.certificate

        return True

    def showPortrait(self) -> None:
        image = Image.open(self.portrait)
        image.show()

    @property
    def is_valid(self):
        return self.idCheck

    def validate(self):
        """Validate if the ID is loaded correctly.

        Validate ID card if it is read correctly,
        raises and Exception if there is an Error in read
        returns True if there's no error

        Returns:
            True: everything's ok
            bool

        Raises:
            Exception: Error if not read.
        """
        if not self.idCheck:
            raise Exception("ID is not loaded correctly. Code:", self.startup_result)
        return True

    def _encodeFields(self):
        for attribute, value in self.__dict__.items():
            if isinstance(value, bytes):
                self.__dict__[attribute] = value.decode("UTF-8")
                # setattr(self, attribute, value.decode('UTF-8'))

    def _generate_random_number(self, length):
        return ''.join(random.choices(string.digits, k=length))

    def _random_date(self, start_date, end_date):
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start_date + datetime.timedelta(days=random_number_of_days)

    def _generate_jmbg(self):
        year = str(random.randint(1950, 2022)).zfill(4)
        month = str(random.randint(1, 12)).zfill(2)
        day = str(random.randint(1, 28)).zfill(2)
        reg = str(random.randint(70, 99)).zfill(2)  # Region code
        unique = str(random.randint(100, 999)).zfill(3)
        return day + month + year[2:] + reg + unique

    def _random_surname(self):
        surnames = ['Petrović', 'Nikolić', 'Jovanović', 'Marković', 'Đorđević', 'Ilić', 'Stojanović', 'Pavlović']
        return random.choice(surnames)

    def _random_given_name(self):
        names = ['Aleksandar', 'Miloš', 'Nikola', 'Jelena', 'Milica', 'Ana', 'Marko', 'Marija']
        return random.choice(names)

    def _random_street(self):
        streets = ['Bulevar Oslobođenja', 'Cara Dušana', 'Kralja Petra', 'Vojvode Stepe', 'Milovana Glišića']
        return random.choice(streets)

    def __getitem__(self, attribute):
        return self.__dict__[attribute]


if __name__ == "__main__":
    card = IDCard()
    card.simulate_card_reader()  # Use the emulated card reader for testing
    print(card)
