<template>
  <div>
    <div>
      <SearchBar/>
    </div>
    <div class="ui stackable grid vertically padded container">
      <div class="four wide column">
        <HomeSidebar :user="user"/>
        <h4 class="ui horizontal divider header">
            Feed Options
        </h4>
        <FeedFilter />
      </div>
      <div class="eight wide column">
        <div class="ui segment">
          <h2 class="ui medium dividing header">Recommended News</h2>
          <Feed
            :feed.sync="orderFilterFeed"
            :authUser="user"
          />
        </div>
      </div>
      <div class="four wide column">
        <WhoToFollow/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import HomeSidebar from '../Utilities/HomeSidebar.vue';
import Feed from './Feed.vue';
import SearchBar from '../Utilities/SearchBar.vue';
import WhoToFollow from './SuggestFollow.vue';
import FeedFilter from '../Utilities/FeedFilter.vue'

export default {
  name: 'Home',
  components: {
    HomeSidebar,
    Feed,
    SearchBar,
    WhoToFollow,
    FeedFilter
  },
  data() {
    return {
      user: {},
      feed: [],
      order: null,
      filtered: []
    };
  },
  beforeRouteEnter(to, from, next) {
    const token = localStorage.getItem('auth-token');
    return token ? next() : next('/login');
  },
  created() {
    this.fetchAuthenticatedUser();
    this.fetchUserFeed();
    this.$eventBus.$on('FeedOrderAction', this.setOrder);
    this.$eventBus.$on('FeedFilterAction', this.setFilter);
  },
  beforeDestroy() {
    this.$eventBus.$off('FeedOrderAction');
    this.$eventBus.$off('FeedFilterAction');
  },
  computed: {
    orderFilterFeed(){
      let feed = this.feed;
      if (this.filtered.length)
        feed = this.feed.filter(data => this.filtered.includes(data.topic_id))

      switch (this.order) {
        case "date":
          return feed.sort(function(a,b) {
              a = a.date.split('/').reverse().join('');
              b = b.date.split('/').reverse().join('');
              return b.localeCompare(a);
            }
          );
        case "topic":
          return feed.sort((a, b) => { return b.topic_id - a.topic_id;}
          );
        default:
          return feed;
      }
    }
  },
  methods: {
    fetchAuthenticatedUser() {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      axios.get('/account/me', config)
        .then((response) => {
          this.user = response.data.data;
        });
    },
    fetchUserFeed() {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      
      axios.get('/feed', config)
        .then((response) => {
          this.feed = response.data.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });

    },
    setOrder(opt) {
      this.order = opt;
    },
    setFilter(opt) {
      this.filtered = opt;
    },

  }
};
</script>
