# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution

from openprocurement.auctions.core.utils import (
    TZ,
    get_now,
    log_auction_status_change
)
from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.core.models import AUCTION_STAND_STILL_TIME

from openprocurement.auctions.tessel.constants import (
    STAGE_TIMEDELTA,
    BESTBID_TIMEDELTA,
    SEALEDBID_TIMEDELTA,
    SERVICE_TIMEDELTA
)

from urllib import quote
from base64 import b64encode

PKG = get_distribution(__package__)
LOGGER = getLogger(PKG.project_name)


def generate_auction_url(request, bid_id=None):
    auction_module_url = request.registry.auction_module_url
    auction_id = request.validated['auction']['id']
    if bid_id:
        auction_id = request.validated['auction_id']
        signature = quote(b64encode(request.registry.signer.signature('{}_{}'.format(auction_id, bid_id))))
        return '{}/insider-auctions/{}/login?bidder_id={}&signature={}'.format(auction_module_url, auction_id, bid_id, signature)
    return '{}/insider-auctions/{}'.format(auction_module_url, auction_id)


def check_auction_status(request):
    auction = request.validated['auction']
    adapter = request.registry.getAdapter(auction, IAuctionManager)
    if auction.awards:
        awards_statuses = set([award.status for award in auction.awards])
    else:
        awards_statuses = set([""])
    if not awards_statuses.difference(set(['unsuccessful', 'cancelled'])):
        adapter.pendify_auction_status('unsuccessful')
        log_auction_status_change(request, auction, auction.status)
    if auction.contracts and auction.contracts[-1].status == 'active':
        adapter.pendify_auction_status('complete')
        log_auction_status_change(request, auction, auction.status)


def check_status(request):
    auction = request.validated['auction']
    now = get_now()
    for award in auction.awards:
        request.content_configurator.check_award_status(request, award, now)
    if auction.status == 'active.tendering' and auction.enquiryPeriod.endDate <= now:
        auction.status = 'active.auction'
        auction.auctionUrl = generate_auction_url(request)
        log_auction_status_change(request, auction, auction.status)
        return True
    elif auction.status == 'active.awarded':
        standStillEnds = [
            a.complaintPeriod.endDate.astimezone(TZ)
            for a in auction.awards
            if a.complaintPeriod.endDate
        ]
        if not standStillEnds:
            return True
        standStillEnd = max(standStillEnds)
        if standStillEnd <= now:
            check_auction_status(request)


def invalidate_empty_bids(auction):
    for bid in auction['bids']:
        if not bid.get('value') and bid['status'] == "active":
            bid['status'] = 'invalid'


def merge_auction_results(auction, request):
    if 'bids' not in auction:
        return
    for auction_bid in request.validated['data']['bids']:
        for bid in auction['bids']:
            if bid['id'] == auction_bid['id']:
                bid.update(auction_bid)
                break
    request.validated['data']['bids'] = auction['bids']


def calc_auction_end_time(stages, start):
    return start + stages * STAGE_TIMEDELTA + SERVICE_TIMEDELTA + SEALEDBID_TIMEDELTA + BESTBID_TIMEDELTA + AUCTION_STAND_STILL_TIME
