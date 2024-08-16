## -*- coding: utf-8; -*-

<script type="text/x-template" id="${grid.vue_tagname}-template">
  <${b}-table :data="data"
              hoverable
              :loading="loading">

    % for column in grid.get_vue_columns():
        <${b}-table-column field="${column['field']}"
                           label="${column['label']}"
                           v-slot="props"
                           cell-class="c_${column['field']}">
          % if grid.is_linked(column['field']):
              <a :href="props.row._action_url_view"
                 v-html="props.row.${column['field']}" />
          % else:
              <span v-html="props.row.${column['field']}"></span>
          % endif
        </${b}-table-column>
    % endfor

    % if grid.actions:
        <${b}-table-column field="actions"
                           label="Actions"
                           v-slot="props">
          % for action in grid.actions:
              <a v-if="props.row._action_url_${action.key}"
                 :href="props.row._action_url_${action.key}"
                 class="${action.link_class}">
                ${action.render_icon_and_label()}
              </a>
              &nbsp;
          % endfor
        </${b}-table-column>
    % endif

  </${b}-table>
</script>

<script>

  let ${grid.vue_component} = {
      template: '#${grid.vue_tagname}-template',
      methods: {},
  }

  let ${grid.vue_component}CurrentData = ${json.dumps(grid.get_vue_data())|n}

  let ${grid.vue_component}Data = {
      data: ${grid.vue_component}CurrentData,
      loading: false,
  }

</script>
