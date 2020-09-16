<template>
    <div>
        <div class="ui attached segment">
            <h3>PocketNews</h3>
        </div>
        <div class="ui fluid four item menu">
            <router-link class="item" to="/home" id="home_button">
                <i class="home icon"></i>
            </router-link>
            <router-link class="item" :to="'/profile/' + user.username" id="profile_button">
                <i class="user icon"></i>
            </router-link>
            <router-link class="item" to="/settings/account" id="settings_button">
                <i class="setting icon"></i>
            </router-link>
            <a class="item" @click="logout" id="logout_button">
              <i class="sign out icon"></i>
            </a>
        </div>
    </div>
</template>

<script>


export default {
  name: 'HomeSidebar',
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      news: '',
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('auth-token');
      this.$router.push('/login');
    },
  },
};
</script>
