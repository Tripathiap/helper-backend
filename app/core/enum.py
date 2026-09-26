from enum import Enum


class ServiceType(str, Enum):
    PLUMBING = "plumbing"
    ELECTRICITY = "electricity"
    CARPENTRY = "carpentry"
    CLEANING = "cleaning"
    PAINTING = "painting"
    APPLIANCE = "appliance"
    OTHER = "other"
