<template>
  <div>
    <div>
      <SearchBar/>
    </div>
  <div class="ui stackable grid vertically padded container">
    <div class="four wide column">
        <homeSidebar :user="user"/>
    </div> 
    <div class="eleven wide column">
      <div class="ui segment">
        <div class="container">
            <div class="row my-2">
                <div class="col-lg-8 order-lg-2 ">
                    <div class="bottom aligned twelve wide column">
                      <div class="ui horizontal relaxed link list">
                        <div class="item">
                          <div class="content">
                            <router-link class="item" :to="'/profile/' + information.username">
                              <div class="header">Profile <br>
                                <p style="color:grey;">
                                  <strong>{{this.information.username}}</strong>
                                </p>
                              </div>
                            </router-link>
                          </div>
                        </div>
                        <div class="item">
                          <div class="content">
                            <router-link class="item" :to="'/profile/' + information.username+ '/following'">
                              <div class="header" id="following">Following <br>
                                <p style="color:grey;">
                                  <strong>{{this.information.n_followers}}</strong>
                                </p>
                              </div>
                            </router-link>
                          </div>
                        </div>
                        <div class="item">
                          <div class="content">
                            <router-link class="item" :to="'/profile/' + information.username+ '/followers'">
                              <div class="header" id="followers">Followers <br>
                                <p style="color:grey;">
                                  <strong>{{this.information.n_following}}</strong>
                                </p>
                              </div>
                            </router-link>
                          </div>
                        </div>
                    </div>
                    <div class="twelve wide column">
                        <div class="ui segment" id="frame_users">
                            <h4>Following</h4>
                            <template v-if="information.followers.length == 0">
                              <div class="header">This user doesn't follow any other user</div>
                            </template>
                            <div v-for ="(user, index) in information.followers" :key="index">
                                <div class="ui centered card">
                                    <div class="content" id="relation_user">
                                        <div class="header">
                                            <router-link class="item" id="redirect_profile_username" :to="'/profile/' + user.username">
                                                <i class="user icon large"></i>
                                                <div class="header" id="relation_username">{{user.username}}</div>
                                            </router-link>
                                        </div> 
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> 
            </div>
            <div class="col-lg-4 order-lg-1 text-center">
              <img src="https://www.gravatar.com/avatar/default?s=200&r=pg&d=mm" 
                class="mx-auto img-fluid img-circle d-block" alt="avatar">
              <br>
              <h5 class="mt-2">{{information.first_name}} {{information.last_name}}</h5>
              <h6 class="mt-2">{{information.email}}</h6>
              <template v-if="information.dob != 'Undefined'">
                <template v-if="information.dob != null">
                  <template v-if="information.publicinfo != null">
                    <template v-if="information.dob != ''">
                      <template v-if="information.publicinfo[2] == 1">
                        <h5>
                          <i class="calendar icon"></i>
                          <b>Birth Date:</b>
                        </h5>
                        <p>
                          {{information.dob}}
                        </p>
                      </template>
                    </template>
                  </template>
                </template>
              </template>
              <template v-if="information.display_follow == 'True'">
                <b-button
                  type="submit"
                  style="margin:10px;"
                  v-on:click.prevent="onSubmit"
                  variant="info"
                >
                  <i class="icon user"></i>
                  {{this.information.state}}
                </b-button>
              </template>
            </div>
        </div>
    </div>
    </div>
</div>
</div>
</div>
</div>
</template>
<script>
import axios from 'axios';
import HomeSidebar from '../Utilities/HomeSidebar.vue';
import SearchBar from '../Utilities/SearchBar.vue';

export default {
  props: ['userpath'],
  data() {
    return {
      information: {
        name: '',
        surname: '',
        email: '',
        username: '',
        city: '',
        bio: '',
        dob: '',
        n_following: '',
        n_followers: '',
        following: [],
        followers: [],
        interested: [],
        state: '',
        display_follow: '',
        // news_like: '',
        publicinfo: '',
      },
      user: {},
      username: '',
    };
  },
  components: {
    homeSidebar: HomeSidebar,
    SearchBar,
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
    getInformation() {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          username: this.$route.params.username,
        },
      };
      const path = '/profile';
      axios.get(path, config)
        .then((res) => {
          if (res.data.status === 'success') {
            this.information = res.data.information;
          } else {
            this.$router.push('/404');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit(){
      const payload = {
        following: this.information.username,
      };
      this.follow(payload);
    },
    follow(payload){
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
      const path = '/social/follow';
      axios
        .post(path, payload, config)
        .then(res => {
          if (res.data.status === "fail") {
            this.message = `Error while updating information. ${res.data.reason}`;
            this.showAlert = true;
          } else {
            this.message = "Information Updated";
            this.showSuccess = true;
            this.getInformation();
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    initForm() {
      this.fetchAuthenticatedUser();
      this.getInformation();
    }
  },
  created() {
    this.fetchAuthenticatedUser();
    this.getInformation();
  },
};
</script>
