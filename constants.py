"""Constants for PO3 file generation."""

# Giro type codes
PLUSGIRO_CODE = "00"
BANKGIRO_CODE = "05"
EXPENSE_CODE = "09"

# File format constants
CURRENCY = "SEK"
LINE_LENGTH = 80
RECORD_TYPE_HEADER = "MH00"
RECORD_TYPE_TRAILER = "MT00"
RECORD_TYPE_PAYMENT = "PI00"
RECORD_TYPE_NOTE = "BA00"
RECORD_TYPE_BENEFICIARY = "BE01"

# Column names
COL_APPROVED = "Godkänt"
COL_PAID = "Utbetalt"
COL_AMOUNT = "Belopp"
COL_NAME = "Ditt namn"
COL_ACTIVITY = "Verksamhet"
COL_DESCRIPTION = "Kort beskrivning av köp"
