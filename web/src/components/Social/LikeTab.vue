<template>
    <div class="meta">
    <a class="like" v-if="isFavoritedByUser" v-on:click="unFavoriteTweet">
        <i class="like red icon"></i> {{ favorites.length }}
    </a>
    <a class="like" v-else v-on:click="favoriteTweet">
        <i class="like icon"></i> {{ favorites.length }}
    </a>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LikeTab',
  props: {
    news: {
      type: Object,
      required: true,
    },
    authUser: {
      type: Object,
      required: true,
    } 
  },
  data() {
    return {
      favorites: [],
    };
  },
  created () {
    this.getFavorite();
  },
  computed: {
    isFavoritedByUser () {
      for (const user_id of this.favorites) {
        if (user_id === this.authUser.id) {
          return true
        }
      }
      return false
    }
  },
  methods: {
    getFavorite() {
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      const payload = {
        news_id: this.news.id,
      }
      axios
        .post("/social/favorite", payload, config)
        .then(res => {
          this.favorites = res.data.users
        })
        .catch(error => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    unFavoriteTweet () {
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      const payload = {
        news_id: this.news.id,
      }
      axios
        .post("/social/dislike", payload, config)
        .then(res => {
          this.response = res.data.status
          this.getFavorite()
        })
        .catch(error => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    favoriteTweet () {  
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      const payload = {
        news_id: this.news.id,
      }
      axios
        .post("/social/like", payload, config)
        .then(res => {
          this.response = res.data.status
          this.getFavorite()
        })
        .catch(error => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
  },
};
</script>
