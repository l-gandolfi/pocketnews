import Vue from 'vue';
import VueRouter from 'vue-router';
import Topics from '../components/Access/Topics.vue';
import WaitConfirm from '../components/Access/WaitConfirm.vue';
import PasswordResetRequest from '../components/Access/PasswordResetRequest.vue';
import ChangePassword from '../components/Access/ChangePassword.vue';
import EmailCheck from '../components/Access/EmailCheck.vue';
import Login from '../components/Access/Login.vue';
import Registration from '../components/Access/Registration.vue';
import Users_Admin from '../components/Admin/Users_Admin.vue';
import Home from '../components/Home/Home.vue';
import SingleTweet from '../components/Home/SingleTweet.vue';
import EditAccount from '../components/Settings/EditAccount.vue';
import EditTopics from '../components/Settings/EditTopics.vue';
import ModifyPublicProfile from '../components/Settings/ModifyPublicProfile.vue';
import Profile from '../components/Social/Profile.vue';
import NotFound from '../components/Utilities/NotFound.vue';
import Following from '../components/Social/Following.vue';
import Followers from '../components/Social/Followers';
import Search from '../components/Utilities/Search.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    alias: '/home',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Home',
      requiresAuth: true,
    },
  },
  {
    path: '/topics',
    name: 'Topic',
    component: Topics,
    meta: {
      title: 'Topics',
      requiresAuth: true,
    },
  },
  {
    path: '/registration',
    name: 'Registration',
    component: Registration,
    meta: {
      title: 'Registration',
      requiresAuth: false,
    },
  },
  {
    path: '/settings/account',
    name: 'EditAccount',
    component: EditAccount,
    meta: {
      title: 'Settings',
      requiresAuth: true,
    },
  },
  {
    path: '/admin/users',
    name: 'Users Admin',
    component: Users_Admin,
    meta: {
      title: 'Users List',
      requiresAuth: true,
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Login',
      requiresAuth: false,
    },
  },
  {
    path: '/profile/:username',
    name: 'Profile',
    component: Profile,
    props: true,
    meta: {
      title: 'Profile',
      requiresAuth: true,
    },
  },
  {
    path: '/settings/profile',
    name: 'ModifyPublicProfile',
    component: ModifyPublicProfile,
    meta: {
      title: 'Edit profile',
      requiresAuth: true,
    },
  },
  {
    path: '/settings/topics',
    name: 'EditTopics',
    component: EditTopics,
    meta: {
      title: 'Edit topics',
      requiresAuth: true,
    },
  },
  {
    path: '*',
    name: '404',
    component: NotFound,
  },
  {
    path: '/waitConfirm/:user_id',
    name: 'WaitConfirm',
    component: WaitConfirm,
  },
  {
    path: '/passwordResetRequest',
    name: 'passwordResetRequest',
    component: PasswordResetRequest,
  },
  {
    path: '/changePassword/:user_id',
    name: 'changePassword',
    component: ChangePassword,
  },
  {
    path: '/emailCheck/:user_id',
    name: 'emailCheck',
    component: EmailCheck,
  },
  {
    path: '/search/:username',
    name: 'Search',
    component: Search,
  },
  {
    path: '/news/:id',
    component: SingleTweet,
    props: true
  },
  {
    path: '/profile/:username/followers',
    name: 'Followers',
    component: Followers,
    props: true,
    meta: {
      title: 'Followers',
      requiresAuth: true,
    },
  },
  {
    path: '/profile/:username/following',
    name: 'Following',
    component: Following,
    props: true,
    meta: {
      title: 'Following',
      requiresAuth: true,
    },
  }

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth-token');
  const topic = localStorage.getItem('topic');

  if (to.path == '/topics') {
    localStorage.setItem('inTopic', 1);
  }
  else {
    localStorage.setItem('inTopic', 0);
  }

  const inTopic = localStorage.getItem('inTopic');

  if (to.matched.some((record) => record.meta.requiresAuth) && !token) {
    next('/login');
  } else if (token && topic == '0' && inTopic == '0') {
    next('/topics')
  } else {
    next()
  }
});

export default router;
