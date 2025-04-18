<template>
  <section class="home-wrapper">
    <div class="home-content">
      <h1 class="title">Welcome&nbsp;Home</h1>

      <ul class="nav-list">
        <li v-for="link in links" :key="link.to">
          <router-link :to="link.to" class="nav-link">
            <span class="icon">{{ link.icon }}</span>
            {{ link.text }}
          </router-link>
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      links: [
        { to: '/accept-donation',  text: 'Accept Donation',     icon: '🎁' },
        { to: '/find-single-item', text: 'Find Single Item',    icon: '🔍' },
        { to: '/find-order-items', text: 'Find Order Items',    icon: '📦' },
        { to: '/start-order',      text: 'Start an Order',      icon: '📝' },
        { to: '/add-to-order',     text: 'Add to Current Order',icon: '➕' },
        { to: '/prepare-order',    text: 'Prepare Order',       icon: '🚚' },
        { to: '/my-orders',        text: 'My Orders',           icon: '📑' }
      ]
    }
  }
}
</script>

<style scoped>
/* ---------- Layout ---------- */
.home-wrapper{
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background:linear-gradient(145deg,#f6f9fc,#eef3f7);
  font-family:"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
.home-content{
  text-align:center;
  width:clamp(280px,90vw,480px);
  padding:32px 24px;
  background:#fff;
  border-radius:24px;
  box-shadow:0 12px 25px rgba(0,0,0,.07);
}

/* ---------- Title ---------- */
.title{
  font-size:2.25rem;
  font-weight:700;
  margin-bottom:24px;
  color:#333;
}

/* ---------- Navigation list ---------- */
.nav-list{
  margin:0;
  padding:0;
  display:flex;
  flex-direction:column;
  gap:14px;
}
.nav-link{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  padding:14px 20px;
  background:#f4f7fa;
  border-radius:14px;
  text-decoration:none;
  color:#1f2937;
  font-size:1rem;
  font-weight:600;
  transition:all .25s ease;
  box-shadow:0 2px 5px rgba(0,0,0,.06);
}
.nav-link:hover{
  transform:translateY(-2px);
  box-shadow:0 6px 12px rgba(0,0,0,.1);
  background:#e8eef4;
}
.nav-link:active{
  transform:translateY(0);
  box-shadow:0 3px 6px rgba(0,0,0,.08);
}
.icon{
  font-size:1.25rem;
}
</style>
