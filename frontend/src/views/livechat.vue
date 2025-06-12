<template>
  <div class="chat-container">
    <div class="main-content">
      <div class="header-section">
        <div class="header-content">
          <div class="header-icon">
            <i class="bi bi-chat-dots-fill"></i>
          </div>
          <div class="header-text">
            <h1 class="header-title">AI Chat Assistant</h1>
            <p class="header-subtitle">
              Your intelligent companion for all your queries.
            </p>
          </div>
        </div>
      </div>

      <div class="chat-area">
        <div class="chat-messages" ref="chatMessages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="[
              'message',
              message.sender === 'user' ? 'user-message' : 'ai-message',
            ]"
          >
            <div
              :class="[
                'message-avatar',
                message.sender === 'user' ? 'user-avatar' : 'ai-avatar',
              ]"
            >
              <i
                :class="[
                  message.sender === 'user'
                    ? 'bi bi-person-fill'
                    : 'bi bi-robot',
                ]"
              ></i>
            </div>
            <div
              :class="[
                'message-bubble',
                message.sender === 'user' ? 'user-bubble' : 'ai-bubble',
              ]"
            >
              <p v-html="formatMessage(message.text)"></p>
            </div>
          </div>
          <div v-if="isLoading" class="message ai-message loading-message">
            <div class="message-avatar ai-avatar">
              <i class="bi bi-robot"></i>
            </div>
            <div class="message-bubble ai-bubble">
              <span class="loading-dots"
                ><span>.</span><span>.</span><span>.</span></span
              >
            </div>
          </div>
        </div>

        <div class="chat-input-area">
          <textarea
            v-model="newMessage"
            @keydown.enter.prevent="sendMessage"
            :disabled="isLoading"
            placeholder="Ketik pesan Anda..."
            rows="1"
            class="chat-input"
          ></textarea>
          <button
            @click="sendMessage"
            :disabled="isLoading || newMessage.trim() === ''"
            class="send-button"
          >
            <i class="bi bi-send-fill"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChatComponent",
  data() {
    return {
      newMessage: "",
      messages: [],
      geminiApiKey: import.meta.env.VITE_GEMINI_API_KEY,
      geminiApiUrl: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent`,
      isLoading: false,
    };
  },
  methods: {
    formatMessage(text) {
      return text.replace(/\n/g, "<br>");
    },

    async sendMessage() {
      if (this.newMessage.trim() === "" || this.isLoading) return;

      const userMessage = this.newMessage.trim();
      this.messages.push({
        text: userMessage,
        sender: "user",
      });

      this.newMessage = "";
      this.isLoading = true;
      this.$nextTick(() => {
        this.scrollToBottom();
      });

      try {
        if (!this.geminiApiKey) {
          console.error(
            "GEMINI_API_KEY is not defined in environment variables."
          );
          this.messages.push({
            text: "Error: API key not found, please check your configuration.",
            sender: "ai",
          });
          this.isLoading = false;
          this.$nextTick(() => this.scrollToBottom());
          return;
        }
        const chatHistory = this.messages.map((msg) => ({
          role: msg.sender === "user" ? "user" : "model",
          parts: [{ text: msg.text }],
        }));
        if (
          this.messages.length > 0 &&
          this.messages[this.messages.length - 1].sender === "ai" &&
          this.messages[this.messages.length - 1].text.includes("...")
        ) {
          chatHistory.pop();
        }

        const requestBody = {
          contents: chatHistory,
          generationConfig: {
            maxOutputTokens: 800,
            temperature: 0.7,
            topP: 1,
            topK: 1,
          },
        };

        const response = await axios.post(this.geminiApiUrl, requestBody, {
          headers: {
            "Content-Type": "application/json",
          },
          params: {
            key: this.geminiApiKey,
          },
        });

        let geminiResponseText = "No response from AI.";
        if (
          response.data &&
          response.data.candidates &&
          response.data.candidates.length > 0
        ) {
          const firstCandidate = response.data.candidates[0];
          if (
            firstCandidate.content &&
            firstCandidate.content.parts &&
            firstCandidate.content.parts.length > 0
          ) {
            geminiResponseText = firstCandidate.content.parts[0].text;
          } else if (firstCandidate.finishReason) {
            if (firstCandidate.finishReason === "SAFETY") {
              geminiResponseText =
                "Sorry, this response violates our safety policy. Please try another question.";
            } else if (firstCandidate.finishReason === "STOP") {
              geminiResponseText =
                "AI finished, but did not generate text. Please try another question.";
            } else if (firstCandidate.finishReason === "RECITATION") {
              geminiResponseText =
                "Sorry, I cannot answer this question because it may relate to misinformation.";
            } else {
              geminiResponseText = `AI finished with reason: ${firstCandidate.finishReason}.`;
            }
          }
        } else if (
          response.data &&
          response.data.promptFeedback &&
          response.data.promptFeedback.blockReason
        ) {
          geminiResponseText = `Sorry, your question was blocked for security reasons: ${response.data.promptFeedback.blockReason}.`;
        }

        this.messages.push({
          text: geminiResponseText,
          sender: "ai",
        });
      } catch (error) {
        console.error("Error sending message to Gemini:", error);
        let errorMessage =
          "Sorry, an error occurred while trying to get a response from AI. Please try again.";

        if (axios.isAxiosError(error)) {
          if (error.response) {
            const statusCode = error.response.status;
            const errorData = error.response.data;

            if (statusCode === 429) {
              errorMessage =
                "Too many requests to the AI. Please wait a moment and try again.";
            } else if (statusCode === 400) {
              if (errorData && errorData.error && errorData.error.message) {
                if (errorData.error.message.includes("API_KEY_INVALID")) {
                  errorMessage =
                    "Error: Gemini API key is invalid or not set up correctly.";
                } else if (
                  errorData.error.message.includes("PROMPT_TOO_LONG")
                ) {
                  errorMessage =
                    "Message too long. Please shorten your question.";
                } else if (errorData.error.message.includes("SAFETY")) {
                  errorMessage =
                    "Sorry, your question was blocked for security reasons.";
                } else {
                  errorMessage = `Error: ${errorData.error.message}`;
                }
              } else {
                errorMessage = `Error (${statusCode}): There is an issue with your request.`;
              }
            } else if (statusCode === 403) {
              errorMessage = `Access Denied (${statusCode}): Make sure your API key has the correct permissions.`;
            } else if (statusCode === 500 || statusCode === 503) {
              errorMessage = `AI server is down (${statusCode}). Please try again later.`;
            } else if (statusCode === 404) {
              errorMessage = `Error (${statusCode}): AI model not found or incorrect API URL. Make sure 'gemini-1.5-flash-latest' is available.`;
            } else {
              errorMessage = `Network/server error (${statusCode}): ${
                errorData.error
                  ? errorData.error.message
                  : "An unknown issue occurred."
              }`;
            }
          } else if (error.request) {
            errorMessage =
              "Unable to connect to the AI server. Please check your internet connection.";
          } else {
            errorMessage = `Axios Error: ${error.message}`;
          }
        } else {
          errorMessage = `Error: ${error.message}`;
        }

        this.messages.push({
          text: errorMessage,
          sender: "ai",
        });
      } finally {
        this.isLoading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    scrollToBottom() {
      const chatMessages = this.$refs.chatMessages;
      if (chatMessages) {
        requestAnimationFrame(() => {
          chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: "smooth",
          });
        });
      }
    },
  },
  mounted() {
    this.messages = [
      {
        text: "Hello! This is AI created By Rizal, what can I help you with today?",
        sender: "ai",
      },
    ];
    this.$nextTick(() => {
      this.scrollToBottom();
    });
  },
};
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css");

.chat-container {
  min-height: 100vh;
  background: linear-gradient(145deg, #0f0f23, #1a1a2e, #16213e);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  overflow-x: hidden;
}

.main-content {
  margin-left: 280px;
  width: calc(100% - 280px);
  box-sizing: border-box;
  padding: 32px;
  min-height: 100vh;
  animation: fadeIn 0.8s ease-out;
  display: flex;
  flex-direction: column;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-section {
  margin-bottom: 40px;
  flex-shrink: 0;
}
.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}
.header-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  flex-shrink: 0;
}
.header-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}
.header-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  margin: 8px 0 0 0;
  font-weight: 400;
}

.chat-area {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background: rgba(36, 39, 68, 0.5);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  margin-bottom: 24px;
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 10px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 10px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #764ba2;
}

.message {
  display: flex;
  align-items: flex-start;
  max-width: 85%;
}

.message.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.ai-message {
  align-self: flex-start;
  flex-direction: row;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  flex-shrink: 0;
}

.user-avatar {
  background: linear-gradient(135deg, #764ba2, #667eea);
  margin-left: 15px;
}

.ai-avatar {
  background: rgba(255, 255, 255, 0.1);
  margin-right: 15px;
}

.message-bubble {
  padding: 12px 18px;
  border-radius: 18px;
  font-size: 16px;
  line-height: 1.6;
  position: relative;
  word-wrap: break-word;
}

.user-bubble {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-bubble {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.9);
  border-bottom-left-radius: 4px;
}

.message-bubble::before {
  content: "";
  position: absolute;
  bottom: 0;
  width: 0;
  height: 0;
  border: 10px solid transparent;
}

.user-bubble::before {
  right: -8px;
  border-top-color: #764ba2;
  border-bottom-color: transparent;
  border-right-color: transparent;
}

.ai-bubble::before {
  left: -8px;
  border-top-color: rgba(255, 255, 255, 0.08);
  border-bottom-color: transparent;
  border-left-color: transparent;
}

.chat-input-area {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 10px 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.chat-input {
  flex-grow: 1;
  background: transparent;
  border: none;
  outline: none;
  color: white;
  font-size: 16px;
  padding: 8px 0;
  resize: none;
  min-height: 20px;
  max-height: 150px;
  overflow-y: auto;
}

.chat-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.chat-input::-webkit-scrollbar {
  width: 8px;
}

.chat-input::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 10px;
}

.chat-input::-webkit-scrollbar-thumb {
  background: #4a548d;
  border-radius: 10px;
}

.chat-input::-webkit-scrollbar-thumb:hover {
  background: #5a649d;
}

.send-button {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.send-button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(102, 126, 234, 0.6);
}

.send-button:disabled {
  background: rgba(102, 126, 234, 0.4);
  cursor: not-allowed;
  box-shadow: none;
}

.loading-message .loading-dots {
  display: inline-block;
  vertical-align: bottom;
  overflow: hidden;
  height: 1.2em;
}

.loading-dots span {
  animation: blink 1.4s infinite linear;
  opacity: 0;
}

.loading-dots span:nth-child(1) {
  animation-delay: 0s;
}
.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0% {
    opacity: 0;
  }
  30% {
    opacity: 1;
  }
  60% {
    opacity: 0;
  }
  100% {
    opacity: 0;
  }
}
@media (max-width: 1200px) {
  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 24px;
  }
}
@media (max-width: 768px) {
  .header-title {
    font-size: 28px;
  }
  .chat-area {
    padding: 16px;
  }
  .chat-input-area {
    padding: 8px 10px;
  }
  .chat-input {
    font-size: 15px;
  }
  .send-button {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
  .message-bubble {
    padding: 10px 15px;
    font-size: 14px;
  }
  .message-avatar {
    width: 35px;
    height: 35px;
    font-size: 18px;
  }
  .user-avatar {
    margin-left: 10px;
  }
  .ai-avatar {
    margin-right: 10px;
  }
}
</style>
