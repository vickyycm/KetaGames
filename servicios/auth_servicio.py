import pyrebase

const firebaseConfig = {
    apiKey: "AIzaSyBB38NzFrv5jScFiQHc9flcv2e3NrP_YRw",
    authDomain: "ketagames-7402d.firebaseapp.com",
    projectId: "ketagames-7402d",
    storageBucket: "ketagames-7402d.firebasestorage.app",
    messagingSenderId: "1033685707707",
    appId: "1:1033685707707:web:8cb0f5dcf9e06b020af29e",
    measurementId: "G-NXEWF4CF1P"
  };

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

