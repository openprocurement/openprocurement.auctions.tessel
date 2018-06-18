# -*- coding: utf-8 -*-
from openprocurement.auctions.tessel.models import TesselAuction
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator,
    AuctionManagerAdapter
)
from openprocurement.auctions.core.plugins.awarding.v3_1.adapters import (
    AwardingV3_1ConfiguratorMixin
)


class AuctionTesselConfigurator(AuctionConfigurator,
                                AwardingV3_1ConfiguratorMixin):
    name = 'Auction Tessel Configurator'
    model = TesselAuction


class AuctionTesselManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        pass

    def change_auction(self, request):
        pass
