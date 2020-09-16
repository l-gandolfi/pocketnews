<template>
  <div class="event">

    <div class="label">
      <i class="newspaper icon large"></i>
    </div>
    <div class="content">
      
      <div class="summary">
        <a class="left" style="color:DodgerBlue;"> {{ news.author }} </a>
        <div class="date">
          {{news.date}}
        </div>
      </div>
      
      <router-link :to="'/news/' + news.id">
        <div class="extra text">
          <!-- {{news.text}} -->
          {{get_text(news.text)}}
        </div>
      </router-link>
      <div>
        <LikeTab
          :news="news"
          :authUser="authUser"
        />
      </div>
    </div>

    <div class="label" v-if="news.topic">
      <a class="ui right ribbon label small ">{{news.topic}}</a>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import LikeTab from '../Social/LikeTab.vue';

export default {
  name: 'News',
  components: {
    LikeTab,
  },
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
  methods: {
    get_text(text) {
      return decodeURIComponent(JSON.parse(text));
    } 
  }
};
</script>
