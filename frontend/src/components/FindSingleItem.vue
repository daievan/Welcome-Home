<template>
  <div class="wrapper">
    <h1>Find Single Item</h1>

    <form @submit.prevent="fetchItem">
      <label>Item ID</label>
      <select v-model="itemID" required>
        <option disabled value="">Select item</option>
        <option v-for="id in itemOptions" :key="id" :value="id">{{ id }}</option>
      </select>

      <button class="primary-btn">Search</button>
    </form>

    <table v-if="locations.length">
      <thead>
        <tr><th>Piece #</th><th>Room</th><th>Shelf</th><th>Shelf Desc.</th></tr>
      </thead>
      <tbody>
        <tr v-for="loc in locations" :key="loc.pieceNum">
          <td>{{ loc.pieceNum }}</td><td>{{ loc.roomNum }}</td><td>{{ loc.shelfNum }}</td><td>{{ loc.shelfDescription }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default{
  name:'FindSingleItem',
  data(){return{itemID:'',itemOptions:[],locations:[],error:''}},
  created(){fetch('/api/get_item_ids').then(r=>r.json()).then(d=>this.itemOptions=d);},
  methods:{
    async fetchItem(){
      this.error='';this.locations=[];
      try{
        const r=await fetch('/api/find_single_item',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({itemID:this.itemID})});
        const data=await r.json();
        if(!r.ok) throw new Error(data.error||'Failed');
        this.locations=data.locations;
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
.primary-btn{background:#4f46e5;color:#fff;border:none;border-radius:6px;padding:10px 22px;white-space:nowrap;font-weight:600;cursor:pointer;}
.primary-btn:hover{background:#4338ca;}

table{width:100%;border-collapse:collapse;margin-top:16px;font-size:15px;}
th,td{border:1px solid #e5e7eb;padding:8px;text-align:center;}
.error{color:#dc2626;text-align:center;margin-top:16px;}
</style>
