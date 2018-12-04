# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.tessel.tests.base import (
    BaseTesselAuctionWebTest, test_bids,
)
from openprocurement.auctions.core.tests.cancellation import (
    AuctionCancellationResourceTestMixin,
    AuctionCancellationDocumentResourceTestMixin
)


class TesselAuctionCancellationResourceTest(BaseTesselAuctionWebTest,
                                             AuctionCancellationResourceTestMixin):
    initial_status = 'active.tendering'
    initial_bids = test_bids


class TesselAuctionCancellationDocumentResourceTest(BaseTesselAuctionWebTest,
                                                     AuctionCancellationDocumentResourceTestMixin):

    def setUp(self):
        super(TesselAuctionCancellationDocumentResourceTest, self).setUp()
        # Create cancellation
        response = self.app.post_json('/auctions/{}/cancellations?acc_token={}'.format(
            self.auction_id, self.auction_token
        ), {'data': {'reason': 'cancellation reason'}})
        cancellation = response.json['data']
        self.cancellation_id = cancellation['id']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(TesselAuctionCancellationResourceTest))
    tests.addTest(unittest.makeSuite(TesselAuctionCancellationDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
