import logging

from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import IContentConfigurator
from openprocurement.auctions.core.interfaces import IAuctionManager

from openprocurement.auctions.tessel.models import TesselAuction, ITesselAuction
from openprocurement.auctions.tessel.adapters import (
    AuctionTesselConfigurator,
    AuctionTesselManagerAdapter
)
from openprocurement.auctions.tessel.constants import (
    VIEW_LOCATIONS,
    DEFAULT_PROCUREMENT_METHOD_TYPE,
    DEFAULT_LEVEL_OF_ACCREDITATION
)

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    procurement_method_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        procurement_method_types.append(DEFAULT_PROCUREMENT_METHOD_TYPE)
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(TesselAuction,
                                                 procurementMethodType)

    for view_module in VIEW_LOCATIONS:
        config.scan(view_module)

    config.registry.registerAdapter(
        AuctionTesselConfigurator,
        (ITesselAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AuctionTesselManagerAdapter,
        (ITesselAuction, ),
        IAuctionManager
    )

    LOGGER.info("Included openprocurement.auctions.tessel plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_config.get('accreditation'):
        config.registry.accreditation['auction'][TesselAuction._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['auction'][TesselAuction._internal_type] = plugin_config['accreditation']
