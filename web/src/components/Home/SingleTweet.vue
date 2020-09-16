<template>
  <div>
    <div>
      <SearchBar/>
    </div>
    <div class="ui stackable grid vertically padded container">
      <div class="four wide column">
        <HomeSidebar :user="user"/>
      </div>
      <div class="eight wide column" style="margin-top:0px;">
        <div class="ui segment">
          <div class="ui feed">
            <div class="event">
              <div class="label">
                <img src="https://www.gravatar.com/avatar/default?s=200&r=pg&d=mm">
              </div>
              <div class="content">
                <div class="summary">
                  <a style="color:DodgerBlue;"> {{ news.author }} </a>
                  <div class="date">
                    {{news.date}}
                  </div>
                </div>
                <div class="extra text">
                  {{ get_text(news.text) }}
                </div>
                <div>
                  <LikeTab
                    :news="news"
                    :authUser="user"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="ui segment">
          <h2 class="ui medium dividing header">Similar news</h2>
          <Feed
            :feed.sync="feed"
            :authUser="user"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import HomeSidebar from '../Utilities/HomeSidebar.vue';
import Feed from './Feed.vue';
import SearchBar from '../Utilities/SearchBar.vue';
import LikeTab from '../Social/LikeTab.vue';

export default {
  name: 'SingleTweet',
    components: {
      HomeSidebar,
      Feed,
      SearchBar,
      LikeTab,
    },
  data () {
    return {
      news: '',
      user: '',
      feed: [],
    }
  },
  created () {
    this.fetchTweet();
    this.fetchAuthenticatedUser();
    this.get_similar();
  },
  methods: {   
    fetchTweet () {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      var url_id = this.$route.params.id;
      axios.get('/news/'+url_id, config).then(response => {
        this.news = response.data.news
      })
    },
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
    get_text(text) {
      return decodeURIComponent(JSON.parse(text));
    },
    get_similar() {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      var url_id = this.$route.params.id;
      axios.get('/news/recommended/'+url_id, config)
        .then((response) => {
          this.feed = response.data.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
  }
}
</script>
