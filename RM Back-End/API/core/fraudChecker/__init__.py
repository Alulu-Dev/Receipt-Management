""":
TODO: 1. create a mock database data for ECRA record
TODO: 2. create a function that listen on new receipt during upload and check against ECRA database
TODO: 3. create a function that  list caught receipts and returns details with status of report to ECRA
"""

from .fraudChecker import (report_illegal_receipts as report_fraud,
                           check_legality_of_receipts as check_fraud)
