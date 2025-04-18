<template>
  <div class="card">
    <h1>Accept Donation</h1>

    <form @submit.prevent="submitForm" class="grid-form">

      <!-- 基本字段 -->
      <label>Donor ID</label>
      <select v-model="donor_id" required>
        <option disabled value="">Select donor</option>
        <option v-for="d in donorOptions" :key="d" :value="d">{{ d }}</option>
      </select>

      <label>Main Category</label>
      <select v-model="mainCategory" @change="fetchSubCategories" required>
        <option disabled value="">Select main category</option>
        <option v-for="c in mainCategories" :key="c" :value="c">{{ c }}</option>
      </select>

      <label>Sub Category</label>
      <select v-model="subCategory" required>
        <option disabled value="">Select sub category</option>
        <option v-for="s in subCategories" :key="s" :value="s">{{ s }}</option>
      </select>

      <label>Description</label><input v-model="item_description" required />
      <label>Photo Filename</label><input v-model="photo_filename" required />
      <label>Material</label><input v-model="material" required />
      <label>Color</label><input v-model="color" required />

      <label>Is New</label>
      <select v-model="is_new">
        <option :value="1">Yes</option>
        <option :value="0">No</option>
      </select>

      <label>Has Pieces</label>
      <select v-model="has_pieces" @change="updatePieceFields">
        <option :value="1">Yes</option>
        <option :value="0">No</option>
      </select>

      <!-- Piece 列表 -->
      <template v-for="(piece, idx) in pieces" :key="idx">
        <!-- 标题行（跨 2 列）-->
        <h3 class="piece-title" :style="{gridColumn:'1 / -1'}">Piece {{ idx+1 }}</h3>

        <!-- Piece 字段：每行 label+input 与上面同一网格对齐 -->
        <label>Description</label><input v-model="piece.description" required />

        <label>Room Number</label>
        <select v-model="piece.room_num" required>
          <option disabled value="">Select room</option>
          <option v-for="loc in locationOptions" :key="'r'+loc.roomNum" :value="loc.roomNum">{{ loc.roomNum }}</option>
        </select>

        <label>Shelf Number</label>
        <select v-model="piece.shelf_num" required>
          <option disabled value="">Select shelf</option>
          <option v-for="loc in locationOptions" :key="'s'+loc.shelfNum" :value="loc.shelfNum">{{ loc.shelfNum }}</option>
        </select>

        <label>Length</label><input type="number" v-model="piece.length" min="0" step="0.1" />
        <label>Width</label><input type="number" v-model="piece.width"  min="0" step="0.1" />
        <label>Height</label><input type="number" v-model="piece.height" min="0" step="0.1" />
        <label>Notes</label><input v-model="piece.notes" />
      </template>

      <!-- Add piece 按钮 -->
      <div></div>
      <button v-if="has_pieces==1" type="button" class="secondary-btn" @click="addPiece">Add Piece</button>

      <!-- 日期、提交 -->
      <label>Donation Date</label><input type="date" v-model="donation_date" required />

      <div></div>
      <button type="submit" class="primary-btn">Submit Donation</button>
    </form>

    <p v-if="error"   class="msg error">{{ error }}</p>
    <p v-if="success" class="msg success">{{ success }}</p>
  </div>
</template>

<script>
export default {
  name:'AcceptDonation',
  data(){return{
    donor_id:'',mainCategory:'',subCategory:'',item_description:'',
    photo_filename:'',material:'',color:'',is_new:1,has_pieces:1,
    pieces:[],donation_date:'',mainCategories:[],subCategories:[],
    donorOptions:[],locationOptions:[],error:'',success:''
  }},
  created(){
    Promise.all([
      fetch('/api/get_main_categories'),
      fetch('/api/get_donors'),
      fetch('/api/get_locations')
    ])
      .then(async([c,d,l])=>{
        this.mainCategories = await c.json();
        this.donorOptions   = await d.json();
        this.locationOptions= await l.json();
        this.updatePieceFields();
      })
      .catch(()=>this.error='Initialization failed');
  },
  methods:{
    fetchSubCategories(){
      fetch(`/api/get_subcategories/${this.mainCategory}`)
        .then(r=>r.json())
        .then(data=>this.subCategories=data);
    },
    newPiece(){return{description:'',room_num:'',shelf_num:'',length:'',width:'',height:'',notes:''};},
    updatePieceFields(){this.pieces=Number(this.has_pieces)?[this.newPiece(),this.newPiece()]:[this.newPiece()];},
    addPiece(){this.pieces.push(this.newPiece());},
    async submitForm(){
      this.error='';this.success='';
      try{
        const r=await fetch('/api/accept_donation',{
          method:'POST',headers:{'Content-Type':'application/json'},
          body:JSON.stringify({
            donor_id:this.donor_id,mainCategory:this.mainCategory,subCategory:this.subCategory,
            item_description:this.item_description,photo_filename:this.photo_filename,
            material:this.material,color:this.color,is_new:this.is_new,has_pieces:this.has_pieces,
            donation_date:this.donation_date,pieces:this.pieces
          })
        });
        const data=await r.json();
        if(!r.ok) throw new Error(data.error||'Submission failed');
        this.success='Donation submitted successfully!';
      }catch(e){this.error=e.message;}
    }
  }
};
</script>

<style scoped>
/* 将变量声明到 .card，确保 scoped 后仍能命中 */
.card{--primary:#4f46e5;}

.card{
  max-width:1100px;margin:40px auto;padding:32px 40px;
  border:1px solid #e5e7eb;border-radius:14px;
  box-shadow:0 6px 14px rgba(0,0,0,.05);
}
h1{text-align:center;font-size:40px;margin-bottom:34px;}

.grid-form{
  display:grid;
  grid-template-columns:220px 1fr;
  gap:14px 22px;
}

label{
  font-weight:600;color:#374151;align-self:center;
}
input,select{
  width:100%;padding:10px 12px;
  border:1px solid #d1d5db;border-radius:6px;font-size:15px;
  transition:border .2s,box-shadow .2s;
}
input:focus,select:focus{
  border-color:var(--primary);outline:none;
  box-shadow:0 0 0 2px rgba(79,70,229,.25);
}

.primary-btn,.secondary-btn{
  padding:12px 0;border:none;border-radius:6px;
  font-weight:600;cursor:pointer;font-size:15px;
  transition:background .2s;white-space:nowrap;
}
.primary-btn{
  background:var(--primary);color:#fff;
}
.primary-btn:hover{background:#4338ca;}
.secondary-btn{
  background:#e0e7ff;color:#3730a3;
}
.secondary-btn:hover{background:#c7d2fe;}

.piece-title{
  background:#f9fafb;padding:6px 12px;border-radius:6px;
  font-size:20px;margin:26px 0 8px;
}

.msg{text-align:center;margin-top:18px;}
.msg.error{color:#dc2626;}
.msg.success{color:#16a34a;}
</style>
