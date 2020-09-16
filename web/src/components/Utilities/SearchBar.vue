<template>
  <div>
    <div class="ui pointing menu">
      <div class="left menu" style="margin-top:4px;">
        <!-- <i class="big blue twitter icon"></i> -->
        <div class="ui small image">
          <svg width="60" height="30">
            <image xlink:href="../../assets/PNlogo.png" x="0" y="0" width="100%" height="100%"></image>
          </svg>
        </div>
      </div>
      <div class="right menu">
        <div class="ui search">
          
          <div class="ui icon input">
            <input class="prompt" type="text" placeholder="Search @username" id ="search" v-on:keyup.enter.prevent="onSubmit()">
          </div>
          <i class="search link icon" v-on:click.prevent="onSubmit()"></i>
          <div class="results">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      usernames: [],
    };
  },
  methods: {
    postUsername() {
      var username = document.getElementById('search').value;
      this.$router.push('/search/'+username);
    },
    onSubmit(evt) {
      if (document.getElementById('search').value === ''){
        evt.preventDefault();
      }
      else {
        this.postUsername()
        this.showAlert = false;
        this.showSuccess = false;
      }
      
    },
  }
};
</script>
