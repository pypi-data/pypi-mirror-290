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

from pyramid.renderers import render
from webhelpers2.html import HTML

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

    .. attribute:: vue_tagname

       String name for Vue component tag.  By default this is
       ``'wutta-grid'``.  See also :meth:`render_vue_tag()`.
    """

    def __init__(
            self,
            request,
            model_class=None,
            key=None,
            columns=None,
            data=None,
            renderers={},
            actions=[],
            linked_columns=[],
            vue_tagname='wutta-grid',
    ):
        self.request = request
        self.model_class = model_class
        self.key = key
        self.data = data
        self.renderers = renderers or {}
        self.actions = actions or []
        self.linked_columns = linked_columns or []
        self.vue_tagname = vue_tagname

        self.config = self.request.wutta_config
        self.app = self.config.get_app()

        self.set_columns(columns or self.get_columns())

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
                'label': self.app.make_title(name),
            })
        return columns

    def get_vue_data(self):
        """
        Returns a list of Vue-compatible data records.

        This uses :attr:`data` as the basis, but may add some extra
        values to each record, e.g. URLs for :attr:`actions` etc.

        Importantly, this also ensures each value in the dict is
        JSON-serializable, using
        :func:`~wuttaweb.util.make_json_safe()`.

        :returns: List of data record dicts for use with Vue table
           component.
        """
        original_data = self.data or []

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
                value = record[key]
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
