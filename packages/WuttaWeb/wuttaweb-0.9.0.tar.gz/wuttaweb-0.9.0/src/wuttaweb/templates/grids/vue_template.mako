## -*- coding: utf-8; -*-

<script type="text/x-template" id="${grid.vue_tagname}-template">
  <${b}-table :data="data"
              :loading="loading"

              narrowed
              hoverable
              icon-pack="fas"

              ## paging
              % if grid.paginated:
                  paginated
                  pagination-size="is-small"
                  :per-page="perPage"
                  :current-page="currentPage"
                  @page-change="onPageChange"
                  % if grid.paginate_on_backend:
                      backend-pagination
                      :total="pagerStats.item_count"
                  % endif
              % endif
              >

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

    % if grid.paginated:
        <template #footer>
          <div style="display: flex; justify-content: space-between;">
            <div></div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
              <span>
                showing
                {{ renderNumber(pagerStats.first_item) }}
                - {{ renderNumber(pagerStats.last_item) }}
                of {{ renderNumber(pagerStats.item_count) }} results;
              </span>
              <b-select v-model="perPage"
                        % if grid.paginate_on_backend:
                            @input="onPageSizeChange"
                        % endif
                        size="is-small">
                <option v-for="size in pageSizeOptions"
                        :value="size">
                  {{ size }}
                </option>
              </b-select>
              <span>
                per page
              </span>
            </div>
          </div>
        </template>
      % endif

  </${b}-table>
</script>

<script>

  let ${grid.vue_component}CurrentData = ${json.dumps(grid.get_vue_data())|n}

  const ${grid.vue_component}Data = {
      data: ${grid.vue_component}CurrentData,
      loading: false,

      ## paging
      % if grid.paginated:
          pageSizeOptions: ${json.dumps(grid.pagesize_options)|n},
          perPage: ${json.dumps(grid.pagesize)|n},
          currentPage: ${json.dumps(grid.page)|n},
          % if grid.paginate_on_backend:
              pagerStats: ${json.dumps(grid.get_vue_pager_stats())|n},
          % endif
      % endif
  }

  const ${grid.vue_component} = {
      template: '#${grid.vue_tagname}-template',
      computed: {

          % if not grid.paginate_on_backend:

              pagerStats() {
                  let last = this.currentPage * this.perPage
                  let first = last - this.perPage + 1
                  if (last > this.data.length) {
                      last = this.data.length
                  }
                  return {
                      'item_count': this.data.length,
                      'items_per_page': this.perPage,
                      'page': this.currentPage,
                      'first_item': first,
                      'last_item': last,
                  }
              },

          % endif
      },
      methods: {

          renderNumber(value) {
              if (value != undefined) {
                  return value.toLocaleString('en')
              }
          },

          getBasicParams() {
              return {
                  % if grid.paginated and grid.paginate_on_backend:
                      pagesize: this.perPage,
                      page: this.currentPage,
                  % endif
              }
          },

          async fetchData(params, success, failure) {

              if (params === undefined || params === null) {
                  params = new URLSearchParams(this.getBasicParams())
              } else {
                  params = new URLSearchParams(params)
              }
              if (!params.has('partial')) {
                  params.append('partial', true)
              }
              params = params.toString()

              this.loading = true
              this.$http.get(`${request.path_url}?${'$'}{params}`).then(response => {
                  console.log(response)
                  console.log(response.data)
                  if (!response.data.error) {
                      ${grid.vue_component}CurrentData = response.data.data
                      this.data = ${grid.vue_component}CurrentData
                      % if grid.paginated and grid.paginate_on_backend:
                          this.pagerStats = response.data.pager_stats
                      % endif
                      this.loading = false
                      if (success) {
                          success()
                      }
                  } else {
                      this.$buefy.toast.open({
                          message: data.error,
                          type: 'is-danger',
                          duration: 2000, // 4 seconds
                      })
                      this.loading = false
                      if (failure) {
                          failure()
                      }
                  }
              })
              .catch((error) => {
                  this.data = []
                  % if grid.paginated and grid.paginate_on_backend:
                      this.pagerStats = {}
                  % endif
                  this.loading = false
                  if (failure) {
                      failure()
                  }
                  throw error
              })
          },

          % if grid.paginated:

              % if grid.paginate_on_backend:
                  onPageSizeChange(size) {
                      this.fetchData()
                  },
              % endif

              onPageChange(page) {
                  this.currentPage = page
                  % if grid.paginate_on_backend:
                      this.fetchData()
                  % endif
              },

          % endif
      },
  }

</script>
