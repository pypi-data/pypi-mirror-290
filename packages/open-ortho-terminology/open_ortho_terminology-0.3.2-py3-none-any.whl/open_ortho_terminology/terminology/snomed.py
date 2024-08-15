""" snomed: a collection of static SNOMED-CT codes.

Used whenever a code is necessary, for various implementations.

"""
from . import Code

PREFIX = "SCT"
SYSTEM = "http://snomed.info/sct"

class CodeSnomed(Code):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.prefix = PREFIX
        self.system = SYSTEM

dental_chair = CodeSnomed(
    code='706356006',
    display='Dental examination/treatment chair')

orthod_treatment_perm_class1 = CodeSnomed(
    code='3891000',
    display='Comprehensive orthodontic treatment, permanent dentition, for class I malocclusion')

ortho_treatment = CodeSnomed(
    code='122452007',
    display='Comprehensive orthodontic treatment')

orthodontist = CodeSnomed(
    code='37504001',
    display='Orthodontist')

clinical_staff = CodeSnomed(
    code='4162009',
    display='Dental assistant')

admin_staff = CodeSnomed(
    code='224608005',
    display='Administrative healthcare staff')

tech_support = CodeSnomed(
    code='159324001',
    display='Technical assistant')
