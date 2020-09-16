<template>
  <div class="ui stackable grid vertically padded container">
    <div class="four wide column">
      <homeSidebar :user="user" />
      <modifySidebar :user="user"/>
    </div>
    <div class="eight wide column">
      <div class="ui segment">
        <div>
          <h2 class="ui dividing header">Profile settings</h2>
          <b-card
            overlay
            img-src="https://i.picsum.photos/id/3/900/250.jpg"
            img-alt="Card Image"
            text-variant="white"
          ></b-card>
        </div>
        <hr />
        <h5>In this page you can change or update your public profile information.</h5>
        <h6>Select checkboxes near the information you want to be publicly visible.</h6>
        <br />
        <alertSucc :message="message" v-if="showSuccess"></alertSucc>
        <alertFail :message="message" v-if="showAlert"></alertFail>
        <b-form v-on:submit.prevent="onSubmit" @reset="onReset" class="ui form">
          <b-form-checkbox-group v-model="form.visiblecheck">
            <b-form-group
              id="form-city-group"
              label="Choose your City:"
              label-for="form-city-input"
            >
              <b-form-checkbox value="city">
                <b-form-input 
                  id="form-city-input" 
                  type="text" 
                  :state="this.invalidCity"
                  aria-describedby="city-live-feedback"
                  v-model="form.city"></b-form-input>
                <b-form-invalid-feedback
                id="city-live-feedback"
                >Your city must be at most 30 chracters long</b-form-invalid-feedback>
              </b-form-checkbox>
            </b-form-group>
            <b-form-group id="form-bio-group" label="Edit your Bio:" label-for="form-bio-input">
              <b-form-checkbox value="bio">
                <b-form-textarea
                  id="form-bio-input"
                  type="text"
                  size="lg"
                  rows="6"
                  :state="this.invalidBio"
                  aria-describedby="bio-live-feedback"
                  v-model="form.bio"
                ></b-form-textarea>
                <b-form-invalid-feedback
                id="bio-live-feedback"
                >Your bio must be at most 120 chracters long</b-form-invalid-feedback>
              </b-form-checkbox> 
            </b-form-group>
            <b-form-group
              id="form-dob-group"
              label="Edit your Date of Birth:"
              label-for="form-dob-input"
            >
              <b-form-checkbox value="dob">
                <b-form-input id="form-dob-input" v-model="form.dob" type="date"></b-form-input>
              </b-form-checkbox>
            </b-form-group>
            <b-form-group
              id="form-topics-group"
              label="Show topics you like in your public profile:"
              label-for="form-topics-input"
            >
              <b-form-checkbox value="topics">Show Interested Topics</b-form-checkbox>
            </b-form-group>
            <b-form-group
              id="form-like-group"
              label="Show posts you liked in your public profile:"
              label-for="form-like-input"
            >
              <b-form-checkbox value="liked">Show Latest Posts</b-form-checkbox>
            </b-form-group>
          </b-form-checkbox-group>
          <b-button type="submit" style="margin:10px;" variant="info">Submit</b-button>
          <b-button type="reset" style="margin:10px;" variant="secondary">Reset</b-button>
        </b-form>
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
      information: {
        city: "",
        bio: "",
        dob: "",
        visiblecheck: [],
      },
      form: {
        city: "",
        bio: "",
        dob: "",
        visiblecheck: [],
        publicinfo: "",
      },
      user: {},
      message: "",
      showAlert: false,
      showSuccess: false,
    };
  },
  components: {
    homeSidebar: HomeSidebar,
    modifySidebar: ModifySidebar,
    alertFail: AlertFail,
    alertSucc: AlertSucc,
  },
  computed: {
    invalidBio() {
      let bioCheck= null;
      if (
        this.form.bio.length > 120
      ) {
        bioCheck = false;
      } else {
        bioCheck = true;
      }
      return bioCheck;
    },
    invalidCity() {
      let bioCity= null;
      if (
        this.form.city.length > 30
      ) {
        bioCity = false;
      } else {
        bioCity = true;
      }
      return bioCity;
    }
  },
  methods: {
    fetchAuthenticatedUser() {
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      axios
        .get("/account/me", config)
        .then(res => {
          this.user = res.data.data;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getUserInformation() {
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      axios
        .get("/modifypublicprofile", config)
        .then(res => {
          this.information = res.data.information;
          this.form.visiblecheck = this.information.visiblecheck;
          this.form.bio = this.information.bio;
          this.form.dob = this.information.dob;
          this.form.city = this.information.city;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editUserInformation(payload) {
      const token = localStorage.getItem("auth-token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
      axios
        .post("/modifypublicprofile", payload, config)
        .then(res => {
          if (res.data.status === "fail") {
            this.message = `Error while updating information. ${res.data.reason}`;
            this.showAlert = true;
          } else {
            this.message = "Information Updated";
            this.showSuccess = true;
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    initForm() {
      this.form.visiblecheck = information.visiblecheck;
      this.fetchAuthenticatedUser();
      this.onReset();
    },
    onSubmit(evt) {
      this.showAlert = false;
      this.showSuccess = false;
      if (
        this.invalidBio === false ||
        this.invalidCity === false
      ) {
        evt.preventDefault();
        this.message =
          "Error while updating information. Please check all fields";
        this.showAlert = true;
      }
      else {
        if (this.form.visiblecheck.includes("city")) {
        this.form.publicinfo += "1";
        } else {
          this.form.publicinfo += "0";
        }
        if (this.form.visiblecheck.includes("bio")) {
          this.form.publicinfo += "1";
        } else {
          this.form.publicinfo += "0";
        }
        if (this.form.visiblecheck.includes("dob")) {
          this.form.publicinfo += "1";
        } else {
          this.form.publicinfo += "0";
        }
        if (this.form.visiblecheck.includes("topics")) {
          this.form.publicinfo += "1";
        } else {
          this.form.publicinfo += "0";
        }
        if (this.form.visiblecheck.includes("liked")) {
          this.form.publicinfo += "1";
        } else {
          this.form.publicinfo += "0";
        }
        const payload = {
          city: this.form.city,
          bio: this.form.bio,
          dob: this.form.dob,
          publicinfo: this.form.publicinfo
        };
        this.editUserInformation(payload);
        this.form.publicinfo = "";
        this.initForm();
        } 
    },
    onReset() {
      this.form.city = "";
      this.form.bio = "";
      this.form.dob = "";
      this.form.publicinfo = "";
      this.form.visiblecheck = [];
      this.showAlert = false;
      this.showSuccess = false;
      this.getUserInformation();
    }
  },
  created() {
    this.fetchAuthenticatedUser();
    this.getUserInformation();
  }
};
</script>
