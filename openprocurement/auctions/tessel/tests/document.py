# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.tessel.tests.base import BaseTesselAuctionWebTest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.document import (
    AuctionDocumentResourceTestMixin,
    AuctionDocumentWithDSResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.document_blanks import (
    # TesselAuctionDocumentWithDSResourceTest
    create_auction_document_vdr,
    put_auction_document_vdr,
)
from openprocurement.auctions.tessel.tests.blanks.document_blanks import (
    patch_auction_document
)


class TesselAuctionDocumentResourceTest(BaseTesselAuctionWebTest, AuctionDocumentResourceTestMixin):
    docservice = False
    test_patch_auction_document = snitch(patch_auction_document)


class TesselAuctionDocumentWithDSResourceTest(TesselAuctionDocumentResourceTest, AuctionDocumentWithDSResourceTestMixin):
    docservice = True

    test_patch_auction_document = snitch(patch_auction_document)

    test_create_auction_document_pas = None
    test_put_auction_document_pas = None


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(TesselAuctionDocumentResourceTest))
    tests.addTest(unittest.makeSuite(TesselAuctionDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
