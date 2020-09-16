<template>
    <div class="ui stackable grid vertically padded container">
        <div class="eleven wide column" style="margin:0 auto;">
            <div class="ui segment">       
                <b-card title="" header-tag="header" footer-tag="footer" 
                header-bg-variant="dark"
                header-text-variant="white"
                footer-bg-variant="dark"
                footer-text-variant="white">
                <template v-slot:header>
                  <h1 class="mb-0">Topics Selection</h1>
                </template>
                <b-card overlay
                img-src="https://i.picsum.photos/id/9/650/250.jpg"
                img-alt="Card Image"  
                >
                </b-card>
                <template v-slot:footer>
                  <em>In order to complete the registration phase, you have to express your preferences.</em>
                </template>
                </b-card>
                <br><br>
                <h3>Topics Available</h3>
                <br>
                Select the topic(s) you prefer from the list below! Then, click <b>Confirm</b>.
                <br><br>
                <table class="table table-hover justify-content-md-center">
                    <tbody>
                    <tr v-for="(topic, index) in topics" :key="index">
                        <td>
                        <div class="btn-group-center" role="group">
                            <span v-if="topic.clicked">
                            <b-button block 
                                variant="success" 
                                size="lg" 
                                @click="topic.clicked=false; control_topic();">
                                {{ topic.topic }}
                            </b-button>
                            </span>
                            <span v-else>
                            <b-button block 
                                variant="info" 
                                size="lg" 
                                @click="topic.clicked=true; control_topic();">
                                {{ topic.topic }}
                            </b-button>
                            </span>
                        </div>
                        </td>
                    </tr>
                    <br><br>
                    <div class="btn-group-center" role="group">
                        <b-button pill block
                        variant="warning"
                        size="lg"
                        :disabled="control == false"
                        v-b-modal.topic-confirm-modal>
                        Confirm
                        </b-button><br>
                        <b-button pill block
                        variant="danger"
                        size="lg"
                        @click="onReset()">
                        Reset
                        </b-button>
                    </div>
                    </tbody>
                </table>
            
                </div>
                    <b-modal ref="addTopics"
                        id="topic-confirm-modal"
                        title="Saving topics.."
                        hide-footer>
                    <b-form @submit="onSubmit" class="w-100">
                        Topics has been saved! <br>
                        <br><br>
                        <b-button type="submit" variant="primary">Continue</b-button>
                    </b-form>
                    </b-modal>
              </div>
      </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      topics: [],
      control: false,
    };
  },
  methods: {
    getTopics() {
      const token = localStorage.getItem('auth-token');
      localStorage.setItem('inTopic', '1')
      const path = '/topics';
      axios.get(path,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((res) => {
          if (res.data.topic_sel == 0) {
            this.topics = res.data.topics;
          } else {
            this.$router.push('/home');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onReset() {
      this.getTopics();
      this.control = false;
    },
    sendTopics(payload) {
      const token = localStorage.getItem('auth-token');


      const path = '/topics';
      axios.post(path, payload,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then(() => {
          localStorage.setItem('topic', 1);
          this.$router.push('/home');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTopics();
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTopics.hide();
      const topics_clicked = [];
      for (let i = 0; i < this.topics.length; i++) {
        if (this.topics[i].clicked == true) { topics_clicked.push({ topic: this.topics[i].topic, id: this.topics[i].id }); }
      }
      //GUARDA
      const payload = { topics: topics_clicked };
      this.sendTopics(payload);
    },
    control_topic() {
      this.control = false;
      for (let i = 0; i < this.topics.length; i++) {
        if (this.topics[i].clicked == true) { this.control = true; }
      }
    },
  },
  created() {
    this.getTopics();
  },
};
</script>
