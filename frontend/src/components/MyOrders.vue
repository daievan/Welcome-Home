<template>
  <div class="my-orders">
    <h1>My Orders</h1>

    <!-- 客户视图 -->
    <section v-if="role === '3'">
      <h2>Your Orders (Client)</h2>
      <table class="orders-table" v-if="orders.length">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Date</th>
            <th>Notes</th>
            <th>Item ID</th>
            <th>Description</th>
            <th>Found</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(order, idx) in orders" :key="idx">
            <td>{{ order.orderID }}</td>
            <td>{{ order.orderDate }}</td>
            <td>{{ order.orderNotes }}</td>
            <td>{{ order.ItemID }}</td>
            <td>{{ order.iDescription }}</td>
            <td>{{ order.found ? 'Yes' : 'No' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="msg">No orders found.</p>
    </section>

    <!-- 员工视图 -->
    <section v-if="role === '1'">
      <h2>Your Managed Orders</h2>
      <table class="orders-table" v-if="supervise_orders.length">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Date</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(o, idx) in supervise_orders" :key="idx">
            <td>{{ o.orderID }}</td>
            <td>{{ o.orderDate }}</td>
            <td>{{ o.orderNotes }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="msg">No supervised orders.</p>

      <h2>Your Delivery Orders</h2>
      <table class="orders-table" v-if="deliver_orders.length">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Date</th>
            <th>Notes</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(o, idx) in deliver_orders" :key="idx">
            <td>{{ o.orderID }}</td>
            <td>{{ o.orderDate }}</td>
            <td>{{ o.orderNotes }}</td>
            <td>{{ o.status }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="msg">No delivery orders.</p>
    </section>

    <!-- 志愿者视图 -->
    <section v-if="role === '2'">
      <h2>Your Delivery Assignments</h2>
      <table class="orders-table" v-if="orders.length">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Date</th>
            <th>Notes</th>
            <th>Delivery Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(order, idx) in orders" :key="idx">
            <td>{{ order.orderID }}</td>
            <td>{{ order.orderDate }}</td>
            <td>{{ order.orderNotes }}</td>
            <td>{{ order.deliveryDate }}</td>
            <td>{{ order.status }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="msg">No assignments found.</p>
    </section>
  </div>
</template>

<script>
export default {
  name: 'MyOrders',
  data() {
    return {
      role: '',
      orders: [],
      supervise_orders: [],
      deliver_orders: []
    }
  },
  async created() {
    try {
      const res = await fetch('/api/my_orders')
      const data = await res.json()
      this.role = data.role
      this.orders = data.orders || []
      this.supervise_orders = data.supervise_orders || []
      this.deliver_orders = data.deliver_orders || []
    } catch {
      // 简单提示
      alert('Failed to load orders')
    }
  }
}
</script>

<style scoped>
.my-orders {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
h1, h2 {
  color: #333;
  margin-bottom: 16px;
  text-align: center;
}
.orders-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
}
.orders-table th,
.orders-table td {
  padding: 12px 8px;
  border-bottom: 1px solid #eee;
}
.orders-table th {
  background: #f3f4f6;
  font-weight: 600;
  color: #444;
}
.msg {
  text-align: center;
  color: #6b7280;
  margin-top: 12px;
}
</style>
