const cart = new Map();   // product id -> quantity
let products = [];

const money = (cents) => `$${(cents / 100).toFixed(2)}`;
const $ = (id) => document.getElementById(id);

async function loadProducts() {
  const res = await fetch("/api/products");
  products = await res.json();
  $("products").innerHTML = "";
  for (const p of products) {
    const li = document.createElement("li");
    li.innerHTML = `<span class="emoji">${p.image}</span><strong></strong><span>${money(p.price)}</span>`;
    li.querySelector("strong").textContent = p.name;
    const button = document.createElement("button");
    button.textContent = "Add to cart";
    button.onclick = () => { cart.set(p.id, (cart.get(p.id) || 0) + 1); render(); };
    li.append(button);
    $("products").append(li);
  }
}

async function render() {
  $("cart").innerHTML = "";
  for (const [id, quantity] of cart) {
    const li = document.createElement("li");
    li.textContent = `${products.find((p) => p.id === id).name} × ${quantity}`;
    $("cart").append(li);
  }
  $("error").textContent = "";
  if (cart.size === 0) { $("totals").innerHTML = "<dt>Total</dt><dd>$0.00</dd>"; return; }
  const items = [...cart].map(([product_id, quantity]) => ({ product_id, quantity }));
  const res = await fetch("/api/cart/total", {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ items, discount_code: $("code").value || null }),
  });
  if (!res.ok) { $("error").textContent = "Could not price the cart. Please try again."; return; }
  const t = await res.json();
  $("totals").innerHTML = `<dt>Subtotal</dt><dd>${money(t.subtotal)}</dd><dt>Discount</dt><dd>−${money(t.discount)}</dd>`
    + `<dt>Tax</dt><dd>${money(t.tax)}</dd><dt>Total</dt><dd><strong>${money(t.total)}</strong></dd>`;
}

$("code").addEventListener("change", render);
loadProducts().then(render).catch(() => { $("error").textContent = "The shop is unavailable right now."; });
