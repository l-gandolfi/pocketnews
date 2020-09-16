<template>
<div class="ui small orderfilter">
  <b-button id="btn-reorder" size="sm" v-b-toggle.collapse-1 class="m-1" block variant="outline-light">Feed Order</b-button>

  <b-collapse id="collapse-1" >
    <b-form-select size="sm" v-model="order" :options="orderOptions" @change="orderChange" :select-size="2"></b-form-select>
  </b-collapse>

  <b-button id="btn-filter" size="sm" v-b-toggle.collapse-2 class="m-1" block variant="outline-light">Feed Filter</b-button>
  <b-collapse id="collapse-2">
    <b-form-select size="sm" v-model="filter" :options="filterOptions" @change="filterChange" multiple :select-size="11"></b-form-select>
  </b-collapse>
  <b-button id="btn-reset" size="sm" class="m-1" block variant="outline-light" @click="resetOptions">Reset Options</b-button>
</div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "FeedFilter",
    data() {
      return {
        order: null,
        orderOptions: [
          { value: 'date', text: 'by Date' },
          { value: 'topic', text: 'by Topic' },
        ],
        filter: [],
        filterOptions: []
      }
    },
    created() {
      this.fetchTopics()
    },
    methods: {
      orderChange() {
        this.$eventBus.$emit('FeedOrderAction', this.order);
      },
      filterChange() {
        this.$eventBus.$emit('FeedFilterAction', this.filter);
      },
      resetOptions() {
        this.order = null;
        this.filter = []
        
        this.$eventBus.$emit('FeedFilterAction', this.filter);
        this.$eventBus.$emit('FeedOrderAction', this.order);
      },
      fetchTopics() {
        const token = localStorage.getItem('auth-token');
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
         };
        axios.get('/topics', config)
          .then((response) => {
            response.data.topics.forEach(element => this.filterOptions.push({value: element.id, text: element.topic}));
            
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
        },
    }
  }
</script>
<style scoped>
.orderfilter {
  margin-top: 1em;
}

.collapse{
  padding-left: 5px;
}
</style>
