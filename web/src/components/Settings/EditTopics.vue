<template>
  <div class="ui stackable grid vertically padded container">
    <div class="four wide column">
      <homeSidebar :user="user" />
      <modifySidebar :user="user"/>
    </div>
    <div class="eight wide column">
      <div class="ui segment">
        <h2 class="ui dividing header">Topic settings</h2>
        <div>
          <b-card overlay img-src="https://i.picsum.photos/id/3/900/250.jpg" img-alt="Card Image"></b-card>
        </div>
        <hr />
        <h5>In this page you can change or update your favourite topics.</h5>
        <br />
        <alertSucc :message="message" v-if="showSuccess"></alertSucc>
        <alertFail :message="message" v-if="showAlert"></alertFail>
        <table class="table table-hover justify-content-md-center">
          <tbody>
            <tr v-for="(topic, index) in topics" :key="index">
              <td>
                <span v-if="topic.clicked">
                  <button
                    class="ui fluid primary button"
                    v-on:click="topic.clicked=false"
                  >{{ topic.topic }}</button>
                </span>
                <span v-else>
                  <button
                    class="ui fluid info button"
                    v-on:click="topic.clicked=true"
                  >{{ topic.topic }}</button>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <b-button
          type="submit"
          style="margin:10px;"
          v-on:click.prevent="onSubmit"
          variant="info"
        >Submit</b-button>
        <b-button type="reset" style="margin:10px;" v-on:click="onReset" variant="secondary">Reset</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ModifySidebar from "../Utilities/ModifySidebar.vue";
import HomeSidebar from "../Utilities/HomeSidebar.vue";
import AlertSucc from "../Utilities/AlertSucc.vue";
import AlertFail from "../Utilities/AlertFail.vue";

export default {
  data() {
    return {
      user: {},
      topics: [],
      control: false,
      showSuccess: false,
      showAlert: false
    };
  },
  components: {
    homeSidebar: HomeSidebar,
    modifySidebar: ModifySidebar,
    alertSucc: AlertSucc,
    alertFail: AlertFail
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
        .then((response) => {
          this.user = response.data.data;
        });
    },
    getUserTopics() {
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      axios
        .get("/settings/topics", config)
        .then(res => {
          this.topics = res.data.topics;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editUserTopics(payload) {
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      axios
        .post("settings/topics", payload, config)
        .then(res => {
          if (res.data.status === "fail") {
            this.message = `Error while updating information. ${res.data.reason}`;
            this.showAlert = true;
          } else {
            this.message = "Information Updated";
            this.initForm();
            this.showSuccess = true;
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onReset() {
      this.getUserTopics();
    },
    onSubmit(evt) {
      const topics_clicked = [];
      for (let i = 0; i < this.topics.length; i++) {
        if (this.topics[i].clicked == true) {
          topics_clicked.push({
            topic: this.topics[i].topic,
            id: this.topics[i].id
          });
        }
      }
      this.showAlert = false;
      this.showSuccess = false;
      if (topics_clicked.length == 0) {
        evt.preventDefault();
        this.message =
          "Error while updating preferences. You must select at least one topic";
        this.showAlert = true;
        this.initForm();
      } else {
        const payload = { topics: topics_clicked };
        this.editUserTopics(payload);
      }
    },
    initForm() {
      this.fetchAuthenticatedUser();
      this.getUserTopics();
    }
  },
  created() {
    this.fetchAuthenticatedUser();
    this.getUserTopics();
  }
};
</script>