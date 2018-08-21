# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from copy import deepcopy

from openprocurement.auctions.core.tests.base import (
    BaseWebTest,
    BaseAuctionWebTest,
    test_organization as base_test_organization,
    test_auction_data, base_test_bids, test_document_data,
    MOCK_CONFIG as BASE_MOCK_CONFIG,
)
from openprocurement.auctions.core.utils import (
    apply_data_patch,
    connection_mock_config
)


from openprocurement.auctions.tessel.constants import DEFAULT_PROCUREMENT_METHOD_TYPE

now = datetime.now()

PARTIAL_MOCK_CONFIG = {
    "auctions.tessel": {
        "use_default": True,
        "plugins": {
            "tessel.migration": None
        },
        "migration": False,
        "aliases": [],
        "accreditation": {
            "create": [3],
            "edit": [4]
        }
    }
}
MOCK_CONFIG_PARTIAL_AUCTION = {
    "url": "http://auction-sandbox.openprocurement.org",
    "public_key": "fe3b3b5999a08e68dfe62687c2ae147f62712ceace58c1ffca8ea819eabcb5d1"
    }



MOCK_CONFIG = connection_mock_config(
    PARTIAL_MOCK_CONFIG,
    base=BASE_MOCK_CONFIG,
    connector=('plugins', 'api', 'plugins', 'auctions.core', 'plugins')
)


MOCK_CONFIG = connection_mock_config(
    MOCK_CONFIG_PARTIAL_AUCTION,
    base=MOCK_CONFIG,
    connector=('config','auction')
)

test_insider_auction_data = deepcopy(test_auction_data)
for item in test_insider_auction_data['items']:
    item['classification']['scheme'] = 'CPV'
    item['classification']['id'] = '51413000-0'

test_insider_auction_data['auctionParameters'] = {
    'type': 'insider',
    'dutchSteps': 88
}
test_insider_auction_data.update({
    'registrationFee': {
        'amount': 700.87,
        'currency': 'UAH'
    },
    'bankAccount': {
        'bankName': 'name of bank',
        'accountIdentification': [
            {
                'scheme': 'accountNumber',
                'id': '111111-8',
                'description': 'some description'
            }
        ]
    }
})

tessel_document_data = deepcopy(test_document_data)
tessel_document_data['documentType'] = 'x_dgfAssetFamiliarization'
del tessel_document_data['hash']
tessel_document_data['accessDetails'] = 'access details'

test_insider_auction_data['documents'] = [
    tessel_document_data
]

del test_insider_auction_data['dgfID']
del test_insider_auction_data['dgfDecisionDate']
del test_insider_auction_data['dgfDecisionID']

schema_properties = {
    "code": "06000000-2",
    "version": "001",
    "properties": {
        "region": "Вінницька область",
        "district": "м.Вінниця",
        "cadastral_number": "1",
        "area": 1,
        "forms_of_land_ownership": ["державна"],
        "co_owners": False,
        "availability_of_utilities": True,
        "current_use": True
   }
 }

test_insider_auction_data_with_schema = deepcopy(test_insider_auction_data)
# test_insider_auction_data_with_schema['items'][0]['classification']['id'] = schema_properties['code']
# test_insider_auction_data_with_schema['items'][0]['schema_properties'] = schema_properties

test_organization = deepcopy(base_test_organization)
test_organization['additionalIdentifiers'] = [{
    "scheme": u"UA-FIN",
    "id": u"А01 457213"
}]

test_bids = []
for i in base_test_bids:
    bid = deepcopy(i)
    bid.update({'eligible': True})
    bid.update({'qualified': True})
    bid['tenderers'] = [test_organization]
    test_bids.append(bid)

test_lots = [
    {
        'title': 'lot title',
        'description': 'lot description',
        'value': test_auction_data['value'],
        'minimalStep': test_auction_data['minimalStep'],
    }
]

for data in test_insider_auction_data, test_insider_auction_data_with_schema:
    data["procurementMethodType"] = DEFAULT_PROCUREMENT_METHOD_TYPE
    del data['minimalStep']


class BaseInsiderWebTest(BaseWebTest):

    """Base Web Test to test openprocurement.auctions.tessel.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG


class BaseInsiderAuctionWebTest(BaseAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_insider_auction_data
    initial_organization = test_organization
    mock_config = MOCK_CONFIG

    def set_status(self, status, extra=None):
        data = {'status': status}
        if status == 'active.tendering':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=1)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=5)).isoformat()
                }
            })
        elif status == 'active.auction':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now + timedelta(hours=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=2)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.awarded':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=11)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=12)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=10)).isoformat(),
                    "endDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'complete':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=11)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=10)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=11)).isoformat(),
                                "endDate": (now - timedelta(days=10)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        if extra:
            data.update(extra)
        auction = self.db.get(self.auction_id)
        auction.update(apply_data_patch(auction, data))
        self.db.save(auction)
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        #response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.app.authorization = authorization
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response
