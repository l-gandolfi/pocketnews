<template>
  <div>
    <div>
      <SearchBar/>
    </div>
    <div class="ui stackable grid vertically padded container">
      <div class="four wide column">
        <HomeSidebar :user="user"/>
      </div>
        <div class="eight wide column">
            <div class="ui segment">
            <h2 class="ui medium dividing header centered page grid">Users Found</h2>
                <template v-if="usernames.length != 0">
                    <div class="ui feed centered page grid">
                        <tr v-for="(username, index) in usernames" :key="index">
                            <pre>
                            </pre>
                            <div class="event">
                                <div class="content">
                                    <div class="summary">
                                        <router-link :to="'/profile/'+username">         
                                          <h3>{{username}}</h3>
                                          <i class="user icon huge" 
                                            style="color:DodgerBlue;"></i>
                                        </router-link>
                                    </div>
                                </div>      
                            </div>
                        </tr>
                    </div>
                </template>
                <template v-if="usernames.length == 0">
                    <h4 class="ui dividing header centered page grid">
                        <pre>
                        </pre>
                        No users found matching your search.
                    </h4>
                </template>
            </div>
        </div>
      </div>
</div>
</template>

<script>
import axios from 'axios';
import HomeSidebar from "./HomeSidebar.vue"
import SearchBar from './SearchBar.vue';
export default {
  props: ['userpath'],
  components: {
    HomeSidebar,
    SearchBar,
  },
  data() {
    return {
      user: {},
      usernames: [],
    };
  },
  methods: {
    fetchAuthenticatedUser() {
      const path = '/account/me';
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      axios.get(path, config)
        .then((res) => {
          this.user = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getUsernames() {  
      axios.get('/search', { params: { username: this.$route.params.username} })
        .then((res) => {
          this.usernames = res.data.usernames;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getUsernames()
    this.fetchAuthenticatedUser()
  },
};
</script>
