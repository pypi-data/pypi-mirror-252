# from .models.sql_mirror.sql_mirror import SQLMirror
from .models.advocacy_campaigns.advocacy_campaign import AdvocacyCampaign
from .models.advocacy_campaigns.advocacy_campaigns import AdvocacyCampaigns
from .models.attendances.attendance import Attendance
from .models.attendances.attendances import Attendances
from .models.campaigns.campaign import Campaign
from .models.campaigns.campaigns import Campaigns
from .models.custom_fields.custom_fields import CustomFields
from .models.donations.donations import Donations
from .models.donations.donation import Donation
from .models.embed.embed import Embed
from .models.event_campaigns.event_campaign import EventCampaign
from .models.event_campaigns.event_campaigns import EventCampaigns
from .models.events.event import Event
from .models.events.events import Events
from .models.forms.form import Form
from .models.forms.forms import Forms
from .models.fundraising_pages.fundraising_page import FundraisingPage
from .models.fundraising_pages.fundraising_pages import FundraisingPages
from .models.items.items import Items
from .models.items.item import Item
from .models.lists.list import List
from .models.lists.lists import Lists
from .models.messages.message import Message
from .models.messages.messages import Messages
from .models.metadata.metadata import Metadata
from .models.outreaches.outreach import Outreach
from .models.outreaches.outreaches import Outreaches
from .models.people.people import People
from .models.people.person import Person
from .models.petitions.petition import Petition
from .models.petitions.petitions import Petitions
from .models.queries.queries import Queries
from .models.queries.query import Query
from .models.signatures.signature import Signature
from .models.signatures.signatures import Signatures
from .models.submissions.submissions import Submissions
from .models.submissions.submission import Submission
from .models.taggings.tagging import Tagging
from .models.taggings.taggings import Taggings
from .models.tags.tag import Tag
from .models.tags.tags import Tags
from .models.wrappers.wrapper import Wrapper
from .models.wrappers.wrappers import Wrappers


class ActionNetwork(object):
    def __init__(self, osdi_token=None):
        assert not (osdi_token is None)
        self.base_url = "https://actionnetwork.org/api/v2/"
        self.osdi_token = osdi_token
        self.headers = {
            "Content-Type": "application/json",
            "OSDI-API-Token": self.osdi_token,
        }
        # Advocacy campaigns (More Info: https://actionnetwork.org/docs/v2/advocacy_campaigns)
        self.advocacy_campaigns = AdvocacyCampaigns(headers=self.headers)
        self.advocacy_campaigns = AdvocacyCampaign(headers=self.headers)
        # attendances (More Info: https://actionnetwork.org/docs/v2/attendances)
        self.attendances = Attendances(headers=self.headers)
        self.attendance = Attendance(headers=self.headers)
        # campaigns (More Info: https://actionnetwork.org/docs/v2/campaigns)
        self.campaigns = Campaigns(headers=self.headers)
        self.campaign = Campaign(headers=self.headers)
        # Custom Fields (More Info: https://actionnetwork.org/docs/v2/custom_fields)
        self.custom_fields = CustomFields(headers=self.headers)
        # donations (More Info: https://actionnetwork.org/docs/v2/donations)
        self.donations = Donations(headers=self.headers)
        self.donation = Donation(headers=self.headers)
        # Embeds (More Info: https://actionnetwork.org/docs/v2/embed)
        self.embeds = Embed(headers=self.headers)
        # Event campaigns (More Info: https://actionnetwork.org/docs/v2/event_campaigns)
        self.event_campaigns = EventCampaigns(headers=self.headers)
        self.event_campaign = EventCampaign(headers=self.headers)
        # events (More Info: https://actionnetwork.org/docs/v2/events)
        self.events = Events(headers=self.headers)
        self.event = Event(headers=self.headers)
        # forms (More Info: https://actionnetwork.org/docs/v2/forms)
        self.forms = Forms(headers=self.headers)
        self.forms = Form(headers=self.headers)
        # Fundraising Pages (More Info: https://actionnetwork.org/docs/v2/fundraising_pages)
        self.fundraising_pages = FundraisingPages(headers=self.headers)
        self.fundraising_page = FundraisingPage(headers=self.headers)
        # items (More Info: https://actionnetwork.org/docs/v2/items)
        self.items = Items(headers=self.headers)
        self.item = Item(headers=self.headers)
        # lists (More Info: https://actionnetwork.org/docs/v2/lists)
        self.lists = Lists(headers=self.headers)
        self.list = List(headers=self.headers)
        # messages (More Info: https://actionnetwork.org/docs/v2/messages)
        self.messages = Messages(headers=self.headers)
        self.message = Message(headers=self.headers)
        # metadata (More Info: https://actionnetwork.org/docs/v2/metadata)
        self.metadata = Metadata(headers=self.headers)
        # outreaches (More Info: https://actionnetwork.org/docs/v2/outreaches)
        self.outreaches = Outreaches(headers=self.headers)
        self.outreach = Outreach(headers=self.headers)
        # people (More Info: https://actionnetwork.org/docs/v2/people)
        self.people = People(headers=self.headers)
        self.person = Person(headers=self.headers)
        # petitions (More Info: https://actionnetwork.org/docs/v2/petitions)
        self.petitions = Petitions(headers=self.headers)
        self.petition = Petition(headers=self.headers)
        # queries (More Info: https://actionnetwork.org/docs/v2/queries)
        self.queries = Queries(headers=self.headers)
        self.query = Query(headers=self.headers)
        # signatures (More Info: https://actionnetwork.org/docs/v2/signatures)
        self.signatures = Signatures(headers=self.headers)
        self.signature = Signature(headers=self.headers)
        # submissions (More Info: https://actionnetwork.org/docs/v2/submissions)
        self.submissions = Submissions(headers=self.headers)
        self.submission = Submission(headers=self.headers)
        # tags (More Info: https://actionnetwork.org/docs/v2/tags)
        self.tags = Tags(headers=self.headers)
        self.tag = Tag(headers=self.headers)
        # taggings (More Info: https://actionnetwork.org/docs/v2/taggings)
        self.taggings = Taggings(headers=self.headers)
        self.tagging = Tagging(headers=self.headers)
        # wrappers (More Info: https://actionnetwork.org/docs/v2/wrappers)
        self.wrappers = Wrappers(headers=self.headers)
        self.wrapper = Wrapper(headers=self.headers)
        # TODO: Later
        # SQL Mirror (More Info: https://actionnetwork.org/contact?group=uploads)
        # self.sql_mirror = SQLMirror

   