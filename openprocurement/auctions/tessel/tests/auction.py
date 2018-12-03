# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.blanks.auction_blanks import (
    get_auction_auction_not_found,
    post_auction_auction_document
)
from openprocurement.auctions.tessel.tests.base import (
    BaseTesselAuctionWebTest,
    test_bids,
    test_organization,
    test_insider_auction_data
)
from openprocurement.auctions.tessel.tests.blanks.auction_blanks import (
    # TesselAuctionAuctionResourceTest
    get_auction_auction,
    post_auction_auction,
    patch_auction_auction,
    # TesselAuctionBidInvalidationAuctionResourceTest
    post_auction_all_invalid_bids,
    post_auction_one_bid_without_value,
    post_auction_zero_bids,
    post_auction_one_valid_bid,
    # TesselAuctionDraftBidAuctionResourceTest
    post_auction_all_draft_bids,
    # TesselAuctionSameValueAuctionResourceTest
    post_auction_auction_not_changed,
    post_auction_auction_reversed,
    # TesselAuctionNoBidsResourceTest
    post_auction_no_bids
)


class TesselAuctionAuctionResourceTest(BaseTesselAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids

    test_get_auction_auction_not_found = snitch(get_auction_auction_not_found)
    test_get_auction_auction = snitch(get_auction_auction)
    test_post_auction_auction = snitch(post_auction_auction)
    test_patch_auction_auction = snitch(patch_auction_auction)
    test_post_auction_auction_document = snitch(post_auction_auction_document)


class TesselAuctionBidInvalidationAuctionResourceTest(BaseTesselAuctionWebTest):
    initial_status = 'active.auction'
    initial_data = test_insider_auction_data
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            'qualified': True,
            "eligible": True
        }
        for i in range(3)
    ]

    test_post_auction_all_invalid_bids = unittest.skip("zero minimalstep")(snitch(post_auction_all_invalid_bids))
    test_post_auction_one_bid_without_value = snitch(post_auction_one_bid_without_value)
    test_post_auction_zero_bids = snitch(post_auction_zero_bids)
    test_post_auction_one_valid_bid = snitch(post_auction_one_valid_bid)


class TesselAuctionDraftBidAuctionResourceTest(BaseTesselAuctionWebTest):
    initial_status = 'active.auction'
    # initial_data = test_insider_auction_data
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            'qualified': True,
            "eligible": True,
            'status' : 'draft'
        }
        for i in range(3)
    ]

    test_post_auction_all_draft_bids = snitch(post_auction_all_draft_bids)


class TesselAuctionSameValueAuctionResourceTest(BaseTesselAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            'qualified': True,
            'eligible': True
        }
        for i in range(3)
    ]

    test_post_auction_auction_not_changed = snitch(post_auction_auction_not_changed)
    test_post_auction_auction_reversed = snitch(post_auction_auction_reversed)


class TesselAuctionNoBidsResourceTest(BaseTesselAuctionWebTest):
    initial_status = 'active.auction'

    test_post_auction_zero_bids = snitch(post_auction_no_bids)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(TesselAuctionAuctionResourceTest))
    tests.addTest(unittest.makeSuite(TesselAuctionBidInvalidationAuctionResourceTest))
    tests.addTest(unittest.makeSuite(TesselAuctionDraftBidAuctionResourceTest))
    tests.addTest(unittest.makeSuite(TesselAuctionSameValueAuctionResourceTest))
    tests.addTest(unittest.makeSuite(TesselAuctionNoBidsResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
