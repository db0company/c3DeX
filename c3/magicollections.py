from django.db.models import Q, Count
from django.utils.translation import ugettext_lazy as _
from magi.magicollections import (
    MagiCollection,
    MainItemCollection,
    SubItemCollection,
    AccountCollection as _AccountCollection,
    UserCollection as _UserCollection,
)
from magi.utils import (
    addParametersToURL,
    getMagiCollection,
    justReturn,
)
from c3.c3_translations import ct
from c3 import models, forms

############################################################
# User
############################################################

class UserCollection(_UserCollection):
    class ItemView(_UserCollection.ItemView):
        profile_accounts_top_template = 'profile_accounts_top_template'

############################################################
# Account = attended CCC
############################################################

class AccountCollection(_AccountCollection):
    title = 'CCC'
    plural_title = 'CCC'
    navbar_link = False
    form_class = forms.AccountForm
    icon = 'event'
    reportable = False

    add_sentence = ct['I was there']

    fields_icons = {
        'ccc': 'event',
    }

    class ItemView(_AccountCollection.ItemView):
        fields_exclude = ['creation']

    class AddView(_AccountCollection.AddView):
        unique_per_owner = True

        def before_save(self, request, instance, type=None):
            if 'attended_cccs' in request.session:
                del request.session['attended_cccs']
            return instance

    class EditView(_AccountCollection.EditView):
        def get_item(self, request, pk):
            if pk == 'unique':
                return {
                    'ccc': request.GET.get('ccc', request.GET.get('ccc_id', None)),
                    'owner': request.user,
                }
            return super(_AccountCollection.EditView, self).get_item(request, pk)

        def before_save(self, request, instance, type=None):
            if 'attended_cccs' in request.session:
                del request.session['attended_cccs']
            return instance

        def before_delete(self, request, item, ajax=False):
            if 'attended_cccs' in request.session:
                del request.session['attended_cccs']

############################################################
# CCC
############################################################

class CCCCollection(MainItemCollection):
    queryset = models.CCC.objects.all()
    title = 'CCC'
    plural_title = 'CCC'
    translated_fields = ['name', 'm_description']
    icon = 'event'

    fields_icons = {
        'type': 'category',
        'name': 'about',
        'number': 'hashtag',
        'start_date': 'date',
        'end_date': 'date',
        'main_url': 'link',
        'description': 'about',
        'talks': 'voice-actress',
    }

    def get_queryset(self, queryset, parameters, request):
        queryset = super(CCCCollection, self).get_queryset(queryset, parameters, request)
        if request.user.is_authenticated():
            account_collection = getMagiCollection('account')
            queryset = queryset.extra({
                u'total_{}'.format(account_collection.name):
                'SELECT COUNT(*) FROM c3_account WHERE ccc_id = c3_ccc.id AND owner_id  = {fk_owner_ids}'.format(
                    fk_owner_ids=request.user.id,
                )
            })
        return queryset

    def buttons_per_item(self, view, request, context, item):
        buttons = super(CCCCollection, self).buttons_per_item(view, request, context, item)
        account_collection = getMagiCollection('account')
        badge_total = getattr(item, u'total_{}'.format(account_collection.name), 0)
        ajax_title = u'{}: {}'.format(account_collection.add_sentence, unicode(item))
        delete_sentence = ct['Nevermind, I didn\'t go']
        buttons['account'] = {
            'title': (
                delete_sentence
                if badge_total > 0
                else account_collection.add_sentence
            ),
            'show': True,
            'open_in_new_window': False,
            'icon': 'add',
            'ajax_title': ajax_title,
            'url': addParametersToURL(account_collection.get_add_url(), { self.name: item.pk }),
            'ajax_url': addParametersToURL(account_collection.get_add_url(ajax=True), { self.name: item.pk }),
            'badge': badge_total,
            'classes': view.item_buttons_classes,
            'extra_attributes': {
                'unique-per-owner': 'true',
                'quick-add-to-collection': 'true',
                'parent-item': self.name,
                'parent-item-id': item.pk,
                'alt-message': (
                    account_collection.add_sentence
                    if badge_total > 0
                    else delete_sentence
                ),
            },
        }
        if not request.user.is_authenticated():
            buttons['account']['has_permissions'] = True
            buttons['account']['url'] = u'/signup/?next={url}&next_title={title}'.format(
                url=buttons['account']['url'],
                title=ajax_title,
            )
            buttons['account']['ajax_url'] = None
        else:
            buttons['account']['has_permissions'] = account_collection.add_view.has_permissions(request, context)
        return buttons

    class ListView(MainItemCollection.ListView):
        default_ordering = '-start_date'
        auto_filter_form = True
        item_buttons_classes = property(
            lambda _s: MainItemCollection.ListView.item_buttons_classes.fget(_s) + ['btn-lg'])

    class ItemView(MainItemCollection.ItemView):
        fields_prefetched_together = ['talks']

############################################################
# Hackerspace
############################################################

class HackerspaceCollection(MainItemCollection):
    queryset = models.Hackerspace.objects.all()
    title = ct['Hackerspace']
    plural_title = ct['Hackerspaces']
    navbar_link = False
    translated_fields = ['m_description']

############################################################
# Session
############################################################

class SessionCollection(SubItemCollection):
    queryset = models.Session.objects.all()
    main_collection = 'ccc'
    title = ct['Session']
    plural_title = ct['Sessions']
    translated_fields = ['m_description']

############################################################
# Talk
############################################################

def to_AttendedTalkCollection(cls):
    class _AttendedTalkCollection(cls):
        title = ct['Attended talk']
        plural_title = ct['Attended talks']
        add_sentence = ct['I was there']
        icon = 'date'

        class ListView(cls.ListView):
            item_padding = 20
            show_items_names = True

            def top_buttons(self, request, context):
                buttons = super(_AttendedTalkCollection.ListView, self).top_buttons(request, context)
                if 'add_to_collected' in buttons:
                    buttons['add_to_collected']['title'] = _(u'Add {thing}').format(
                        thing=self.collection.title.lower())
                return buttons

        class AddView(cls.AddView):
            unique_per_owner = True
            quick_add_to_collection = justReturn(True)
            add_to_collection_variables = cls.AddView.add_to_collection_variables + [
                'ccc_id',
            ]

    return _AttendedTalkCollection

def to_WatchedTalkCollection(cls):
    class _WatchedTalkCollection(cls):
        title = ct['Watched talk']
        plural_title = ct['Watched talks']
        add_sentence = ct['I watched it']
        icon = 'film'

        class ListView(cls.ListView):
            item_padding = 20
            show_items_names = True
            add_button_use_collection_icon = True

        class AddView(cls.AddView):
            unique_per_owner = True
            quick_add_to_collection = justReturn(True)

    return _WatchedTalkCollection

def to_WantToWatchTalkCollection(cls):
    class _WantToWatchTalkCollection(cls):
        title = ct['Talk I want to watch']
        plural_title = ct['Talks I want to watch']
        add_sentence = ct['Add to watchlist']
        icon = 'star-empty'

        class ListView(cls.ListView):
            item_padding = 20
            show_items_names = True
            add_button_use_collection_icon = True

        class AddView(cls.AddView):
            unique_per_owner = True
            quick_add_to_collection = justReturn(True)

    return _WantToWatchTalkCollection

class TalkCollection(SubItemCollection):
    queryset = models.Talk.objects.all()
    main_collection = 'ccc'
    title = ct['Talk']
    plural_title = ct['Talks']

    collectible = [
        models.AttendedTalk,
        models.WatchedTalk,
        models.WantToWatchTalk,
    ]

    def collectible_to_class(self, model_class):
        return {
            'attendedtalk': to_AttendedTalkCollection,
            'watchedtalk': to_WatchedTalkCollection,
            'wanttowatchtalk': to_WantToWatchTalkCollection,
        }[model_class.collection_name](super(TalkCollection, self).collectible_to_class(model_class))

    class ListView(SubItemCollection.ListView):
        default_ordering = '-start_date'
        show_items_names = True
        auto_filter_form = True

        quick_add_view = True

        def get_queryset(self, queryset, parameters, request):
            queryset = super(TalkCollection.ListView, self).get_queryset(queryset, parameters, request)
            selected_account = request.GET.get(u'add_to_attendedtalk', None)
            if selected_account:
                ccc = models.Account.objects.select_related('ccc').get(id=selected_account).ccc
                queryset = queryset.filter(ccc=ccc)
            return queryset

        def buttons_per_item(self, request, context, item):
            buttons = super(TalkCollection.ListView, self).buttons_per_item(request, context, item)
            selected_account = request.GET.get(u'add_to_attendedtalk', None)
            if ('attendedtalk' in buttons
                and not selected_account
                and not request.GET.get(u'added_attendedtalk', None)):
                del(buttons['attendedtalk'])
            return buttons

    class ItemView(SubItemCollection.ItemView):
        def buttons_per_item(self, request, context, item):
            buttons = super(TalkCollection.ItemView, self).buttons_per_item(request, context, item)
            if 'attendedtalk' in buttons:
                del(buttons['attendedtalk'])
            return buttons

############################################################
# Question
############################################################

class QuestionCollection(MagiCollection):
    queryset = models.Question.objects.all()
    navbar_link_title = 'Q&A'
    title = ct['Question']
    plural_title = ct['Questions']
    icon = 'idea'

    fields_icons = {
        'name': 'idea',
        'owner': 'voice-actress',
    }

    class ListView(MagiCollection.ListView):
        add_button_subtitle = None

        def top_buttons(self, request, context):
            buttons = super(QuestionCollection.ListView, self).top_buttons(request, context)
            if not request.user.is_authenticated():
                buttons['add']['has_permissions'] = True
            return buttons

        def buttons_per_item(self, request, context, item):
            buttons = super(QuestionCollection.ListView, self).buttons_per_item(request, context, item)
            buttons['see_answers'] = {
                'show': True, 'has_permissions': True,
                'title': ct['See answers'],
                'url': item.item_url,
                'icon': 'idea',
                'classes': self.item_buttons_classes,
            }
            return buttons

        def extra_context(self, context):
            context['ajax_item_view_enabled'] = False

    class ItemView(MagiCollection.ItemView):
        fields_preselected = ['owner']

############################################################
# Project
############################################################

class ProjectCollection(MainItemCollection):
    queryset = models.Project.objects.all()
    title = ct['Project']
    plural_title = ct['Projects']
    navbar_link = False

############################################################
# CCC Link
############################################################

class CCCLinkCollection(SubItemCollection):
    queryset = models.CCCLink.objects.all()
    main_collection = 'ccc'
    title = _('Link')
    plural_title = _('Links')
    translated_fields = ['name']

############################################################
# Link
############################################################

class LinkCollection(MagiCollection):
    queryset = models.Link.objects.all()
    title = _('Link')
    plural_title = _('Links')
    translated_fields = ['name']
    icon = 'link'
    navbar_link_list = 'links'
    navbar_link_title = _('More')

    class ItemView(MagiCollection.ItemView):
        ajax = False

############################################################
# Photo
############################################################

class PhotoCollection(MainItemCollection):
    queryset = models.Photo.objects.all()
    title = ct['Photo']
    plural_title = ct['Photos']
    navbar_link = False
