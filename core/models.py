from django.db import models
# Create your models here.
class UnderConstruction(models.Model):
    """Under Construction Model - To put website in maintenance mode"""
    status = models.IntegerField(default=0)  # 0=Normal, 1=Under Construction
    updated_at = models.DateTimeField(auto_now=True)

class FinancialYear(models.Model):
    year_name  = models.CharField(max_length=20, verbose_name='Year Name')  # e.g. 2024-25
    start_date = models.DateField(verbose_name='Start Date')
    end_date   = models.DateField(verbose_name='End Date')
    is_current = models.BooleanField(default=False, verbose_name='Current Year')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Dairy(models.Model):
    STATUS_CHOICES = [
        ('active',    'Active'),
        ('inactive',  'Inactive'),
        ('suspended', 'Suspended'),
    ]
    LANGUAGE_CHOICES = [
        ('mr', 'Marathi'),
        ('hi', 'Hindi'),
        ('en', 'English'),
    ]
    # ── Basic Info ──
    dairy_name           = models.CharField(max_length=200, verbose_name='Dairy Name')
    owner_name     = models.CharField(max_length=150, verbose_name='Owner Name')
    mobile         = models.CharField(max_length=10, unique=True, verbose_name='Mobile Number')
    email          = models.EmailField(blank=True, null=True, verbose_name='Email')
    pin            = models.CharField(max_length=20, verbose_name='Login PIN')
    # ── Address ──
    address        = models.TextField(blank=True, null=True, verbose_name='Address')
    # ── Settings ──
    language       = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='mr', verbose_name='Language')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Status')
    # ── Timestamps ──
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)


class DairyWalletLedger(models.Model):
    TRANSACTION_REASON_CHOICES = [
        ('free_trial',  'Free Trial Bonus'),
        ('recharge',    'Wallet Recharge'),
        ('entry_debit', 'Milk Entry Debit'),
    ]

    # ── Relations ──
    dairy          = models.ForeignKey(Dairy, on_delete=models.CASCADE, related_name='wallet_ledger', verbose_name='Dairy')
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Financial Year')

    # ── Transaction Info ──
    transaction_reason = models.CharField(max_length=20, choices=TRANSACTION_REASON_CHOICES, verbose_name='Reason')
    credit_amount      = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Credit Amount (₹)')
    debit_amount       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Debit Amount (₹)')
    credit_entries     = models.IntegerField(default=0, verbose_name='Credit Entries')
    debit_entries      = models.IntegerField(default=0, verbose_name='Debit Entries')

    # ── Timestamps ──
    created_at = models.DateTimeField(auto_now_add=True)

    # ── Razorpay ──
    razorpay_order_id   = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature  = models.CharField(max_length=255, blank=True, null=True)
    is_paid             = models.BooleanField(default=False)


class Farmer(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('cow',     'Cow / गाय'),
        ('buffalo', 'Buffalo / म्हैस'),
        ('both',    'Both / दोन्ही'),
    ]
    # ── Relations ──
    dairy         = models.ForeignKey(Dairy, on_delete=models.CASCADE, related_name='farmers', verbose_name='Dairy')
    # ── Basic Info ──
    farmer_code   = models.CharField(max_length=20, verbose_name='Farmer Code')
    name          = models.CharField(max_length=150, verbose_name='Farmer Name')
    mobile        = models.CharField(max_length=10, verbose_name='Mobile Number')
    address       = models.TextField(blank=True, null=True, verbose_name='Address')
    # ── Cattle Info ──
    animal_type   = models.CharField(max_length=10, choices=ANIMAL_TYPE_CHOICES, default='buffalo', verbose_name='Animal Type')
    # ── Bank Details ──
    bank_name     = models.CharField(max_length=150, blank=True, null=True, verbose_name='Bank Name')
    account_no    = models.CharField(max_length=30, blank=True, null=True, verbose_name='Account Number')
    ifsc_code     = models.CharField(max_length=15, blank=True, null=True, verbose_name='IFSC Code')
    # ── Status ──
    is_active     = models.BooleanField(default=True, verbose_name='Active')
    # ── Timestamps ──
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('dairy', 'farmer_code')


class RateChart(models.Model):
    CHART_TYPE_CHOICES = (
        ('per_kg', 'Per Kg'),
        ('step', 'Step Based'),
    )
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=10,choices=Farmer.ANIMAL_TYPE_CHOICES)
    chart_type = models.CharField(max_length=20,choices=CHART_TYPE_CHOICES)
    start_rate = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RateChartRange(models.Model):
    RANGE_TYPE_CHOICES = (
        ('fat', 'Fat'),
        ('snf', 'SNF'),
    )
    rate_chart = models.ForeignKey(RateChart,on_delete=models.CASCADE,related_name='ranges')
    range_type = models.CharField(max_length=10,choices=RANGE_TYPE_CHOICES)
    from_value = models.DecimalField(max_digits=5,decimal_places=1)
    to_value = models.DecimalField(max_digits=5,decimal_places=1)
    rate = models.DecimalField(max_digits=10,decimal_places=2)

class RateChartStep(models.Model):
    STEP_TYPE_CHOICES = (
        ('fat', 'Fat'),
        ('snf', 'SNF'),
    )
    rate_chart = models.ForeignKey(RateChart,on_delete=models.CASCADE,related_name='steps')
    step_type = models.CharField(max_length=10,choices=STEP_TYPE_CHOICES)
    value = models.DecimalField(max_digits=5,decimal_places=1)
    increment = models.DecimalField(max_digits=10,decimal_places=2)

class MilkCollectionSetting(models.Model):
    dairy = models.OneToOneField(Dairy,on_delete=models.CASCADE)
    enable_snf = models.BooleanField(default=True)
    enable_collection_slip = models.BooleanField(default=True)
    enable_sms = models.BooleanField(default=False)
    enable_whatsapp = models.BooleanField(default=False)


class MilkCollection(models.Model):
    SHIFT_CHOICES = (
        ('morning', 'Morning'),
        ('evening', 'Evening'),
    )
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE,related_name='milk_collections')
    financial_year = models.ForeignKey(FinancialYear,on_delete=models.SET_NULL,null=True,blank=True)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE,related_name='milk_collections')
    collection_date = models.DateField()
    shift = models.CharField(max_length=10,choices=SHIFT_CHOICES)
    animal_type = models.CharField(max_length=10,choices=Farmer.ANIMAL_TYPE_CHOICES)
    milk_liter = models.DecimalField(max_digits=8,decimal_places=2)
    fat = models.DecimalField(max_digits=5,decimal_places=2)
    snf = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    rate = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class CollectionSlip(models.Model):
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE)
    collection = models.OneToOneField(MilkCollection,on_delete=models.CASCADE)
    slip_no = models.CharField(max_length=30,unique=True)
    printed_at = models.DateTimeField(auto_now_add=True)

class SMSQueue(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE,null=True,blank=True)
    collection = models.ForeignKey(MilkCollection,on_delete=models.CASCADE,null=True,blank=True)
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    sent_at = models.DateTimeField(null=True,blank=True)
    error_message = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)