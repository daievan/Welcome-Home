<template>
  <div class="card">
    <h1>Add to Current Order</h1>
    <p v-if="currentOrderID" class="order-id">Current Order ID: <strong>{{ currentOrderID }}</strong></p>

    <form @submit.prevent="submitForm" class="grid-form">

      <label>Main Category</label>
      <select v-model="mainCategory" @change="fetchSubCategories" required>
        <option disabled value="">Select main category</option>
        <option v-for="c in mainCategories" :key="c" :value="c">{{ c }}</option>
      </select>

      <label>Sub Category</label>
      <select v-model="subCategory" @change="fetchItems" required>
        <option disabled value="">Select sub category</option>
        <option v-for="s in subCategories" :key="s" :value="s">{{ s }}</option>
      </select>

      <label>Available Items</label>
      <select v-model="item_id" required>
        <option disabled value="">Select an item</option>
        <option v-for="i in items" :key="i.ItemID" :value="i.ItemID">
          {{ i.iDescription }} - {{ i.material }} ({{ i.color }})
        </option>
      </select>

      <div></div>
      <button type="submit" class="primary-btn">Add to Order</button>
    </form>

    <p v-if="error"   class="msg error">{{ error }}</p>
    <p v-if="success" class="msg success">{{ success }}</p>
  </div>
</template>

<script>
export default {
  name: 'AddToOrder',
  data () {
    return {
      mainCategory: '',
      subCategory: '',
      item_id: '',
      mainCategories: [],
      subCategories: [],
      items: [],
      currentOrderID: '',
      error: '',
      success: ''
    }
  },
  created () {
    // 主分类
    fetch('/api/get_main_categories')
      .then(r => r.json())
      .then(d => (this.mainCategories = d))

    // 当前订单 ID
    fetch('/api/get_current_order_id')
      .then(r => r.json())
      .then(d => (this.currentOrderID = d.order_id || ''))
  },
  methods: {
    fetchSubCategories () {
      fetch(`/api/get_subcategories/${this.mainCategory}`)
        .then(r => r.json()).then(d => {
          this.subCategories = d
          this.subCategory = ''; this.items = []
        })
    },
    fetchItems () {
      fetch(`/api/get_items/${this.mainCategory}/${this.subCategory}`)
        .then(r => r.json()).then(d => {
          this.items = d; this.item_id = ''
        })
    },
    async submitForm () {
      this.error = this.success = ''
      try {
        const r = await fetch('/api/add_to_order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            item_id: this.item_id,
            mainCategory: this.mainCategory,
            subCategory: this.subCategory
          })
        })
        const data = await r.json()
        if (!r.ok) throw new Error(data.error || 'Add failed')
        this.success = data.message
        this.fetchItems() // 更新下拉排除已选
      } catch (e) { this.error = e.message }
    }
  }
}
</script>

<style scoped>

.card            {max-width:1000px;margin:40px auto;padding:32px 40px;border:1px solid #e5e7eb;
                  border-radius:14px;box-shadow:0 6px 14px rgba(0,0,0,.05);}
h1               {text-align:center;font-size:36px;margin-bottom:24px}
.order-id        {text-align:center;margin-bottom:20px;font-size:17px}

.grid-form       {display:grid;grid-template-columns:220px 1fr;gap:14px 22px}
label            {font-weight:600;color:#374151;align-self:center}

input,select     {width:100%;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;
                  font-size:15px;transition:border .2s,box-shadow .2s}
input:focus,select:focus{border-color:var(--primary,#4f46e5);
                  box-shadow:0 0 0 2px rgba(79,70,229,.25);outline:none}

.primary-btn     {padding:12px 0;border:none;border-radius:6px;font-weight:600;cursor:pointer;
                  background:var(--primary,#4f46e5);color:#fff;transition:background .2s}
.primary-btn:hover{background:#4338ca}

.msg             {text-align:center;margin-top:18px}
.msg.error       {color:#dc2626}
.msg.success     {color:#16a34a}
</style>
