<template>
  <div class="ui segment" id="who-to-follow-segment">
    <h2 class="ui medium dividing header">Who to Follow</h2>
    <div class="ui divided link items">
      <div class="item" v-for="user in usersToFollow" :key="user.id">
        <div class="ui avatar image">
          <img src="https://www.gravatar.com/avatar/default?s=200&r=pg&d=mm">
        </div>
        <br>
        <div class="content" id="user_info">
          <router-link class="ui small header" :to="'/profile/'+user.username">
            {{ user.name }} {{ user.surname }} <br> 
            <p style="color:DodgerBlue;"> {{ `@${user.username}` }} </p>
          </router-link>
        </div>
        <div class="meta">
            <button id="follow_him" class="ui compact button mini primary" @click="followUser(user.username)">Follow</button>
        </div>
      </div>
      <i id="refresh" class="refresh link icon" @click="fetchWhoToFollow"></i>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
name: 'WhoToFollow',
data () {
    return {
    usersToFollow: []
    }
},
created () {
    this.fetchWhoToFollow()
},
methods: {
    fetchWhoToFollow () {
    const token = localStorage.getItem('auth-token');
    const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
    };
    axios
        .get('/social/who-to-follow', config)
        .then(response => {
        this.usersToFollow = response.data.data
        })
    },
    followUser (username) {
    const token = localStorage.getItem('auth-token')
    const payload = {
        following: username,
      };
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
          this.fetchWhoToFollow();
        }
      })
      .catch(error => {
        // eslint-disable-next-line
        console.log(error);
      });
    }, 
}
};
</script>
