<template>
  <div class="ui stackable grid vertically padded container">
    <div class="four wide column">
        <homeSidebar :user="information"/>
        <modifySidebar/>
    </div> 
    <div class="eight wide column">
      <div class="ui segment">
        <h2 class="ui dividing header">Account settings</h2>
              <div>
                  <b-card
                  overlay
                  img-src="https://i.picsum.photos/id/3/900/250.jpg"
                  img-alt="Card Image"                  >
                  </b-card>
              </div>
            <hr>
            <h5>In this page you can change or update your basic information.</h5>
            <br>
            <alertSucc :message=message v-if="showSuccess"></alertSucc>
            <alertFail :message=message v-if="showAlert"></alertFail>
            <b-form v-on:submit.prevent="onSubmit" @reset="onReset" class="ui form">
              <b-form-group
                id="form-firstname-group"
                label="Edit your First Name:"
                label-for="form-firstname-input"
              >
                <b-form-input
                  id="form-firstname-input"
                  type="text"
                  v-model="form.name"
                  :state="this.invalidName"
                  aria-describedby="name-live-feedback"
                  v-bind:placeholder="information.name"
                ></b-form-input>
                <b-form-invalid-feedback
                  id="name-live-feedback"
                >Please insert a valid Name at most 20 characters long.</b-form-invalid-feedback>
              </b-form-group>
              <b-form-group
                id="form-lastname-group"
                label="Edit your Last Name:"
                label-for="form-lastname-input"
              >
                <b-form-input
                  id="form-lastname-input"
                  type="text"
                  v-model="form.surname"
                  :state="this.invalidSurname"
                  aria-describedby="surname-live-feedback"
                  v-bind:placeholder="information.surname"
                ></b-form-input>
                <b-form-invalid-feedback
                  id="surname-live-feedback"
                >Please insert a valid Surname at most 20 characters long.</b-form-invalid-feedback>
              </b-form-group>
              <b-form-group
                id="form-username-group"
                label="Edit your Usernname:"
                label-for="form-username-input"
              >
                <b-form-input
                  id="form-username-input"
                  type="text"
                  v-model="form.username"
                  :state="this.invalidUsername"
                  aria-describedby="username-live-feedback"
                  v-bind:placeholder="information.username"
                ></b-form-input>
                <b-form-invalid-feedback
                  id="username-live-feedback"
                >Please insert Username al least 5 characters and at most 20 characters long.</b-form-invalid-feedback>
              </b-form-group>
              <b-form-group id="form-email-group" label="Edit your Email:" label-for="form-email-input">
                <b-form-input
                  id="form-email-input"
                  type="text"
                  v-model="form.email"
                  :state="this.invalidEmail"
                  aria-describedby="email-live-feedback"
                  v-bind:placeholder="information.email"
                ></b-form-input>
                <b-form-invalid-feedback id="email-feedback">Please check your email. It should be
                  at most 120 charaters long and respect this format "example@mail.com".
                </b-form-invalid-feedback>
              </b-form-group>
              <b-form-group
                id="form-confirmemail-group"
                label="Confirm your Email:"
                label-for="form-confirmemail-input"
              >
                <b-form-input
                  id="form-confirmemail-input"
                  type="text"
                  v-model="form.confirmemail"
                  :state="this.invalidConfirmationEmail"
                  aria-describedby="confirmemail-live-feedback"
                  v-bind:placeholder="information.email"
                ></b-form-input>
                <b-form-invalid-feedback
                  id="confirmemail-live-feedback"
                >Please check both Email and Email confirmation fields.</b-form-invalid-feedback>
              </b-form-group>
              <b-form-group
                id="form-password-group"
                label="Edit your Password:"
                label-for="form-password-input"
              >
                <b-form-input
                  id="form-password-input"
                  type="password"
                  v-model="form.password"
                  :state="this.invalidPassword"
                  aria-describedby="password-live-feedback"
                  placeholder="Your password"
                ></b-form-input>
                <b-form-invalid-feedback
                  id="password-live-feedback"
                >Please insert a Password at least 6 characters long. (less than 60 characters)</b-form-invalid-feedback>
              </b-form-group>
              <b-form-group
                id="form-confirmpassword-group"
                label="Confirm your Password:"
                label-for="form-confirmpassword-input"
              >
                <b-form-input
                  id="form-confirmpassword-input"
                  type="password"
                  v-model="form.confirmpassword"
                  :state="this.invalidConfirmationPassword"
                  aria-describedby="confirmpassword-live-feedback"
                  placeholder="Your password"
                ></b-form-input>
                <b-form-invalid-feedback
                  id="confirmpassword-live-feedback"
                >Please check both Password and Password confirmation fields.</b-form-invalid-feedback>
              </b-form-group>
              <br>
              <b-button variant="outline-danger" v-b-modal.delete-confirm-modal>Delete Account</b-button>
              <br><br>
              <b-button type="submit" style="margin:10px;" variant="info">Submit</b-button>
              <b-button type="reset"  style="margin:10px;" variant="secondary">Reset</b-button>
            </b-form>
            </div>
        </div>
        <b-modal ref="deleteAccount"
                    id="delete-confirm-modal"
                    title="Deleting is irreversible.."
                    hide-footer>       
              <b-form @submit="deleteHim" @reset="doNotDeleteHim" class="w-200">
                Are you sure you want to delete your account? 
                <br><br><br>
                <b-button-group>
                  <b-button type="submit" variant="danger">I'm sure</b-button>
                  <b-button type="reset" style="margin-left:10px;" variant="secondary">I've changed my mind</b-button>
                </b-button-group>
              </b-form>
            </b-modal>
    </div>
</template>

<script>
import axios from 'axios';
import ModifySidebar from '../Utilities/ModifySidebar.vue';
import HomeSidebar from '../Utilities/HomeSidebar.vue';
import AlertSucc from '../Utilities/AlertSucc.vue';
import AlertFail from '../Utilities/AlertFail.vue';

axios.defaults.baseURL = 'http://localhost:8000';

export default {
  data() {
    return {
      user: {},
      information: {
        name: '',
        surname: '',
        email: '',
        username: '',
        password: '',
      },
      form: {
        name: '',
        surname: '',
        username: '',
        email: '',
        confirmemail: '',
        password: '',
        confirmpassword: '',
      },
      message: '',
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
    invalidName() {
      let nameCheck = null;
      if (this.form.name === "") {
        nameCheck = null;
      } else if (this.form.name.length <= 20) {
        nameCheck = true;
      } else if (this.form.name.length > 20) {
        nameCheck = false;
      }
      return nameCheck;
    },
    invalidSurname() {
      let surnameCheck = null;
      if (this.form.surname === "") {
        surnameCheck = null;
      } else if (this.form.surname.length <= 20) {
        surnameCheck = true;
      } else if (this.form.surname.length > 20) {
        surnameCheck = false;
      }
      return surnameCheck;
    },
    invalidUsername() {
      let usernameCheck = null;
      if (this.form.username === "") {
        usernameCheck = null;
      } else if (this.form.username.length >= 5 && this.form.username.length <= 20) {
        usernameCheck = true;
      } else if (this.form.username.length < 5 || this.form.username.length > 20) {
        usernameCheck = false;
      }
      return usernameCheck;
    },
    invalidPassword() {
      let passwordCheck = null;
      if (this.form.password === "") {
        passwordCheck = null;
      } else if (this.form.password.length >= 6 && this.form.username.length <= 60) {
        passwordCheck = true;
      } else if (this.form.password.length < 6 || this.form.password.length > 60) {
        passwordCheck = false;
      }
      return passwordCheck;
    },
    invalidConfirmationPassword() {
      let passwordConfCheck = null;
      if (
        this.form.password.length !== this.form.confirmpassword.length ||
        this.invalidPassword === false
      ) {
        passwordConfCheck = false;
      } else if (
        this.form.password.length === this.form.confirmpassword.length &&
        this.invalidPassword !== null &&
        this.invalidPassword !== false
      ) {
        passwordConfCheck = true;
      }
      return passwordConfCheck;
    },
    invalidEmail() {
      const re = new RegExp("[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$");
      let emailCheck = null;
      if (this.form.email !== "") {
        if (!re.test(this.form.email)) {
          emailCheck = false;
        } else if (re.test(this.form.email)) {
          emailCheck = true;
        }
      }
      return emailCheck;
    },
    invalidConfirmationEmail() {
      let emailConfCheck = null;
      if (
        this.form.email.length !== this.form.confirmemail.length ||
        this.invalidEmail === false
      ) {
        emailConfCheck = false;
      } else if (
        this.form.email.length === this.form.confirmemail.length &&
        this.invalidEmail !== null &&
        this.invalidEmail !== false
      ) {
        emailConfCheck = true;
      }
      return emailConfCheck;
    }
  },
  methods: {
    getUserInformation() {
      const path = '/account/me';
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      axios.get(path, config)
        .then((res) => {
          this.information = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editUserInformation(payload) {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      const path = '/editaccount';
      axios.post(path, payload, config)
        .then((res) => {
          if (res.data.status === 'fail') {
            this.message = `Error while updating information. ${res.data.reason}`;
            this.showAlert = true;
          } else {
            this.message = 'Information Updated';
            this.initForm();
            this.showSuccess = true;
          }
        })
        .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
        });
    },
    initForm() {
      this.onReset();
      this.getUserInformation();
    },
    onSubmit(evt) {
      if (this.invalidPassword === false || this.invalidConfirmationPassword === false
      || this.invalidEmail === false || this.invalidConfirmationEmail === false || this.invalidUsername === false) {
        evt.preventDefault();
        this.message = 'Error while updating information. Please check all fields';
        this.showAlert = true;
      } else {
        const payload = {
          name: this.form.name,
          surname: this.form.surname,
          username: this.form.username,
          email: this.form.email,
          confirmemail: this.form.confirmemail,
          password: this.form.password,
          confirmpassword: this.form.confirmpassword,
        };
        this.editUserInformation(payload);
      }
    },
    onReset() {
      this.form.name = '';
      this.form.surname = '';
      this.form.username = '';
      this.form.email = '';
      this.form.confirmemail = '';
      this.form.password = '';
      this.form.confirmpassword = '';
      this.showAlert = false;
      this.showSuccess = false;
    },
    deleteHim(evt) {
      evt.preventDefault();
      this.$refs.deleteAccount.hide();

      const path = '/settings/delete';
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      
      axios.get(path, config)
        .then((res) => {
          localStorage.removeItem('auth-token');
          this.$router.push('/login');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    doNotDeleteHim(evt) {
      evt.preventDefault();
      this.$refs.deleteAccount.hide();
      console.log('Modal hidden');
      this.initForm();
      //this.getUserInformation();
    },
  },
  created() {
    this.getUserInformation();
  },
};
</script>