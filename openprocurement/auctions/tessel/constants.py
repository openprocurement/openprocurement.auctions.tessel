# -*- coding: utf-8 -*-
from datetime import timedelta

DUTCH_PERIOD = timedelta(minutes=405)
QUICK_DUTCH_PERIOD = timedelta(minutes=10)

TENDER_PERIOD_STATUSES = ['active.tendering', 'active.auction']
NUMBER_OF_STAGES = 80   # from openprocurement.auction.tessel.constants import DUTCH_ROUNDS as NUMBER_OF_STAGES
DUTCH_TIMEDELTA = timedelta(minutes=405)    # from openprocurement.auction.tessel.constants import DUTCH_TIMEDELTA
STAGE_TIMEDELTA = DUTCH_TIMEDELTA / NUMBER_OF_STAGES
SEALEDBID_TIMEDELTA = timedelta(minutes=10)  # from openprocurement.auction.tessel.constants import SEALEDBID_TIMEDELTA
BESTBID_TIMEDELTA = timedelta(minutes=5)    # from openprocurement.auction.tessel.constants import BESTBID_TIMEDELTA
FIRST_PAUSE = timedelta(seconds=30)
END_PHASE_PAUSE = timedelta(seconds=20)
SERVICE_TIMEDELTA = FIRST_PAUSE + END_PHASE_PAUSE

VIEW_LOCATIONS = [
    "openprocurement.auctions.tessel.views",
]

DEFAULT_PROCUREMENT_METHOD_TYPE = "sellout.insider"

AUCTION_STATUSES = [
    'draft', 'pending.activation', 'active.tendering', 'active.auction', 'active.qualification',
    'active.awarded', 'complete', 'cancelled', 'unsuccessful'
]

CONTRACT_TYPES = ['yoke']

DEFAULT_LEVEL_OF_ACCREDITATION = {'create': [3],
                                  'edit': [4]}
