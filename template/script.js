// Frontend script aligned with Flask blueprints and cookie-based auth

// ---------- REGISTER ----------
if (document.getElementById("registerForm")) {
  document
    .getElementById("registerForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const user = {
        username: username.value,
        email: email.value,
        name: (window.name && name.value) || username.value,
        password: password.value,
      };
      const res = await fetch(`/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(user),
      });
      if (res.ok) {
        alert("✅ Registration successful!");
        window.location.href = "/login";
      } else {
        const data = await res.json().catch(() => ({}));
        alert(data.error || data.message || "❌ Registration failed!");
      }
    });
}

// ---------- LOGIN ----------
if (document.getElementById("loginForm")) {
  document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const creds = { email: email.value, password: password.value };
    const res = await fetch(`/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(creds),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      window.location.href = "/";
    } else alert(data.error || data.message || "❌ Login failed!");
  });
}

// ---------- LOGOUT ----------
if (document.getElementById("logoutBtn")) {
  document.getElementById("logoutBtn").addEventListener("click", () => {
    window.location.href = "/login";
  });
}

// ---------- PRODUCTS + AI CHAT ----------
if (document.getElementById("productForm")) {
  const productForm = document.getElementById("productForm");
  const productList = document.getElementById("productList");
  const chatBox = document.getElementById("chat-box");
  const sendBtn = document.getElementById("sendBtn");
  const promptInput = document.getElementById("prompt");

  async function loadProducts() {
    const res = await fetch(`/products/`, { credentials: "include" });
    const data = await res.json().catch(() => []);
    const items = Array.isArray(data) ? data : data.products || [];
    productList.innerHTML = items
      .map(
        (p) => `
      <div class="product-item">
        <span>${p.name} - $${p.price}</span>
        <button onclick="deleteProduct('${p.id}')">🗑️</button>
      </div>`
      )
      .join("");
  }

  productForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const newProduct = {
      name: productName.value,
      price: parseFloat(productPrice.value),
      description: productDesc.value,
    };

    await fetch(`/products/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(newProduct),
    });
    productName.value = productPrice.value = productDesc.value = "";
    loadProducts();
  });

  window.deleteProduct = async (id) => {
    await fetch(`/products/${id}`, {
      method: "DELETE",
      credentials: "include",
    });
    loadProducts();
  };

  async function sendMessage() {
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    appendMessage(prompt, "user");
    promptInput.value = "";

    const loader = document.createElement("div");
    loader.classList.add("loader");
    chatBox.appendChild(loader);

    try {
      const res = await fetch(`/ai_agent/api/ai/agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json().catch(() => ({}));
      loader.remove();
      appendMessage(
        (data && (data.reply || data.response)) || "No reply",
        "ai"
      );
    } catch {
      loader.remove();
      appendMessage("❌ Network error", "ai");
    }
  }

  function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  if (sendBtn) sendBtn.addEventListener("click", sendMessage);
  loadProducts();
}
