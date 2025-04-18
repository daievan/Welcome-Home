<template>
  <div class="prepare-order">
    <h1>Prepare Order</h1>
    <form @submit.prevent="prepareOrder" class="form-container">
      <div class="field">
        <label for="search_type">Search By</label>
        <select id="search_type" v-model="search_type" @change="loadSearchOptions">
          <option value="order_number">Order Number</option>
          <option value="client_username">Client Username</option>
        </select>
      </div>

      <div class="field">
        <label for="search_value">Select Value</label>
        <select id="search_value" v-model="search_value">
          <option disabled value="">Please select</option>
          <option v-for="value in search_options" :key="value" :value="value">
            {{ value }}
          </option>
        </select>
      </div>

      <div class="actions">
        <button type="submit">Prepare</button>
      </div>
    </form>

    <div v-if="items.length" class="results">
      <h2>Prepared Items</h2>
      <table class="result-table">
        <thead>
          <tr>
            <th>Item ID</th>
            <th>Description</th>
            <th>Room #</th>
            <th>Shelf #</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, i) in items" :key="i">
            <td>{{ item.ItemID }}</td>
            <td>{{ item.iDescription }}</td>
            <td>{{ item.roomNum }}</td>
            <td>{{ item.shelfNum }}</td>
            <td>{{ item.pNotes }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-if="!items.length && success" class="msg info">{{ success }}</p>
    <p v-if="error" class="msg error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'PrepareOrder',
  data() {
    return {
      search_type: 'order_number',
      search_value: '',
      search_options: [],
      items: [],
      error: '',
      success: ''
    }
  },
  methods: {
    async loadSearchOptions() {
      this.search_value = ''
      this.search_options = []
      try {
        const url = this.search_type === 'order_number'
          ? '/api/get_order_ids'
          : '/api/get_clients'
        const res = await fetch(url)
        this.search_options = await res.json()
      } catch {
        this.error = 'Failed to load options.'
      }
    },
    async prepareOrder() {
      this.error = ''
      this.success = ''
      this.items = []
      try {
        const res = await fetch('/api/prepare_order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            search_type: this.search_type,
            search_value: this.search_value
          })
        })
        const data = await res.json()
        if (!res.ok) {
          this.error = data.error || 'Failed to prepare order.'
        } else {
          this.items = data.items || []
          this.success = this.items.length > 0
            ? ''
            : 'No items to prepare or already prepared.'
        }
      } catch {
        this.error = 'Network or server error.'
      }
    }
  },
  mounted() {
    this.loadSearchOptions()
  }
}
</script>

<style scoped>
.prepare-order {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}
.form-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}
.field {
  flex: 1 1 200px;
  display: flex;
  flex-direction: column;
}
.field label {
  margin-bottom: 6px;
  font-weight: 600;
  color: #555;
}
.field select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.actions {
  flex: 1 1 100%;
  text-align: right;
}
.actions button {
  padding: 10px 24px;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.actions button:hover {
  background: #4338ca;
}
.results h2 {
  margin-bottom: 12px;
  color: #333;
}
.result-table {
  width: 100%;
  border-collapse: collapse;
}
.result-table th,
.result-table td {
  padding: 12px 8px;
  border-bottom: 1px solid #eee;
  text-align: left;
}
.result-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #444;
}
.msg {
  text-align: center;
  padding: 12px 0;
  border-radius: 4px;
}
.msg.error {
  color: #b91c1c;
}
.msg.info {
  color: #1e40af;
}
</style>
