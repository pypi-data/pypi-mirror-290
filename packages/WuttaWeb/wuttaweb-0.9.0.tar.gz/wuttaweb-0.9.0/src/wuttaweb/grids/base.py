# -*- coding: utf-8; -*-
################################################################################
#
#  wuttaweb -- Web App for Wutta Framework
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Base grid classes
"""

import functools
import json
import logging

import sqlalchemy as sa

import paginate
from pyramid.renderers import render
from webhelpers2.html import HTML

from wuttaweb.db import Session
from wuttaweb.util import FieldList, get_model_fields, make_json_safe


log = logging.getLogger(__name__)


class Grid:
    """
    Base class for all grids.

    :param request: Reference to current :term:`request` object.

    :param columns: List of column names for the grid.  This is
       optional; if not specified an attempt will be made to deduce
       the list automatically.  See also :attr:`columns`.

    .. note::

       Some parameters are not explicitly described above.  However
       their corresponding attributes are described below.

    Grid instances contain the following attributes:

    .. attribute:: key

       Presumably unique key for the grid; used to track per-grid
       sort/filter settings etc.

    .. attribute:: vue_tagname

       String name for Vue component tag.  By default this is
       ``'wutta-grid'``.  See also :meth:`render_vue_tag()`.

    .. attribute:: model_class

       Model class for the grid, if applicable.  When set, this is
       usually a SQLAlchemy mapped class.  This may be used for
       deriving the default :attr:`columns` among other things.

    .. attribute:: columns

       :class:`~wuttaweb.forms.base.FieldList` instance containing
       string column names for the grid.  Columns will appear in the
       same order as they are in this list.

       See also :meth:`set_columns()` and :meth:`get_columns()`.

    .. attribute:: data

       Data set for the grid.  This should either be a list of dicts
       (or objects with dict-like access to fields, corresponding to
       model records) or else an object capable of producing such a
       list, e.g. SQLAlchemy query.

       This is the "full" data set; see also
       :meth:`get_visible_data()`.

    .. attribute:: labels

       Dict of column label overrides.

       See also :meth:`get_label()` and :meth:`set_label()`.

    .. attribute:: renderers

       Dict of column (cell) value renderer overrides.

       See also :meth:`set_renderer()`.

    .. attribute:: actions

       List of :class:`GridAction` instances represenging action links
       to be shown for each record in the grid.

    .. attribute:: linked_columns

       List of column names for which auto-link behavior should be
       applied.

       See also :meth:`set_link()` and :meth:`is_linked()`.

    .. attribute:: paginated

       Boolean indicating whether the grid data should be paginated
       vs. all data shown at once.  Default is ``False`` which means
       the full set of grid data is sent for each request.

       See also :attr:`pagesize` and :attr:`page`, and
       :attr:`paginate_on_backend`.

    .. attribute:: paginate_on_backend

       Boolean indicating whether the grid data should be paginated on
       the backend.  Default is ``True`` which means only one "page"
       of data is sent to the client-side component.

       If this is ``False``, the full set of grid data is sent for
       each request, and the client-side Vue component will handle the
       pagination.

       Only relevant if :attr:`paginated` is also true.

    .. attribute:: pagesize_options

       List of "page size" options for the grid.  See also
       :attr:`pagesize`.

       Only relevant if :attr:`paginated` is true.  If not specified,
       constructor will call :meth:`get_pagesize_options()` to get the
       value.

    .. attribute:: pagesize

       Number of records to show in a data page.  See also
       :attr:`pagesize_options` and :attr:`page`.

       Only relevant if :attr:`paginated` is true.  If not specified,
       constructor will call :meth:`get_pagesize()` to get the value.

    .. attribute:: page

       The current page number (of data) to display in the grid.  See
       also :attr:`pagesize`.

       Only relevant if :attr:`paginated` is true.  If not specified,
       constructor will assume ``1`` (first page).
    """

    def __init__(
            self,
            request,
            vue_tagname='wutta-grid',
            model_class=None,
            key=None,
            columns=None,
            data=None,
            labels={},
            renderers={},
            actions=[],
            linked_columns=[],
            paginated=False,
            paginate_on_backend=True,
            pagesize_options=None,
            pagesize=None,
            page=1,
    ):
        self.request = request
        self.vue_tagname = vue_tagname
        self.model_class = model_class
        self.key = key
        self.data = data
        self.labels = labels or {}
        self.renderers = renderers or {}
        self.actions = actions or []
        self.linked_columns = linked_columns or []

        self.config = self.request.wutta_config
        self.app = self.config.get_app()

        self.set_columns(columns or self.get_columns())

        self.paginated = paginated
        self.paginate_on_backend = paginate_on_backend
        self.pagesize_options = pagesize_options or self.get_pagesize_options()
        self.pagesize = pagesize or self.get_pagesize()
        self.page = page

    def get_columns(self):
        """
        Returns the official list of column names for the grid, or
        ``None``.

        If :attr:`columns` is set and non-empty, it is returned.

        Or, if :attr:`model_class` is set, the field list is derived
        from that, via :meth:`get_model_columns()`.

        Otherwise ``None`` is returned.
        """
        if hasattr(self, 'columns') and self.columns:
            return self.columns

        columns = self.get_model_columns()
        if columns:
            return columns

        return []

    def get_model_columns(self, model_class=None):
        """
        This method is a shortcut which calls
        :func:`~wuttaweb.util.get_model_fields()`.

        :param model_class: Optional model class for which to return
           fields.  If not set, the grid's :attr:`model_class` is
           assumed.
        """
        return get_model_fields(self.config,
                                model_class=model_class or self.model_class)

    @property
    def vue_component(self):
        """
        String name for the Vue component, e.g. ``'WuttaGrid'``.

        This is a generated value based on :attr:`vue_tagname`.
        """
        words = self.vue_tagname.split('-')
        return ''.join([word.capitalize() for word in words])

    def set_columns(self, columns):
        """
        Explicitly set the list of grid columns.

        This will overwrite :attr:`columns` with a new
        :class:`~wuttaweb.forms.base.FieldList` instance.

        :param columns: List of string column names.
        """
        self.columns = FieldList(columns)

    def append(self, *keys):
        """
        Add some columns(s) to the grid.

        This is a convenience to allow adding multiple columns at
        once::

           grid.append('first_field',
                       'second_field',
                       'third_field')

        It will add each column to :attr:`columns`.
        """
        for key in keys:
            if key not in self.columns:
                self.columns.append(key)

    def remove(self, *keys):
        """
        Remove some column(s) from the grid.

        This is a convenience to allow removal of multiple columns at
        once::

           grid.remove('first_field',
                       'second_field',
                       'third_field')

        It will remove each column from :attr:`columns`.
        """
        for key in keys:
            if key in self.columns:
                self.columns.remove(key)

    def set_label(self, key, label):
        """
        Set/override the label for a column.

        :param key: Name of column.

        :param label: New label for the column header.

        See also :meth:`get_label()`.

        Label overrides are tracked via :attr:`labels`.
        """
        self.labels[key] = label

    def get_label(self, key):
        """
        Returns the label text for a given column.

        If no override is defined, the label is derived from ``key``.

        See also :meth:`set_label()`.
        """
        if key in self.labels:
            return self.labels[key]
        return self.app.make_title(key)

    def set_renderer(self, key, renderer, **kwargs):
        """
        Set/override the value renderer for a column.

        :param key: Name of column.

        :param renderer: Callable as described below.

        Depending on the nature of grid data, sometimes a cell's
        "as-is" value will be undesirable for display purposes.

        The logic in :meth:`get_vue_data()` will first "convert" all
        grid data as necessary so that it is at least JSON-compatible.

        But then it also will invoke a renderer override (if defined)
        to obtain the "final" cell value.

        A renderer must be a callable which accepts 3 args ``(record,
        key, value)``:

        * ``record`` is the "original" record from :attr:`data`
        * ``key`` is the column name
        * ``value`` is the JSON-safe cell value

        Whatever the renderer returns, is then used as final cell
        value.  For instance::

           from webhelpers2.html import HTML

           def render_foo(record, key, value):
              return HTML.literal("<p>this is the final cell value</p>")

           grid = Grid(columns=['foo', 'bar'])
           grid.set_renderer('foo', render_foo)

        Renderer overrides are tracked via :attr:`renderers`.
        """
        if kwargs:
            renderer = functools.partial(renderer, **kwargs)
        self.renderers[key] = renderer

    def set_link(self, key, link=True):
        """
        Explicitly enable or disable auto-link behavior for a given
        column.

        If a column has auto-link enabled, then each of its cell
        contents will automatically be wrapped with a hyperlink.  The
        URL for this will be the same as for the "View"
        :class:`GridAction`
        (aka. :meth:`~wuttaweb.views.master.MasterView.view()`).
        Although of course each cell gets a different link depending
        on which data record it points to.

        It is typical to enable auto-link for fields relating to ID,
        description etc. or some may prefer to auto-link all columns.

        See also :meth:`is_linked()`; the list is tracked via
        :attr:`linked_columns`.

        :param key: Column key as string.

        :param link: Boolean indicating whether column's cell contents
           should be auto-linked.
        """
        if link:
            if key not in self.linked_columns:
                self.linked_columns.append(key)
        else: # unlink
            if self.linked_columns and key in self.linked_columns:
                self.linked_columns.remove(key)

    def is_linked(self, key):
        """
        Returns boolean indicating if auto-link behavior is enabled
        for a given column.

        See also :meth:`set_link()` which describes auto-link behavior.

        :param key: Column key as string.
        """
        if self.linked_columns:
            if key in self.linked_columns:
                return True
        return False

    ##############################
    # paging methods
    ##############################

    def get_pagesize_options(self, default=None):
        """
        Returns a list of default page size options for the grid.

        It will check config but if no setting exists, will fall
        back to::

           [5, 10, 20, 50, 100, 200]

        :param default: Alternate default value to return if none is
           configured.

        This method is intended for use in the constructor.  Code can
        instead access :attr:`pagesize_options` directly.
        """
        options = self.config.get_list('wuttaweb.grids.default_pagesize_options')
        if options:
            options = [int(size) for size in options
                       if size.isdigit()]
            if options:
                return options

        return default or [5, 10, 20, 50, 100, 200]

    def get_pagesize(self, default=None):
        """
        Returns the default page size for the grid.

        It will check config but if no setting exists, will fall back
        to a value from :attr:`pagesize_options` (will return ``20`` if
        that is listed; otherwise the "first" option).

        :param default: Alternate default value to return if none is
           configured.

        This method is intended for use in the constructor.  Code can
        instead access :attr:`pagesize` directly.
        """
        size = self.config.get_int('wuttaweb.grids.default_pagesize')
        if size:
            return size

        if default:
            return default

        if 20 in self.pagesize_options:
            return 20

        return self.pagesize_options[0]

    ##############################
    # configuration methods
    ##############################

    def load_settings(self, store=True):
        """
        Load all effective settings for the grid, from the following
        places:

        * request params
        * user session

        The first value found for a given setting will be applied to
        the grid.

        .. note::

           As of now, "pagination" settings are the only type
           supported by this logic.  Filter/sort coming soon...

        The overall logic for this method is as follows:

        * collect settings
        * apply settings to current grid
        * optionally save settings to user session

        Saving the settings to user session will allow the grid to
        "remember" its current settings when user refreshes the page.

        :param store: Flag indicating whether the collected settings
           should then be saved to the user session.
        """

        # initial default settings
        settings = {}
        if self.paginated and self.paginate_on_backend:
            settings['pagesize'] = self.pagesize
            settings['page'] = self.page

        # grab settings from request and/or user session
        if self.paginated and self.paginate_on_backend:
            self.update_page_settings(settings)

        else:
            # no settings were found in request or user session, so
            # nothing needs to be saved
            store = False

        # maybe store settings in user session, for next time
        if store:
            self.persist_settings(settings)

        # update ourself to reflect settings
        if self.paginated and self.paginate_on_backend:
            self.pagesize = settings['pagesize']
            self.page = settings['page']

    def request_has_settings(self):
        """ """
        for key in ['pagesize', 'page']:
            if key in self.request.GET:
                return True
        return False

    def update_page_settings(self, settings):
        """ """
        # update the settings dict from request and/or user session

        # pagesize
        pagesize = self.request.GET.get('pagesize')
        if pagesize is not None:
            if pagesize.isdigit():
                settings['pagesize'] = int(pagesize)
        else:
            pagesize = self.request.session.get(f'grid.{self.key}.pagesize')
            if pagesize is not None:
                settings['pagesize'] = pagesize

        # page
        page = self.request.GET.get('page')
        if page is not None:
            if page.isdigit():
                settings['page'] = int(page)
        else:
            page = self.request.session.get(f'grid.{self.key}.page')
            if page is not None:
                settings['page'] = int(page)

    def persist_settings(self, settings):
        """ """
        model = self.app.model
        session = Session()

        # func to save a setting value to user session
        def persist(key, value=lambda k: settings.get(k)):
            skey = f'grid.{self.key}.{key}'
            self.request.session[skey] = value(key)

        if self.paginated and self.paginate_on_backend:
            persist('pagesize')
            persist('page')

    ##############################
    # data methods
    ##############################

    def get_visible_data(self):
        """
        Returns the "effective" visible data for the grid.

        This uses :attr:`data` as the starting point but may morph it
        for pagination etc. per the grid settings.

        Code can either access :attr:`data` directly, or call this
        method to get only the data for current view (e.g. assuming
        pagination is used), depending on the need.

        See also these methods which may be called by this one:

        * :meth:`paginate_data()`
        """
        data = self.data or []

        if self.paginated and self.paginate_on_backend:
            self.pager = self.paginate_data(data)
            data = self.pager

        return data

    def paginate_data(self, data):
        """
        Apply pagination to the given data set, based on grid settings.

        This returns a "pager" object which can then be used as a
        "data replacement" in subsequent logic.

        This method is called by :meth:`get_visible_data()`.
        """
        pager = paginate.Page(data,
                              items_per_page=self.pagesize,
                              page=self.page)
        return pager

    ##############################
    # rendering methods
    ##############################

    def render_vue_tag(self, **kwargs):
        """
        Render the Vue component tag for the grid.

        By default this simply returns:

        .. code-block:: html

           <wutta-grid></wutta-grid>

        The actual output will depend on various grid attributes, in
        particular :attr:`vue_tagname`.
        """
        return HTML.tag(self.vue_tagname, **kwargs)

    def render_vue_template(
            self,
            template='/grids/vue_template.mako',
            **context):
        """
        Render the Vue template block for the grid.

        This returns something like:

        .. code-block:: none

           <script type="text/x-template" id="wutta-grid-template">
             <b-table>
               <!-- columns etc. -->
             </b-table>
           </script>

        .. todo::

           Why can't Sphinx render the above code block as 'html' ?

           It acts like it can't handle a ``<script>`` tag at all?

        Actual output will of course depend on grid attributes,
        :attr:`vue_tagname` and :attr:`columns` etc.

        :param template: Path to Mako template which is used to render
           the output.
        """
        context['grid'] = self
        context.setdefault('request', self.request)
        output = render(template, context)
        return HTML.literal(output)

    def get_vue_columns(self):
        """
        Returns a list of Vue-compatible column definitions.

        This uses :attr:`columns` as the basis; each definition
        returned will be a dict in this format::

           {
               'field': 'foo',
               'label': "Foo",
           }

        See also :meth:`get_vue_data()`.
        """
        if not self.columns:
            raise ValueError(f"you must define columns for the grid! key = {self.key}")

        columns = []
        for name in self.columns:
            columns.append({
                'field': name,
                'label': self.get_label(name),
            })
        return columns

    def get_vue_data(self):
        """
        Returns a list of Vue-compatible data records.

        This calls :meth:`get_visible_data()` but then may modify the
        result, e.g. to add URLs for :attr:`actions` etc.

        Importantly, this also ensures each value in the dict is
        JSON-serializable, using
        :func:`~wuttaweb.util.make_json_safe()`.

        :returns: List of data record dicts for use with Vue table
           component.  May be the full set of data, or just the
           current page, per :attr:`paginate_on_backend`.
        """
        original_data = self.get_visible_data()

        # TODO: at some point i thought it was useful to wrangle the
        # columns here, but now i can't seem to figure out why..?

        # # determine which columns are relevant for data set
        # columns = None
        # if not columns:
        #     columns = self.get_columns()
        #     if not columns:
        #         raise ValueError("cannot determine columns for the grid")
        # columns = set(columns)
        # if self.model_class:
        #     mapper = sa.inspect(self.model_class)
        #     for column in mapper.primary_key:
        #         columns.add(column.key)

        # # prune data fields for which no column is defined
        # for i, record in enumerate(original_data):
        #     original_data[i]= dict([(key, record[key])
        #                             for key in columns])

        # we have action(s), so add URL(s) for each record in data
        data = []
        for i, record in enumerate(original_data):
            original_record = record

            record = dict(record)

            # convert data if needed, for json compat
            record = make_json_safe(record,
                                    # TODO: is this a good idea?
                                    warn=False)

            # customize value rendering where applicable
            for key in self.renderers:
                value = record.get(key, None)
                record[key] = self.renderers[key](original_record, key, value)

            # add action urls to each record
            for action in self.actions:
                key = f'_action_url_{action.key}'
                if key not in record:
                    url = action.get_url(original_record, i)
                    if url:
                        record[key] = url

            data.append(record)

        return data

    def get_vue_pager_stats(self):
        """
        Returns a simple dict with current grid pager stats.

        This is used when :attr:`paginate_on_backend` is in effect.
        """
        pager = self.pager
        return {
            'item_count': pager.item_count,
            'items_per_page': pager.items_per_page,
            'page': pager.page,
            'page_count': pager.page_count,
            'first_item': pager.first_item,
            'last_item': pager.last_item,
        }


class GridAction:
    """
    Represents a "row action" hyperlink within a grid context.

    All such actions are displayed as a group, in a dedicated
    **Actions** column in the grid.  So each row in the grid has its
    own set of action links.

    A :class:`Grid` can have one (or zero) or more of these in its
    :attr:`~Grid.actions` list.  You can call
    :meth:`~wuttaweb.views.base.View.make_grid_action()` to add custom
    actions from within a view.

    :param request: Current :term:`request` object.

    .. note::

       Some parameters are not explicitly described above.  However
       their corresponding attributes are described below.

    .. attribute:: key

       String key for the action (e.g. ``'edit'``), unique within the
       grid.

    .. attribute:: label

       Label to be displayed for the action link.  If not set, will be
       generated from :attr:`key` by calling
       :meth:`~wuttjamaican:wuttjamaican.app.AppHandler.make_title()`.

       See also :meth:`render_label()`.

    .. attribute:: url

       URL for the action link, if applicable.  This *can* be a simple
       string, however that will cause every row in the grid to have
       the same URL for this action.

       A better way is to specify a callable which can return a unique
       URL for each record.  The callable should expect ``(obj, i)``
       args, for instance::

          def myurl(obj, i):
              return request.route_url('widgets.view', uuid=obj.uuid)

          action = GridAction(request, 'view', url=myurl)

       See also :meth:`get_url()`.

    .. attribute:: icon

       Name of icon to be shown for the action link.

       See also :meth:`render_icon()`.

    .. attribute:: link_class

       Optional HTML class attribute for the action's ``<a>`` tag.
    """

    def __init__(
            self,
            request,
            key,
            label=None,
            url=None,
            icon=None,
            link_class=None,
    ):
        self.request = request
        self.config = self.request.wutta_config
        self.app = self.config.get_app()
        self.key = key
        self.url = url
        self.label = label or self.app.make_title(key)
        self.icon = icon or key
        self.link_class = link_class or ''

    def render_icon_and_label(self):
        """
        Render the HTML snippet for action link icon and label.

        Default logic returns the output from :meth:`render_icon()`
        and :meth:`render_label()`.
        """
        html = [
            self.render_icon(),
            self.render_label(),
        ]
        return HTML.literal(' ').join(html)

    def render_icon(self):
        """
        Render the HTML snippet for the action link icon.

        This uses :attr:`icon` to identify the named icon to be shown.
        Output is something like (here ``'trash'`` is the icon name):

        .. code-block:: html

           <i class="fas fa-trash"></i>

        See also :meth:`render_icon_and_label()`.
        """
        if self.request.use_oruga:
            return HTML.tag('o-icon', icon=self.icon)

        return HTML.tag('i', class_=f'fas fa-{self.icon}')

    def render_label(self):
        """
        Render the label text for the action link.

        Default behavior is to return :attr:`label` as-is.

        See also :meth:`render_icon_and_label()`.
        """
        return self.label

    def get_url(self, obj, i=None):
        """
        Returns the action link URL for the given object (model
        instance).

        If :attr:`url` is a simple string, it is returned as-is.

        But if :attr:`url` is a callable (which is typically the most
        useful), that will be called with the same ``(obj, i)`` args
        passed along.

        :param obj: Model instance of whatever type the parent grid is
           setup to use.

        :param i: Zero-based sequence for the object, within the
           parent grid.

        See also :attr:`url`.
        """
        if callable(self.url):
            return self.url(obj, i)

        return self.url
