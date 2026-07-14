<template>
  <div class="card border-0 shadow-sm rounded-3 overflow-hidden mt-4" style="height: 75vh;">
    <div class="row g-0 h-100">
      <!-- Sidebar / Conversations List -->
      <div class="col-md-4 border-end h-100 d-flex flex-column bg-white">
        <div class="p-3 border-bottom bg-light">
          <h5 class="mb-0 fw-bold text-dark">Chats (Shortlisted Candidates)</h5>
        </div>
        <div class="overflow-auto flex-grow-1">
          <div v-if="conversations.length === 0" class="p-4 text-center text-muted">
            No shortlisted candidates found.
          </div>
          <div 
            v-for="conv in conversations" 
            :key="conv.application_id"
            class="p-3 border-bottom cursor-pointer transition-all"
            :class="{'bg-light': activeConv?.application_id === conv.application_id, 'hover-bg-light': activeConv?.application_id !== conv.application_id}"
            @click="selectConversation(conv)"
          >
            <div class="d-flex justify-content-between align-items-baseline mb-1">
              <h6 class="mb-0 fw-bold text-dark">{{ conv.student_name }}</h6>
              <small class="text-muted" style="font-size: 11px;">{{ formatTime(conv.last_timestamp) }}</small>
            </div>
            <div class="text-muted small text-truncate">{{ conv.job_title }}</div>
            <div class="text-secondary small text-truncate mt-1">
              {{ conv.last_message || 'Start the conversation...' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="col-md-8 h-100 d-flex flex-column bg-white">
        <template v-if="activeConv">
          <!-- Chat Header -->
          <div class="p-3 border-bottom bg-light d-flex justify-content-between align-items-center">
            <div>
              <h5 class="mb-0 fw-bold text-dark">{{ activeConv.student_name }}</h5>
              <small class="text-muted">Application: {{ activeConv.job_title }}</small>
            </div>
            <span class="badge bg-success rounded-pill px-3">{{ activeConv.status }}</span>
          </div>

          <!-- Messages Area -->
          <div class="flex-grow-1 overflow-auto p-4" style="background-color: #f8f9fa;" ref="msgContainer">
            <div v-if="messages.length === 0" class="text-center text-muted mt-5">
              <p>No messages yet.</p>
              <p class="small">You must send the first message to start the conversation.</p>
            </div>
            
            <div 
              v-for="msg in messages" 
              :key="msg.id"
              class="mb-3 d-flex"
              :class="{'justify-content-end': msg.sender_id === currentUserId, 'justify-content-start': msg.sender_id !== currentUserId}"
            >
              <div 
                class="p-3 rounded-3 shadow-sm"
                style="max-width: 75%;"
                :class="{'bg-primary text-white': msg.sender_id === currentUserId, 'bg-white text-dark border': msg.sender_id !== currentUserId}"
              >
                <div style="font-size: 14.5px;">{{ msg.content }}</div>
                <div class="text-end mt-1" :class="{'text-white-50': msg.sender_id === currentUserId, 'text-muted': msg.sender_id !== currentUserId}" style="font-size: 10px;">
                  {{ formatTime(msg.timestamp) }}
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="p-3 border-top bg-white">
            <form @submit.prevent="sendMessage" class="d-flex gap-2">
              <input 
                type="text" 
                v-model="newMessage" 
                class="form-control rounded-pill px-4 shadow-none border-2" 
                placeholder="Type a message..." 
                required
              >
              <button type="submit" class="btn btn-primary rounded-circle shadow-sm d-flex align-items-center justify-content-center" style="width: 44px; height: 44px;" :disabled="!newMessage.trim()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
              </button>
            </form>
          </div>
        </template>
        
        <div v-else class="h-100 d-flex flex-column align-items-center justify-content-center text-muted bg-light">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          <h4 class="fw-normal">Select a conversation</h4>
          <p>Choose a shortlisted candidate to start messaging.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      conversations: [],
      activeConv: null,
      messages: [],
      newMessage: '',
      currentUserId: null
    }
  },
  mounted() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      this.currentUserId = JSON.parse(userStr).id;
    }
    this.fetchConversations();
  },
  methods: {
    async fetchConversations() {
      try {
        const response = await api.get('/company/messages/conversations');
        this.conversations = response.data;
      } catch (error) {
        console.error('Error fetching conversations:', error);
      }
    },
    async selectConversation(conv) {
      this.activeConv = conv;
      await this.fetchMessages();
    },
    async fetchMessages() {
      if (!this.activeConv) return;
      try {
        const response = await api.get(`/company/messages/${this.activeConv.application_id}`);
        this.messages = response.data;
        this.scrollToBottom();
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },
    async sendMessage() {
      if (!this.newMessage.trim() || !this.activeConv) return;
      
      try {
        const response = await api.post(`/company/messages/${this.activeConv.application_id}`, {
          content: this.newMessage
        });
        
        this.messages.push(response.data);
        this.newMessage = '';
        this.fetchConversations(); // update last message in sidebar
        this.scrollToBottom();
      } catch (error) {
        console.error('Error sending message:', error);
        alert(error.response?.data?.msg || 'Failed to send message');
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.msgContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    formatTime(isoString) {
      if (!isoString) return '';
      const date = new Date(isoString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  }
}
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
.transition-all { transition: background-color 0.2s; }
.hover-bg-light:hover { background-color: #f8f9fa !important; }
</style>
