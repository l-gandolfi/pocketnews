<template>
    <div class="ui feed">
        <News
            v-for="news in feed"
            :key="news.id"
            :news="news"
            :authUser="authUser"
            />
    </div>
</template>

<script>
import News from './News.vue';

export default {
  name: 'Feed',
  components: {
    News,
  },
  props: {
    feed: {
      type: Array,
      required: true,
    },
    authUser: {
      type: Object,
      required: true,
    },
  }
};
</script>
