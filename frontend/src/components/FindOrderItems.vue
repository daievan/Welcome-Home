<template>
  <div class="wrapper">
    <h1>Find Order Items</h1>

    <form @submit.prevent="fetchOrderItems">
      <label>Order ID</label>
      <select v-model="orderID" required>
        <option disabled value="">Select order</option>
        <option v-for="id in orderOptions" :key="id" :value="id">{{ id }}</option>
      </select>

      <button class="primary-btn">Search</button>
    </form>

    <table v-if="items.length">
      <thead>
        <tr>
          <th>Item ID</th><th>Description</th><th>Piece #</th>
          <th>Room</th><th>Shelf</th><th>Shelf Desc.</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="it in items" :key="it.ItemID+'-'+it.pieceNum">
          <td>{{ it.ItemID }}</td><td>{{ it.itemDescription }}</td><td>{{ it.pieceNum }}</td>
          <td>{{ it.roomNum }}</td><td>{{ it.shelfNum }}</td><td>{{ it.shelfDescription }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default{
  name:'FindOrderItems',
  data(){return{orderID:'',orderOptions:[],items:[],error:''}},
  created(){fetch('/api/get_order_ids').then(r=>r.json()).then(d=>this.orderOptions=d);},
  methods:{
    async fetchOrderItems(){
      this.error='';this.items=[];
      try{
        const r=await fetch('/api/find_order_items',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({orderID:this.orderID})});
        const data=await r.json();
        if(!r.ok) throw new Error(data.error||'Failed');
        this.items=data.items;
      }catch(e){this.error=e.message;}
    }
  }
};
</script>

<style scoped>
.wrapper{max-width:900px;margin:40px auto;padding:28px;border:1px solid #e5e7eb;border-radius:14px;}
h1{text-align:center;margin-bottom:28px;font-size:36px;}
form{display:flex;gap:14px;align-items:center;justify-content:center;margin-bottom:24px;}
label{font-weight:600;color:#374151;}
select{min-width:300px;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:15px;}
.primary-btn{background:#4f46e5;color:#fff;border:none;border-radius:6px;padding:10px 22px;font-weight:600;white-space:nowrap;cursor:pointer;}
.primary-btn:hover{background:#4338ca;}

table{width:100%;border-collapse:collapse;margin-top:16px;font-size:15px;}
th,td{border:1px solid #e5e7eb;padding:8px;text-align:center;}
.error{color:#dc2626;text-align:center;margin-top:16px;}
</style>
