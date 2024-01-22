from __future__ import annotations

import calendar
import datetime
from decimal import Decimal
from io import StringIO
from typing import Annotated, Any, ClassVar, Optional

import bcrypt
from hx_markup import Element
from ormspace import functions
from spacestar.model import SpaceModel
from ormspace.model import modelmap, SearchModel
from ormspace.annotations import DateField, DateTimeField, PasswordField, PositiveDecimalField, PositiveIntegerField
from pydantic import BeforeValidator, computed_field, Field
from typing_extensions import Self

from detadoc.annotations import BodyMeasureFloat, BodyMeasureInteger, OptionalFloat, OptionalInteger, string_to_list, \
    StringList
from detadoc.bases import EmailBase, FinancialBase, Profile, SpaceSearchModel, Staff, Transaction
from detadoc.enum import Account, AccountSubtype, CashFlow, InvoiceType, AccountType, DosageForm, MedicationRoute, \
    PaymentMethod, Period
from detadoc.regex import ActiveDrug, Package


    
@modelmap
class User(EmailBase):
    EXIST_QUERY = 'email'
    password: PasswordField
    created: DateField
    updated: Optional[datetime.date] = Field(None)
    
    def __str__(self):
        return self.email
    
    @classmethod
    async def get_and_check(cls, email: str, password: str) -> Optional[User]:
        user = await cls.get_by_email(email)
        if user:
            if user.check(password):
                return user
        return None
    
    @classmethod
    def create_encrypted(cls, email: str, password: str) -> Self:
        return cls(email=email, password=cls.encrypt_password(password))
    
    @classmethod
    def encrypt_password(cls, password: str) -> bytes:
        return bcrypt.hashpw(functions.str_to_bytes(password), bcrypt.gensalt())
    
    def check(self, password: str) -> bool:
        return bcrypt.checkpw(functions.str_to_bytes(password), self.password)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.email == other.email
    
    def __hash__(self):
        return hash(self.email)


@modelmap
class Register(User):
    TABLE_NAME = 'User'
    password_repeat: bytes
    
    def model_post_init(self, __context: Any) -> None:
        assert self.password == self.password_repeat
        self.password = self.encrypt_password(self.password)
    
    def asjson(self):
        data = super().asjson()
        data.pop('password_repeat', None)
        return data
    

@modelmap
class Patient(Profile):
    MODEL_GROUPS = ['Profile']
    
    
class PactientKeyBase(SpaceModel):
    patient_key: Patient.Key
    
    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        if self.patient_key:
            if not self.patient_key.instance:
                if patient:= Patient.instance_from_context(self.patient_key.data):
                    self.patient_key.set_instance(patient)
                    
    @property
    def patient(self) -> Patient:
        return self.patient_key.instance if self.patient_key else None
    
    @patient.setter
    def patient(self, value: Patient) -> None:
        self.patient_key.set_instance(value)

@modelmap
class Doctor(Staff):
    MODEL_GROUPS = ['Profile', 'Staff']
    EXIST_QUERY = 'key'
    crm: str
    specialties: StringList
    subspecialties: StringList
    
    @classmethod
    async def data(cls) -> dict:
        return await cls.fetch_one('admin')
    
    @classmethod
    async def instance(cls) -> Optional[Self]:
        if data := await cls.data():
            return cls(**data)
        return None
    
    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        self.key = 'admin'
    
    def __str__(self):
        if self.gender.value.lower().startswith('masculino'):
            return f'Dr. {self.name}'
        return f'Dra. {self.name}'


@modelmap
class Employee(Staff):
    MODEL_GROUPS = ['Profile', 'Staff']


@modelmap
class Service(SearchModel):
    FETCH_QUERY = {'active': True}
    name: str
    price: PositiveDecimalField
    return_days: PositiveIntegerField = Field(0)
    active: bool = Field(True)
    notes: StringList
    created: DateField
    
    def __str__(self):
        return f'{self.name} valor R$ {self.price}'
    

@modelmap
class JournalEntry(SpaceModel):
    transaction: Transaction
    description: str = ''
    
    def __lt__(self, other):
        assert isinstance(other, type(self))
        return self.transaction.accounting_date < other.transaction.accounting_date
    
    def __str__(self):
        return f'{self.transaction.display} {self.description}'
    
    @property
    def value(self) -> Decimal:
        if self.account.type == self.transaction_type:
            return self.amount
        return Decimal('0') - self.amount
    
    @property
    def account(self):
        return self.transaction.account
    
    @property
    def amount(self):
        return self.transaction.amount
    
    @property
    def account_subtype(self):
        return self.account.subtype
    
    @property
    def account_type(self):
        return self.account.subtype.type
    
    @property
    def transaction_type(self):
        return self.transaction.type
    
    @property
    def date(self) -> datetime.date:
        return self.transaction.accounting_date
    
    def balance(self):
        return sum([i.amount for i in self.assets()]) - sum([i.amount for i in self.liabilities()]) - sum(
                i.amount for i in self.equity())
    
    def revenues(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.RE]
    
    def expenses(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.EX]
    
    def assets(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.AT]
    
    def liabilities(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.LI]
    
    def equity(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.SE]
    
    def dividends(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.DI]
    
    def profit(self):
        return sum([i.amount for i in self.revenues()]) - sum([i.amount for i in self.expenses()])

@modelmap
class Invoice(FinancialBase):
    REVENUE_ACCOUNT: ClassVar[Account] = Account.GRE
    EXPENSE_ACCOUNT: ClassVar[Account] = Account.GEX
    PAYABLE_ACCOUNT: ClassVar[Account] = Account.PLI
    RECEIVABLE_ACCOUNT: ClassVar[Account] = Account.RAT
    CASH_ACCOUNT: ClassVar[Account] = Account.CAT
    BANK_ACCOUNT: ClassVar[Account] = Account.BAT
    INVOICE_TYPE: ClassVar[InvoiceType] = InvoiceType.G
    
    @computed_field
    @property
    def type(self) -> str:
        return self.INVOICE_TYPE.name
    
    def __str__(self):
        if self.flow == CashFlow.EX:
            if self.has_payment():
                return f'- {self.amount} R$ {self.date} {self.EXPENSE_ACCOUNT.title} {self.description}'
            return f'{self.amount} R$ {self.date + datetime.timedelta(days=31)} {self.PAYABLE_ACCOUNT.title} {self.description}'
        if self.has_payment():
            return f'{self.amount} R$ {self.date} {self.REVENUE_ACCOUNT.title} {self.description}'
        return f'{self.amount} R$ {self.date + datetime.timedelta(days=31)} {self.RECEIVABLE_ACCOUNT.title} {self.description}'
    
    def has_payment(self):
        return self.method != PaymentMethod.NO
    
    async def setup_instance(self):
        pass
    
    def not_same_day(self):
        return self.created != self.date
    
    @classmethod
    async def save_journal_entry(cls, data: dict):
        instance = cls(**data)
        await instance.setup_instance()
        transactions = []
        account = instance.REVENUE_ACCOUNT if instance.flow == CashFlow.RE else instance.EXPENSE_ACCOUNT
        opposite_flow = "D" if account.type == AccountType.C else "C"
        if instance.has_payment():
            transactions.append(f'{account} {instance.amount} {account.type} {instance.date} {instance.key} {instance.description}')
            if instance.method == PaymentMethod.CA:
                transactions.append(f'{instance.CASH_ACCOUNT} {instance.amount} {opposite_flow} {instance.date} {instance.key} {instance.description}')
            elif instance.method in [PaymentMethod.PI, PaymentMethod.TR, PaymentMethod.DC, PaymentMethod.AD]:
                transactions.append(f'{instance.BANK_ACCOUNT} {instance.amount} {opposite_flow} {instance.date} {instance.key} {instance.description}')
            elif instance.method == PaymentMethod.CC:
                transactions.append(f'{instance.RECEIVABLE_ACCOUNT} {instance.amount} {opposite_flow} {instance.date} {instance.key} {instance.description}')
        else:
            transactions.append(f'{account} {instance.amount} {account.type} {instance.created} {instance.key} {instance.description}')
            if instance.flow == CashFlow.RE:
                transactions.append(f'{instance.RECEIVABLE_ACCOUNT} {instance.amount} {instance.RECEIVABLE_ACCOUNT.type} {instance.date} {instance.key} {instance.description}')
            else:
                transactions.append(f'{instance.PAYABLE_ACCOUNT} {instance.amount} {instance.PAYABLE_ACCOUNT.type} {instance.date} {instance.key} {instance.description}')

        await JournalEntry.Database.put_all([i.asjson() for i in [JournalEntry(transaction=t) for t in transactions]])

    
    async def save_new(self):
        new = await super().save_new()
        if new:
            await self.save_journal_entry(new)
        return new


@modelmap
class RentInvoice(Invoice):
    REVENUE_ACCOUNT = Account.RRE
    EXPENSE_ACCOUNT = Account.REX
    INVOICE_TYPE = InvoiceType.R
    TABLE_NAME = 'Invoice'


@modelmap
class ProductInvoice(Invoice):
    REVENUE_ACCOUNT = Account.PRE
    EXPENSE_ACCOUNT = Account.PEX
    INVOICE_TYPE = InvoiceType.P
    TABLE_NAME = 'Invoice'

   
@modelmap
class ServiceInvoice(Invoice, PactientKeyBase):
    REVENUE_ACCOUNT = Account.SRE
    EXPENSE_ACCOUNT = Account.SEX
    INVOICE_TYPE = InvoiceType.S
    TABLE_NAME = 'Invoice'
    service_key: Service.Key
    description: Optional[str] = Field('Receita de Serviço')
    discount: Annotated[
        PositiveDecimalField, Field(Decimal('0')), BeforeValidator(lambda x: Decimal('0') if not x else Decimal(x))]
    flow: CashFlow = CashFlow.RE

    def __str__(self):
        self.description = f'{self.service or self.service_key} {self.patient or self.patient_key}'
        return super().__str__()

    async def setup_instance(self):
        if not self.patient:
            self.patient_key.set_instance(await Patient.fetch_instance(str(self.patient_key)))
        if not self.service:
            self.service_key.set_instance(await Service.fetch_instance(str(self.service_key)))

    

        
    
    @property
    def service(self):
        return self.service_key.instance
    
    def balance(self):
        value = self.service.price - self.amount
        if value > self.discount:
            return value - self.discount
        return 0
    
    def ammount_check(self):
        return self.service.price - self.discount - self.amount
    

    
@modelmap
class ExpenseInvoice(Invoice):
    EXPENSE_ACCOUNT = Account.GEX
    INVOICE_TYPE = InvoiceType.G
    flow: CashFlow = CashFlow.EX
    TABLE_NAME: ClassVar[str] = 'Invoice'
    

@modelmap
class EnergyInvoice(ExpenseInvoice):
    EXPENSE_ACCOUNT = Account.EEX
    TABLE_NAME: ClassVar[str] = 'Invoice'
    
@modelmap
class WaterInvoice(ExpenseInvoice):
    EXPENSE_ACCOUNT = Account.WEX
    TABLE_NAME: ClassVar[str] = 'Invoice'
    
@modelmap
class PhoneInvoice(ExpenseInvoice):
    EXPENSE_ACCOUNT = Account.TEX
    TABLE_NAME: ClassVar[str] = 'Invoice'


@modelmap
class RevenueInvoice(Invoice):
    REVENUE_ACCOUNT = Account.GRE
    INVOICE_TYPE = InvoiceType.G
    flow: CashFlow = CashFlow.RE
    TABLE_NAME: ClassVar[str] = 'Invoice'
    

@modelmap
class Medication(SpaceSearchModel):
    label: Optional[str] = Field(None)
    drugs: Annotated[list[ActiveDrug], BeforeValidator(string_to_list)]
    route: MedicationRoute = Field(MedicationRoute.O)
    dosage_form: DosageForm
    package: Package
    pharmaceutical: Optional[str] = Field(None)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and str(self) == str(other)
    
    def __hash__(self):
        return hash(str(self))
    
    @property
    def is_generic(self):
        return self.label is None
    
    @property
    def is_single_drug(self):
        return len(self.drugs) == 1
    
    @property
    def package_content(self):
        return getattr(self.package, '_content', None)
    
    @property
    def package_size(self):
        return Decimal(functions.parse_number(getattr(self.package, '_size', None)))

    @property
    def drug_names(self):
        return functions.join([getattr(i, '_name') for i in self.drugs], sep=" + ")
    
    @property
    def drug_strengths(self):
        return functions.join([f"{getattr(i, '_strength')}{getattr(i, '_unit')}" for i in self.drugs], sep=" + ")
    
    @property
    def name(self):
        if not self.is_generic:
            return f'{self.label} ({self.drug_names}) {self.drug_strengths}'
        return f'{self.drug_names.title()} {self.drug_strengths}'
    
    def __str__(self):
        if not self.is_generic:
            return f'{self.name} {self.package}'
        return f'{self.name} {self.package}'



@modelmap
class Event(PactientKeyBase):
    # patient_key: Patient.Key
    title: str
    notes: Optional[str] = Field(None)
    date: Optional[datetime.date] = Field(None)
    
    def __str__(self):
        return f'{functions.years(self.date, self.patient.bdate)} anos: {self.title}'
    
    
@modelmap
class Prescription(PactientKeyBase):
    medication_key: Medication.Key
    start: DateField
    period: Period = Period.D
    frequency: Decimal = Field(Decimal('1'))
    dosage: Decimal = Field(Decimal('1'))
    posology: str
    boxes: Optional[int] = None
    duration: Optional[Decimal] = Field(Decimal('30'))
    end: Optional[DateField] = None
    
    def __str__(self):
        if self.end:
            return f'{self.medication.name} {self.dosage} {self.medication.dosage_form.value} {self.frequency}x/{self.period.value} {self.posology} (interrompido {self.end})'
        if self.duration:
            return f'{self.medication.name} {self.dosage} {self.medication.dosage_form.value} {self.frequency}x/{self.period.value}  {self.posology} [{self.remaining_days} dias, {self.boxes or self.computed_boxes} cx]'
        return f'{self.medication.name} {self.dosage} {self.medication.dosage_form.value} {self.frequency}x/{self.period.value} {self.posology}'
    
    def asjson(self):
        data = super().asjson()
        data.pop('search', None)
        return data
    
    @property
    def medication(self):
        return self.medication_key.instance
    
    
    @computed_field(repr=False)
    @property
    def computed_boxes(self) -> Optional[Decimal]:
        if self.duration:
            day_needed = self.daily_dosage
            needed = self.duration * day_needed
            if package_size:= self.medication.package_size:
                return Decimal((needed/package_size).__ceil__())
        return None
    
    @property
    def daily_dosage(self):
        return ((self.dosage * self.frequency)/self.period.timedelta().days).__round__(2)
    
    @property
    def expiration_date(self) -> datetime.date:
        return self.start + datetime.timedelta(days=self.total_days)
    
    @property
    def total_days(self):
        boxes = self.boxes or self.computed_boxes
        return  int(boxes * self.medication.package_size/ self.daily_dosage)
    
    @property
    def remaining_days(self):
        return self.total_days - (datetime.date.today() - self.start).days
        
        
    
    @medication.setter
    def medication(self, value: Medication):
        self.medication_key.set_instance(value)
        
        
    async def set_instance(self):
        if not self.medication:
            self.medication = await Medication.fetch_instance(self.medication_key)
    
@modelmap
class BodyMeasure(SpaceModel):
    patient_key: Patient.Key
    created: DateTimeField
    weight: BodyMeasureFloat
    height: BodyMeasureFloat
    waist: BodyMeasureFloat
    hip: BodyMeasureFloat
    sbp: BodyMeasureInteger
    dbp: BodyMeasureInteger
    hr: BodyMeasureInteger
    rr: BodyMeasureInteger
    
    def __lt__(self, other):
        return self.created < other.created
    
    def __element__(self):
        def make(label, value):
            return Element()
        children = [
                Element('div', '.grid-3', Element('h6', children=str(self.patient_key.instance.age)))
        ]
        return Element('li', '.list-group-item', Element('div', '.grid-4', children=children))
    
    def __str__(self):
        with StringIO() as buf:
            buf.write(f'{self.created.date()} {self.created.hour}h')
            for k, v in self.model_fields.items():
                if value:= getattr(self, k):
                    if k == 'weight':
                        buf.write(f", peso {value}Kg")
                    elif k == 'height':
                        buf.write(f", altura {value}cm")
                    elif k == 'waist':
                        buf.write(f", cintura {value}cm")
                    elif k == 'hip':
                        buf.write(f", quadril {value}cm")
                    elif k == 'hr':
                        buf.write(f", FC {value}bpm")
                    elif k == 'rr':
                        buf.write(f", FR {value}rpm")
            if self.waist_hip_ratio:
                buf.write(f", CQR {self.waist_hip_ratio}")
            if self.bmi:
                buf.write(f", IMC {self.bmi}Kg/m2")
            if self.sbp and self.dbp:
                buf.write(f', PA {self.sbp}/{self.dbp}mmHg')
            return buf.getvalue()
        
    @property
    def waist_hip_ratio(self):
        if self.waist and self.hip:
            return (self.waist / self.hip).__round__(2)
        return None
    
    @property
    def bmi(self):
        if self.weight and self.height:
            return (self.weight / (self.height/100 * self.height/100)).__round__(1)
        return None
            

@modelmap
class Visit(SpaceModel):
    created: DateTimeField
    patient_key: Patient.Key
    complaints: str
    intro: Optional[str] = Field(None)
    subjective: Optional[str] = Field(None)
    objective: Optional[str] = Field(None)
    assessment: Optional[str] = Field(None)
    plan: Optional[str] = Field(None)
    end: DateTimeField
    
    def __lt__(self, other):
        return self.created < other.created
    
    def __str__(self):
        return f'{self.created.date()} {self.complaints}'
    
if __name__ == '__main__':
    x = Medication(label='Brintellix', drugs='vortioxetina 10mg', route='O', dosage_form='TAB', package='30 comp')
    print(x)
    print(x.package_content)
    print(x.package_size)
    print(x.drug_names)
    print(x.search)

