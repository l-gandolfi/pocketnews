<template>
  <div id="app">
    <keep-alive v-bind:include="[ 'SingleTweet' ]">
      <router-view :key="$route.fullPath"></router-view> 
    </keep-alive>
  </div>
</template>

<script>
export default {
  name: 'app',
  watch: {
    $route: {
      handler: (to) => {
        document.title = to.meta.title || 'PocketNews';
      },
      immediate: true,
    },
  },

};
</script>

<style>
@import "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.13/semantic.min.css";
#app {
  margin-top: 0px;
  text-align: center;
}
body {
 background-color: #8DB4B9;
}

</style>
