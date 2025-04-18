<template>
  <div class="card">
    <h1>Start an Order</h1>

    <form @submit.prevent="startOrder" class="grid-form">
      <label>Client Username</label>
      <select v-model="client_username" required>
        <option disabled value="">Select client</option>
        <option v-for="c in clientOptions" :key="c" :value="c">{{ c }}</option>
      </select>

      <label>Order Notes</label>
      <textarea rows="3" v-model="order_notes" />

      <div></div>
      <button type="submit" class="primary-btn">Start Order</button>
    </form>

    <p v-if="error"   class="msg error">{{ error }}</p>
    <p v-if="success" class="msg success">{{ success }}</p>
  </div>
</template>

<script>
export default {
  name: 'StartOrder',
  data () {
    return {
      client_username: '',
      order_notes: '',
      clientOptions: [],
      error: '',
      success: ''
    }
  },
  created () {
    fetch('/api/get_clients')
      .then(r => r.json())
      .then(data => (this.clientOptions = data))
      .catch(() => (this.error = 'Failed to load clients'))
  },
  methods: {
    async startOrder () {
      this.error = this.success = ''
      try {
        const r = await fetch('/api/start_order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_username: this.client_username,
            order_notes: this.order_notes
          })
        })
        const data = await r.json()
        if (!r.ok) throw new Error(data.error || 'Failed to start')
        this.success = `Order started! ID: ${data.order_id}`
        this.client_username = this.order_notes = ''
      } catch (e) {
        this.error = e.message
      }
    }
  }
}
</script>

<style scoped>

.card            {max-width:900px;margin:40px auto;padding:32px 40px;border:1px solid #e5e7eb;
                  border-radius:14px;box-shadow:0 6px 14px rgba(0,0,0,.05);}
h1               {text-align:center;font-size:36px;margin-bottom:30px}
.grid-form       {display:grid;grid-template-columns:200px 1fr;gap:14px 22px}
label            {font-weight:600;color:#374151;align-self:center}
input,select,textarea{width:100%;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;
                  font-size:15px;transition:border .2s,box-shadow .2s}
input:focus,select:focus,textarea:focus{border-color:var(--primary,#4f46e5);
                  box-shadow:0 0 0 2px rgba(79,70,229,.25);outline:none}
textarea         {resize:vertical}
.primary-btn     {padding:12px 0;border:none;border-radius:6px;font-weight:600;cursor:pointer;
                  background:var(--primary,#4f46e5);color:#fff;transition:background .2s}
.primary-btn:hover{background:#4338ca}
.msg             {text-align:center;margin-top:18px}
.msg.error       {color:#dc2626}
.msg.success     {color:#16a34a}
</style>
