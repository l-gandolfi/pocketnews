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
                <div class="col-lg-8 order-lg-2">
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
                    </div> 
                    <div class="tab-content py-4">
                        <div class="tab-pane active" id="profile">
                            <h2 style="color:DodgerBlue;">{{information.username}} </h2>
                            <br>
                            <div class="row">
                                <div class="col-md-6">
                                  <template v-if="information.bio != 'Undefined'">
                                    <template v-if="information.bio != null">
                                      <template v-if="information.publicinfo != null">
                                        <template v-if="information.bio != ''">
                                          <template v-if="information.publicinfo[1] == 1">
                                            <h5>
                                              <i class="pencil alternate icon"></i>
                                              <b>About:</b>
                                            </h5>
                                            <p>
                                                {{information.bio}}
                                            </p>
                                          </template>
                                        </template>
                                      </template>
                                    </template>
                                  </template>
                                  <template v-if="information.city != 'Undefined'">
                                    <template v-if="information.city != null">
                                      <template v-if="information.publicinfo != null">
                                        <template v-if="information.city != ''">
                                          <template v-if="information.publicinfo[0] == 1">
                                            <h5>
                                              <i class="home icon"></i>
                                              <b>Currently living in:</b>
                                            </h5>
                                            <p>
                                                {{information.city}}
                                            </p>
                                          </template>
                                        </template>
                                      </template>
                                    </template>
                                  </template>
                                  
                                </div>
                                <div class="col-md-6">
                                  <template v-if="information.interested != null">
                                    <template v-if="information.publicinfo != null">
                                      <template v-if="information.publicinfo[3] == 1">
                                        <h5>
                                          <i class="heart icon"></i>
                                          <b>Favourite topics:</b>
                                        </h5>
                                        <div v-for ="(topic, index) in information.interested" :key="index">
                                          <a class="ui blue large label" style="margin-bottom:5px;">
                                            {{topic.topic}}
                                            
                                          </a>
                                        </div>
                                      </template>
                                    </template>
                                  </template>
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
      <div class="ui segment">
        <template v-if="information.publicinfo != None">
          <template v-if="information.publicinfo[4] == 1">
            <template v-if="this.information.username === this.user.username">
              <h2> My liked news</h2>
            </template>
            <template v-else>
            <h2> News liked by 
              <h3 style="color:DodgerBlue;"> {{this.information.username}} </h3>
            </h2>
            </template>
              <Feed
                :feed.sync="likes"
                :authUser="user"
              />
            </template>
          <template v-else>
            <h2> The user has chosen to not show liked news</h2>
          </template>
        </template>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import HomeSidebar from '../Utilities/HomeSidebar.vue';
import SearchBar from '../Utilities/SearchBar.vue';
import Feed from '../Home/Feed.vue';

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
        interested: [],
        n_following: '',
        n_followers: '',
        following: [],
        followers: [],
        state: '',
        display_follow: '',
        // news_like: '',
        publicinfo: '',
      },
      user: {},
      likes: [],
    };
  },
  components: {
    homeSidebar: HomeSidebar,
    SearchBar,
    Feed,
  },
  created() {
      this.fetchAuthenticatedUser();
      this.getInformation();
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
        .then((res) => {
          this.user = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getInformation() {
      const path = '/profile';
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          username: this.$route.params.username,
        },
      };

      axios.get(path, config)
        .then((res) => {
          if (res.data.status === 'success') {
            this.information = res.data.information;
            if(this.user.username === this.information.username)
              this.information.publicinfo = '11111'

            const payload = {
              user: this.information.username,
            }
            axios.post('/social/likes', payload, config)
              .then((res) => {
                if (res.data.status === 'success') {
                  this.likes = res.data.data;
                } 
              })
              .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
              });
          } else {
            this.$router.push('/404');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit(evt){
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
      axios
        .post('/social/follow', payload, config)
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