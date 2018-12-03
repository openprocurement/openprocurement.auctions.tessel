# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.question import AuctionQuestionResourceTestMixin

from openprocurement.auctions.tessel.tests.base import BaseTesselAuctionWebTest


class TesselAuctionQuestionResourceTest(BaseTesselAuctionWebTest, AuctionQuestionResourceTestMixin):
    pass


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(TesselAuctionQuestionResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
