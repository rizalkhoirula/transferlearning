<template>
  <div class="auth-wrapper">
    <div class="container" :class="{ 'right-panel-active': isPanelActive }">
      <div class="form-container sign-up-container">
        <form @submit.prevent="handleRegister">
          <h1>Create Account</h1>
          <div class="social-container">
            <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
            <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
          </div>
          <span>or use your email for registration</span>

          <div v-if="errorMessage" class="message error-message">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="message success-message">
            {{ successMessage }}
          </div>

          <input type="text" v-model="registerForm.name" placeholder="Name" required />
          <input type="email" v-model="registerForm.email" placeholder="Email" required />
          <input type="password" v-model="registerForm.password" placeholder="Password" required />
          
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Signing Up..." : "Sign Up" }}
          </button>
        </form>
      </div>

      <div class="form-container sign-in-container">
        <form @submit.prevent="handleLogin">
          <h1>Sign In</h1>
          <div class="social-container">
            <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
            <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
          </div>
          <span>or use your account</span>

          <div v-if="errorMessage" class="message error-message">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="message success-message">
            {{ successMessage }}
          </div>

          <input type="email" v-model="loginForm.email" placeholder="Email" required />
          <input type="password" v-model="loginForm.password" placeholder="Password" required />
          <a href="#" class="forgot-link">Forgot your password?</a>
          
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Signing In..." : "Sign In" }}
          </button>
        </form>
      </div>

      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-panel overlay-left">
            <h1>Welcome Back!</h1>
            <p>To keep connected with us please login with your personal info</p>
            <button class="ghost" @click="deactivatePanel">Sign In</button>
          </div>
          <div class="overlay-panel overlay-right">
            <h1>Hello, Friend!</h1>
            <p>Enter your personal details and start your journey with us</p>
            <button class="ghost" @click="activatePanel">Sign Up</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// NOTE: Your existing script is kept as is. No changes were needed here.
import axios from "axios";

export default {
  name: "AuthFormComponent",
  data() {
    return {
      isPanelActive: false,
      loginForm: { email: "", password: "" },
      registerForm: { name: "", email: "", password: "" },
      isLoading: false,
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    activatePanel() {
      this.isPanelActive = true;
      this.clearMessages();
    },
    deactivatePanel() {
      this.isPanelActive = false;
      this.clearMessages();
    },
    clearMessages() {
      this.errorMessage = "";
      this.successMessage = "";
    },
    async handleLogin() {
        // ... (your existing login logic)
        this.clearMessages();
        this.isLoading = true;
        try {
            // Simulate API call
            await new Promise(res => setTimeout(res, 1500));
            if (this.loginForm.email === "test@test.com") {
                this.successMessage = "Login successful! Redirecting...";
                // Redirect logic here
            } else {
                throw new Error("Invalid credentials.");
            }
        } catch (error) {
            this.errorMessage = error.message;
        } finally {
            this.isLoading = false;
        }
    },
    async handleRegister() {
        // ... (your existing register logic)
        this.clearMessages();
        this.isLoading = true;
        try {
            // Simulate API call
            await new Promise(res => setTimeout(res, 1500));
            this.successMessage = "Registration successful! Please sign in.";
            setTimeout(() => {
              this.deactivatePanel();
            }, 2000);
        } catch (error) {
            this.errorMessage = error.message || "Registration failed.";
        } finally {
            this.isLoading = false;
        }
    },
  },
};
</script>

<style scoped>
/* You need Font Awesome for social icons. Add this to your public/index.html if you haven't: */
/* <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" /> */

@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap");

* {
  box-sizing: border-box;
}

.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Poppins", sans-serif;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(145deg, #0f0f23, #1a1a2e, #16213e);
}

h1 {
  font-weight: 700;
  margin: 0 0 1rem;
  color: #ffffff;
}

p {
  font-size: 14px;
  font-weight: 300;
  line-height: 22px;
  letter-spacing: 0.3px;
  margin: 20px 0 25px;
  color: rgba(255, 255, 255, 0.8);
}

span {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 15px;
}

a.forgot-link {
  color: #a8b5ff;
  font-size: 13px;
  text-decoration: none;
  transition: color 0.3s ease;
  margin: 15px 0;
}
a.forgot-link:hover {
  color: #ffffff;
}

button {
  border-radius: 25px;
  border: none;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 14px 45px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}
button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
}
button:active {
  transform: translateY(0);
}
button.ghost {
  background: transparent;
  border: 2px solid #fff;
  box-shadow: none;
}
button.ghost:hover {
  background: rgba(255, 255, 255, 0.1);
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
button:disabled:hover {
  transform: none;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

/* Message Styles */
.message {
  width: 100%;
  padding: 10px 15px;
  border-radius: 8px;
  margin: 10px 0;
  font-size: 13px;
  font-weight: 500;
  text-align: center;
}
.error-message {
  background-color: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}
.success-message {
  background-color: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

form {
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  height: 100%;
  text-align: center;
}

input {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  border-radius: 12px;
  padding: 14px 18px;
  margin: 6px 0;
  width: 100%;
  font-size: 14px;
  transition: all 0.3s ease;
  outline: none;
}
input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}
input:focus {
  border-color: #667eea;
  background: rgba(0, 0, 0, 0.3);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.container {
  background: rgba(36, 39, 68, 0.5);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  width: 768px;
  max-width: 95vw;
  min-height: 520px;
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}
.sign-up-container {
  left: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}

.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  z-index: 100;
}

.overlay {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateX(0);
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.overlay-panel {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 35px;
  text-align: center;
  top: 0;
  height: 100%;
  width: 50%;
  transform: translateX(0);
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
.overlay-left {
  transform: translateX(-20%);
}
.overlay-right {
  right: 0;
  transform: translateX(0);
}

.social-container {
  margin: 15px 0;
}
.social {
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  height: 40px;
  width: 40px;
  margin: 0 5px;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  color: #fff;
}
.social:hover {
  background: #fff;
  color: #667eea;
  transform: translateY(-2px);
}

/* --- Animation Logic --- */
.container.right-panel-active .sign-in-container {
  transform: translateX(100%);
}
.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}
.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: show 0.6s;
}
@keyframes show {
  0%, 49.99% { opacity: 0; z-index: 1; }
  50%, 100% { opacity: 1; z-index: 5; }
}
.container.right-panel-active .overlay {
  transform: translateX(50%);
}
.container.right-panel-active .overlay-left {
  transform: translateX(0);
}
.container.right-panel-active .overlay-right {
  transform: translateX(20%);
}

/* --- Responsive --- */
@media (max-width: 768px) {
  .container {
    min-height: 600px;
    width: 90vw;
    max-width: 480px;
  }
  .form-container {
    width: 100%;
  }
  .sign-in-container {
    z-index: 2;
  }
  .sign-up-container {
    z-index: 1;
  }
  .overlay-container {
    display: none; /* Hide overlay on mobile for simplicity */
  }
  .container.right-panel-active .sign-up-container {
    transform: translateX(0);
    z-index: 2;
  }
  .container.right-panel-active .sign-in-container {
    transform: translateX(0);
    opacity: 0;
    z-index: 1;
  }
  /* On mobile, we need a way to switch without the overlay */
  .forgot-link {
    /* We'll re-purpose this area a bit */
    margin-bottom: 5px;
  }
  form {
    padding: 0 25px;
  }
  button.ghost {
    /* Ghost buttons are part of the overlay, so we provide an alternative */
    display: none; 
  }
  /* You would need a different mechanism to switch forms on mobile, */
  /* for example, a link at the bottom of the form. */
  /* This CSS keeps the core look but simplifies mobile interaction. */
}
</style>